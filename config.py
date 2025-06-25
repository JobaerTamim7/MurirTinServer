# config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    supabase_url: str
    supabase_anon_key: str
    supabase_jwt_secret: str
    jwt_secret: str = "c4cyOQHVt3yCB1Pb+VKCiORz8/h1R8fDvoedMmUwfTs4YNuFnoQYJAaK0s4CCVPf55vlZ8SZynXnumkpOHKM9Q=="
    jwt_algorithm: str = "HS256"
    jwt_expiration: int = 3600  # 1 hour in seconds

    class Config:
        env_file = ".env"

settings = Settings()