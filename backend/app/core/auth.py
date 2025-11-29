"""
Authentication Utilities

This module provides JWT token generation/validation and password hashing.
Used by the authentication routes for secure user management.

Functions:
- hash_password: Hash a plain password using bcrypt
- verify_password: Verify a password against its hash
- create_access_token: Generate a JWT token for authentication
- decode_access_token: Decode and validate a JWT token
"""

import os
from datetime import datetime, timedelta
from typing import Optional
import jwt
from passlib.context import CryptContext

# Password hashing configuration
# Using bcrypt algorithm for secure password storage
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT configuration
# Load from environment variables for security
JWT_SECRET = os.getenv("JWT_SECRET", "your_secret_key_change_this_in_production")
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = 24  # Tokens expire after 24 hours


def hash_password(password: str) -> str:
    """
    Hash a plain text password using bcrypt
    
    Args:
        password: Plain text password
        
    Returns:
        Hashed password string
        
    Example:
        hashed = hash_password("mypassword123")
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against its hash
    
    Args:
        plain_password: Plain text password to verify
        hashed_password: Stored hashed password
        
    Returns:
        True if password matches, False otherwise
        
    Example:
        is_valid = verify_password("mypassword123", stored_hash)
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Create a JWT access token
    
    Args:
        data: Dictionary of data to encode in the token (e.g., user_id)
        expires_delta: Optional custom expiration time
        
    Returns:
        Encoded JWT token string
        
    Example:
        token = create_access_token({"user_id": 1})
    """
    to_encode = data.copy()
    
    # Set expiration time
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS)
    
    # Add expiration to token payload
    to_encode.update({"exp": expire})
    
    # Encode and return token
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str):
    """
    Decode and validate a JWT token
    
    Args:
        token: JWT token string
        
    Returns:
        Decoded token payload dict, or None if invalid/expired
        
    Example:
        payload = decode_access_token(token)
        if payload:
            user_id = payload.get("user_id")
    """
    try:
        # Decode token and verify signature
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        # Token has expired
        return None
    except jwt.InvalidTokenError:
        # Token is invalid
        return None
