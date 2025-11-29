import requests
from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.core.database import SessionLocal
from backend.app.db import crud
import httpx

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Helper function to get token from database
def get_token_from_db(db: Session, user_id: int, platform: str):
    account = crud.get_social_account(db, user_id, platform)
    if not account:
        raise HTTPException(status_code=404, detail=f"{platform} account not connected")
    return account.access_token

# ==================== Instagram Analytics ====================

@router.get('/instagram/insights')
async def get_ig_insights(user_id: int, db: Session = Depends(get_db)):
    """Get Instagram media insights"""
    token = get_token_from_db(db, user_id, "instagram")
    
    url = f"https://graph.instagram.com/me/media?fields=id,caption,media_type,media_url,timestamp,like_count,comments_count&access_token={token}"
    
    async with httpx.AsyncClient() as client:
        res = await client.get(url)
        data = res.json()
    
    return {"posts": data.get("data", [])}

@router.get('/instagram/profile')
async def get_ig_profile(user_id: int, db: Session = Depends(get_db)):
    """Get Instagram profile information"""
    token = get_token_from_db(db, user_id, "instagram")
    
    url = f"https://graph.instagram.com/me?fields=id,username,account_type,media_count&access_token={token}"
    
    async with httpx.AsyncClient() as client:
        res = await client.get(url)
        data = res.json()
    
    return data

# ==================== Twitter Analytics ====================

@router.get('/twitter/tweets')
async def get_twitter_tweets(user_id: int, db: Session = Depends(get_db)):
    """Get user's recent tweets"""
    token = get_token_from_db(db, user_id, "twitter")
    account = crud.get_social_account(db, user_id, "twitter")
    twitter_user_id = account.account_id
    
    url = f"https://api.twitter.com/2/users/{twitter_user_id}/tweets?tweet.fields=created_at,public_metrics"
    
    async with httpx.AsyncClient() as client:
        res = await client.get(
            url,
            headers={"Authorization": f"Bearer {token}"}
        )
        data = res.json()
    
    return {"tweets": data.get("data", [])}

@router.get('/twitter/profile')
async def get_twitter_profile(user_id: int, db: Session = Depends(get_db)):
    """Get Twitter profile information"""
    token = get_token_from_db(db, user_id, "twitter")
    
    url = "https://api.twitter.com/2/users/me?user.fields=created_at,description,public_metrics"
    
    async with httpx.AsyncClient() as client:
        res = await client.get(
            url,
            headers={"Authorization": f"Bearer {token}"}
        )
        data = res.json()
    
    return data.get("data", {})

# ==================== YouTube Analytics ====================

@router.get('/youtube/videos')
async def get_youtube_videos(user_id: int, db: Session = Depends(get_db)):
    """Get YouTube channel videos"""
    token = get_token_from_db(db, user_id, "youtube")
    account = crud.get_social_account(db, user_id, "youtube")
    channel_id = account.account_id
    
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={channel_id}&maxResults=25&order=date&type=video"
    
    async with httpx.AsyncClient() as client:
        res = await client.get(
            url,
            headers={"Authorization": f"Bearer {token}"}
        )
        data = res.json()
    
    return {"videos": data.get("items", [])}

@router.get('/youtube/analytics')
async def get_youtube_analytics(user_id: int, db: Session = Depends(get_db)):
    """Get YouTube channel analytics"""
    token = get_token_from_db(db, user_id, "youtube")
    account = crud.get_social_account(db, user_id, "youtube")
    channel_id = account.account_id
    
    # Get channel statistics
    url = f"https://www.googleapis.com/youtube/v3/channels?part=statistics&id={channel_id}"
    
    async with httpx.AsyncClient() as client:
        res = await client.get(
            url,
            headers={"Authorization": f"Bearer {token}"}
        )
        data = res.json()
    
    return {"analytics": data.get("items", [{}])[0].get("statistics", {})}

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
