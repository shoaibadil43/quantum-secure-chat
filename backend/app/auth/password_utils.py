"""
Password Utilities
Password hashing and validation
"""

from passlib.context import CryptContext
import logging

logger = logging.getLogger(__name__)

# Password hashing context
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12
)


class PasswordUtils:
    """Password utility functions"""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password"""
        try:
            return pwd_context.hash(password)
        except Exception as e:
            logger.error(f"Password hashing error: {str(e)}")
            raise
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify password against hash"""
        try:
            return pwd_context.verify(plain_password, hashed_password)
        except Exception as e:
            logger.error(f"Password verification error: {str(e)}")
            return False
    
    @staticmethod
    def is_strong_password(password: str) -> bool:
        """Check if password meets strength requirements"""
        # Simple requirement: at least 6 characters
        return len(password) >= 6


password_utils = PasswordUtils()
