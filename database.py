# database.py
from supabase import create_client, Client
from config import settings
from redis.asyncio import Redis
from asyncio import run


redis : Redis = Redis(
    host=settings.redis_host,
    port=settings.redis_port,
    decode_responses=True,
    username=settings.redis_username,
    password=settings.redis_password
)
supabase: Client = create_client(settings.supabase_url, settings.supabase_anon_key)