    finally:
        db.close()

# ==================== Instagram OAuth ====================

@router.get('/instagram')
def instagram_auth():
    """Initiate Instagram OAuth flow"""
    app_id = os.getenv("INSTAGRAM_APP_ID")
    redirect = os.getenv("INSTAGRAM_REDIRECT_URI")
    auth_url = f"https://api.instagram.com/oauth/authorize?client_id={app_id}&redirect_uri={redirect}&scope=user_profile,user_media&response_type=code"
    return {"auth_url": auth_url}

@router.get('/instagram/callback')
async def instagram_callback(code: str, db: Session = Depends(get_db)):
    """Handle Instagram OAuth callback"""
    app_id = os.getenv("INSTAGRAM_APP_ID")
    secret = os.getenv("INSTAGRAM_SECRET")
    redirect = os.getenv("INSTAGRAM_REDIRECT_URI")
    
    # Exchange code for access token
    token_url = "https://api.instagram.com/oauth/access_token"
    data = {
        "client_id": app_id,
        "client_secret": secret,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect,
    }
    
    async with httpx.AsyncClient() as client:
        res = await client.post(token_url, data=data)
        token_data = res.json()
    
    if "access_token" not in token_data:
        raise HTTPException(status_code=400, detail="Failed to get access token")
    
    access_token = token_data["access_token"]
    user_id = token_data.get("user_id")
    
    # TODO: Create or get user, for now using a dummy user_id=1
    # In production, you'd create a user or link to existing user
    dummy_user_id = 1
    
    # Store social account
    crud.create_or_update_social_account(
        db=db,
        user_id=dummy_user_id,
        platform="instagram",
        account_id=str(user_id),
        access_token=access_token
    )
    
    # Create JWT token for the user
    jwt_token = create_access_token({"user_id": dummy_user_id, "platform": "instagram"})
    
    return {
        "message": "Instagram connected successfully",
        "access_token": jwt_token,
        "platform": "instagram"
    }

# ==================== Twitter/X OAuth ====================

@router.get('/twitter')
def twitter_auth():
    """Initiate Twitter OAuth 2.0 flow"""
    client_id = os.getenv("TWITTER_CLIENT_ID")
    redirect_uri = os.getenv("TWITTER_REDIRECT_URI")
    
    # Twitter OAuth 2.0 with PKCE
    state = "random_state_string"  # In production, generate and store this securely
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
    
    # Exchange code for access token
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
    
    # Get user info
    async with httpx.AsyncClient() as client:
        user_res = await client.get(
            "https://api.twitter.com/2/users/me",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        user_data = user_res.json()
    
    twitter_user_id = user_data.get("data", {}).get("id")
    
    # TODO: Create or get user
    dummy_user_id = 1
    
    # Store social account
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

# ==================== YouTube (Google) OAuth ====================

@router.get('/youtube')
def youtube_auth():
    """Initiate YouTube (Google) OAuth flow"""
    client_id = os.getenv("GOOGLE_CLIENT_ID")
    redirect_uri = os.getenv("GOOGLE_REDIRECT_URI")
    
    scope = "https://www.googleapis.com/auth/youtube.readonly https://www.googleapis.com/auth/yt-analytics.readonly"
    
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
    
    # Exchange code for access token
    token_url = "https://oauth2.googleapis.com/token"
    
    data = {
        "code": code,
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code"
    }
    
    async with httpx.AsyncClient() as client:
        res = await client.post(token_url, data=data)
        token_data = res.json()
    
    if "access_token" not in token_data:
        raise HTTPException(status_code=400, detail="Failed to get access token")
    
    access_token = token_data["access_token"]
    
    # Get YouTube channel info
    async with httpx.AsyncClient() as client:
        channel_res = await client.get(
            "https://www.googleapis.com/youtube/v3/channels?part=id&mine=true",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        channel_data = channel_res.json()
    
    channel_id = channel_data.get("items", [{}])[0].get("id")
    
    # TODO: Create or get user
    dummy_user_id = 1
    
    # Store social account
    crud.create_or_update_social_account(
        db=db,
        user_id=dummy_user_id,
        platform="youtube",
        account_id=str(channel_id),
        access_token=access_token
    )
    
    jwt_token = create_access_token({"user_id": dummy_user_id, "platform": "youtube"})
    
    return {
        "message": "YouTube connected successfully",
        "access_token": jwt_token,
        "platform": "youtube"
    }

# ==================== User Registration/Login ====================

from pydantic import BaseModel

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
    from backend.app.core.auth import hash_password
    
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

@router.post('/login')
def login(user: UserLogin, db: Session = Depends(get_db)):
    """Login user"""
    from backend.app.core.auth import verify_password
    
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