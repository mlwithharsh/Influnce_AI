from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
import requests
import os
import httpx
from datetime import datetime, timedelta
from backend.app.core.database import SessionLocal
from backend.app.db import crud, models
from backend.app.core.auth import create_access_token, hash_password, verify_password
from pydantic import BaseModel

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ==================== User Registration/Login ====================

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

@router.post('/register')
def register(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    try:
        # Check if user exists
        existing_user = crud.get_user_by_email(db, user.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Create user
        hashed_password = hash_password(user.password)
        new_user = crud.create_user(
            db=db,
            username=user.username,
            email=user.email,
            hashed_password=hashed_password
        )
        
        # Create JWT token
        jwt_token = create_access_token({"user_id": new_user.id})
        
        return {
            "message": "User registered successfully",
            "access_token": jwt_token,
            "user_id": new_user.id
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"Registration error: {e}")
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")

@router.post('/login')
def login(user: UserLogin, db: Session = Depends(get_db)):
    """Login user"""
    try:
        # Get user
        db_user = crud.get_user_by_email(db, user.email)
        if not db_user:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        # Verify password
        if not verify_password(user.password, db_user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        # Create JWT token
        jwt_token = create_access_token({"user_id": db_user.id})
        
        return {
            "message": "Login successful",
            "access_token": jwt_token,
            "user_id": db_user.id
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"Login error: {e}")
        raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")

# ==================== Instagram (via Facebook) OAuth ====================

@router.get('/instagram')
def instagram_auth():
    """Initiate Instagram OAuth flow (via Facebook Graph API)"""
    app_id = os.getenv("FACEBOOK_APP_ID")
    redirect = os.getenv("INSTAGRAM_REDIRECT_URI")
    state = "random_state_string"  # Should be randomized per request
    
    # Scopes required for Instagram Graph API
    scope = "instagram_basic,instagram_manage_insights,pages_show_list,pages_read_engagement"
    
    auth_url = (
        f"https://www.facebook.com/v18.0/dialog/oauth?"
        f"client_id={app_id}&"
        f"redirect_uri={redirect}&"
        f"state={state}&"
        f"scope={scope}&"
        f"response_type=code"
    )
    return {"auth_url": auth_url}

@router.get('/instagram/callback')
async def instagram_callback(code: str, db: Session = Depends(get_db)):
    """Handle Instagram OAuth callback"""
    app_id = os.getenv("FACEBOOK_APP_ID")
    secret = os.getenv("FACEBOOK_APP_SECRET")
    redirect = os.getenv("INSTAGRAM_REDIRECT_URI")
    
    async with httpx.AsyncClient() as client:
        # 1. Exchange code for User Access Token
        token_url = "https://graph.facebook.com/v18.0/oauth/access_token"
        params = {
            "client_id": app_id,
            "client_secret": secret,
            "redirect_uri": redirect,
            "code": code
        }
        res = await client.get(token_url, params=params)
        token_data = res.json()
        
        if "access_token" not in token_data:
            raise HTTPException(status_code=400, detail=f"Failed to get access token: {token_data}")
            
        user_access_token = token_data["access_token"]
        expires_in = token_data.get("expires_in", 5184000) # Default 60 days
        
        # 2. Get User's Pages to find the connected Instagram Business Account
        pages_url = "https://graph.facebook.com/v18.0/me/accounts"
        params = {
            "access_token": user_access_token,
            "fields": "id,name,access_token,instagram_business_account"
        }
        res = await client.get(pages_url, params=params)
        pages_data = res.json()
        
        if "data" not in pages_data:
             raise HTTPException(status_code=400, detail="Failed to retrieve pages")

        ig_account_id = None
        page_access_token = None
        
        # Find the first page with a connected Instagram Business Account
        for page in pages_data.get("data", []):
            if "instagram_business_account" in page:
                ig_account_id = page["instagram_business_account"]["id"]
                page_access_token = page["access_token"]
                break
        
        if not ig_account_id:
            raise HTTPException(status_code=400, detail="No Instagram Business Account connected to user's pages")

    # TODO: Get real user_id from session/auth
    dummy_user_id = 1
    
    # Calculate expiry
    expires_at = datetime.utcnow() + timedelta(seconds=expires_in)
    
    # Store social account
    crud.create_or_update_social_account(
        db=db,
        user_id=dummy_user_id,
        platform="instagram",
        account_id=ig_account_id,
        access_token=page_access_token,
        expires_at=expires_at
    )
    
    jwt_token = create_access_token({"user_id": dummy_user_id, "platform": "instagram"})
    
    return {
        "message": "Instagram connected successfully",
        "access_token": jwt_token,
        "platform": "instagram",
        "account_id": ig_account_id
    }

# ==================== YouTube OAuth ====================

@router.get('/youtube')
def youtube_auth():
    """Initiate YouTube OAuth flow"""
    client_id = os.getenv("GOOGLE_CLIENT_ID")
    redirect_uri = os.getenv("GOOGLE_REDIRECT_URI")
    
    scope = (
        "https://www.googleapis.com/auth/youtube.readonly "
        "https://www.googleapis.com/auth/yt-analytics.readonly"
    )
    
    auth_url = (
        f"https://accounts.google.com/o/oauth2/v2/auth?"
        f"client_id={client_id}&"
        f"redirect_uri={redirect_uri}&"
        f"response_type=code&"
        f"scope={scope}&"
        f"access_type=offline&"
        f"prompt=consent"
    )
    
    return {"auth_url": auth_url}

@router.get('/youtube/callback')
async def youtube_callback(code: str, db: Session = Depends(get_db)):
    """Handle YouTube OAuth callback"""
    client_id = os.getenv("GOOGLE_CLIENT_ID")
    client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
    redirect_uri = os.getenv("GOOGLE_REDIRECT_URI")
    
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "code": code,
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code"
    }
    
    async with httpx.AsyncClient() as client:
        # 1. Exchange code for tokens
        res = await client.post(token_url, data=data)
        token_data = res.json()
        
        if "access_token" not in token_data:
            raise HTTPException(status_code=400, detail="Failed to get access token")
            
        access_token = token_data["access_token"]
        refresh_token = token_data.get("refresh_token")
        expires_in = token_data.get("expires_in", 3600)
        
        # 2. Get Channel Info to get the Channel ID
        channel_url = "https://www.googleapis.com/youtube/v3/channels"
        params = {
            "part": "id,snippet",
            "mine": "true"
        }
        headers = {"Authorization": f"Bearer {access_token}"}
        
        res = await client.get(channel_url, params=params, headers=headers)
        channel_data = res.json()
        
        if "items" not in channel_data or not channel_data["items"]:
             raise HTTPException(status_code=400, detail="No YouTube channel found for this user")
             
        channel_id = channel_data["items"][0]["id"]

    dummy_user_id = 1
    expires_at = datetime.utcnow() + timedelta(seconds=expires_in)
    
    crud.create_or_update_social_account(
        db=db,
        user_id=dummy_user_id,
        platform="youtube",
        account_id=channel_id,
        access_token=access_token,
        refresh_token=refresh_token,
        expires_at=expires_at
    )
    
    jwt_token = create_access_token({"user_id": dummy_user_id, "platform": "youtube"})
    
    return {
        "message": "YouTube connected successfully",
        "access_token": jwt_token,
        "platform": "youtube",
        "account_id": channel_id
    }

GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://openidconnect.googleapis.com/v1/userinfo"

@router.get('/twitter')
def twitter_auth():
    """Initiate Twitter OAuth 2.0 flow"""
    client_id = os.getenv("TWITTER_CLIENT_ID")
    redirect_uri = os.getenv("TWITTER_REDIRECT_URI")
    
    state = "random_state_string"
    scope = "tweet.read users.read offline.access"
    
    auth_url = (
        f"https://twitter.com/i/oauth2/authorize?"
        f"response_type=code&"
        f"client_id={client_id}&"
        f"redirect_uri={redirect_uri}&"
        f"scope={scope}&"
        f"state={state}&"
        f"code_challenge=challenge&"
        f"code_challenge_method=plain"
    )
    
    return {"auth_url": auth_url}

@router.get('/twitter/callback')
async def twitter_callback(code: str, state: str, db: Session = Depends(get_db)):
    """Handle Twitter OAuth callback"""
    client_id = os.getenv("TWITTER_CLIENT_ID")
    client_secret = os.getenv("TWITTER_CLIENT_SECRET")
    redirect_uri = os.getenv("TWITTER_REDIRECT_URI")
    
    token_url = "https://api.twitter.com/2/oauth2/token"
    
    data = {
        "code": code,
        "grant_type": "authorization_code",
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "code_verifier": "challenge"
    }
    
    async with httpx.AsyncClient() as client:
        res = await client.post(
            token_url,
            data=data,
            auth=(client_id, client_secret)
        )
        token_data = res.json()
    
    if "access_token" not in token_data:
        raise HTTPException(status_code=400, detail="Failed to get access token")
    
    access_token = token_data["access_token"]
    
    async with httpx.AsyncClient() as client:
        user_res = await client.get(
            "https://api.twitter.com/2/users/me",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        user_data = user_res.json()
    
    twitter_user_id = user_data.get("data", {}).get("id")
    
    dummy_user_id = 1
    
    crud.create_or_update_social_account(
        db=db,
        user_id=dummy_user_id,
        platform="twitter",
        account_id=str(twitter_user_id),
        access_token=access_token
    )
    
    jwt_token = create_access_token({"user_id": dummy_user_id, "platform": "twitter"})
    
    return {
        "message": "Twitter connected successfully",
        "access_token": jwt_token,
        "platform": "twitter"
    }
