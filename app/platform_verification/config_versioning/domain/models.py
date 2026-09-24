"""
Enterprise Configuration, Versioning & Dependency Management Domain Models.
Strict Pydantic v2 validation, Semantic Versioning, and Immutable Snapshots.
"""
from datetime import datetime, timezone
from enum import Enum
import hashlib
from typing import Any, Dict, List, Optional
import uuid
from pydantic import BaseModel, Field


class ConfigDomain(str, Enum):
    PLATFORM = "PLATFORM"
    VERIFICATION = "VERIFICATION"
    EXECUTION = "EXECUTION"
    AI = "AI"
    DATASET = "DATASET"
    SECURITY = "SECURITY"
    INFRASTRUCTURE = "INFRASTRUCTURE"


class DependencyCategory(str, Enum):
    PYTHON_PACKAGE = "PYTHON_PACKAGE"
    SYSTEM_LIBRARY = "SYSTEM_LIBRARY"
    CONTAINER_IMAGE = "CONTAINER_IMAGE"
    AI_MODEL = "AI_MODEL"
    EXTERNAL_API = "EXTERNAL_API"
    DATABASE = "DATABASE"
    MESSAGE_BROKER = "MESSAGE_BROKER"
    CLOUD_SERVICE = "CLOUD_SERVICE"


class DependencyStatus(str, Enum):
    APPROVED = "APPROVED"
    PROHIBITED = "PROHIBITED"
    PROBATIONARY = "PROBATIONARY"
    DEPRECATED = "DEPRECATED"


class EnvironmentTier(str, Enum):
    DEVELOPMENT = "DEVELOPMENT"
    INTEGRATION = "INTEGRATION"
    STAGING = "STAGING"
    PRODUCTION_SHADOW = "PRODUCTION_SHADOW"
    PRODUCTION = "PRODUCTION"
    CHAOS = "CHAOS"
    SECURITY_LAB = "SECURITY_LAB"


class ChangeApprovalStatus(str, Enum):
    DRAFT = "DRAFT"
    SUBMITTED = "SUBMITTED"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    APPLIED = "APPLIED"
    ROLLED_BACK = "ROLLED_BACK"


class SemanticVersion(BaseModel):
    major: int = 1
    minor: int = 0
    patch: int = 0
    prerelease: Optional[str] = None
    build: Optional[str] = None

    def __str__(self) -> str:
        ver = f"{self.major}.{self.minor}.{self.patch}"
        if self.prerelease:
            ver += f"-{self.prerelease}"
        if self.build:
            ver += f"+{self.build}"
        return ver

    def __repr__(self) -> str:
        return f"SemanticVersion({self})"

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, str):
            other = SemanticVersion.parse(other)
        if not isinstance(other, SemanticVersion):
            return False
        return (self.major, self.minor, self.patch, self.prerelease) == (other.major, other.minor, other.patch, other.prerelease)

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, str):
            other = SemanticVersion.parse(other)
        if not isinstance(other, SemanticVersion):
            return NotImplemented
        if (self.major, self.minor, self.patch) != (other.major, other.minor, other.patch):
            return (self.major, self.minor, self.patch) < (other.major, other.minor, other.patch)
        if self.prerelease is None and other.prerelease is not None:
            return False
        if self.prerelease is not None and other.prerelease is None:
            return True
        return (self.prerelease or "") < (other.prerelease or "")

    def __le__(self, other: Any) -> bool:
        return self == other or self < other

    def __gt__(self, other: Any) -> bool:
        return not (self <= other)

    def __ge__(self, other: Any) -> bool:
        return not (self < other)

    @classmethod
    def parse(cls, version_str: str) -> "SemanticVersion":
        clean = version_str.strip().lstrip("v")
        prerelease = None
        build = None
        if "+" in clean:
            clean, build = clean.split("+", 1)
        if "-" in clean:
            clean, prerelease = clean.split("-", 1)
        parts = clean.split(".")
        major = int(parts[0]) if len(parts) > 0 and parts[0].isdigit() else 1
        minor = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 0
        patch = int(parts[2]) if len(parts) > 2 and parts[2].isdigit() else 0
        return cls(major=major, minor=minor, patch=patch, prerelease=prerelease, build=build)

    def bump_major(self) -> "SemanticVersion":
        return SemanticVersion(major=self.major + 1, minor=0, patch=0)

    def bump_minor(self) -> "SemanticVersion":
        return SemanticVersion(major=self.major, minor=self.minor + 1, patch=0)

    def bump_patch(self) -> "SemanticVersion":
        return SemanticVersion(major=self.major, minor=self.minor, patch=self.patch + 1)

    def is_breaking(self, other: "SemanticVersion") -> bool:
        return self.major != other.major

    def satisfies(self, range_spec: str) -> bool:
        """Evaluates basic semantic version constraint ranges like ^1.2.0, ~1.2.0, >=1.0.0, <2.0.0"""
        spec = range_spec.strip()
        if spec.startswith("^"):
            base = SemanticVersion.parse(spec[1:])
            if base.major > 0:
                return self >= base and self.major == base.major
            return self >= base and self.minor == base.minor
        if spec.startswith("~"):
            base = SemanticVersion.parse(spec[1:])
            return self >= base and self.major == base.major and self.minor == base.minor
        if "," in spec:
            clauses = [c.strip() for c in spec.split(",")]
            return all(self.satisfies(c) for c in clauses)
        if spec.startswith(">="):
            return self >= SemanticVersion.parse(spec[2:])
        if spec.startswith("<="):
            return self <= SemanticVersion.parse(spec[2:])
        if spec.startswith(">"):
            return self > SemanticVersion.parse(spec[1:])
        if spec.startswith("<"):
            return self < SemanticVersion.parse(spec[1:])
        if spec.startswith("=="):
            return self == SemanticVersion.parse(spec[2:])
        return self == SemanticVersion.parse(spec)


class DependencyItem(BaseModel):
    name: str
    version: str  # Strictly pinned (e.g. 0.115.0)
    category: DependencyCategory
    license: str = "Apache-2.0"
    source: str = "PyPI"
    sha256_checksum: str = ""
    is_direct: bool = True
    vulnerabilities: List[str] = Field(default_factory=list)
    status: DependencyStatus = DependencyStatus.APPROVED
    owner: str = "Enterprise Platform Engineering"
    compatibility_matrix: Dict[str, str] = Field(default_factory=dict)
    first_introduced: str = "1.0.0"
    last_updated: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class AIModelMetadata(BaseModel):
    provider: str = "Google Vertex / Gemini"
    model_name: str = "gemini-2.5-flash"
    version: str = "2026-03-stable"
    temperature: float = 0.0
    top_p: float = 0.95
    max_tokens: int = 4096
    parameters_fingerprint: str = ""


class PromptTemplateVersion(BaseModel):
    template_id: str = Field(default_factory=lambda: f"pmt_{uuid.uuid4().hex[:8]}")
    name: str
    semantic_version: str = "1.0.0"
    raw_prompt: str
    prompt_hash: str = ""
    author: str = "AI Evaluation Architect"
    system_instructions: Optional[str] = None
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def __init__(self, **data):
        super().__init__(**data)
        if not self.prompt_hash and self.raw_prompt:
            self.prompt_hash = hashlib.sha256(self.raw_prompt.encode("utf-8")).hexdigest()


class RAGRetrievalConfigVersion(BaseModel):
    config_id: str = Field(default_factory=lambda: f"rag_cfg_{uuid.uuid4().hex[:8]}")
    version: str = "1.0.0"
    embedding_model: str = "text-embedding-004"
    chunk_size: int = 512
    chunk_overlap: int = 64
    vector_db_version: str = "qdrant-v1.9.0"
    top_k: int = 10
    similarity_metric: str = "COSINE"


class AgentConfigVersion(BaseModel):
    agent_id: str = Field(default_factory=lambda: f"agt_cfg_{uuid.uuid4().hex[:8]}")
    version: str = "1.0.0"
    model: AIModelMetadata = Field(default_factory=AIModelMetadata)
    allowed_tools: List[str] = Field(default_factory=list)
    max_reasoning_steps: int = 10
    memory_strategy: str = "EPISODIC_BUFFER"


class EnvironmentFingerprint(BaseModel):
    fingerprint_id: str = Field(default_factory=lambda: f"env_fp_{uuid.uuid4().hex[:8]}")
    tier: EnvironmentTier = EnvironmentTier.INTEGRATION
    os_kernel: str = "Windows / Linux 6.8.0-generic"
    python_version: str = "3.14.0"
    cpu_count: int = 8
    memory_total_gb: float = 32.0
    container_image_digest: str = "sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    git_commit_sha: str = "main-2026-c98f7e2a"
    environment_variables_hash: str = ""
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class ConfigurationSnapshot(BaseModel):
    snapshot_id: str = Field(default_factory=lambda: f"cfg_snap_{uuid.uuid4().hex[:12]}")
    tenant_id: str = "default-tenant"
    environment: EnvironmentTier = EnvironmentTier.INTEGRATION
    semantic_version: str = "1.0.0"
    resolved_configuration: Dict[str, Any]
    configuration_hash: str
    dependency_manifest_hash: str
    environment_fingerprint: EnvironmentFingerprint
    ai_artifacts_fingerprint: Optional[str] = None
    creator: str = "Enterprise Configuration Resolver"
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    is_frozen: bool = True


class ExecutionSnapshot(BaseModel):
    snapshot_id: str = Field(default_factory=lambda: f"exec_snap_{uuid.uuid4().hex[:12]}")
    verification_id: str
    code_commit_sha: str
    configuration_snapshot_id: str
    configuration_hash: str
    dataset_id: str
    dataset_version: str
    dataset_hash: str
    model_identifier: str
    model_version: str
    prompt_template_id: str
    prompt_version: str
    prompt_hash: str
    dependency_lock_hash: str
    sbom_manifest_id: str
    environment_tier: EnvironmentTier
    environment_fingerprint_id: str
    infrastructure_version: str
    feature_flags_state: Dict[str, bool] = Field(default_factory=dict)
    composite_execution_hash: str = ""
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def compute_composite_hash(self) -> str:
        payload = f"{self.code_commit_sha}:{self.configuration_hash}:{self.dataset_hash}:{self.model_identifier}:{self.model_version}:{self.prompt_hash}:{self.dependency_lock_hash}:{self.environment_fingerprint_id}:{self.infrastructure_version}"
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    def __init__(self, **data):
        super().__init__(**data)
        if not self.composite_execution_hash:
            self.composite_execution_hash = self.compute_composite_hash()


class ArtifactMetadata(BaseModel):
    artifact_id: str = Field(default_factory=lambda: f"art_{uuid.uuid4().hex[:10]}")
    version: str = "1.0.0"
    category: str = "EVIDENCE_PACKAGE"
    producer: str = "Platform Verification Engine"
    checksum_sha256: str
    storage_uri: str
    dependencies: List[str] = Field(default_factory=list)
    attributes: Dict[str, Any] = Field(default_factory=dict)
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class DatabaseMigrationRecord(BaseModel):
    migration_id: str
    version: str
    author: str
    description: str
    checksum_sha256: str
    rollback_sql: str
    affected_components: List[str] = Field(default_factory=list)
    is_applied: bool = False
    applied_at: Optional[str] = None
    execution_time_ms: float = 0.0


class FeatureFlag(BaseModel):
    flag_key: str
    name: str
    description: str
    owner: str = "Platform Architecture Lead"
    is_enabled: bool = False
    rollout_percentage: int = 100
    enabled_environments: List[EnvironmentTier] = Field(default_factory=lambda: list(EnvironmentTier))
    allowed_tenants: List[str] = Field(default_factory=list)
    expiration_date: Optional[str] = None
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class SecretReference(BaseModel):
    secret_id: str = Field(default_factory=lambda: f"sec_{uuid.uuid4().hex[:8]}")
    key_name: str
    source: str = "VAULT_KMS"
    vault_path: str = "secret/data/docutask/verification"
    version: int = 1
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    expires_at: Optional[str] = None
    rotation_interval_days: int = 90
    is_rotated: bool = False
    is_revoked: bool = False


class SecretRotationRecord(BaseModel):
    rotation_id: str = Field(default_factory=lambda: f"rot_{uuid.uuid4().hex[:8]}")
    secret_id: str
    old_version: int
    new_version: int
    reason: str
    rotated_by: str = "KMS Automation"
    rotated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class ConfigurationDiff(BaseModel):
    source_snapshot_id: str
    target_snapshot_id: str
    has_changes: bool
    modified_keys: Dict[str, Dict[str, Any]] = Field(default_factory=dict)
    added_keys: Dict[str, Any] = Field(default_factory=dict)
    removed_keys: Dict[str, Any] = Field(default_factory=dict)
    dependency_changes: List[str] = Field(default_factory=list)
    ai_model_drift: bool = False
    human_readable_summary: str = "No configuration changes detected."


class DriftReport(BaseModel):
    report_id: str = Field(default_factory=lambda: f"drift_{uuid.uuid4().hex[:8]}")
    target_environment: EnvironmentTier
    baseline_snapshot_id: str
    baseline_hash: str
    current_hash: str
    is_drifted: bool
    unauthorized_mutations: List[str] = Field(default_factory=list)
    detected_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class ChangeRequest(BaseModel):
    change_id: str = Field(default_factory=lambda: f"chg_{uuid.uuid4().hex[:8]}")
    title: str
    author: str
    reason: str
    target_scope: str = "MODULE"
    proposed_changes: Dict[str, Any]
    impact_assessment: str
    rollback_plan: str
    status: ChangeApprovalStatus = ChangeApprovalStatus.DRAFT
    target_version: str = "1.1.0"
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    approved_by: Optional[str] = None
    approved_at: Optional[str] = None


class RollbackRecord(BaseModel):
    rollback_id: str = Field(default_factory=lambda: f"rbk_{uuid.uuid4().hex[:8]}")
    change_id: str
    from_snapshot_id: str
    to_snapshot_id: str
    reason: str
    executed_by: str = "Enterprise SRE Architect"
    is_successful: bool = True
    executed_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class SBOMManifest(BaseModel):
    sbom_id: str = Field(default_factory=lambda: f"sbom_{uuid.uuid4().hex[:8]}")
    format: str = "CycloneDX_1.5"
    spec_version: str = "1.5"
    serial_number: str = Field(default_factory=lambda: f"urn:uuid:{uuid.uuid4()}")
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    components_count: int
    direct_dependencies_count: int
    transitive_dependencies_count: int
    components: List[DependencyItem]
    sha256_bom_hash: str
