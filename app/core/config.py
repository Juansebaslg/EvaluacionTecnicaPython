# app/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Settings(BaseSettings):
    APP_NAME: str = "chat-messages-api"
    DATABASE_URL: str = "sqlite:///./app.db"
    BANNED_WORDS: List[str] = ["palabrota1", "palabrota2", "foo", "bar"]
    MAX_LIMIT: int = 100
    DEFAULT_LIMIT: int = 20
    API_KEY: str = "supersecretkey" 

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)

settings = Settings()






