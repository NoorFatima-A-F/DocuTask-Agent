"""
Abstract interfaces for Part 3B: Enterprise Service Communication & Distributed System Verification Framework.
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from app.platform_verification.service_communication.domain.models import (
    ServiceDependencyGraph,
    DependencyAnalysisReport,
    CommunicationContractReport,
    TimeoutValidationReport,
    RetryBehaviorReport,
    CircuitBreakerReport,
    NetworkFailureReport,
    DistributedConsistencyReport,
    TraceabilityReport,
    DistributedSystemCertificationReport,
    ServiceCommunicationEvidencePackage,
)


class IDependencyGraphAnalyzer(ABC):
    @abstractmethod
    def analyze_dependencies(self, graph: ServiceDependencyGraph) -> DependencyAnalysisReport:
        """Discovers dependencies, calculates complexity score, and detects cycles/SPOFs."""
        pass


class IContractValidator(ABC):
    @abstractmethod
    def validate_contracts(self, contracts: List[Dict[str, Any]]) -> CommunicationContractReport:
        """Validates request/response schemas, error structures, and breaking changes."""
        pass


class ITimeoutRetryEvaluator(ABC):
    @abstractmethod
    def evaluate_timeouts_and_retries(self, services: List[Dict[str, Any]]) -> (TimeoutValidationReport, RetryBehaviorReport):
        """Evaluates timeout thresholds, exponential backoff, and retry storm prevention."""
        pass


class ICircuitBreakerTester(ABC):
    __test__ = False
    @abstractmethod
    def test_circuit_breaker(self, service_name: str, simulated_failures: int) -> CircuitBreakerReport:
        """Validates 3-state transitions (CLOSED -> OPEN -> HALF_OPEN) and fast-fail behavior."""
        pass


class INetworkFailureSimulator(ABC):
    @abstractmethod
    def simulate_network_failures(self, scenarios: List[Dict[str, Any]]) -> NetworkFailureReport:
        """Simulates latency spikes, packet loss, and severed connections."""
        pass


class IDistributedConsistencyVerifier(ABC):
    @abstractmethod
    def verify_consistency(self, workflows: List[Dict[str, Any]]) -> DistributedConsistencyReport:
        """Verifies idempotency keys, compensation transactions, and prevents orphan states."""
        pass


class ITraceabilityValidator(ABC):
    @abstractmethod
    def validate_traceability(self, trace_spans: List[Dict[str, Any]]) -> TraceabilityReport:
        """Verifies end-to-end request_id, trace_id, and correlation_id propagation."""
        pass


class IDistributedSystemScoringEngine(ABC):
    @abstractmethod
    def calculate_scorecard(
        self,
        dep_rep: DependencyAnalysisReport,
        contract_rep: CommunicationContractReport,
        timeout_rep: TimeoutValidationReport,
        retry_rep: RetryBehaviorReport,
        cb_rep: CircuitBreakerReport,
        net_rep: NetworkFailureReport,
        cons_rep: DistributedConsistencyReport,
        trace_rep: TraceabilityReport,
    ) -> DistributedSystemCertificationReport:
        """Computes weighted composite score and assigns certification tier."""
        pass


class IServiceCommunicationEvidenceStore(ABC):
    @abstractmethod
    def seal_and_store_evidence(self, package: ServiceCommunicationEvidencePackage) -> str:
        """Persists and seals distributed verification evidence package with SHA-256."""
        pass

    @abstractmethod
    def retrieve_evidence(self, package_id: str) -> Optional[ServiceCommunicationEvidencePackage]:
        """Retrieves stored evidence package."""
        pass
