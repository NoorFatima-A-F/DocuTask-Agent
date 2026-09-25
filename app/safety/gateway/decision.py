"""Safety Decision Models and Violation Definitions."""

from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime, timezone
import uuid


class SafetyStatus(str, Enum):
    """Enforcement decision status."""
    ALLOW = "ALLOW"
    ALLOW_WITH_AUDIT = "ALLOW_WITH_AUDIT"
    MODIFY = "MODIFY"
    REDACT = "REDACT"
    REQUIRE_HUMAN = "REQUIRE_HUMAN"
    ESCALATE = "ESCALATE"
    BLOCK = "BLOCK"


class ViolationSeverity(str, Enum):
    """Severity classification for safety violations."""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class SafetyCategory(str, Enum):
    """Categories of AI safety violations."""
    PROMPT_INJECTION = "PROMPT_INJECTION"
    INDIRECT_INJECTION = "INDIRECT_INJECTION"
    JAILBREAK = "JAILBREAK"
    PII_LEAKAGE = "PII_LEAKAGE"
    MALICIOUS_INPUT = "MALICIOUS_INPUT"
    UNAUTHORIZED_TOOL = "UNAUTHORIZED_TOOL"
    DESTRUCTIVE_TOOL = "DESTRUCTIVE_TOOL"
    TOXICITY = "TOXICITY"
    SECRET_LEAKAGE = "SECRET_LEAKAGE"
    HALLUCINATION = "HALLUCINATION"
    GROUNDING_FAILURE = "GROUNDING_FAILURE"
    HIGH_COMPOSITE_RISK = "HIGH_COMPOSITE_RISK"
    POLICY_VIOLATION = "POLICY_VIOLATION"


class SafetyViolation(BaseModel):
    """Specific safety rule or boundary violation."""
    violation_id: str = Field(default_factory=lambda: f"viol_{uuid.uuid4().hex[:8]}")
    category: SafetyCategory
    severity: ViolationSeverity
    message: str
    location: Optional[str] = None  # "input", "output", "tool_arg", "doc_chunk_3"
    rule_id: Optional[str] = None
    evidence: Optional[str] = None
    details: Dict[str, Any] = Field(default_factory=dict)
    detected_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class SafetyDecision(BaseModel):
    """Complete evaluation decision returned by the AI Safety Gateway."""
    decision_id: str = Field(default_factory=lambda: f"dec_{uuid.uuid4().hex[:10]}")
    status: SafetyStatus = SafetyStatus.ALLOW
    is_allowed: bool = True
    violations: List[SafetyViolation] = Field(default_factory=list)
    sanitized_content: Optional[str] = None
    composite_risk_score: float = 0.0
    explanation: Optional[str] = None
    required_actions: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    decided_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @property
    def has_critical_violations(self) -> bool:
        return any(v.severity == ViolationSeverity.CRITICAL for v in self.violations)

    @property
    def highest_severity(self) -> Optional[ViolationSeverity]:
        if not self.violations:
            return None
        severities = [v.severity for v in self.violations]
        if ViolationSeverity.CRITICAL in severities:
            return ViolationSeverity.CRITICAL
        if ViolationSeverity.HIGH in severities:
            return ViolationSeverity.HIGH
        if ViolationSeverity.MEDIUM in severities:
            return ViolationSeverity.MEDIUM
        return ViolationSeverity.LOW
