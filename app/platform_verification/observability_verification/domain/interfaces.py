"""
Abstract interfaces for Part 3E: Enterprise Observability & Reliability Verification Framework.
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from app.platform_verification.observability_verification.domain.models import (
    ObservabilityArchitectureReport,
    LoggingQualityReport,
    MetricsInventoryReport,
    DistributedTraceReport,
    AiWorkflowObservabilityReport,
    AlertQualityReport,
    SloComplianceReport,
    IncidentResponseReport,
    ObservabilityCertificationReport,
    ObservabilityVerificationEvidencePackage,
)


class IObservabilityArchitectureAnalyzer(ABC):
    @abstractmethod
    def analyze_architecture(self, services: List[Dict[str, Any]]) -> ObservabilityArchitectureReport:
        """Audits telemetry instrumentation across all core services."""
        pass


class ILoggingSecurityValidator(ABC):
    @abstractmethod
    def validate_logging(self, log_samples: List[Dict[str, Any]]) -> LoggingQualityReport:
        """Validates structured JSON logging schema and scans for leaked credentials/PII."""
        pass


class IMetricsTelemetryVerifier(ABC):
    @abstractmethod
    def verify_metrics_inventory(self, metrics: List[Dict[str, Any]]) -> MetricsInventoryReport:
        """Audits Golden Signals (latency, traffic, errors, saturation) and AI-specific metrics."""
        pass


class IDistributedTraceVerifier(ABC):
    @abstractmethod
    def verify_distributed_tracing(self, trace_spans: List[Dict[str, Any]]) -> DistributedTraceReport:
        """Verifies OpenTelemetry context propagation and complete workflow reconstructability."""
        pass


class IAiWorkflowObservabilityAuditor(ABC):
    @abstractmethod
    def audit_ai_workflow(self, workflow_telemetry: Dict[str, Any]) -> AiWorkflowObservabilityReport:
        """Verifies granular tracing of agent planning, tool usage, retrieval chunks, and token attribution."""
        pass


class IAlertQualityValidator(ABC):
    @abstractmethod
    def validate_alerts(self, alert_rules: List[Dict[str, Any]]) -> AlertQualityReport:
        """Evaluates actionable alert rule definitions, symptoms, probable causes, and runbook links."""
        pass


class ISloComplianceEngine(ABC):
    @abstractmethod
    def evaluate_slos(self, slo_data: List[Dict[str, Any]]) -> SloComplianceReport:
        """Calculates Availability, Latency, Processing SLOs and error budget burn rates."""
        pass


class IIncidentRecoverySimulator(ABC):
    @abstractmethod
    def simulate_incidents(self, incident_scenarios: List[Dict[str, Any]]) -> IncidentResponseReport:
        """Simulates chaos incidents and measures MTTD, MTTR, and recovery success rate."""
        pass


class IObservabilityScoringEngine(ABC):
    @abstractmethod
    def calculate_scorecard(
        self,
        log_rep: LoggingQualityReport,
        metric_rep: MetricsInventoryReport,
        trace_rep: DistributedTraceReport,
        alert_rep: AlertQualityReport,
        slo_rep: SloComplianceReport,
        inc_rep: IncidentResponseReport,
    ) -> ObservabilityCertificationReport:
        """Computes weighted composite score and assigns certification tier."""
        pass


class IObservabilityEvidenceStore(ABC):
    @abstractmethod
    def seal_and_store_evidence(self, package: ObservabilityVerificationEvidencePackage) -> str:
        """Persists and seals observability verification evidence package with SHA-256."""
        pass

    @abstractmethod
    def retrieve_evidence(self, package_id: str) -> Optional[ObservabilityVerificationEvidencePackage]:
        """Retrieves stored evidence package."""
        pass
