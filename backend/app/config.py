"""
Application Configuration
Manages environment variables and app settings
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings"""
    
    # Server
    APP_NAME: str = "Quantum Secure Chat"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "False") == "True"
    
    # Database
    DATABASE_URL: str = os.getenv(
    "DATABASE_URL",
    "sqlite:///./test.db"
)
    
    # Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    
    # JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Encryption
    MASTER_KEY: str = os.getenv("MASTER_KEY", "default-master-key-32-bytes-long")
    
    # BB84 Configuration
    BB84_QUBIT_COUNT: int = 4096
    BB84_ERROR_THRESHOLD: float = 0.11
    BB84_SIFT_RATIO: float = 0.5
    
    # CORS
    CORS_ORIGINS: list = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]
    
    # Security
    MAX_FAILED_LOGIN_ATTEMPTS: int = 5
    LOCKOUT_DURATION_MINUTES: int = 15
    
    model_config = {
    "env_file": ".env",
    "case_sensitive": True
}

settings = Settings()
