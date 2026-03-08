"""
Input Validators
"""

import re
from typing import Tuple


class Validators:
    """Input validation utilities"""
    
    @staticmethod
    def validate_email(email: str) -> Tuple[bool, str]:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if re.match(pattern, email):
            return True, ""
        return False, "Invalid email format"
    
    @staticmethod
    def validate_username(username: str) -> Tuple[bool, str]:
        """Validate username"""
        if len(username) < 3:
            return False, "Username must be at least 3 characters"
        if len(username) > 255:
            return False, "Username must be less than 255 characters"
        if not re.match(r'^[a-zA-Z0-9_-]+$', username):
            return False, "Username can only contain letters, numbers, _, and -"
        return True, ""
    
    @staticmethod
    def validate_message(message: str) -> Tuple[bool, str]:
        """Validate message"""
        if not message or not message.strip():
            return False, "Message cannot be empty"
        if len(message) > 4096:
            return False, "Message exceeds maximum length (4096 chars)"
        return True, ""
    
    @staticmethod
    def validate_room_name(name: str) -> Tuple[bool, str]:
        """Validate chat room name"""
        if not name or not name.strip():
            return False, "Room name cannot be empty"
        if len(name) > 255:
            return False, "Room name exceeds maximum length (255 chars)"
        return True, ""


validators = Validators()
