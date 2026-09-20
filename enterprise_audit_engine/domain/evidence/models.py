"""Enterprise Evidence Verification Platform Domain Models and Classification."""

from enum import Enum
from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
from uuid import UUID, uuid4
import hashlib
import json
from pydantic import BaseModel, Field, ConfigDict


class EvidenceClassification(str, Enum):
    """Strictly controlled ontology of evidence-based classifications."""
    VERIFIED = "VERIFIED"
    VERIFIED_BY_EXECUTION = "VERIFIED_BY_EXECUTION"
    VERIFIED_BY_STATIC_ANALYSIS = "VERIFIED_BY_STATIC_ANALYSIS"
    VERIFIED_BY_CONFIGURATION = "VERIFIED_BY_CONFIGURATION"
    CONFIGURATION_PRESENT = "CONFIGURATION_PRESENT"
    CONFIGURATION_PRESENT_RUNTIME_NOT_VERIFIED = "CONFIGURATION_PRESENT_RUNTIME_NOT_VERIFIED"
    PARTIALLY_VERIFIED = "PARTIALLY_VERIFIED"
    EVIDENCE_FOUND = "EVIDENCE_FOUND"
    EVIDENCE_INSUFFICIENT = "EVIDENCE_INSUFFICIENT"
    DOCUMENTATION_ONLY = "DOCUMENTATION_ONLY"
    PROTOTYPE = "PROTOTYPE"
    STUB = "STUB"
    UNKNOWN = "UNKNOWN"
    NOT_VERIFIED = "NOT_VERIFIED"
    CRITICAL_FINDING = "CRITICAL_FINDING"


class EvidenceConfidence(str, Enum):
    """Deterministic confidence levels based on evidence depth."""
    NONE = "NONE"
    LOW = "LOW"            # Configuration only
    MEDIUM = "MEDIUM"      # Static code analysis only
    HIGH = "HIGH"          # Static code + automated test execution
    VERY_HIGH = "VERY_HIGH"  # Runtime execution + benchmarks + telemetry logs


class EvidenceSourceType(str, Enum):
    """The four strictly distinct sources of audit evidence."""
    STATIC_SOURCE_CODE = "STATIC_SOURCE_CODE"
    CONFIGURATION_FILE = "CONFIGURATION_FILE"
    RUNTIME_EXECUTION = "RUNTIME_EXECUTION"
    AUTOMATED_TEST_EXECUTION = "AUTOMATED_TEST_EXECUTION"


class EvidenceRecord(BaseModel):
    """Immutable evidence record with cryptographic fingerprint and chain of custody."""
    model_config = ConfigDict(frozen=True)

    id: str = Field(default_factory=lambda: f"EV-{uuid4().hex[:8].upper()}")
    parent_evidence_id: Optional[str] = None
    category: str
    collector: str
    source_type: EvidenceSourceType
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    command: Optional[str] = None
    environment: Dict[str, Any] = Field(default_factory=dict)
    exit_code: Optional[int] = None
    duration_ms: float = 0.0
    artifact_paths: List[str] = Field(default_factory=list)
    raw_payload: Dict[str, Any] = Field(default_factory=dict)
    summary: str
    confidence: EvidenceConfidence
    classification: EvidenceClassification
    content_hash: str = ""

    def calculate_hash(self) -> str:
        """Computes SHA-256 fingerprint of evidence record content."""
        data = {
            "id": self.id,
            "parent_evidence_id": self.parent_evidence_id,
            "category": self.category,
            "collector": self.collector,
            "source_type": self.source_type.value,
            "timestamp": self.timestamp,
            "command": self.command,
            "exit_code": self.exit_code,
            "summary": self.summary,
            "classification": self.classification.value,
            "raw_payload": self.raw_payload,
        }
        serialized = json.dumps(data, sort_keys=True, default=str)
        return hashlib.sha256(serialized.encode("utf-8")).hexdigest()

    @classmethod
    def create(cls, **kwargs) -> "EvidenceRecord":
        """Factory method that instantiates and seals the evidence hash."""
        instance = cls(**kwargs)
        h = instance.calculate_hash()
        return instance.model_copy(update={"content_hash": h})


class CollectorHealthStatus(BaseModel):
    """Health and execution verification for an individual collector."""
    collector_name: str
    execution_attempted: bool = True
    execution_completed: bool = False
    exception_message: Optional[str] = None
    timeout_occurred: bool = False
    exit_code: int = 0
    duration_ms: float = 0.0
    artifacts_generated_count: int = 0
    evidence_generated_count: int = 0
    stdout_hash: str = ""
    stderr_hash: str = ""


class AuditRunMetadata(BaseModel):
    """Audit run execution provenance and environmental fingerprint."""
    run_id: str = Field(default_factory=lambda: f"RUN-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}")
    timestamp_start: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    timestamp_end: Optional[str] = None
    git_commit_hash: str = "HEAD"
    branch: str = "main"
    repository_url: str = "https://github.com/NoorFatima-A-F/DocuTask-Agent"
    engine_version: str = "2.0.0"
    python_version: str = "3.12"
    os_information: str = "Enterprise Linux / Windows Standard"
    dependency_versions: Dict[str, str] = Field(default_factory=dict)
    executor_identity: str = "Enterprise-Audit-Engine-Automated-Runner"
    configuration_hash: str = ""


class CollectorExecutionManifest(BaseModel):
    """Manifest of all executed collectors during an audit run."""
    run_id: str
    collectors: List[CollectorHealthStatus] = Field(default_factory=list)
    total_duration_ms: float = 0.0
    all_collectors_healthy: bool = True


class VerificationDimension(str, Enum):
    """The 6 dimensions of the Verification Strength Model."""
    SOURCE_INSPECTION = "SOURCE_INSPECTION"          # Weight: 20
    AUTOMATED_TEST_EXECUTION = "AUTOMATED_TESTS"     # Weight: 20
    RUNTIME_EXECUTION = "RUNTIME_EXECUTION"          # Weight: 25
    SECURITY_VALIDATION = "SECURITY_VALIDATION"      # Weight: 15
    BENCHMARK_EVIDENCE = "BENCHMARK_EVIDENCE"        # Weight: 10
    REPRODUCIBILITY = "REPRODUCIBILITY"              # Weight: 10


class VerificationScorecard(BaseModel):
    """Weighted verification strength evaluation."""
    subsystem: str
    source_inspection_score: float = 0.0      # max 20
    automated_tests_score: float = 0.0        # max 20
    runtime_execution_score: float = 0.0      # max 25
    security_validation_score: float = 0.0    # max 15
    benchmark_evidence_score: float = 0.0     # max 10
    reproducibility_score: float = 0.0        # max 10
    total_score: float = 0.0                  # max 100
    classification: EvidenceClassification
    confidence: EvidenceConfidence
    justification: str


class AuditFinding(BaseModel):
    """An audited finding derived strictly from verified evidence records."""
    finding_id: str = Field(default_factory=lambda: f"FND-{uuid4().hex[:6].upper()}")
    subsystem: str
    claim: str
    evidence_ids: List[str]
    classification: EvidenceClassification
    confidence: EvidenceConfidence
    risk_level: str = "LOW"  # CRITICAL, HIGH, MEDIUM, LOW, INFO
    analysis: str
    recommendations: List[str] = Field(default_factory=list)
    limitations: List[str] = Field(default_factory=list)


class AuditReportManifest(BaseModel):
    """Immutable manifest of an executed evidence audit run."""
    run_id: str
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    metadata: Optional[AuditRunMetadata] = None
    execution_manifest: Optional[CollectorExecutionManifest] = None
    total_evidence_collected: int
    findings_count: int
    maturity_scorecard: Dict[str, str] = Field(default_factory=dict)
    evidence_hashes: List[str] = Field(default_factory=list)
    tamper_proof_manifest_hash: str = ""
