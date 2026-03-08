"""
WebSocket Routes
Real-time chat and messaging
"""

from fastapi import APIRouter, WebSocket, Depends, HTTPException, status
from sqlalchemy.orm import Session
import json
import logging
from typing import Optional

from app.db.database import get_db
from app.models import Message, ChatSession, User
from app.websocket_manager import connection_manager
from app.auth.jwt_handler import jwt_handler
from app.security.encryption import encryption_manager
from app.utils.validators import validators

logger = logging.getLogger(__name__)

router = APIRouter()


def verify_token_from_query(token: str) -> Optional[str]:
    """Verify JWT token from query parameter"""
    payload = jwt_handler.verify_token(token)
    if payload:
        return payload.get("sub")
    return None


@router.websocket("/chat/{room_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    room_id: str,
    token: str,
    db: Session = Depends(get_db)
):
    """WebSocket endpoint for real-time chat"""
    
    # Verify token
    user_id = verify_token_from_query(token)
    if not user_id:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        logger.warning(f"Invalid token for room {room_id}")
        return
    
    # Verify user and room access
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return
    
    session = db.query(ChatSession).filter(ChatSession.id == room_id).first()
    if not session:
        await websocket.close(code=status.WS_1011_SERVER_ERROR)
        logger.warning(f"Room {room_id} not found")
        return
    
    # Connect
    await connection_manager.connect(websocket, user_id, room_id)
    
    # Notify others
    await connection_manager.broadcast_to_room(
        room_id,
        {
            "type": "user_joined",
            "user_id": user_id,
            "username": user.username,
            "timestamp": str(__import__('datetime').datetime.utcnow())
        },
        exclude_user=user_id
    )
    
    try:
        while True:
            # Receive message
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            message_type = message_data.get("type", "message")
            
            if message_type == "message":
                # Validate message
                is_valid, error_msg = validators.validate_message(message_data.get("content", ""))
                if not is_valid:
                    await websocket.send_json({"type": "error", "message": error_msg})
                    continue
                
                # Store in database
                content = message_data.get("content")
                db_message = Message(
                    session_id=room_id,
                    sender_id=user_id,
                    content=content,
                    is_delivered=True
                )
                db.add(db_message)
                db.commit()
                db.refresh(db_message)
                
                # Broadcast to room
                await connection_manager.broadcast_to_room(
                    room_id,
                    {
                        "type": "message",
                        "message_id": db_message.id,
                        "sender_id": user_id,
                        "username": user.username,
                        "content": content,
                        "timestamp": str(db_message.created_at)
                    }
                )
            
            elif message_type == "typing":
                # Broadcast typing indicator
                await connection_manager.broadcast_to_room(
                    room_id,
                    {
                        "type": "typing",
                        "user_id": user_id,
                        "username": user.username
                    },
                    exclude_user=user_id
                )
            
            elif message_type == "stop_typing":
                # Broadcast stop typing
                await connection_manager.broadcast_to_room(
                    room_id,
                    {
                        "type": "stop_typing",
                        "user_id": user_id
                    },
                    exclude_user=user_id
                )
    
    except Exception as e:
        logger.error(f"WebSocket error: {str(e)}")
    
    finally:
        connection_manager.disconnect(user_id, websocket)
        
        # Notify others
        await connection_manager.broadcast_to_room(
            room_id,
            {
                "type": "user_left",
                "user_id": user_id,
                "username": user.username,
                "timestamp": str(__import__('datetime').datetime.utcnow())
            }
        )


@router.post("/generate-key/{room_id}")
async def generate_quantum_key(
    room_id: str,
    token: str = None,
    db: Session = Depends(get_db)
):
    """Generate BB84 quantum key for room"""
    
    if not token:
        raise HTTPException(status_code=401, detail="No token provided")
    
    user_id = verify_token_from_query(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    session = db.query(ChatSession).filter(ChatSession.id == room_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Generate key using BB84
    from app.security.bb84.bb84 import run_simple_bb84
    
    result = run_simple_bb84(qubit_count=4096)
    
    return {
        "status": "success",
        "key_generated": result.get("success"),
        "key_length": result.get("final_key_bytes"),
        "qber": result.get("qber"),
        "security_message": result.get("security_message")
    }
