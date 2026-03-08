"""
Database Schemas (Pydantic)
Used for request/response validation
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime


class UserCreate(BaseModel):
    """User creation schema"""
    username: str = Field(..., min_length=3, max_length=255)
    email: EmailStr
    password: str = Field(..., min_length=12)
    full_name: Optional[str] = None


class UserResponse(BaseModel):
    """User response schema"""
    id: str
    username: str
    email: str
    full_name: Optional[str]
    avatar_url: Optional[str]
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    """User login schema"""
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """Token response schema"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class MessageCreate(BaseModel):
    """Message creation schema"""
    session_id: str
    content: str = Field(..., min_length=1, max_length=4096)
    encryption_key_id: Optional[str] = None


class MessageResponse(BaseModel):
    """Message response schema"""
    id: str
    sender_id: str
    session_id: str
    content: str
    encrypted_content: Optional[str]
    is_delivered: bool
    is_read: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class ChatSessionCreate(BaseModel):
    """Chat session creation schema"""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    is_group: bool = False
    is_encrypted: bool = True


class ChatSessionResponse(BaseModel):
    """Chat session response schema"""
    id: str
    owner_id: str
    name: str
    description: Optional[str]
    is_group: bool
    is_encrypted: bool
    created_at: datetime
    messages: List[MessageResponse] = []
    
    class Config:
        from_attributes = True


class EncryptionKey(BaseModel):
    """Encryption key schema"""
    id: str
    session_id: str
    key_type: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True
