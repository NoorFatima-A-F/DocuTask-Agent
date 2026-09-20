"""
Memory Subsystem Policies.
Defines RetentionPolicy, ExpirationPolicy, PromotionPolicy, CompressionPolicy, and SnapshotPolicy.
"""

from pydantic import BaseModel, Field


class RetentionPolicy(BaseModel):
    """Memory retention policy configuration."""
    retention_days: int = Field(default=30, ge=1)
    auto_archive: bool = Field(default=True)
    model_config = {"frozen": True}


class ExpirationPolicy(BaseModel):
    """TTL expiration policy configuration."""
    ttl_seconds: float = Field(default=86400.0, gt=0.0)  # 24h default
    hard_delete_on_expiration: bool = Field(default=False)
    model_config = {"frozen": True}


class PromotionPolicy(BaseModel):
    """Memory tier promotion policy configuration (Short-Term to Long-Term)."""
    importance_threshold: float = Field(default=0.8, ge=0.0, le=1.0)
    access_frequency_threshold: int = Field(default=5, ge=1)
    model_config = {"frozen": True}


class CompressionPolicy(BaseModel):
    """Context window compression policy configuration."""
    max_tokens: int = Field(default=4000, ge=100)
    enable_summarization: bool = Field(default=True)
    model_config = {"frozen": True}


class SnapshotPolicy(BaseModel):
    """Memory state snapshotting policy configuration."""
    snapshot_frequency_steps: int = Field(default=1, ge=1)
    max_snapshots_to_keep: int = Field(default=10, ge=1)
    model_config = {"frozen": True}
