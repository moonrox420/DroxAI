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
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Security scheme
security = HTTPBearer()

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
    if not os.path.exists(USERS_FILE):
        return {}
    try:
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        # Log the error in production
        print(f"Error loading users file: {e}")
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

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_token(token: str) -> Optional[Dict]:
    """Decode and validate a JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except PyJWTError:
        return None

def get_user(email: str) -> Optional[Dict]:
    """Get user by email"""
    users = load_users()
    return users.get(email)

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

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict:
    """Get current authenticated user from token"""
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
