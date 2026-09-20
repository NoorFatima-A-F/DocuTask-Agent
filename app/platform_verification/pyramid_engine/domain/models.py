"""
Domain models for Enterprise Verification Pyramid & Multi-Level Testing Architecture (PART 2).
"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional


class VerificationLevel(str, Enum):
    L0_NOT_TESTED = "Level 0 - Not Tested"
    L1_UNIT = "Level 1 - Unit Verification"
    L2_COMPONENT = "Level 2 - Component Verification"
    L3_INTEGRATION = "Level 3 - Integration Verification"
    L4_SYSTEM = "Level 4 - System Verification"
    L5_PRODUCTION = "Level 5 - Production Verification"
    L6_ADVERSARIAL = "Level 6 - Adversarial Verification"
    L7_ENTERPRISE_CERTIFICATION = "Level 7 - Enterprise Certification"


class TestClassification(str, Enum):
    __test__ = False
    FUNCTIONAL = "functional"
    RELIABILITY = "reliability"
    PERFORMANCE = "performance"
    SECURITY = "security"
    AI_QUALITY = "ai_quality"
    COMPLIANCE = "compliance"


class FailureSeverity(str, Enum):
    CRITICAL = "CRITICAL"  # security breach, data corruption, crash
    HIGH = "HIGH"          # workflow failure, incorrect AI output
    MEDIUM = "MEDIUM"      # degraded performance, non-blocking bug
    LOW = "LOW"            # minor UI/log issue


class PyramidExecutionStatus(str, Enum):
    PASSED = "PASSED"
    FAILED = "FAILED"
    BLOCKED = "BLOCKED"
    SKIPPED = "SKIPPED"


class ContinuousTrigger(str, Enum):
    COMMIT = "COMMIT"              # Runs L1
    PULL_REQUEST = "PULL_REQUEST"  # Runs L1 - L3
    NIGHTLY = "NIGHTLY"            # Runs L1 - L5
    RELEASE = "RELEASE"            # Runs L1 - L7


@dataclass
class ComponentCoverageItem:
    """Tracks verification status and risk for a platform component."""
    component_name: str
    owner: str
    risk_level: FailureSeverity
    current_level: VerificationLevel = VerificationLevel.L0_NOT_TESTED
    missing_coverage: List[str] = field(default_factory=list)
    is_verified: bool = False
    last_verified_at: Optional[str] = None


@dataclass(frozen=True)
class TestDefinition:
    """Defines an executable test case in the pyramid."""
    __test__ = False
    id: str
    name: str
    level: VerificationLevel
    classification: TestClassification
    description: str
    target_component: str
    parameters: Dict[str, Any] = field(default_factory=dict)
    timeout_ms: int = 5000
    retry_count: int = 0


@dataclass
class TestExecutionRecord:
    """Execution metadata and results for a single test."""
    test_id: str
    name: str
    level: VerificationLevel
    environment: str
    dataset: str
    version: str
    executor: str
    status: PyramidExecutionStatus
    result: Dict[str, Any] = field(default_factory=dict)
    duration_ms: float = 0.0
    error_message: Optional[str] = None
    evidence_ref: Optional[str] = None
    executed_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class LevelExecutionSummary:
    """Aggregated execution results for a specific pyramid level."""
    level: VerificationLevel
    total_tests: int
    passed_tests: int
    failed_tests: int
    blocked_tests: int
    duration_ms: float
    status: PyramidExecutionStatus
    pass_rate: float
    records: List[TestExecutionRecord] = field(default_factory=list)


@dataclass
class DefectRecord:
    """Permanent defect record created upon verification failure."""
    bug_id: str
    title: str
    original_failure: str
    component: str
    severity: FailureSeverity
    detected_at_level: VerificationLevel
    root_cause: str = ""
    status: str = "OPEN"
    regression_test_id: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class RegressionRecord:
    """Permanent regression test definition safeguarding against recurring bugs."""
    bug_id: str
    original_failure: str
    test_case_id: str
    expected_behavior: str
    current_result: str
    version: str
    verified: bool = True
    verified_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class PyramidDashboardSummary:
    """High-level metrics for verification maturity and platform risk."""
    total_components: int
    verified_components: int
    unverified_components: int
    coverage_pct: float
    overall_pass_rate: float
    maturity_distribution: Dict[str, int]
    open_defects_by_severity: Dict[str, int]
    risk_index: float  # 0.0 (low risk) to 100.0 (extreme risk)


@dataclass
class PyramidExecutionReport:
    """Complete multi-level verification pyramid execution report."""
    report_id: str
    execution_id: str
    system_version: str
    trigger: ContinuousTrigger
    timestamp: str
    level_summaries: Dict[VerificationLevel, LevelExecutionSummary]
    overall_status: PyramidExecutionStatus
    certification_achieved: bool
    blocking_failures: List[str] = field(default_factory=list)
    defects_created: List[DefectRecord] = field(default_factory=list)
    duration_ms: float = 0.0
