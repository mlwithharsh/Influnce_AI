from sqlalchemy.orm import Session
from backend.app.db import models

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

