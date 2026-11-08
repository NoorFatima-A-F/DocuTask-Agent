"""Centralized Application Configuration.

Loads settings from environment variables and optional .env file with strong
typing, validation, and secure defaults via Pydantic Settings.
"""

from datetime import date
from typing import Annotated, Any, Literal

from pydantic import Field, field_validator, model_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict

# Dev-only placeholder; startup refuses it outside development/test.
DEFAULT_JWT_SECRET = "replace-with-a-secure-random-secret-in-production-use-openssl-rand-hex-32"  # noqa: S105  # nosec B105
#: Environments where the insecure default JWT secret is tolerated.
INSECURE_SECRET_ENVIRONMENTS = frozenset({"development", "test"})
MIN_JWT_SECRET_BYTES = 32

#: List settings read from env as comma-separated strings (or a JSON array).
CsvList = Annotated[list[str], NoDecode]


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
    APP_VERSION: str = "2.0.0"
    ENVIRONMENT: str = Field(default="development", description="Environment: development, staging, production")
    DEBUG: bool = Field(default=False, description="Debug mode flag")
    LOG_LEVEL: str = Field(default="INFO", description="Logging level: DEBUG, INFO, WARNING, ERROR, CRITICAL")

    # API & Server Configuration
    API_V1_PREFIX: str = "/api/v1"
    API_V1_STR: str = "/api/v1"
    HOST: str = "0.0.0.0"  # noqa: S104  # nosec B104 - container bind address
    PORT: int = 8000

    CORS_ORIGINS: CsvList = Field(
        default_factory=lambda: ["http://localhost:3000", "http://localhost:8000"],
        description="Allowed CORS origins",
    )
    BACKEND_CORS_ORIGINS: CsvList = Field(
        default_factory=lambda: ["http://localhost:3000", "http://localhost:8000"],
        description="Allowed CORS origins alias",
    )

    # Authentication & Security
    JWT_SECRET: str = Field(
        default=DEFAULT_JWT_SECRET,
        description="Secret key used for signing JWT tokens (generate with: openssl rand -hex 32)",
    )
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    MIN_PASSWORD_LENGTH: int = 8
    REQUIRE_PASSWORD_SPECIAL_CHAR: bool = True

    # Database Configuration
    DATABASE_URL: str = Field(
        default="sqlite+aiosqlite:///./docutask.db",
        description="Database connection URL (PostgreSQL asyncpg or SQLite aiosqlite)",
    )
    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 20
    DB_ECHO: bool = False

    # Gemini (the only LLM provider). Key precedence: GEMINI_API_KEY, then GOOGLE_API_KEY.
    GEMINI_API_KEY: str | None = Field(default=None, description="Gemini API key (preferred)")
    GOOGLE_API_KEY: str | None = Field(default=None, description="Gemini API key (used if GEMINI_API_KEY unset)")
    GEMINI_MODEL: str = Field(
        default="gemini-3.8-flash",
        description="Gemini model ID used for extraction (stable, no shutdown date as of 2026-11-08)",
    )
    GEMINI_CONNECT_TIMEOUT_SECONDS: float = 5.0
    GEMINI_READ_TIMEOUT_SECONDS: float = 60.0

    @field_validator(
        "CORS_ORIGINS",
        "BACKEND_CORS_ORIGINS",
        "TRUSTED_PROXIES",
        "ALLOWED_EXTENSIONS",
        "ALLOWED_MIME_TYPES",
        mode="before",
    )
    @classmethod
    def _split_csv(cls, value: Any) -> Any:
        if isinstance(value, str):
            text = value.strip()
            if text.startswith("["):
                import json

                return json.loads(text)
            return [item.strip() for item in text.split(",") if item.strip()]
        return value

    @field_validator("DATABASE_URL")
    @classmethod
    def _use_async_postgres_driver(cls, url: str) -> str:
        """Managed Postgres providers hand out ``postgres://`` URLs; the app needs asyncpg."""
        for prefix in ("postgres://", "postgresql://"):
            if url.startswith(prefix):
                return "postgresql+asyncpg://" + url[len(prefix) :]
        return url

    @model_validator(mode="after")
    def _require_bucket_for_s3(self) -> "Settings":
        if self.STORAGE_BACKEND == "s3" and not (self.S3_BUCKET or "").strip():
            raise ValueError("STORAGE_BACKEND=s3 requires S3_BUCKET")
        return self

    @model_validator(mode="after")
    def _refuse_weak_jwt_secret_outside_dev(self) -> "Settings":
        """Fail at startup if a non-dev/test environment uses the default or a short JWT secret."""
        if self.ENVIRONMENT.strip().lower() in INSECURE_SECRET_ENVIRONMENTS:
            return self
        if self.JWT_SECRET == DEFAULT_JWT_SECRET:
            raise ValueError(
                f"JWT_SECRET is the built-in default; set a random secret for ENVIRONMENT={self.ENVIRONMENT!r} "
                "(openssl rand -hex 32)"
            )
        if len(self.JWT_SECRET.encode("utf-8")) < MIN_JWT_SECRET_BYTES:
            raise ValueError(f"JWT_SECRET must be at least {MIN_JWT_SECRET_BYTES} bytes outside development/test")
        return self

    @property
    def gemini_api_key(self) -> str | None:
        """Resolved Gemini key: GEMINI_API_KEY wins over GOOGLE_API_KEY; blank values count as unset."""
        return (self.GEMINI_API_KEY or "").strip() or (self.GOOGLE_API_KEY or "").strip() or None

    # Storage & Cache Configuration
    STORAGE_BACKEND: Literal["local", "s3"] = Field(
        default="local",
        description="local: files on this machine's disk (API and worker must share it). "
        "s3: S3-compatible bucket, required when the API and worker run on different machines.",
    )
    S3_BUCKET: str | None = None
    S3_PREFIX: str = "documents/"
    S3_ENDPOINT_URL: str | None = Field(default=None, description="For R2/MinIO/B2; empty for AWS S3")
    S3_REGION: str | None = None
    STORAGE_LOCAL_PATH: str = "./uploads"
    STORAGE_LOCAL_DIR: str = "./uploads"
    MAX_UPLOAD_SIZE_MB: int = 50
    MAX_FILENAME_LENGTH: int = 255
    ALLOWED_EXTENSIONS: CsvList = Field(default_factory=lambda: [".pdf", ".png", ".jpg", ".jpeg", ".tiff", ".bmp"])
    ALLOWED_MIME_TYPES: CsvList = Field(
        default_factory=lambda: ["application/pdf", "image/png", "image/jpeg", "image/tiff", "image/bmp"]
    )
    REDIS_URL: str | None = Field(
        default=None,
        description="Redis connection URL for background task queues and rate limiting",
    )

    # Rate Limiting & Gating
    RATE_LIMIT_PER_MINUTE: int = Field(default=120, description="Requests per minute per client IP on /api/*")
    TRUSTED_PROXIES: CsvList = Field(
        default_factory=list,
        description="CIDRs of reverse proxies whose X-Forwarded-For is trusted (e.g. 10.0.0.0/8). "
        "Empty: use the TCP peer.",
    )
    CONFIDENCE_THRESHOLD_HITL: float = 0.85


#: USD per 1M tokens, keyed by model ID. Each entry is a list of (effective_from, input, output),
#: newest last. Source: https://aistudio.google.com/docs/pricing (paid tier, text), checked 2026-11-08.
#: Models not listed here get ``estimated_cost = None``; never guess a price.
GEMINI_PRICING_USD_PER_1M: dict[str, list[tuple[date, float, float]]] = {
    "gemini-3.8-flash": [(date(2026, 1, 1), 0.75, 3.75), (date(2027, 1, 1), 1.50, 7.50)],
    "gemini-3.6-flash": [(date(2026, 1, 1), 0.75, 3.75), (date(2027, 1, 1), 1.50, 7.50)],
    "gemini-3.5-flash-lite": [(date(2026, 1, 1), 0.30, 2.50)],
    "gemini-3.1-flash-lite": [(date(2026, 1, 1), 0.25, 1.50)],
}


# Global Singleton Instance
settings = Settings()
