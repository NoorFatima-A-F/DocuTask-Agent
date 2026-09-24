"""
Verification Management Domain: Definitions, Requirements, Categories, and Invariants.
"""
from datetime import datetime, timezone
from enum import Enum
from typing import List
from pydantic import BaseModel, Field
import uuid


class VerificationCategory(str, Enum):
    FUNCTIONAL = "FUNCTIONAL"
    PERFORMANCE = "PERFORMANCE"
    RELIABILITY = "RELIABILITY"
    SECURITY = "SECURITY"
    AI_QUALITY = "AI_QUALITY"
    COMPLIANCE = "COMPLIANCE"
    COST = "COST"
    USABILITY = "USABILITY"
    ROBUSTNESS = "ROBUSTNESS"
    SCALABILITY = "SCALABILITY"


class VerificationStatus(str, Enum):
    DRAFT = "DRAFT"
    APPROVED = "APPROVED"
    DEPRECATED = "DEPRECATED"
    ARCHIVED = "ARCHIVED"


class RequirementSeverity(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INFORMATIONAL = "INFORMATIONAL"


class VerificationRequirement(BaseModel):
    requirement_id: str = Field(default_factory=lambda: f"req_{uuid.uuid4().hex[:8]}")
    metric_name: str
    operator: str = ">="  # >=, <=, ==, !=, >, <, in_range
    target_threshold: float
    severity: RequirementSeverity = RequirementSeverity.CRITICAL
    is_mandatory: bool = True
    description: str = ""


class VerificationDefinition(BaseModel):
    definition_id: str = Field(default_factory=lambda: f"vdef_{uuid.uuid4().hex[:8]}")
    tenant_id: str = "default-tenant"
    name: str
    description: str
    category: VerificationCategory = VerificationCategory.AI_QUALITY
    verification_type: str = "AUTOMATED_SUITE"
    owner: str = "Enterprise Verification Architect"
    priority: int = 1  # 1 (Highest) to 5
    risk_level: str = "HIGH"
    status: VerificationStatus = VerificationStatus.DRAFT
    semantic_version: str = "1.0.0"
    objective: str
    scope: List[str] = Field(default_factory=list)
    expected_behavior: str = ""
    requirements: List[VerificationRequirement] = Field(default_factory=list)
    required_datasets: List[str] = Field(default_factory=list)
    required_environment_tier: str = "INTEGRATION"
    required_plugins: List[str] = Field(default_factory=list)
    created_by: str = "System"
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def approve(self, approver: str) -> None:
        self.status = VerificationStatus.APPROVED
        self.updated_at = datetime.now(timezone.utc).isoformat()

    def deprecate(self) -> None:
        self.status = VerificationStatus.DEPRECATED
        self.updated_at = datetime.now(timezone.utc).isoformat()
