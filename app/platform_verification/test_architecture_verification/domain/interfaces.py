"""
Abstract interfaces for Part 2G: Enterprise Test Architecture Verification Framework.
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from app.platform_verification.test_architecture_verification.domain.models import (
    TestPyramidReport,
    UnitTestQualityReport,
    CoverageQualityReport,
    AiEvaluationTestReport,
    FlakyTestDetectionReport,
    EnvironmentReproducibilityReport,
    TestQualityScorecard,
    TestArchitectureEvidencePackage,
)


class IPyramidAnalyzer(ABC):
    @abstractmethod
    def analyze_pyramid(self, test_manifest: Dict[str, List[str]]) -> TestPyramidReport:
        """Analyzes test directory layout, test counts, and pyramid distribution ratios."""
        pass


class IUnitQualityEvaluator(ABC):
    @abstractmethod
    def evaluate_unit_quality(self, test_files: List[str]) -> UnitTestQualityReport:
        """Verifies mocking of external APIs and isolates unit test boundaries."""
        pass


class ICoverageQualityEngine(ABC):
    @abstractmethod
    def evaluate_coverage_and_mutations(self, coverage_data: Dict[str, Any]) -> CoverageQualityReport:
        """Evaluates line, branch, and mutation test scores."""
        pass


class IAiEvaluationVerifier(ABC):
    @abstractmethod
    def verify_ai_evaluation_suite(self, ai_test_data: Dict[str, Any]) -> AiEvaluationTestReport:
        """Verifies prompt regression thresholds, ground truth F1, and hallucination tests."""
        pass


class IReliabilityAnalyzer(ABC):
    @abstractmethod
    def analyze_reliability_and_flakiness(self, execution_history: List[Dict[str, Any]]) -> FlakyTestDetectionReport:
        """Detects flakiness, verifies order independence, and classifies test stability."""
        pass


class IEnvironmentValidator(ABC):
    @abstractmethod
    def validate_environment_reproducibility(self, env_meta: Dict[str, Any]) -> EnvironmentReproducibilityReport:
        """Verifies pinned dependencies, container setups, and fixture isolation."""
        pass


class ITestScoringEngine(ABC):
    __test__ = False
    @abstractmethod
    def calculate_scorecard(
        self,
        pyramid: TestPyramidReport,
        unit_quality: UnitTestQualityReport,
        coverage: CoverageQualityReport,
        ai_eval: AiEvaluationTestReport,
        reliability: FlakyTestDetectionReport,
        env: EnvironmentReproducibilityReport,
    ) -> TestQualityScorecard:
        """Computes weighted composite score and assigns certification tier."""
        pass


class ITestEvidenceStore(ABC):
    __test__ = False
    @abstractmethod
    def seal_and_store_evidence(self, package: TestArchitectureEvidencePackage) -> str:
        """Persists and seals test architecture verification evidence with SHA-256."""
        pass

    @abstractmethod
    def retrieve_evidence(self, package_id: str) -> Optional[TestArchitectureEvidencePackage]:
        """Retrieves stored evidence package."""
        pass
