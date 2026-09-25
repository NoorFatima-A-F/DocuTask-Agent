"""
Part 3G.6 — Multi-Region / Cloud Failover Verification Framework.
"""
from app.platform_verification.multi_region_failover.domain.models import (
    CloudRegion,
    FailoverMode,
    ReplicationHealth,
    AvailabilityTier,
    RegionalServiceItem,
    MultiRegionArchitectureReport,
    CloudPortabilityReport,
    DatabaseReplicationReport,
    StorageReplicationReport,
    TrafficFailoverReport,
    WorkflowCheckpointReport,
    ChaosOutageReport,
    AvailabilityMetricsReport,
    MultiRegionScorecard,
)
from app.platform_verification.multi_region_failover.architecture.architecture_validator import (
    MultiRegionArchitectureValidator,
)
from app.platform_verification.multi_region_failover.architecture.portability_verifier import (
    CloudPortabilityVerifier,
)
from app.platform_verification.multi_region_failover.replication.database_replication_verifier import (
    DatabaseReplicationVerifier,
)
from app.platform_verification.multi_region_failover.replication.storage_replication_verifier import (
    StorageReplicationVerifier,
)
from app.platform_verification.multi_region_failover.traffic.traffic_failover_engine import (
    TrafficFailoverEngine,
)
from app.platform_verification.multi_region_failover.orchestrator.failover_orchestrator import (
    FailoverOrchestrator,
)
from app.platform_verification.multi_region_failover.state_and_resilience.workflow_checkpoint_verifier import (
    WorkflowCheckpointVerifier,
)
from app.platform_verification.multi_region_failover.state_and_resilience.split_brain_detector import (
    SplitBrainDefenseReport,
    SplitBrainDetector,
)
from app.platform_verification.multi_region_failover.chaos_and_metrics.outage_simulator import (
    OutageSimulator,
)
from app.platform_verification.multi_region_failover.chaos_and_metrics.availability_metrics_engine import (
    AvailabilityMetricsEngine,
)
from app.platform_verification.multi_region_failover.scoring.multi_region_score_engine import (
    MultiRegionScoreEngine,
)
from app.platform_verification.multi_region_failover.exporter.failover_exporter import (
    FailoverExporter,
)
from app.platform_verification.multi_region_failover.runtime.failover_runtime import (
    MasterFailoverExecutionResult,
    FailoverRuntime,
)

__all__ = [
    "CloudRegion",
    "FailoverMode",
    "ReplicationHealth",
    "AvailabilityTier",
    "RegionalServiceItem",
    "MultiRegionArchitectureReport",
    "CloudPortabilityReport",
    "DatabaseReplicationReport",
    "StorageReplicationReport",
    "TrafficFailoverReport",
    "WorkflowCheckpointReport",
    "ChaosOutageReport",
    "AvailabilityMetricsReport",
    "MultiRegionScorecard",
    "MultiRegionArchitectureValidator",
    "CloudPortabilityVerifier",
    "DatabaseReplicationVerifier",
    "StorageReplicationVerifier",
    "TrafficFailoverEngine",
    "FailoverOrchestrator",
    "WorkflowCheckpointVerifier",
    "SplitBrainDefenseReport",
    "SplitBrainDetector",
    "OutageSimulator",
    "AvailabilityMetricsEngine",
    "MultiRegionScoreEngine",
    "FailoverExporter",
    "MasterFailoverExecutionResult",
    "FailoverRuntime",
]
