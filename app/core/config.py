import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from typing import List

# Load environment file based on ENV_PATH or default to .env.dev
env_file = os.getenv("ENV_PATH", ".env.dev")
load_dotenv(dotenv_path=env_file)
ENV_FILE_USED = env_file

class Settings(BaseSettings):
    ENV: str = os.getenv("ENV", "development")
    APP_VERSION: str = os.getenv("APP_VERSION", "1.0.0")

    DATABASE_URL: str

    OFFICE_LAT: float = 43.670116
    OFFICE_LNG: float = -79.385757

    ALLOWED_ORIGINS: List[str] = []

    class Config:
        env_file = env_file
        case_sensitive = True

settings = Settings()

def get_settings() -> Settings:
    return settings
