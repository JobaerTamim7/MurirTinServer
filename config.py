# config.py
from pydantic_settings import BaseSettings,SettingsConfigDict

class Settings(BaseSettings):
    supabase_url: str
    supabase_anon_key: str
    supabase_jwt_secret: str
    redis_host: str 
    redis_port: int 
    redis_username: str 
    redis_password: str 
    jwt_secret: str = "c4cyOQHVt3yCB1Pb+VKCiORz8/h1R8fDvoedMmUwfTs4YNuFnoQYJAaK0s4CCVPf55vlZ8SZynXnumkpOHKM9Q=="
    jwt_algorithm: str = "HS256"
    jwt_expiration: int = 3600  


    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )
settings = Settings() # type: ignore