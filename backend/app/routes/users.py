"""
User Routes
User profile and settings
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import logging

from app.db.database import get_db
from app.db.schemas import UserResponse
from app.models import User
from app.auth.jwt_handler import jwt_handler

logger = logging.getLogger(__name__)

router = APIRouter()


def get_current_user(token: str, db: Session = Depends(get_db)) -> User:
    """Dependency to get current authenticated user"""
    payload = jwt_handler.verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    user_id = payload.get("sub")
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user


@router.get("/me", response_model=UserResponse)
async def get_user_profile(current_user: User = Depends(get_current_user)):
    """Get current user profile"""
    return current_user


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: str, db: Session = Depends(get_db)):
    """Get user by ID"""
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user


@router.get("", response_model=list[UserResponse])
async def list_users(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    """List all active users"""
    users = db.query(User).filter(User.is_active == True).offset(skip).limit(limit).all()
    return users
