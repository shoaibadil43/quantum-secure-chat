"""
Authentication Routes
User registration, login, and token refresh
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
import logging

from app.db.database import get_db
from app.db.schemas import UserCreate, UserLogin, TokenResponse, UserResponse
from app.models import User
from app.auth.password_utils import password_utils
from app.auth.jwt_handler import jwt_handler
from app.utils.validators import validators

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/register", response_model=UserResponse)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    
    # Validate input
    is_valid, error_msg = validators.validate_email(user_data.email)
    if not is_valid:
        raise HTTPException(status_code=400, detail=error_msg)
    
    is_valid, error_msg = validators.validate_username(user_data.username)
    if not is_valid:
        raise HTTPException(status_code=400, detail=error_msg)
    
    if not password_utils.is_strong_password(user_data.password):
        raise HTTPException(
            status_code=400,
            detail="Password must contain uppercase, lowercase, digit, and special character"
        )
    
    # Check existing user
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=409, detail="Email already registered")
    
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(status_code=409, detail="Username already taken")
    
    # Create user
    user = User(
        username=user_data.username,
        email=user_data.email,
        password_hash=password_utils.hash_password(user_data.password),
        full_name=user_data.full_name
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    logger.info(f"New user registered: {user.username}")
    return user


@router.post("/login", response_model=TokenResponse)
async def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    """Login user and return tokens"""
    
    user = db.query(User).filter(User.email == user_credentials.email).first()
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if not user.is_active:
        raise HTTPException(status_code=403, detail="User account is disabled")
    
    if not password_utils.verify_password(user_credentials.password, user.password_hash):
        # Increment failed attempts
        user.failed_login_attempts += 1
        db.commit()
        
        if user.failed_login_attempts >= 5:
            from datetime import datetime, timedelta
            user.locked_until = datetime.utcnow() + timedelta(minutes=15)
            db.commit()
            raise HTTPException(status_code=429, detail="Account locked due to failed attempts")
        
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Reset failed attempts on successful login
    user.failed_login_attempts = 0
    from datetime import datetime
    user.last_login = datetime.utcnow()
    db.commit()
    
    # Create tokens
    access_token = jwt_handler.create_access_token(
        data={"sub": user.id, "username": user.username}
    )
    refresh_token = jwt_handler.create_refresh_token(
        data={"sub": user.id}
    )
    
    logger.info(f"User logged in: {user.username}")
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": 30 * 60
    }


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(token: str):
    """Refresh access token"""
    
    payload = jwt_handler.verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    # Create new access token
    access_token = jwt_handler.create_access_token(
        data={"sub": payload.get("sub"), "username": payload.get("username")}
    )
    
    return {
        "access_token": access_token,
        "refresh_token": token,
        "token_type": "bearer",
        "expires_in": 30 * 60
    }
