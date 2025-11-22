# ORM entities that map to PostgreSQL tables.

from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, Float, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True , index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    social_accounts = relationship("SocialAccount", back_populates="user")


class SocialAccount(Base):
    __tablename__ = "social_accounts"
    id = Column(Integer, primary_key=True , index=True)
    platform = Column(String, unique=True,  nullable=False)
    account_id = Column(String, unique=True, nullable=False)
    access_token = Column(String ,nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="social_accounts")
    posts = relationship("Post", back_populates="social_account")


class PostAnalytics(Base):
    __tablename__ = "post_analytics"
    id = Column(Integer, primary_key=True , index=True)
    post_id = Column(Integer, ForeignKey("post_analytics.id"))
    caption = Column(Text , nullable=False)
    likes = Column(Integer, default=0)
    dislikes = Column(Integer, default=0)
    comments = Column(Integer, default=0)
    share = Column(Integer, default=0)
    views = Column(Integer, default=0)
    posted_at = Column(Integer, default=0 , nullable=False)
    predicted_best_time = Column(DateTime, nullable=True)
    account_id = Column(Integer, ForeignKey("social_accounts.id"))

    account = relationship("SocialAccount", back_populates="posts")

class Trend(Base):
    __tablename__ = "trends"
    id = Column(Integer, primary_key=True , index=True)
    platform = Column(String, unique=True, nullable=False)
    hashtag = Column(String, unique=True, index=True,  nullable=True)
    song_name = Column(String, unique=True, index=True,  nullable=True)
    popularity_score = Column(Float, default=0.0)
    detected_at = Column(DateTime, default=datetime.utcnow)

    