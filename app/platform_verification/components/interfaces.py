"""
Abstract Contracts and Ports for the 16 Enterprise Verification Core Components.
Strictly enforces the Interface Segregation and Dependency Inversion Principles.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple, Callable


class VerificationOrchestratorInterface(ABC):
    @abstractmethod
    async def initialize_lifecycle(self, run_id: str, spec_id: str) -> str:
        pass

    @abstractmethod
    async def transition_state(self, run_id: str, new_state: str) -> str:
        pass

    @abstractmethod
    async def get_status(self, run_id: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def list_runs(self) -> List[Dict[str, Any]]:
        pass


class VerificationRegistryInterface(ABC):
    @abstractmethod
    async def register_capability(self, module_id: str, capability: str, version: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        pass

    @abstractmethod
    async def lookup_capability(self, module_id: str) -> Optional[Dict[str, Any]]:
        pass

    @abstractmethod
    async def list_capabilities(self) -> Dict[str, Dict[str, Any]]:
        pass


class VerificationDefinitionManagerInterface(ABC):
    @abstractmethod
    async def create_definition(self, spec_id: str, name: str, invariants: List[str], parameters: Dict[str, Any]) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def validate_definition(self, spec_id: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def get_definition(self, spec_id: str) -> Optional[Dict[str, Any]]:
        pass


class VerificationExecutionEngineInterface(ABC):
    @abstractmethod
    async def execute_task(self, task_id: str, executable: Callable, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def cancel_task(self, task_id: str) -> bool:
        pass


class DatasetManagerInterface(ABC):
    @abstractmethod
    async def register_dataset(self, dataset_id: str, category: str, content_or_uri: bytes | str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def verify_integrity(self, dataset_id: str, expected_content: bytes) -> bool:
        pass


class EnvironmentManagerInterface(ABC):
    @abstractmethod
    async def register_environment(self, env_id: str, tier: str, profile: Dict[str, Any]) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def validate_readiness(self, env_id: str) -> Dict[str, Any]:
        pass


class ConfigurationManagerInterface(ABC):
    @abstractmethod
    async def resolve_configuration(self, run_id: str, tier_overrides: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def get_snapshot(self, run_id: str) -> Optional[Dict[str, Any]]:
        pass


class EvidenceManagerInterface(ABC):
    @abstractmethod
    async def record_evidence(self, evidence_id: str, run_id: str, tier: str, content: bytes, tags: Optional[List[str]] = None) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def get_evidence(self, evidence_id: str) -> Optional[Dict[str, Any]]:
        pass


class MetricsEngineInterface(ABC):
    @abstractmethod
    async def record_metric(self, run_id: str, metric_name: str, value: float, category: str) -> None:
        pass

    @abstractmethod
    async def get_metrics(self, run_id: str) -> Dict[str, Dict[str, Any]]:
        pass


class StatisticalAnalysisEngineInterface(ABC):
    @abstractmethod
    async def analyze_distribution(self, samples: List[float]) -> Dict[str, Any]:
        pass


class QualityGateEngineInterface(ABC):
    @abstractmethod
    async def evaluate_gates(self, metrics: Dict[str, float], rules: List[Dict[str, Any]]) -> Dict[str, Any]:
        pass


class CertificationEngineInterface(ABC):
    @abstractmethod
    async def issue_certificate(self, run_id: str, level: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def revoke_certificate(self, certificate_id: str, reason: str) -> Dict[str, Any]:
        pass


class ReportingEngineInterface(ABC):
    @abstractmethod
    async def generate_report(self, run_id: str, report_format: str, summary_data: Dict[str, Any]) -> Dict[str, Any]:
        pass


class AuditManagerInterface(ABC):
    @abstractmethod
    async def log_event(self, event_type: str, actor: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def verify_chain_integrity(self) -> bool:
        pass


class TraceabilityManagerInterface(ABC):
    @abstractmethod
    async def link_nodes(self, source_id: str, target_id: str, relation: str) -> None:
        pass

    @abstractmethod
    async def get_lineage(self, node_id: str) -> List[Dict[str, str]]:
        pass


class PluginManagerInterface(ABC):
    @abstractmethod
    async def register_plugin(self, plugin_id: str, name: str, capabilities: List[str]) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def list_active_plugins(self) -> List[Dict[str, Any]]:
        pass


# Aliases
DefinitionManagerInterface = VerificationDefinitionManagerInterface
ExecutionEngineInterface = VerificationExecutionEngineInterface
