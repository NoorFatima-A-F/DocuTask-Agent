"""
Domain models for Part 2G: Enterprise Test Architecture Verification Framework.
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone


class TestCertificationTier(str, Enum):
    ENTERPRISE_TEST_READY = "ENTERPRISE_TEST_READY"
    PRODUCTION_READY = "PRODUCTION_READY"
    NEEDS_IMPROVEMENT = "NEEDS_IMPROVEMENT"
    FAILED = "FAILED"


TestCertificationTier.__test__ = False


class TestArchitectureLayer(str, Enum):
    UNIT = "unit"
    COMPONENT = "component"
    INTEGRATION = "integration"
    API = "api"
    E2E = "e2e"
    PERFORMANCE = "performance"
    SECURITY = "security"
    AI_EVALUATION = "ai_evaluation"
    REGRESSION = "regression"
    FIXTURES = "fixtures"


TestArchitectureLayer.__test__ = False


class FlakinessClass(str, Enum):
    RELIABLE = "RELIABLE"          # < 1% failure
    FLAKY = "FLAKY"                # 1 - 5% failure
    UNSTABLE = "UNSTABLE"          # > 5% failure


@dataclass
class TestPyramidDistribution:
    __test__ = False
    unit_count: int = 0
    component_count: int = 0
    integration_count: int = 0
    api_count: int = 0
    e2e_count: int = 0
    performance_count: int = 0
    security_count: int = 0
    ai_evaluation_count: int = 0
    regression_count: int = 0
    total_tests: int = 0
    unit_ratio: float = 0.0
    integration_ratio: float = 0.0
    e2e_ratio: float = 0.0


@dataclass
class TestPyramidReport:
    __test__ = False
    status: str
    distribution: TestPyramidDistribution
    missing_required_layers: List[str] = field(default_factory=list)
    pyramid_health_score: float = 100.0
    issues: List[str] = field(default_factory=list)


@dataclass
class UnitTestQualityReport:
    __test__ = False
    status: str
    scanned_unit_tests: int
    unmocked_external_calls: List[str] = field(default_factory=list)
    isolation_score: float = 100.0
    issues: List[str] = field(default_factory=list)


@dataclass
class CoverageQualityReport:
    __test__ = False
    line_coverage_pct: float
    branch_coverage_pct: float
    mutation_score_pct: float
    total_mutants_generated: int = 100
    mutants_killed: int = 85
    survived_mutants: List[str] = field(default_factory=list)
    meets_enterprise_thresholds: bool = True


@dataclass
class CriticalPathStepCoverage:
    __test__ = False
    step_name: str
    has_success_test: bool = True
    has_failure_test: bool = True
    has_recovery_test: bool = True


@dataclass
class CriticalPathCoverageReport:
    __test__ = False
    workflow_name: str
    total_steps: int
    covered_steps: int
    step_details: List[CriticalPathStepCoverage] = field(default_factory=list)
    is_fully_covered: bool = True


@dataclass
class AiEvaluationTestReport:
    __test__ = False
    status: str
    prompt_regression_passed: bool = True
    ground_truth_f1_score: float = 0.95
    hallucination_rate_pct: float = 1.2
    stochastic_consistency_pct: float = 98.5
    evaluated_scenarios: int = 50
    issues: List[str] = field(default_factory=list)


@dataclass
class FlakyTestResult:
    __test__ = False
    test_name: str
    runs: int
    failures: int
    failure_rate_pct: float
    classification: FlakinessClass


@dataclass
class FlakyTestDetectionReport:
    __test__ = False
    status: str
    total_evaluated_tests: int
    reliable_tests: int
    flaky_tests: int
    unstable_tests: int
    flaky_test_details: List[FlakyTestResult] = field(default_factory=list)
    order_independence_verified: bool = True


@dataclass
class EnvironmentReproducibilityReport:
    __test__ = False
    status: str
    pinned_dependencies_verified: bool = True
    docker_test_environment_verified: bool = True
    fixture_isolation_verified: bool = True
    reproducibility_score: float = 100.0
    issues: List[str] = field(default_factory=list)


@dataclass
class TestQualityScorecard:
    __test__ = False
    coverage_quality_score: float
    reliability_score: float
    organization_pyramid_score: float
    ai_evaluation_score: float
    reproducibility_score: float
    performance_score: float
    composite_score: float
    tier: TestCertificationTier
    evaluation_timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class TestArchitectureEvidencePackage:
    __test__ = False
    package_id: str
    commit_sha: str
    scorecard: TestQualityScorecard
    pyramid_report: TestPyramidReport
    unit_quality_report: UnitTestQualityReport
    coverage_report: CoverageQualityReport
    ai_evaluation_report: AiEvaluationTestReport
    flakiness_report: FlakyTestDetectionReport
    environment_report: EnvironmentReproducibilityReport
    package_sha256: str = ""
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
