"""
Interfaces and Contracts for Enterprise Verification Plugins and Extensibility.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple
from app.platform_verification.extension_framework.domain.models import (
    PluginMetadata,
    PluginExecutionContext,
    PluginExecutionResult,
    PluginHealthMetrics,
    PluginLifecycleState,
)


class BasePluginInterface(ABC):
    """Root contract for all plugins in the DocuTask Agent platform."""

    @property
    @abstractmethod
    def metadata(self) -> PluginMetadata:
        """Machine-readable metadata describing the plugin."""
        pass

    @abstractmethod
    def initialize(self, context: Dict[str, Any]) -> bool:
        """Initializes plugin state, loads models or warm caches."""
        pass

    @abstractmethod
    def validate(self) -> Tuple[bool, List[str]]:
        """Validates plugin prerequisites, configuration schema, and dependencies."""
        pass

    @abstractmethod
    def configure(self, config: Dict[str, Any]) -> None:
        """Configures plugin with runtime parameters."""
        pass

    @abstractmethod
    def execute(self, context: PluginExecutionContext) -> PluginExecutionResult:
        """Executes core logic within standard context."""
        pass

    @abstractmethod
    def cleanup(self) -> None:
        """Releases locks, GPU memory, or open file descriptors."""
        pass

    @abstractmethod
    def health_check(self) -> PluginHealthMetrics:
        """Returns live health and latency metrics."""
        pass

    def shutdown(self) -> None:
        """Graceful shutdown hook."""
        self.cleanup()


class VerificationPluginInterface(BasePluginInterface):
    """Specialized contract for verification plugins (OCR, RAG, AI accuracy, security)."""

    @abstractmethod
    def collect_evidence(self, context: PluginExecutionContext) -> Dict[str, Any]:
        """Gathers cryptographic raw evidence and artifacts."""
        pass

    @abstractmethod
    def calculate_metrics(self, raw_evidence: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Calculates deterministic or probabilistic metrics from evidence."""
        pass


class ExecutionBackendPluginInterface(BasePluginInterface):
    """Specialized contract for execution backends (K8s, Local, Cloud Workers)."""

    @abstractmethod
    def schedule_task(self, task_spec: Dict[str, Any]) -> str:
        """Schedules a verification task on the execution backend."""
        pass

    @abstractmethod
    def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """Queries the live task status."""
        pass


class DatasetProviderPluginInterface(BasePluginInterface):
    """Specialized contract for dataset providers and synthetic benchmark generators."""

    @abstractmethod
    def load_dataset(self, dataset_name: str, version: str) -> List[Dict[str, Any]]:
        """Loads and returns dataset partitions."""
        pass

    @abstractmethod
    def get_dataset_manifest(self, dataset_name: str) -> Dict[str, Any]:
        """Returns dataset provenance and checksum manifest."""
        pass


class MetricEvaluatorPluginInterface(BasePluginInterface):
    """Specialized contract for evaluation metric calculators."""

    @abstractmethod
    def evaluate_metric(self, predictions: List[Any], ground_truth: List[Any]) -> Dict[str, float]:
        """Calculates quantitative metrics with confidence intervals."""
        pass


class AIProviderPluginInterface(BasePluginInterface):
    """Specialized contract for AI models (Gemini, Claude, OpenAI, Local)."""

    @abstractmethod
    def generate_completion(self, prompt: str, parameters: Dict[str, Any]) -> str:
        """Generates LLM response."""
        pass

    @abstractmethod
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generates embedding vectors."""
        pass


class StorageProviderPluginInterface(BasePluginInterface):
    """Specialized contract for artifact and evidence storage systems."""

    @abstractmethod
    def put_artifact(self, key: str, data: bytes) -> str:
        """Stores artifact returning content addressable URI."""
        pass

    @abstractmethod
    def get_artifact(self, key: str) -> Optional[bytes]:
        """Retrieves raw artifact data."""
        pass


class NotificationPluginInterface(BasePluginInterface):
    """Specialized contract for alert and notification systems."""

    @abstractmethod
    def send_alert(self, title: str, message: str, level: str = "INFO") -> bool:
        """Sends notification to target channel."""
        pass


class ComplianceValidatorPluginInterface(BasePluginInterface):
    """Specialized contract for compliance and regulatory rule checks."""

    @abstractmethod
    def validate_compliance(self, target_spec: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Evaluates regulatory compliance rules."""
        pass


class PluginRegistryInterface(ABC):
    @abstractmethod
    def register_plugin(self, plugin: BasePluginInterface) -> PluginMetadata:
        pass

    @abstractmethod
    def get_plugin(self, plugin_id: str) -> Optional[BasePluginInterface]:
        pass

    @abstractmethod
    def list_plugins(self, capability: Optional[str] = None) -> List[PluginMetadata]:
        pass

    @abstractmethod
    def unregister_plugin(self, plugin_id: str) -> bool:
        pass


class PluginLifecycleManagerInterface(ABC):
    @abstractmethod
    def transition_state(self, plugin_id: str, target_state: PluginLifecycleState, reason: str = "") -> PluginLifecycleState:
        pass

    @abstractmethod
    def get_state(self, plugin_id: str) -> PluginLifecycleState:
        pass


class PluginExecutorInterface(ABC):
    @abstractmethod
    def execute_plugin(self, plugin_id: str, context: PluginExecutionContext) -> PluginExecutionResult:
        pass
