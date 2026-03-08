"""
Message Routes
Message history and management
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import logging

from app.db.database import get_db
from app.db.schemas import MessageCreate, MessageResponse
from app.models import Message, ChatSession
from app.auth.jwt_handler import jwt_handler

logger = logging.getLogger(__name__)

router = APIRouter()


def get_current_user_id(token: str = None) -> str:
    """Get current user ID from token"""
    if not token:
        raise HTTPException(status_code=401, detail="No token provided")
    
    payload = jwt_handler.verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    return payload.get("sub")


@router.get("/session/{session_id}", response_model=list[MessageResponse])
async def get_session_messages(
    session_id: str,
    skip: int = 0,
    limit: int = 50,
    token: str = None,
    db: Session = Depends(get_db)
):
    """Get messages from a chat session"""
    
    user_id = get_current_user_id(token)
    
    # Verify access
    session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    messages = (
        db.query(Message)
        .filter(Message.session_id == session_id)
        .order_by(Message.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    
    return list(reversed(messages))


@router.post("/{message_id}/read")
async def mark_as_read(
    message_id: str,
    token: str = None,
    db: Session = Depends(get_db)
):
    """Mark message as read"""
    
    user_id = get_current_user_id(token)
    
    message = db.query(Message).filter(Message.id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    
    message.is_read = True
    db.commit()
    
    return {"status": "marked_read"}


@router.delete("/{message_id}")
async def delete_message(
    message_id: str,
    token: str = None,
    db: Session = Depends(get_db)
):
    """Delete a message"""
    
    user_id = get_current_user_id(token)
    
    message = db.query(Message).filter(
        Message.id == message_id,
        Message.sender_id == user_id
    ).first()
    
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    
    db.delete(message)
    db.commit()
    
    return {"status": "deleted"}
