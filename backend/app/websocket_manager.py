"""
WebSocket Connection Manager
Handles WebSocket connections and message routing
"""

import json
import logging
from typing import Dict, Set, List, Optional
from fastapi import WebSocket
from datetime import datetime
import asyncio

logger = logging.getLogger(__name__)


class ConnectionManager:
    """Manages WebSocket connections"""
    
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}
        self.user_rooms: Dict[str, Set[str]] = {}
        self.connection_metadata: Dict[WebSocket, dict] = {}
    
    async def connect(self, websocket: WebSocket, user_id: str, room_id: str):
        """Register a new connection"""
        await websocket.accept()
        
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
        self.active_connections[user_id].append(websocket)
        
        if room_id not in self.user_rooms:
            self.user_rooms[room_id] = set()
        self.user_rooms[room_id].add(user_id)
        
        self.connection_metadata[websocket] = {
            "user_id": user_id,
            "room_id": room_id,
            "connected_at": datetime.utcnow(),
            "messages_sent": 0
        }
        
        logger.info(f"User {user_id} connected to room {room_id}")
    
    def disconnect(self, user_id: str, websocket: WebSocket):
        """Remove a connection"""
        if user_id in self.active_connections:
            self.active_connections[user_id].remove(websocket)
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]
        
        if websocket in self.connection_metadata:
            room_id = self.connection_metadata[websocket]["room_id"]
            if room_id in self.user_rooms:
                self.user_rooms[room_id].discard(user_id)
            del self.connection_metadata[websocket]
        
        logger.info(f"User {user_id} disconnected")
    
    async def broadcast_to_room(self, room_id: str, message: dict, exclude_user: Optional[str] = None):
        """Send message to all users in a room"""
        if room_id not in self.user_rooms:
            return
        
        disconnected = []
        for user_id in self.user_rooms[room_id]:
            if exclude_user and user_id == exclude_user:
                continue
            
            if user_id in self.active_connections:
                for connection in self.active_connections[user_id]:
                    try:
                        await connection.send_json(message)
                    except Exception as e:
                        logger.error(f"Error sending to {user_id}: {str(e)}")
                        disconnected.append((user_id, connection))
        
        for user_id, conn in disconnected:
            self.disconnect(user_id, conn)
    
    async def send_personal_message(self, user_id: str, message: dict):
        """Send message to specific user"""
        if user_id in self.active_connections:
            disconnected = []
            for connection in self.active_connections[user_id]:
                try:
                    await connection.send_json(message)
                except Exception as e:
                    logger.error(f"Error sending to {user_id}: {str(e)}")
                    disconnected.append(connection)
            
            for conn in disconnected:
                self.disconnect(user_id, conn)
    
    def get_room_users(self, room_id: str) -> Set[str]:
        """Get all active users in a room"""
        return self.user_rooms.get(room_id, set())
    
    def get_active_connections_count(self) -> int:
        """Get total active connections"""
        return sum(len(conns) for conns in self.active_connections.values())


# Global connection manager instance
connection_manager = ConnectionManager()
