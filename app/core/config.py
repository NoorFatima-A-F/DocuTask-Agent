"""
Centralized Configuration Settings Module.
Uses Pydantic v2 BaseSettings to load environment variables safely.
"""

from typing import List, Union
from pydantic import Field, field_validator
try:
    from pydantic_settings import BaseSettings, SettingsConfigDict
except ImportError:
    from pydantic import BaseModel as BaseSettings
    def SettingsConfigDict(**kwargs):
        return kwargs



class Settings(BaseSettings):
    """Application Settings managed through environment variables."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

    # Core Project Settings
    PROJECT_NAME: str = "AI Document Processing Platform"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    API_V1_STR: str = "/api/v1"

    # Database Configuration
    DATABASE_URL: str = "sqlite+aiosqlite:///./ai_doc_platform.db"

    # Security & JWT Configuration
    JWT_SECRET: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Password Policy
    MIN_PASSWORD_LENGTH: int = 8
    REQUIRE_PASSWORD_SPECIAL_CHAR: bool = True

    # Storage & Upload Settings
    STORAGE_LOCAL_DIR: str = "./storage"
    UPLOAD_DIRECTORY: str = "./storage/uploads"
    MAX_UPLOAD_SIZE_MB: int = 25
    MAX_FILENAME_LENGTH: int = 255
    ALLOWED_EXTENSIONS: List[str] = [
        ".pdf", ".png", ".jpg", ".jpeg", ".tiff", ".bmp", ".docx", ".txt"
    ]
    ALLOWED_MIME_TYPES: List[str] = [
        "application/pdf",
        "image/png",
        "image/jpeg",
        "image/tiff",
        "image/bmp",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "text/plain"
    ]

    # AI Provider - Gemini Settings
    GEMINI_API_KEY: str = "dev_placeholder_key"
    GEMINI_MODEL: str = "gemini-1.5-pro"

    # CORS Settings
    BACKEND_CORS_ORIGINS: List[str] = ["*"]

    @field_validator("ALLOWED_EXTENSIONS", "ALLOWED_MIME_TYPES", mode="before")
    @classmethod
    def assemble_list_settings(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, list):
            return v
        return []

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, list):
            return v
        return ["*"]


settings = Settings()
