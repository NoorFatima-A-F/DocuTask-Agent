"""
Abstract Base Classes & Interfaces for the 15 Core Architectural Components.
Enforces SOLID compliance, dependency inversion, and strict ownership boundaries.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from .models import (
    VerificationDefinition,
    VerificationPlan,
    VerificationRun,
    DatasetRecord,
    EnvironmentReadiness,
    ConfigurationSnapshot,
    EvidenceItem,
    MetricValue,
    StatisticalSummary,
    QualityGatePolicy,
    QualityGateEvaluation,
    ComplianceCertificate,
    VerificationReport,
    AuditEntry,
    TraceabilityNode,
    PluginDescriptor,
    ComponentHealth,
)


class EventBusInterface(ABC):
    @abstractmethod
    def publish(self, event: Any) -> None:
        pass

    @abstractmethod
    def subscribe(self, event_type: str, handler: Any) -> None:
        pass


class EvidenceStoreInterface(ABC):
    @abstractmethod
    def seal_evidence(self, run_id: str, payload: Any, payload_type: str) -> Any:
        pass

    @abstractmethod
    def verify_integrity(self, evidence_id: str, raw_payload: Any) -> bool:
        pass


class CertificationAuthorityInterface(ABC):
    @abstractmethod
    def issue_certificate(self, run: Any, quality_gate_result: Any) -> Any:
        pass

    @abstractmethod
    def verify_certificate(self, certificate: Any) -> bool:
        pass


class VerificationPlugin(ABC):
    @property
    @abstractmethod
    def plugin_name(self) -> str:
        pass

    @property
    @abstractmethod
    def target_domain(self) -> str:
        pass

    @abstractmethod
    def execute_verification(
        self,
        definition: Any,
        env_profile: Any,
        dataset_payload: Dict[str, Any]
    ) -> Dict[str, Any]:
        pass



class IVerificationOrchestrator(ABC):
    @abstractmethod
    def orchestrate_verification(self, definition_id: str, environment_id: str) -> VerificationRun:
        pass

    @abstractmethod
    def cancel_execution(self, run_id: str) -> bool:
        pass

    @abstractmethod
    def get_run_status(self, run_id: str) -> Optional[VerificationRun]:
        pass


class IVerificationRegistry(ABC):
    @abstractmethod
    def register_plugin(self, descriptor: PluginDescriptor) -> None:
        pass

    @abstractmethod
    def get_plugin(self, plugin_id: str) -> Optional[PluginDescriptor]:
        pass

    @abstractmethod
    def list_plugins(self, domain: Optional[str] = None) -> List[PluginDescriptor]:
        pass


class IVerificationDefinitionManager(ABC):
    @abstractmethod
    def create_definition(self, definition: VerificationDefinition) -> VerificationDefinition:
        pass

    @abstractmethod
    def get_definition(self, definition_id: str) -> Optional[VerificationDefinition]:
        pass

    @abstractmethod
    def list_definitions(self) -> List[VerificationDefinition]:
        pass


class IVerificationExecutionEngine(ABC):
    @abstractmethod
    def execute_plan(self, plan: VerificationPlan, correlation_id: str) -> Dict[str, Any]:
        pass


class IDatasetManager(ABC):
    @abstractmethod
    def register_dataset(self, dataset: DatasetRecord) -> DatasetRecord:
        pass

    @abstractmethod
    def get_dataset(self, dataset_id: str) -> Optional[DatasetRecord]:
        pass

    @abstractmethod
    def list_datasets(self) -> List[DatasetRecord]:
        pass


class IEnvironmentManager(ABC):
    @abstractmethod
    def check_readiness(self, environment_id: str) -> EnvironmentReadiness:
        pass

    @abstractmethod
    def list_environments(self) -> List[EnvironmentReadiness]:
        pass


class IConfigurationManager(ABC):
    @abstractmethod
    def create_snapshot(self, parameters: Dict[str, Any], env: str) -> ConfigurationSnapshot:
        pass

    @abstractmethod
    def get_snapshot(self, config_id: str) -> Optional[ConfigurationSnapshot]:
        pass


class IEvidenceManager(ABC):
    @abstractmethod
    def store_evidence(self, run_id: str, evidence_type: str, payload: Any, metadata: Dict[str, Any]) -> EvidenceItem:
        pass

    @abstractmethod
    def verify_evidence_integrity(self, evidence_id: str, raw_payload: Any) -> bool:
        pass

    @abstractmethod
    def list_evidence(self, run_id: str) -> List[EvidenceItem]:
        pass


class IMetricsEngine(ABC):
    @abstractmethod
    def calculate_metrics(self, execution_output: Dict[str, Any]) -> List[MetricValue]:
        pass


class IStatisticalAnalysisEngine(ABC):
    @abstractmethod
    def analyze_distribution(self, metric_name: str, samples: List[float], baseline_samples: Optional[List[float]] = None) -> StatisticalSummary:
        pass


class IQualityGateEngine(ABC):
    @abstractmethod
    def evaluate_gate(self, run_id: str, metrics: List[MetricValue], policy: QualityGatePolicy) -> QualityGateEvaluation:
        pass


class IReportingEngine(ABC):
    @abstractmethod
    def generate_report(self, run: VerificationRun, metrics: List[MetricValue], stats: List[StatisticalSummary], certificate: Optional[ComplianceCertificate]) -> VerificationReport:
        pass


class IAuditManager(ABC):
    @abstractmethod
    def record_event(self, event_type: str, entity_id: str, details: Dict[str, Any], actor: str = "SYSTEM") -> AuditEntry:
        pass

    @abstractmethod
    def get_audit_trail(self, entity_id: Optional[str] = None) -> List[AuditEntry]:
        pass

    @abstractmethod
    def verify_chain_integrity(self) -> bool:
        pass


class ITraceabilityManager(ABC):
    @abstractmethod
    def register_node(self, node: TraceabilityNode) -> None:
        pass

    @abstractmethod
    def link_nodes(self, source_id: str, target_id: str) -> None:
        pass

    @abstractmethod
    def get_lineage(self, root_id: str) -> List[TraceabilityNode]:
        pass


class IPluginManager(ABC):
    @abstractmethod
    def load_plugin(self, descriptor: PluginDescriptor) -> bool:
        pass

    @abstractmethod
    def execute_plugin(self, plugin_id: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        pass
