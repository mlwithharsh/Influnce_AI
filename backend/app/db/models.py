from sqlalchemy import (
    Column, String, Integer, DateTime, ForeignKey, Float, Text, Boolean
)
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    social_accounts = relationship("SocialAccount", back_populates="user")


class SocialAccount(Base):
    __tablename__ = "social_accounts"

    id = Column(Integer, primary_key=True, index=True)
    platform = Column(String, nullable=False)  # instagram / youtube / twitter
    account_id = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))

    access_token = Column(Text, nullable=True)
    refresh_token = Column(Text, nullable=True)
    expires_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="social_accounts")
    posts = relationship("Post", back_populates="social_account")

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    caption = Column(Text)
    posted_at = Column(DateTime, default=datetime.utcnow)
    account_id = Column(Integer, ForeignKey("social_accounts.id"))

    analytics = relationship("PostAnalytics", back_populates="post")


class PostAnalytics(Base):
    __tablename__ = "post_analytics"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id"))
    likes = Column(Integer, default=0)
    dislikes = Column(Integer, default=0)
    comments = Column(Integer, default=0)
    shares = Column(Integer, default=0)
    views = Column(Integer, default=0)
    predicted_best_time = Column(DateTime, nullable=True)

    post = relationship("Post", back_populates="analytics")


class Trend(Base):
    __tablename__ = "trends"

    id = Column(Integer, primary_key=True, index=True)
    platform = Column(String, nullable=False)
    hashtag = Column(String, nullable=True)
    song_name = Column(String, nullable=True)
    popularity_score = Column(Float, default=0.0)
    detected_at = Column(DateTime, default=datetime.utcnow)

class ModelMetadata(Base):
    __tablename__ = "model_metadata"

    id = Column(Integer, primary_key=True, index=True)
    model_name = Column(String, nullable=False)
    version = Column(String, nullable=False)
    trained_at = Column(DateTime, default=datetime.utcnow)
    mae = Column(Float, nullable=True)
