import requests
from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.core.database import SessionLocal
from backend.app.db import crud, models
import httpx
from datetime import datetime, timedelta
import os

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Helper function to get valid token (handles refresh)
async def get_valid_token(db: Session, user_id: int, platform: str):
    account = crud.get_social_account(db, user_id, platform)
    if not account:
        raise HTTPException(status_code=404, detail=f"{platform} account not connected")
    
    # Check expiry
    if account.expires_at and account.expires_at < datetime.utcnow() + timedelta(minutes=5):
        # Token expired or expiring soon
        if platform == "youtube" and account.refresh_token:
            # Refresh YouTube Token
            token_url = "https://oauth2.googleapis.com/token"
            data = {
                "client_id": os.getenv("GOOGLE_CLIENT_ID"),
                "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
                "refresh_token": account.refresh_token,
                "grant_type": "refresh_token"
            }
            async with httpx.AsyncClient() as client:
                res = await client.post(token_url, data=data)
                if res.status_code == 200:
                    token_data = res.json()
                    new_access_token = token_data["access_token"]
                    expires_in = token_data.get("expires_in", 3600)
                    new_expires_at = datetime.utcnow() + timedelta(seconds=expires_in)
                    
                    # Update DB
                    account.access_token = new_access_token
                    account.expires_at = new_expires_at
                    db.commit()
                    return new_access_token
                else:
                    print(f"Failed to refresh YouTube token: {res.text}")
                    # If refresh fails, might need re-login, but return current token for now or raise
                    raise HTTPException(status_code=401, detail="Session expired, please reconnect YouTube")
        
        elif platform == "instagram":
             # Instagram/Facebook long-lived tokens are hard to "refresh" automatically without user interaction 
             # if they are truly expired. But we can try to exchange it again if it's just a session timeout.
             # For now, we'll assume if it's expired, the user needs to re-login.
             pass

    return account.access_token

# ==================== Instagram Analytics ====================

@router.get('/instagram/analytics')
async def get_instagram_analytics(user_id: int, db: Session = Depends(get_db)):
    """Get comprehensive Instagram analytics"""
    token = await get_valid_token(db, user_id, "instagram")
    account = crud.get_social_account(db, user_id, "instagram")
    ig_id = account.account_id
    
    async with httpx.AsyncClient() as client:
        # 1. Profile Data
        profile_url = f"https://graph.facebook.com/v18.0/{ig_id}"
        profile_params = {
            "fields": "username,name,profile_picture_url,followers_count,follows_count,media_count,biography,website",
            "access_token": token
        }
        profile_res = await client.get(profile_url, params=profile_params)
        profile_data = profile_res.json()
        
        # 2. Account Insights (Impressions, Reach, etc.)
        # Note: 'email_contacts', 'phone_call_clicks', 'text_message_clicks', 'get_directions_clicks', 'website_clicks', 'profile_views'
        # are only available for 'day' metric. 'impressions', 'reach' available for 'day', 'week', 'days_28'.
        insights_url = f"https://graph.facebook.com/v18.0/{ig_id}/insights"
        insights_params = {
            "metric": "impressions,reach,profile_views",
            "period": "day",
            "access_token": token
        }
        insights_res = await client.get(insights_url, params=insights_params)
        insights_data = insights_res.json()
        
        # 3. Audience Demographics (Lifetime)
        audience_params = {
            "metric": "audience_city,audience_country,audience_gender_age",
            "period": "lifetime",
            "access_token": token
        }
        audience_res = await client.get(insights_url, params=audience_params)
        audience_data = audience_res.json()
        
        # 4. Media & Media Insights
        media_url = f"https://graph.facebook.com/v18.0/{ig_id}/media"
        media_params = {
            "fields": "id,caption,media_type,media_url,permalink,thumbnail_url,timestamp,like_count,comments_count,insights.metric(impressions,reach,engagement,saved)",
            "access_token": token,
            "limit": 10 # Limit to recent 10 posts
        }
        media_res = await client.get(media_url, params=media_params)
        media_data = media_res.json()

    # Process Data
    stats = {
        "followers": profile_data.get("followers_count"),
        "following": profile_data.get("follows_count"),
        "media_count": profile_data.get("media_count"),
        "insights": insights_data.get("data", []),
        "audience": audience_data.get("data", [])
    }
    
    posts = []
    for post in media_data.get("data", []):
        post_insights = post.get("insights", {}).get("data", [])
        formatted_post = {
            "id": post.get("id"),
            "type": post.get("media_type"),
            "caption": post.get("caption"),
            "url": post.get("media_url") or post.get("permalink"),
            "timestamp": post.get("timestamp"),
            "metrics": {
                "likes": post.get("like_count"),
                "comments": post.get("comments_count"),
                "insights": post_insights
            }
        }
        posts.append(formatted_post)

    return {
        "platform": "instagram",
        "account_id": ig_id,
        "profile": {
            "username": profile_data.get("username"),
            "name": profile_data.get("name"),
            "picture": profile_data.get("profile_picture_url"),
            "bio": profile_data.get("biography")
        },
        "stats": stats,
        "posts": posts,
        "timestamp": datetime.utcnow().isoformat()
    }

# ==================== YouTube Analytics ====================

@router.get('/youtube/analytics')
async def get_youtube_analytics_data(user_id: int, db: Session = Depends(get_db)):
    """Get comprehensive YouTube analytics"""
    token = await get_valid_token(db, user_id, "youtube")
    account = crud.get_social_account(db, user_id, "youtube")
    channel_id = account.account_id
    
    async with httpx.AsyncClient() as client:
        # 1. Channel Statistics
        channel_url = "https://www.googleapis.com/youtube/v3/channels"
        channel_params = {
            "part": "snippet,statistics,contentDetails",
            "id": channel_id,
            "key": os.getenv("GOOGLE_API_KEY") # Optional if using OAuth token, but good to have
        }
        headers = {"Authorization": f"Bearer {token}"}
        channel_res = await client.get(channel_url, params=channel_params, headers=headers)
        channel_data = channel_res.json()
        
        if not channel_data.get("items"):
            raise HTTPException(status_code=404, detail="Channel not found")
            
        channel_item = channel_data["items"][0]
        uploads_playlist_id = channel_item["contentDetails"]["relatedPlaylists"]["uploads"]
        
        # 2. Videos (from Uploads Playlist)
        playlist_url = "https://www.googleapis.com/youtube/v3/playlistItems"
        playlist_params = {
            "part": "snippet,contentDetails",
            "playlistId": uploads_playlist_id,
            "maxResults": 10
        }
        playlist_res = await client.get(playlist_url, params=playlist_params, headers=headers)
        playlist_data = playlist_res.json()
        
        video_ids = [item["contentDetails"]["videoId"] for item in playlist_data.get("items", [])]
        
        # 3. Video Statistics
        videos_url = "https://www.googleapis.com/youtube/v3/videos"
        videos_params = {
            "part": "statistics,snippet",
            "id": ",".join(video_ids)
        }
        videos_res = await client.get(videos_url, params=videos_params, headers=headers)
        videos_data = videos_res.json()
        
        # 4. Analytics Reports (Last 30 days)
        # Note: YouTube Analytics API requires specific dimensions/metrics
        analytics_url = "https://youtubeanalytics.googleapis.com/v2/reports"
        end_date = datetime.utcnow().strftime("%Y-%m-%d")
        start_date = (datetime.utcnow() - timedelta(days=30)).strftime("%Y-%m-%d")
        
        analytics_params = {
            "ids": "channel==MINE",
            "startDate": start_date,
            "endDate": end_date,
            "metrics": "views,estimatedMinutesWatched,averageViewDuration,subscribersGained,likes,comments",
            "dimensions": "day",
            "sort": "day"
        }
        analytics_res = await client.get(analytics_url, params=analytics_params, headers=headers)
        analytics_report = analytics_res.json()
        
        # 5. Demographics
        demographics_params = {
            "ids": "channel==MINE",
            "startDate": start_date,
            "endDate": end_date,
            "metrics": "viewerPercentage",
            "dimensions": "ageGroup,gender",
            "sort": "gender,ageGroup"
        }
        demographics_res = await client.get(analytics_url, params=demographics_params, headers=headers)
        demographics_report = demographics_res.json()

    # Process Data
    stats = {
        "subscribers": channel_item["statistics"].get("subscriberCount"),
        "total_views": channel_item["statistics"].get("viewCount"),
        "video_count": channel_item["statistics"].get("videoCount"),
        "analytics_30d": analytics_report,
        "demographics": demographics_report
    }
    
    posts = []
    for video in videos_data.get("items", []):
        formatted_video = {
            "id": video["id"],
            "title": video["snippet"]["title"],
            "thumbnail": video["snippet"]["thumbnails"]["high"]["url"],
            "published_at": video["snippet"]["publishedAt"],
            "metrics": {
                "views": video["statistics"].get("viewCount"),
                "likes": video["statistics"].get("likeCount"),
                "comments": video["statistics"].get("commentCount")
            }
        }
        posts.append(formatted_video)

    return {
        "platform": "youtube",
        "account_id": channel_id,
        "profile": {
            "title": channel_item["snippet"]["title"],
            "description": channel_item["snippet"]["description"],
            "thumbnail": channel_item["snippet"]["thumbnails"]["high"]["url"]
        },
        "stats": stats,
        "posts": posts,
        "timestamp": datetime.utcnow().isoformat()
    }

# ==================== Connected Accounts ====================

@router.get('/connected-accounts')
def get_connected_accounts(user_id: int, db: Session = Depends(get_db)):
    """Get all connected social accounts for a user"""
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    accounts = []
    for account in user.social_accounts:
        accounts.append({
            "platform": account.platform,
            "account_id": account.account_id,
            "connected": True
        })
    
    return {"connected_accounts": accounts}
