from pydantic_settings import BaseSettings
from typing import List, Optional
import os


class Settings(BaseSettings):
    """Application settings using Pydantic for validation and type safety."""
    
    # API Configuration
    api_title: str = "Editer API"
    api_description: str = "A minimalistic, easily shareable text editor API"
    api_version: str = "1.0.0"
    debug: bool = False
    
    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 8000
    
    # Database Configuration
    mongodb_url: str = "mongodb://localhost:27017"
    database_name: str = "editer"
    
    # CORS Configuration
    allowed_origins: str = "http://localhost:3000,http://localhost:5173,http://127.0.0.1:3000,http://127.0.0.1:5173"
    
    # Security Configuration
    secret_key: Optional[str] = None
    access_token_expire_minutes: int = 30
    
    # Document Configuration
    max_document_size: int = 1024 * 1024  # 1MB
    max_title_length: int = 200
    max_content_length: int = 10 * 1024 * 1024  # 10MB
    
    # Rate Limiting
    rate_limit_requests: int = 100
    rate_limit_window: int = 60  # seconds
    
    # Logging Configuration
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        
        # Environment variable mapping
        fields = {
            "api_title": {"env": "API_TITLE"},
            "api_description": {"env": "API_DESCRIPTION"},
            "api_version": {"env": "API_VERSION"},
            "debug": {"env": "DEBUG"},
            "host": {"env": "API_HOST"},
            "port": {"env": "API_PORT"},
            "mongodb_url": {"env": "MONGODB_URL"},
            "database_name": {"env": "DATABASE_NAME"},
            "allowed_origins": {"env": "ALLOWED_ORIGINS"},
            "secret_key": {"env": "SECRET_KEY"},
            "access_token_expire_minutes": {"env": "ACCESS_TOKEN_EXPIRE_MINUTES"},
            "max_document_size": {"env": "MAX_DOCUMENT_SIZE"},
            "max_title_length": {"env": "MAX_TITLE_LENGTH"},
            "max_content_length": {"env": "MAX_CONTENT_LENGTH"},
            "rate_limit_requests": {"env": "RATE_LIMIT_REQUESTS"},
            "rate_limit_window": {"env": "RATE_LIMIT_WINDOW"},
            "log_level": {"env": "LOG_LEVEL"},
            "log_format": {"env": "LOG_FORMAT"}
        }


# Create settings instance
settings = Settings()
