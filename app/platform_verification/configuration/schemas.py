"""
Configuration Schemas with Pydantic v2.
"""
from typing import Dict
from pydantic import BaseModel, Field

class ExecutionEngineConfig(BaseModel):
    default_strategy: str = "SEQUENTIAL"  # SEQUENTIAL, PARALLEL, ASYNC_WORKER
    max_workers: int = 8
    default_timeout_seconds: int = 300
    retry_limit: int = 3
    circuit_breaker_enabled: bool = True
    circuit_breaker_threshold: int = 5


class StatisticalEngineConfig(BaseModel):
    bootstrap_iterations: int = 1000
    confidence_level: float = 0.95
    drift_p_value_threshold: float = 0.05
    minimum_sample_size: int = 5


class EvidenceStorageConfig(BaseModel):
    storage_type: str = "IN_MEMORY_CAS"  # IN_MEMORY_CAS, GCS, S3, LOCAL_FS
    cas_base_path: str = "/tmp/verification_cas"
    merkle_trees_enabled: bool = True
    sha256_canonical_hashing: bool = True


class SecurityConfig(BaseModel):
    root_hmac_key: str = "DocuTask-Enterprise-Root-Key-2026-Immutable"
    enforce_tamper_detection: bool = True
    require_hard_gate_pass: bool = True


class VerificationPlatformConfig(BaseModel):
    environment: str = "INTEGRATION"
    tenant_id: str = "default-tenant"
    version: str = "2.0.0"
    execution: ExecutionEngineConfig = Field(default_factory=ExecutionEngineConfig)
    statistics: StatisticalEngineConfig = Field(default_factory=StatisticalEngineConfig)
    evidence: EvidenceStorageConfig = Field(default_factory=EvidenceStorageConfig)
    security: SecurityConfig = Field(default_factory=SecurityConfig)
    feature_flags: Dict[str, bool] = Field(default_factory=dict)
