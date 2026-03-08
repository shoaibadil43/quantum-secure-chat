"""
FastAPI Application Entry Point
Quantum Secure Chat Backend
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.gzip import GZipMiddleware
from sqlalchemy import text

from app.config import settings
from app.db.database import Base, engine
from app.routes import auth, users, messages, websocket

# Create FastAPI app

app = FastAPI(
title="Quantum Secure Chat API",
version="1.0.0"
)

# Enable CORS

app.add_middleware(
CORSMiddleware,
allow_origins=["*"],
allow_credentials=True,
allow_methods=["*"],
allow_headers=["*"],
)

# Enable compression

app.add_middleware(GZipMiddleware)

# Trusted host middleware

app.add_middleware(
TrustedHostMiddleware,
allowed_hosts=["*"]
)

# Create database tables

Base.metadata.create_all(bind=engine)

# Register API routes

app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(messages.router, prefix="/api/messages", tags=["Messages"])
app.include_router(websocket.router, prefix="/api/ws", tags=["WebSocket"])

# Root endpoint

@app.get("/")
def root():
    return {
    "message": "Quantum Secure Chat API",
    "version": settings.APP_VERSION,
    "status": "running"
    }

# Health check

@app.get("/health")
def health_check():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return {
            "status": "healthy",
            "database": "connected"
        }
    except Exception:
        return {
            "status": "unhealthy",
            "database": "error"
        }
