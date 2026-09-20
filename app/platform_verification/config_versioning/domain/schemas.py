"""
Configuration Schemas and Validators for 7 Enterprise Configuration Domains.
"""
from typing import Any, Dict, List, Optional, Tuple
from pydantic import BaseModel, Field, field_validator
from app.platform_verification.config_versioning.domain.models import ConfigDomain, EnvironmentTier


class PlatformConfigSchema(BaseModel):
    environment: EnvironmentTier = EnvironmentTier.DEVELOPMENT
    timezone: str = "UTC"
    log_level: str = "INFO"
    service_name: str = "DocuTask Enterprise Agent Platform"
    host: str = "0.0.0.0"
    port: int = 8000


class VerificationConfigSchema(BaseModel):
    timeout_seconds: int = Field(default=300, gt=0, le=7200)
    retry_max_attempts: int = Field(default=3, ge=0, le=10)
    max_parallel_runs: int = Field(default=8, gt=0, le=64)
    confidence_threshold: float = Field(default=0.95, ge=0.0, le=1.0)
    stop_on_failure: bool = False


class ExecutionConfigSchema(BaseModel):
    workers: int = Field(default=8, gt=0, le=128)
    concurrency_limit: int = Field(default=100, gt=0, le=1000)
    checkpoint_enabled: bool = True
    isolation_mode: str = "CONTAINER_SANDBOX"
    execution_engine: str = "ASYNC_WORKFLOW_POOL"


class AIConfigSchema(BaseModel):
    provider: str = "gemini"
    model: str = "gemini-2.5-flash"
    temperature: float = Field(default=0.0, ge=0.0, le=2.0)
    top_p: float = Field(default=0.95, ge=0.0, le=1.0)
    max_tokens: int = Field(default=4096, gt=0, le=65536)
    request_timeout_seconds: int = Field(default=60, gt=0)


class DatasetConfigSchema(BaseModel):
    name: str
    version: str
    uri: str = ""
    checksum_sha256: str = ""
    num_samples: int = Field(default=100, gt=0)
    partition: str = "evaluation"


class SecurityConfigSchema(BaseModel):
    auth_provider: str = "OIDC_JWT"
    token_expiry_minutes: int = Field(default=60, gt=0)
    mtls_enabled: bool = True
    encryption_algorithm: str = "AES-256-GCM"
    audit_logging_enabled: bool = True


class InfrastructureConfigSchema(BaseModel):
    compute_cluster: str = "k8s-us-central1"
    region: str = "us-central1"
    min_memory_gb: float = Field(default=16.0, gt=0)
    cpu_limit_cores: int = Field(default=8, gt=0)
    storage_class: str = "PREMIUM_SSD"


class ConfigurationSchemaValidator:
    @staticmethod
    def validate_domain_config(domain: ConfigDomain, config_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        errors: List[str] = []
        try:
            if domain == ConfigDomain.PLATFORM:
                PlatformConfigSchema(**config_data)
            elif domain == ConfigDomain.VERIFICATION:
                VerificationConfigSchema(**config_data)
            elif domain == ConfigDomain.EXECUTION:
                ExecutionConfigSchema(**config_data)
            elif domain == ConfigDomain.AI:
                AIConfigSchema(**config_data)
            elif domain == ConfigDomain.DATASET:
                DatasetConfigSchema(**config_data)
            elif domain == ConfigDomain.SECURITY:
                SecurityConfigSchema(**config_data)
            elif domain == ConfigDomain.INFRASTRUCTURE:
                InfrastructureConfigSchema(**config_data)
            return True, []
        except Exception as e:
            errors.append(str(e))
            return False, errors


schema_validator = ConfigurationSchemaValidator()
