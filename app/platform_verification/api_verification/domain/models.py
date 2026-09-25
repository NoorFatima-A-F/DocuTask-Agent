"""
Domain models for Enterprise API Architecture Verification (PART 2E).
"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
import hashlib
from typing import List, Optional


class ApiViolationCategory(str, Enum):
    LAYER_PURITY = "LAYER_PURITY"
    CONTRACT_COMPLIANCE = "CONTRACT_COMPLIANCE"
    SECURITY_OWASP = "SECURITY_OWASP"
    TENANT_ISOLATION = "TENANT_ISOLATION"
    VERSION_COMPATIBILITY = "VERSION_COMPATIBILITY"
    ASYNC_AI_WORKFLOW = "ASYNC_AI_WORKFLOW"
    OBSERVABILITY = "OBSERVABILITY"


class ApiViolationSeverity(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class AgentTaskState(str, Enum):
    CREATED = "CREATED"
    RUNNING = "RUNNING"
    WAITING_FOR_HUMAN = "WAITING_FOR_HUMAN"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class ApiCertificationBand(str, Enum):
    ENTERPRISE_API_CERTIFIED = "ENTERPRISE_API_CERTIFIED"  # 95-100
    PRODUCTION_READY_API = "PRODUCTION_READY_API"          # 90-94
    ACCEPTABLE_API = "ACCEPTABLE_API"                      # 80-89
    BREAKING_OR_INSECURE_API = "BREAKING_OR_INSECURE_API"  # 70-79
    FAILED = "FAILED"                                      # < 70


@dataclass
class EndpointPurityMetric:
    """Analysis of an individual API endpoint handler."""
    endpoint_path: str
    http_method: str
    file_path: str
    line_number: int
    line_count: int
    has_direct_sql_import: bool = False
    has_direct_llm_call: bool = False
    has_business_logic_bloat: bool = False
    is_pure: bool = True
    violating_imports: List[str] = field(default_factory=list)


@dataclass
class ApiSecurityFinding:
    """OWASP API Security Top 10 evaluation finding."""
    finding_id: str
    owasp_category: str  # "API1: BOLA", "API2: Broken Auth", "API3: Excessive Data", etc.
    endpoint_path: str
    severity: ApiViolationSeverity
    message: str
    remediation: str


@dataclass
class ApiBreakingChange:
    """Detected breaking change between schema versions."""
    change_type: str  # "REMOVED_FIELD", "RENAMED_FIELD", "CHANGED_TYPE", "NEW_REQUIRED_FIELD"
    path: str
    field_name: str
    version_before: str
    version_after: str
    is_breaking: bool = True
    description: str = ""


@dataclass
class ApiQualityScorecard:
    """Consolidated API readiness scorecard."""
    total_score: float  # 0 to 100
    certification_band: ApiCertificationBand
    layer_purity_score: float
    security_score: float
    compatibility_score: float
    async_workflow_score: float
    total_violations_count: int
    critical_violations_count: int
    is_deployable: bool


@dataclass
class ApiEvidencePackage:
    """Sealed evidence package for API architecture verification."""
    scan_id: str
    repository_name: str = "DocuTask-Agent"
    commit_sha: str = "HEAD"
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    endpoints_analyzed_count: int = 0
    endpoint_metrics: List[EndpointPurityMetric] = field(default_factory=list)
    security_findings: List[ApiSecurityFinding] = field(default_factory=list)
    breaking_changes: List[ApiBreakingChange] = field(default_factory=list)
    scorecard: Optional[ApiQualityScorecard] = None
    evidence_sha256: str = ""

    def compute_sha256(self) -> str:
        score = self.scorecard.total_score if self.scorecard else 0.0
        payload = f"{self.scan_id}:{self.timestamp}:{score}:{len(self.security_findings)}:{len(self.breaking_changes)}"
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()
