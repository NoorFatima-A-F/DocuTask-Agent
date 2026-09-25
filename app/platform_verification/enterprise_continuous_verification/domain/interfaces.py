"""
Phase 3Q: Continuous Infrastructure Verification & CI/CD Assurance — Interfaces.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from .models import (
    BuildArtifactReport,
    ChangeImpactReport,
    ChaosPipelineReport,
    DisposableEnvReport,
    InfrastructureDriftReport,
    IntegrationWorkflowReport,
    PerformanceRegressionReport,
    ProductionReadinessCertificate,
    ReleaseDecision,
    SecurityGateReport,
)


class IChangeImpactAnalyzer(ABC):
    @abstractmethod
    def analyze_changes(self, modified_files: Optional[List[str]] = None) -> ChangeImpactReport: pass


class IBuildVerifier(ABC):
    @abstractmethod
    def verify_build(self, image_name: str = "docutask-api", commit_hash: str = "HEAD") -> BuildArtifactReport: pass


class ISecurityGateEngine(ABC):
    @abstractmethod
    def evaluate_security(
        self,
        critical_cves: int = 0,
        high_cves: int = 0,
        secrets_found: int = 0,
    ) -> SecurityGateReport: pass


class IDisposableEnvManager(ABC):
    @abstractmethod
    def provision_and_test(self) -> DisposableEnvReport: pass


class IIntegrationWorkflowRunner(ABC):
    @abstractmethod
    def execute_e2e_workflow(self) -> IntegrationWorkflowReport: pass


class IPerformanceGateValidator(ABC):
    @abstractmethod
    def validate_performance(
        self,
        current_p95_ms: float = 42.1,
        baseline_p95_ms: float = 40.0,
    ) -> PerformanceRegressionReport: pass


class IChaosPipelineRunner(ABC):
    @abstractmethod
    def run_chaos_experiments(self) -> ChaosPipelineReport: pass


class IDriftDetector(ABC):
    @abstractmethod
    def detect_drift(self, declared_count: int = 28, actual_count: int = 28) -> InfrastructureDriftReport: pass


class IReleaseGatekeeper(ABC):
    @abstractmethod
    def evaluate_release(self, gate_reports: Dict[str, Any]) -> ReleaseDecision: pass
    @abstractmethod
    def issue_certificate(self, decision: ReleaseDecision, gate_reports: Dict[str, Any]) -> ProductionReadinessCertificate: pass
