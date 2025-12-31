"""
Application Configuration
=========================
Environment variables and settings
"""

from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import List
from pathlib import Path
import logging

logger = logging.getLogger(__name__)
BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    # Database - Neon PostgreSQL
    database_url: str
    
    # Google Drive Folder URL
    google_drive_folder_url: str = "https://drive.google.com/drive/folders/1ms1u6tuw22Bsl1SsGpR1zXtkR_zsgddx"
    
    # OpenRouter API (for AI descriptions)
    openrouter_api_key: str = ""
    
    # CORS - Support multiple origins for production
    cors_origins: str = "http://localhost:3000"
    
    # Environment
    environment: str = "development"
    
    # Production settings
    frontend_url: str = "http://localhost:3000"
    
    @property
    def cors_origins_list(self) -> List[str]:
        origins = [origin.strip() for origin in self.cors_origins.split(",")]
        # Always include frontend_url in production
        if self.frontend_url and self.frontend_url not in origins:
            origins.append(self.frontend_url)
        return origins
    
    @property
    def is_production(self) -> bool:
        return self.environment == "production"
    
    class Config:
        env_file = str(BASE_DIR / ".env")
        extra = "allow"


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
