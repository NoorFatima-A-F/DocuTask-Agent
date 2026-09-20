"""
Master Contexts Runtime Container.
Wires the 12 Bounded Contexts with clean separation of concerns and event publishing.
"""
from typing import Dict, Any, Optional

from .verification.contracts import VerificationService, InMemoryVerificationRepository
from .execution.contracts import ExecutionService, InMemoryExecutionRepository
from .datasets.contracts import DatasetService, InMemoryDatasetRepository
from .environments.contracts import EnvironmentService, InMemoryEnvironmentRepository
from .configuration.contracts import ConfigurationService, InMemoryConfigurationRepository
from .evidence.contracts import EvidenceService, InMemoryEvidenceRepository
from .metrics.contracts import MetricsService, InMemoryMetricsRepository
from .statistics.contracts import StatisticsService, InMemoryStatisticsRepository
from .quality.contracts import QualityGateService, InMemoryQualityGateRepository
from .certification.contracts import CertificationService, InMemoryCertificationRepository
from .audit.contracts import AuditLedgerService, InMemoryAuditRepository
from .plugins.contracts import PluginService, InMemoryPluginRepository
from ..infrastructure.storage.cas_store import ContentAddressableStore
from ..shared_kernel.events import get_event_bus

class BoundedContextsRuntime:
    """Enterprise Master Container coordinating all 12 Bounded Contexts."""
    def __init__(self):
        self.cas_store = ContentAddressableStore()
        self.event_bus = get_event_bus()

        self.verification = VerificationService(InMemoryVerificationRepository())
        self.execution = ExecutionService(InMemoryExecutionRepository())
        self.datasets = DatasetService(InMemoryDatasetRepository())
        self.environments = EnvironmentService(InMemoryEnvironmentRepository())
        self.configuration = ConfigurationService(InMemoryConfigurationRepository())
        self.evidence = EvidenceService(InMemoryEvidenceRepository(), self.cas_store)
        self.metrics = MetricsService(InMemoryMetricsRepository())
        self.statistics = StatisticsService(InMemoryStatisticsRepository())
        self.quality = QualityGateService(InMemoryQualityGateRepository())
        self.certification = CertificationService(InMemoryCertificationRepository())
        self.audit = AuditLedgerService(InMemoryAuditRepository())
        self.plugins = PluginService(InMemoryPluginRepository())

_global_contexts_runtime: Optional[BoundedContextsRuntime] = None

def get_contexts_runtime() -> BoundedContextsRuntime:
    global _global_contexts_runtime
    if _global_contexts_runtime is None:
        _global_contexts_runtime = BoundedContextsRuntime()
    return _global_contexts_runtime
