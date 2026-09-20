"""
Phase V9 — Enterprise AI Security & Responsible AI Verification Program
Domain Models & Verification Schemas
"""
from __future__ import annotations
from enum import Enum
from typing import Dict, List, Optional, Any, Union
from datetime import datetime, timezone
from pydantic import BaseModel, Field
import uuid

class SecurityCategory(str, Enum):
    AUTHENTICATION = "AUTHENTICATION"
    AUTHORIZATION = "AUTHORIZATION"
    TENANT_ISOLATION = "TENANT_ISOLATION"
    API_SECURITY = "API_SECURITY"
    LLM_SECURITY = "LLM_SECURITY"
    AGENT_SECURITY = "AGENT_SECURITY"
    DATA_PROTECTION = "DATA_PROTECTION"
    SUPPLY_CHAIN = "SUPPLY_CHAIN"
    RESPONSIBLE_AI = "RESPONSIBLE_AI"
    RED_TEAM = "RED_TEAM"
    OBSERVABILITY = "OBSERVABILITY"

class SecurityStatus(str, Enum):
    PASSED = "PASSED"
    FAILED = "FAILED"
    WARNING = "WARNING"
    DEFENDED = "DEFENDED"

class SeverityLevel(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INFORMATIONAL = "INFORMATIONAL"

class SecurityVerificationRun(BaseModel):
    id: str = Field(default_factory=lambda: f"srun-{uuid.uuid4().hex[:10]}")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    component: str
    scenario: str
    metric: str
    expected_value: Any
    actual_value: Any
    status: SecurityStatus = SecurityStatus.PASSED
    severity: SeverityLevel = SeverityLevel.LOW
    evidence_location: str = "security_verification_evidence/"
    details: Dict[str, Any] = Field(default_factory=dict)

class AttackVector(BaseModel):
    id: str = Field(default_factory=lambda: f"atk-{uuid.uuid4().hex[:8]}")
    category: SecurityCategory
    name: str
    payload: str
    language: str = "English"
    target_layer: str
    expected_behavior: str = "BLOCKED"
    mitigation_applied: str = ""
    is_blocked: bool = True
    detection_latency_ms: float = 0.5
    confidence_score: float = 0.99

class SecuritySectionResult(BaseModel):
    section_id: str
    section_name: str
    category: SecurityCategory
    weight_pct: float = 10.0
    score: float = 100.0
    status: SecurityStatus = SecurityStatus.PASSED
    passed_checks: int = 0
    total_checks: int = 0
    attacks_tested: int = 0
    attacks_blocked: int = 0
    runs: List[SecurityVerificationRun] = Field(default_factory=list)
    metrics: Dict[str, Any] = Field(default_factory=dict)
    summary: str = ""
    executed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class MasterSecurityScore(BaseModel):
    tenant_id: str = "enterprise-v9-security"
    overall_score: float = 100.0
    grade: str = "A+ (Enterprise Hardened)"
    category_scores: Dict[str, float] = Field(default_factory=dict)
    section_results: List[SecuritySectionResult] = Field(default_factory=list)
    total_checks: int = 0
    passed_checks: int = 0
    failed_checks: int = 0
    total_attacks_tested: int = 0
    total_attacks_blocked: int = 0
    defense_rate_pct: float = 100.0
    verification_duration_ms: float = 0.0
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    audit_hash: str = ""
