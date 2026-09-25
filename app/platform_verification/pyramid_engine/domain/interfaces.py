"""
Standardized interfaces for Enterprise Verification Pyramid Architecture.
"""
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from app.platform_verification.pyramid_engine.domain.models import (
    VerificationLevel,
    TestDefinition,
    TestExecutionRecord,
    LevelExecutionSummary,
    DefectRecord,
    RegressionRecord,
    ContinuousTrigger,
    PyramidDashboardSummary,
    PyramidExecutionReport,
    ComponentCoverageItem,
)


class IVerificationLevelRunner(ABC):
    """Executes verification tests for a specific maturity level."""
    @property
    @abstractmethod
    def level(self) -> VerificationLevel:
        pass

    @abstractmethod
    def run_tests(
        self, tests: List[TestDefinition], context: Dict[str, Any]
    ) -> LevelExecutionSummary:
        pass


class IDependencyGate(ABC):
    """Enforces strict prerequisite dependency progression."""
    @abstractmethod
    def can_execute_level(
        self, target_level: VerificationLevel, completed_levels: Dict[VerificationLevel, LevelExecutionSummary]
    ) -> bool:
        pass


class IFailureClassifier(ABC):
    """Classifies verification failures and generates root cause assessments."""
    @abstractmethod
    def classify_failure(
        self, test_record: TestExecutionRecord
    ) -> DefectRecord:
        pass


class IRegressionEngine(ABC):
    """Manages permanent regression test database and prevents defect regression."""
    @abstractmethod
    def register_defect(self, defect: DefectRecord) -> RegressionRecord:
        pass

    @abstractmethod
    def run_regression_suite(self, context: Dict[str, Any]) -> List[TestExecutionRecord]:
        pass


class IPyramidDashboard(ABC):
    """Generates verification maturity and risk assessment summaries."""
    @abstractmethod
    def generate_summary(
        self, components: List[ComponentCoverageItem], defects: List[DefectRecord], reports: List[PyramidExecutionReport]
    ) -> PyramidDashboardSummary:
        pass


class ITestOrchestrator(ABC):
    """Orchestrates multi-level test executions through the pyramid."""
    @abstractmethod
    def execute_pyramid(
        self,
        system_version: str,
        trigger: ContinuousTrigger,
        tests: List[TestDefinition],
        context: Optional[Dict[str, Any]] = None,
    ) -> PyramidExecutionReport:
        pass
