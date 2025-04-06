import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from typing import List


# Automatically load .env
env_file = os.getenv("ENV_PATH", ".env.dev")
load_dotenv(dotenv_path=env_file)
ENV_FILE_USED = env_file

class Settings(BaseSettings):
    ENV: str = os.getenv("ENV", "development")
    APP_VERSION: str = os.getenv("APP_VERSION", "unknown")
    YELP_API_KEY: str
    YELP_BASE_URL: str

    OFFICE_LAT: float = 43.670116
    OFFICE_LNG: float = -79.385757

    ALLOWED_ORIGINS: List[str] = []



settings = Settings()
