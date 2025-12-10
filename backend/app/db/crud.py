from sqlalchemy.orm import Session
from backend.app.db import models
from datetime import datetime

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def create_user(db: Session, username: str, email: str, hashed_password: str):
    user = models.User(username=username, email=email, hashed_password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def create_social_account(db: Session, user_id: int, platform: str, account_id: str, access_token: str):
    social = models.SocialAccount(
        user_id=user_id,
        platform=platform,
        account_id=account_id,
        access_token=access_token
    )
    db.add(social)
    db.commit()
    db.refresh(social)
    return social

def get_social_accounts(db: Session, user_id: int):
    return db.query(models.SocialAccount).filter(models.SocialAccount.user_id == user_id).all()


def create_post(db: Session, account_id: int, caption: str, posted_at):
    post = models.Post(account_id=account_id, caption=caption, posted_at=posted_at)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post



def create_or_update_social_account(
    db: Session, 
    user_id: int, 
    platform: str, 
    account_id: str, 
    access_token: str,
    refresh_token: str = None,
    expires_at: datetime = None
):
    """
    Create a new social account or update existing one
    
    This function handles both initial OAuth connection and token refresh.
    If an account already exists for this user+platform, it updates the token.
    Otherwise, it creates a new account record.
    
    Args:
        db: Database session
        user_id: User's ID
        platform: Platform name (instagram, twitter, youtube)
        account_id: Platform's user ID
        access_token: OAuth access token
        refresh_token: Optional OAuth refresh token
        expires_at: Optional token expiration time
        
    Returns:
        Created or updated SocialAccount object
    """
    # Check if account already exists
    account = get_social_account(db, user_id, platform)
    
    if account:
        # Update existing account
        account.access_token = access_token
        account.account_id = account_id  # Update account_id in case it changed
        if refresh_token:
            account.refresh_token = refresh_token
        if expires_at:
            account.expires_at = expires_at
    else:
        # Create new account
        account = models.SocialAccount(
            user_id=user_id,
            platform=platform,
            account_id=account_id,
            access_token=access_token,
            refresh_token=refresh_token,
            expires_at=expires_at
        )
        db.add(account)
 
def create_post_analytics(db: Session, post_id: int, likes: int, comments: int, shares: int, views: int):
    analytics = models.PostAnalytics(
        post_id=post_id,
        likes=likes,
        comments=comments,
        shares=shares,
        views=views
    )
    db.add(analytics)
    db.commit()
    db.refresh(analytics)
    return analytics


def get_all_posts_with_analytics(db: Session, user_id: int):
    return (
        db.query(models.PostAnalytics)
        .join(models.SocialAccount)
        .filter(models.SocialAccount.user_id == user_id)
        .all()
    )

def get_posts_with_analytics_joined(db: Session, user_id: int):
    return (
        db.query(models.Post)
        .join(models.PostAnalytics, models.Post.id == models.PostAnalytics.post_id)
        .join(models.SocialAccount, models.Post.account_id == models.SocialAccount.id)
        .filter(models.SocialAccount.user_id == user_id)
        .all()
    )
