#!/usr/bin/env python3
"""
Authentication module for DroxAI
Handles user authentication, JWT tokens, and password hashing
"""

import os
import json
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict
from passlib.context import CryptContext
import jwt
from jwt import PyJWTError
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr

# Authentication Configuration
# Set REQUIRE_AUTH=false to disable authentication (useful for single-user deployments)
REQUIRE_AUTH = os.getenv("REQUIRE_AUTH", "false").lower() == "true"

# Admin Configuration
# Admin users (by email) get unlimited session time and don't pay
ADMIN_EMAILS = os.getenv("ADMIN_EMAILS", "").split(",")
ADMIN_EMAILS = [email.strip() for email in ADMIN_EMAILS if email.strip()]

# JWT Configuration
# In production, always set JWT_SECRET_KEY environment variable to a secure random value
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
if not SECRET_KEY:
    # Only use default in development
    import sys
    if "pytest" not in sys.modules and os.getenv("ENVIRONMENT") == "production":
        raise ValueError("JWT_SECRET_KEY must be set in production environment")
    SECRET_KEY = "droxai-dev-secret-key-change-in-production"
    
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Default for regular users
ADMIN_TOKEN_EXPIRE_DAYS = 365  # 1 year for admin users

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Security scheme - auto_error=False allows optional authentication
security = HTTPBearer(auto_error=False)

# Pydantic models
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    username: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    email: str
    username: str
    created_at: str

class Token(BaseModel):
    access_token: str
    token_type: str

# Simple file-based user storage (minimal change approach)
USERS_FILE = os.path.join(os.path.dirname(__file__), "users.json")

def load_users() -> Dict:
    """Load users from JSON file"""
    import logging
    logger = logging.getLogger(__name__)
    
    if not os.path.exists(USERS_FILE):
        return {}
    try:
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        logger.error(f"Error loading users file: {e}")
        return {}

def save_users(users: Dict):
    """Save users to JSON file"""
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None, is_admin: bool = False) -> str:
    """Create a JWT access token (admin users get extended expiration)"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    elif is_admin:
        # Admin users get 1 year tokens (no time limit)
        expire = datetime.now(timezone.utc) + timedelta(days=ADMIN_TOKEN_EXPIRE_DAYS)
    else:
        # Regular users get standard expiration
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "is_admin": is_admin})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_token(token: str) -> Optional[Dict]:
    """Decode and validate a JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except PyJWTError:
        return None

def is_admin_user(email: str) -> bool:
    """Check if user is an admin"""
    return email in ADMIN_EMAILS

def get_user(email: str) -> Optional[Dict]:
    """Get user by email"""
    users = load_users()
    user = users.get(email)
    if user:
        # Add admin flag to user data
        user["is_admin"] = is_admin_user(email)
    return user

def create_user(email: str, username: str, password: str) -> Dict:
    """Create a new user"""
    users = load_users()
    
    # Check if user already exists
    if email in users:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create user
    user = {
        "email": email,
        "username": username,
        "hashed_password": get_password_hash(password),
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    
    users[email] = user
    save_users(users)
    
    return user

def authenticate_user(email: str, password: str) -> Optional[Dict]:
    """Authenticate a user"""
    user = get_user(email)
    if not user:
        return None
    if not verify_password(password, user["hashed_password"]):
        return None
    return user

async def get_current_user(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)) -> Dict:
    """Get current authenticated user from token (or anonymous user if auth disabled)"""
    
    # If authentication is disabled, return anonymous user
    if not REQUIRE_AUTH:
        return {
            "email": "anonymous@localhost",
            "username": "Anonymous User",
            "created_at": datetime.now(timezone.utc).isoformat()
        }
    
    # Authentication is required - validate token
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = credentials.credentials
    payload = decode_token(token)
    
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    email: str = payload.get("sub")
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = get_user(email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user
