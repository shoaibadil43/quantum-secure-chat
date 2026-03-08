"""
Redis Client for Pub/Sub and Caching
"""

import redis
import json
import logging
from typing import Optional, List
from app.config import settings

logger = logging.getLogger(__name__)


class RedisClient:
    """Redis client for pub/sub and caching"""
    
    def __init__(self, url: str = None):
        """Initialize Redis client"""
        url = url or settings.REDIS_URL
        try:
            self.client = redis.from_url(url, decode_responses=True)
            self.client.ping()
            logger.info("Redis connected successfully")
        except Exception as e:
            logger.error(f"Redis connection failed: {str(e)}")
            raise
    
    def publish_message(self, channel: str, message: dict) -> int:
        """Publish message to channel"""
        try:
            return self.client.publish(channel, json.dumps(message))
        except Exception as e:
            logger.error(f"Publish failed: {str(e)}")
            return 0
    
    def set_cache(self, key: str, value: dict, ttl: int = 3600):
        """Set cache value with TTL"""
        try:
            self.client.setex(
                key,
                ttl,
                json.dumps(value)
            )
        except Exception as e:
            logger.error(f"Cache set failed: {str(e)}")
    
    def get_cache(self, key: str) -> Optional[dict]:
        """Get cached value"""
        try:
            value = self.client.get(key)
            return json.loads(value) if value else None
        except Exception as e:
            logger.error(f"Cache get failed: {str(e)}")
            return None
    
    def delete_cache(self, key: str):
        """Delete cache key"""
        try:
            self.client.delete(key)
        except Exception as e:
            logger.error(f"Cache delete failed: {str(e)}")
    
    def store_session(self, session_id: str, user_data: dict, ttl: int = 86400):
        """Store session data"""
        key = f"session:{session_id}"
        self.set_cache(key, user_data, ttl)
    
    def get_session(self, session_id: str) -> Optional[dict]:
        """Retrieve session data"""
        key = f"session:{session_id}"
        return self.get_cache(key)
    
    def close(self):
        """Close Redis connection"""
        try:
            self.client.close()
            logger.info("Redis connection closed")
        except Exception as e:
            logger.error(f"Error closing Redis: {str(e)}")


redis_client = None


def get_redis_client() -> RedisClient:
    """Get redis client instance"""
    global redis_client
    if redis_client is None:
        redis_client = RedisClient()
    return redis_client
