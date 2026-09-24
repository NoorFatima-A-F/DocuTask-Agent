"""Centralized Application Configuration.

Loads settings from environment variables and optional .env file with strong
typing, validation, and secure defaults via Pydantic Settings.
"""

import os
from typing import List, Optional
from pydantic import Field
try:
    from pydantic_settings import BaseSettings, SettingsConfigDict
except ImportError:
    from pydantic import BaseModel as BaseSettings  # type: ignore
    def SettingsConfigDict(**kwargs):  # type: ignore
        return None


class Settings(BaseSettings):
    """Core application settings with environment variable fallbacks."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    # Application Info
    APP_NAME: str = "DocuTask Agent"
    PROJECT_NAME: str = "DocuTask Agent"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = Field(default="development", description="Environment: development, staging, production")
    DEBUG: bool = Field(default=False, description="Debug mode flag")
    LOG_LEVEL: str = Field(default="INFO", description="Logging level: DEBUG, INFO, WARNING, ERROR, CRITICAL")

    # API & Server Configuration
    API_V1_PREFIX: str = "/api/v1"
    API_V1_STR: str = "/api/v1"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    CORS_ORIGINS: List[str] = Field(
        default_factory=lambda: ["http://localhost:3000", "http://localhost:8000"],
        description="Allowed CORS origins",
    )
    BACKEND_CORS_ORIGINS: List[str] = Field(
        default_factory=lambda: ["http://localhost:3000", "http://localhost:8000"],
        description="Allowed CORS origins alias",
    )

    # Authentication & Security
    JWT_SECRET: str = Field(
        default="replace-with-a-secure-random-secret-in-production-use-openssl-rand-hex-32",
        description="Secret key used for signing JWT tokens",
    )
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours

    # Database Configuration
    DATABASE_URL: str = Field(
        default="sqlite+aiosqlite:///./docutask.db",
        description="Database connection URL (PostgreSQL asyncpg or SQLite aiosqlite)",
    )
    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 20
    DB_ECHO: bool = False

    # AI & LLM Provider API Keys (Read exclusively from environment)
    GOOGLE_API_KEY: Optional[str] = Field(
        default=None,
        description="Google Gemini API Key for document extraction and multimodal processing",
    )
    ANTHROPIC_API_KEY: Optional[str] = Field(
        default=None,
        description="Anthropic Claude API Key for secondary fallback extraction",
    )
    OPENAI_API_KEY: Optional[str] = Field(
        default=None,
        description="OpenAI API Key for comparative extraction workflows",
    )

    # Storage & Cache Configuration
    STORAGE_LOCAL_PATH: str = "./uploads"
    STORAGE_LOCAL_DIR: str = "./uploads"
    MAX_UPLOAD_SIZE_MB: int = 50
    REDIS_URL: Optional[str] = Field(
        default=None,
        description="Redis connection URL for background task queues and rate limiting",
    )

    # Rate Limiting & Gating
    RATE_LIMIT_PER_MINUTE: int = 60
    CONFIDENCE_THRESHOLD_HITL: float = 0.85


# Global Singleton Instance
settings = Settings()
