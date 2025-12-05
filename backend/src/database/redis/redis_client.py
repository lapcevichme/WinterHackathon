from redis.asyncio import Redis
from core.config import Settings

config = Settings() # pyright: ignore[reportCallIssue]

redis_client = Redis.from_url(config.REDIS_URL, decode_responses=True)

def get_redis() -> Redis:
    """Returns prepared Redis session"""
    return redis_client
    
