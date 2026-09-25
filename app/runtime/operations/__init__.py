"""
AOIS-HROP Phase 13.7 - Autonomous Operational Intelligence, Self-Healing & Resilience Orchestration Platform
"""

# Legacy AMAEOP Pillar 4 Exports (Preserved for backward compatibility)
from app.runtime.operations.checkpoint_manager import CheckpointManager, MissionCheckpoint, checkpoint_manager
from app.runtime.operations.heartbeat_manager import HeartbeatManager, DepartmentHeartbeat, heartbeat_manager
from app.runtime.operations.persistent_scheduler import PersistentScheduler, ScheduledOperation, persistent_scheduler
from app.runtime.operations.recovery_snapshot import RecoverySnapshotEngine, RecoveryResult
from app.runtime.operations.lease_manager import LeaseManager, ResourceLease, lease_manager

# Phase 13.7 AOIS-HROP Core Exports
from app.runtime.operations.runtime import (
    OperationalRuntime,
    get_operational_runtime,
    RuntimeSupervisor,
    RuntimeInspector,
    RuntimeHeartbeat,
    RuntimeWatchdog,
)
from app.runtime.operations.health import (
    HealthEngine,
    get_health_engine,
    SubsystemHealthEvaluator,
    HealthScoreCalculator,
    DependencyHealthGraph,
    HealthTrendAnalyzer,
    HealthForecastEngine,
)
from app.runtime.operations.incidents import (
    IncidentEngine,
    get_incident_engine,
    IncidentClassifier,
    IncidentDetector,
    IncidentTimelineBuilder,
    IncidentCorrelationEngine,
    IncidentImpactAnalyzer,
)
from app.runtime.operations.diagnostics import (
    DiagnosisEngine,
    get_diagnosis_engine,
    RootCauseEngine,
    DependencyAnalyzer,
    CausalReasoner,
    DiagnosisConfidenceCalculator,
)
from app.runtime.operations.healing import (
    HealingEngine,
    get_healing_engine,
    HealingStrategySelector,
    WorkerRecoveryActuator,
    PlannerRecoveryActuator,
    ResourceRecoveryActuator,
    MemoryRecoveryActuator,
    HealingValidator,
    HealingAuditLedger,
)
from app.runtime.operations.recovery import (
    RecoveryEngine,
    get_recovery_engine,
    CheckpointRecoveryOrchestrator,
    PolicyRecoveryOrchestrator,
    OptimizationRecoveryOrchestrator,
    MissionContinuationEngine,
    RecoveryVerifier,
)
from app.runtime.operations.prediction import (
    FailurePredictor,
    RiskForecastEngine,
    FailureForecast,
    OperationalRiskForecast,
)
from app.runtime.operations.chaos import (
    ChaosEngine,
    get_chaos_engine,
    FaultInjector,
    RecoveryEvaluator,
    ChaosValidator,
    ResilienceBenchmark,
)
from app.runtime.operations.resilience import (
    ResilienceEngine,
    get_resilience_engine,
    AvailabilityCalculator,
    RecoveryMetricsCalculator,
    SLAEvaluator,
    EnterpriseResilienceProfile,
)
from app.runtime.operations.governance import (
    OperationalGovernance,
    get_operational_governance,
    OperationalPolicy,
    ComplianceReport,
    IncidentApprovalWorkflow,
    OperationalAuditLogger,
    ComplianceReporter,
)
from app.runtime.operations.analytics import (
    OperationalAnalytics,
    get_operational_analytics,
)
from app.runtime.operations.events import (
    OperationalSeverity,
    IncidentStatus,
    HealingActionType,
    SubsystemType,
    OperationalBaseEvent,
    RuntimeHeartbeatReceived,
    HealthEvaluated,
    HealthDegraded,
    IncidentDetected,
    IncidentEscalated,
    IncidentResolved,
    DiagnosisCompleted,
    HealingStarted,
    HealingCompleted,
    RecoveryStarted,
    RecoveryCompleted,
    RecoveryFailed,
    ChaosExperimentStarted,
    ChaosExperimentCompleted,
    ResilienceScoreCalculated,
    FailurePredicted,
    RiskForecastGenerated,
    AvailabilityUpdated,
    OperationalAuditGenerated,
    RuntimeRecovered,
)

__all__ = [
    # Legacy
    "CheckpointManager",
    "MissionCheckpoint",
    "checkpoint_manager",
    "HeartbeatManager",
    "DepartmentHeartbeat",
    "heartbeat_manager",
    "PersistentScheduler",
    "ScheduledOperation",
    "persistent_scheduler",
    "RecoverySnapshotEngine",
    "RecoveryResult",
    "LeaseManager",
    "ResourceLease",
    "lease_manager",
    # Phase 13.7 Runtime
    "OperationalRuntime",
    "get_operational_runtime",
    "RuntimeSupervisor",
    "RuntimeInspector",
    "RuntimeHeartbeat",
    "RuntimeWatchdog",
    # Health
    "HealthEngine",
    "get_health_engine",
    "SubsystemHealthEvaluator",
    "HealthScoreCalculator",
    "DependencyHealthGraph",
    "HealthTrendAnalyzer",
    "HealthForecastEngine",
    # Incidents
    "IncidentEngine",
    "get_incident_engine",
    "IncidentClassifier",
    "IncidentDetector",
    "IncidentTimelineBuilder",
    "IncidentCorrelationEngine",
    "IncidentImpactAnalyzer",
    # Diagnostics
    "DiagnosisEngine",
    "get_diagnosis_engine",
    "RootCauseEngine",
    "DependencyAnalyzer",
    "CausalReasoner",
    "DiagnosisConfidenceCalculator",
    # Healing
    "HealingEngine",
    "get_healing_engine",
    "HealingStrategySelector",
    "WorkerRecoveryActuator",
    "PlannerRecoveryActuator",
    "ResourceRecoveryActuator",
    "MemoryRecoveryActuator",
    "HealingValidator",
    "HealingAuditLedger",
    # Recovery
    "RecoveryEngine",
    "get_recovery_engine",
    "CheckpointRecoveryOrchestrator",
    "PolicyRecoveryOrchestrator",
    "OptimizationRecoveryOrchestrator",
    "MissionContinuationEngine",
    "RecoveryVerifier",
    # Prediction
    "FailurePredictor",
    "RiskForecastEngine",
    "FailureForecast",
    "OperationalRiskForecast",
    # Chaos
    "ChaosEngine",
    "get_chaos_engine",
    "FaultInjector",
    "RecoveryEvaluator",
    "ChaosValidator",
    "ResilienceBenchmark",
    # Resilience
    "ResilienceEngine",
    "get_resilience_engine",
    "AvailabilityCalculator",
    "RecoveryMetricsCalculator",
    "SLAEvaluator",
    "EnterpriseResilienceProfile",
    # Governance
    "OperationalGovernance",
    "get_operational_governance",
    "OperationalPolicy",
    "ComplianceReport",
    "IncidentApprovalWorkflow",
    "OperationalAuditLogger",
    "ComplianceReporter",
    # Analytics
    "OperationalAnalytics",
    "get_operational_analytics",
    # Events
    "OperationalSeverity",
    "IncidentStatus",
    "HealingActionType",
    "SubsystemType",
    "OperationalBaseEvent",
    "RuntimeHeartbeatReceived",
    "HealthEvaluated",
    "HealthDegraded",
    "IncidentDetected",
    "IncidentEscalated",
    "IncidentResolved",
    "DiagnosisCompleted",
    "HealingStarted",
    "HealingCompleted",
    "RecoveryStarted",
    "RecoveryCompleted",
    "RecoveryFailed",
    "ChaosExperimentStarted",
    "ChaosExperimentCompleted",
    "ResilienceScoreCalculated",
    "FailurePredicted",
    "RiskForecastGenerated",
    "AvailabilityUpdated",
    "OperationalAuditGenerated",
    "RuntimeRecovered",
]
