"""
Enterprise Autonomous Recovery Engine, Self-Healing Runtime & Failure Management Platform.
Provides RecoveryEngine, FailureClassifier, RootCauseAnalyzer, RecoveryStrategySelector,
RecoveryPlanner, CheckpointRestorer, RollbackCoordinator, CompensationEngine,
ReplayEngine, StateReconciliationEngine, CircuitBreaker, Bulkhead, and DeadLetterQueue.
Autonomous resilience layer observing execution events, diagnosing failures, selecting recovery strategies,
restoring system consistency, coordinating replay, and performing self-healing.
"""

from app.agents.recovery.anomaly_detector import AnomalyDetector
from app.agents.recovery.approval_recovery import ApprovalRecoveryManager
from app.agents.recovery.backoff import BackoffCalculator
from app.agents.recovery.builders import (
    FailureBuilder,
    IncidentBuilder,
    RecoveryRequestBuilder,
    RecoveryStrategyBuilder,
    ReplayBuilder,
)
from app.agents.recovery.bulkhead import Bulkhead, BulkheadManager
from app.agents.recovery.cache import RecoveryCache
from app.agents.recovery.checkpoint_restorer import CheckpointRestorer
from app.agents.recovery.circuit_breaker import CircuitBreaker, CircuitState
from app.agents.recovery.compensation import CompensatingAction, CompensationEngine
from app.agents.recovery.consistency_checker import (
    ConsistencyChecker,
    InconsistencyRecord,
)
from app.agents.recovery.context import (
    RecoveryContext,
    RecoveryRequest,
    RecoveryResult,
)
from app.agents.recovery.dead_letter import DeadLetterQueue, DeadLetterRecord
from app.agents.recovery.decision_adapter import RecoveryDecisionAdapter
from app.agents.recovery.drift_detector import DriftDetector
from app.agents.recovery.engine import RecoveryEngine
from app.agents.recovery.escalation import EscalationEngine, EscalationLevel
from app.agents.recovery.event_replay import EventReplayEngine
from app.agents.recovery.events import (
    CheckpointRestoredEvent,
    CompensationCompletedEvent,
    CompensationStartedEvent,
    DeadLetterCreatedEvent,
    EscalationTriggeredEvent,
    FailureClassifiedEvent,
    FailureDetectedEvent,
    IncidentCreatedEvent,
    RecoveryFailedEvent,
    RecoveryPlannedEvent,
    RecoveryStartedEvent,
    RecoveryStrategySelectedEvent,
    RecoverySucceededEvent,
    ReplayCompletedEvent,
    ReplayStartedEvent,
    RollbackCompletedEvent,
    RollbackStartedEvent,
    RootCauseIdentifiedEvent,
    SelfHealingCompletedEvent,
    SelfHealingStartedEvent,
    StateReconciledEvent,
)
from app.agents.recovery.exceptions import (
    BulkheadExhaustionException,
    CheckpointRestorationException,
    CircuitBreakerOpenException,
    EscalationException,
    FailureClassificationException,
    RecoveryException,
    RollbackCoordinationException,
    StateInconsistencyException,
    UnrecoverableFailureException,
)
from app.agents.recovery.execution_adapter import RecoveryExecutionAdapter
from app.agents.recovery.execution_replay import ExecutionReplayEngine
from app.agents.recovery.factory import RecoveryFactory
from app.agents.recovery.failure import (
    Failure,
    FailureCategory,
    FailureEvidence,
    FailureIdentity,
    FailureSeverity,
)
from app.agents.recovery.failure_analyzer import FailureAnalyzer
from app.agents.recovery.failure_catalog import CatalogEntry, FailureCatalog
from app.agents.recovery.failure_classifier import FailureClassifier
from app.agents.recovery.fallback_manager import FallbackManager
from app.agents.recovery.health_monitor import (
    RecoveryHealthMonitor,
    SubsystemHealthReport,
)
from app.agents.recovery.human_handoff import HumanHandoffManager, HumanHandoffTicket
from app.agents.recovery.incident import Incident, IncidentSeverity, IncidentStatus
from app.agents.recovery.incident_manager import IncidentManager
from app.agents.recovery.interfaces import (
    IFailureClassifier,
    IRecoveryEngine,
    IRecoveryPlanner,
    IRecoveryStrategySelector,
    IRootCauseAnalyzer,
)
from app.agents.recovery.lifecycle import RecoveryLifecycleState
from app.agents.recovery.manager import RecoveryManager
from app.agents.recovery.memory_adapter import RecoveryMemoryAdapter
from app.agents.recovery.metadata import (
    RecoveryIdentity,
    RecoveryMetadata,
    RecoveryStatistics,
)
from app.agents.recovery.metrics import RecoveryMetricRecord, RecoveryMetricsCollector
from app.agents.recovery.orchestrator import RecoveryOrchestrator
from app.agents.recovery.planner_adapter import RecoveryPlannerAdapter
from app.agents.recovery.policy import RecoveryPolicy
from app.agents.recovery.quarantine import QuarantineManager
from app.agents.recovery.recovery_context import RecoveryContextDetails
from app.agents.recovery.recovery_executor import RecoveryExecutor
from app.agents.recovery.recovery_graph import (
    RecoveryEdge,
    RecoveryGraph,
    RecoveryNode,
)
from app.agents.recovery.recovery_planner import RecoveryPlanner
from app.agents.recovery.recovery_session import RecoverySession
from app.agents.recovery.recovery_strategy import (
    RecoveryStrategy,
    RecoveryStrategyDefinition,
)
from app.agents.recovery.replay import ReplayEngine, ReplayInstruction
from app.agents.recovery.repository import RecoveryRepository
from app.agents.recovery.retry_orchestrator import RetryOrchestrator
from app.agents.recovery.retry_policy import RecoveryBackoffType, RecoveryRetryPolicy
from app.agents.recovery.rollback_coordinator import RollbackCoordinator
from app.agents.recovery.root_cause import CausalLink, RootCauseAnalyzer, RootCauseReport
from app.agents.recovery.runtime import RecoveryRuntime
from app.agents.recovery.runtime_monitor import RuntimeHealthStatus, RuntimeMonitor
from app.agents.recovery.self_healing import SelfHealingAction, SelfHealingEngine
from app.agents.recovery.serialization import RecoverySerializer
from app.agents.recovery.snapshot_restorer import SnapshotRestorer
from app.agents.recovery.state_reconciliation import (
    ReconciliationReport,
    StateReconciliationEngine,
)
from app.agents.recovery.strategy_registry import RecoveryStrategyRegistry
from app.agents.recovery.strategy_selector import RecoveryStrategySelector
from app.agents.recovery.tool_adapter import RecoveryToolAdapter
from app.agents.recovery.validation import RecoveryValidationReport, RecoveryValidator
from app.agents.recovery.validators import RecoveryRequestValidator
from app.agents.recovery.worker_monitor import WorkerHealthStatus, WorkerMonitor

__all__ = [
    # Core Recovery Engine & Runtime
    "RecoveryEngine",
    "RecoveryManager",
    "RecoveryOrchestrator",
    "RecoveryRuntime",
    "RecoverySession",
    "RecoveryContext",
    "RecoveryRequest",
    "RecoveryResult",
    "RecoveryLifecycleState",
    "RecoveryPolicy",
    # Failures & Root Cause Analysis
    "Failure",
    "FailureIdentity",
    "FailureEvidence",
    "FailureSeverity",
    "FailureCategory",
    "FailureClassifier",
    "FailureCatalog",
    "CatalogEntry",
    "FailureAnalyzer",
    "RootCauseAnalyzer",
    "RootCauseReport",
    "CausalLink",
    # Incident Management
    "Incident",
    "IncidentSeverity",
    "IncidentStatus",
    "IncidentManager",
    # Recovery Strategy & Planning
    "RecoveryStrategy",
    "RecoveryStrategyDefinition",
    "RecoveryStrategyRegistry",
    "RecoveryStrategySelector",
    "RecoveryPlanner",
    "RecoveryGraph",
    "RecoveryNode",
    "RecoveryEdge",
    "RecoveryExecutor",
    # Checkpoints, Rollback & Compensation
    "CheckpointRestorer",
    "SnapshotRestorer",
    "RollbackCoordinator",
    "CompensationEngine",
    "CompensatingAction",
    # Replay & Reconciliation
    "ReplayEngine",
    "ReplayInstruction",
    "EventReplayEngine",
    "ExecutionReplayEngine",
    "ConsistencyChecker",
    "InconsistencyRecord",
    "StateReconciliationEngine",
    "ReconciliationReport",
    # Resilience, Isolation & Dead Letter
    "DeadLetterQueue",
    "DeadLetterRecord",
    "QuarantineManager",
    "CircuitBreaker",
    "CircuitState",
    "Bulkhead",
    "BulkheadManager",
    "FallbackManager",
    "RetryOrchestrator",
    "RecoveryRetryPolicy",
    "RecoveryBackoffType",
    "BackoffCalculator",
    # Self-Healing & Escalation
    "SelfHealingEngine",
    "SelfHealingAction",
    "EscalationEngine",
    "EscalationLevel",
    "HumanHandoffManager",
    "HumanHandoffTicket",
    "ApprovalRecoveryManager",
    # Adapters
    "RecoveryExecutionAdapter",
    "RecoveryPlannerAdapter",
    "RecoveryDecisionAdapter",
    "RecoveryMemoryAdapter",
    "RecoveryToolAdapter",
    # Health Monitoring & Detection
    "RecoveryHealthMonitor",
    "SubsystemHealthReport",
    "WorkerMonitor",
    "WorkerHealthStatus",
    "RuntimeMonitor",
    "RuntimeHealthStatus",
    "AnomalyDetector",
    "DriftDetector",
    # Interfaces
    "IFailureClassifier",
    "IRootCauseAnalyzer",
    "IRecoveryStrategySelector",
    "IRecoveryPlanner",
    "IRecoveryEngine",
    # Validation, Serialization & Storage
    "RecoveryRequestValidator",
    "RecoveryValidator",
    "RecoveryValidationReport",
    "RecoverySerializer",
    "RecoveryCache",
    "RecoveryRepository",
    "RecoveryFactory",
    # Fluent Builders
    "FailureBuilder",
    "RecoveryRequestBuilder",
    "RecoveryStrategyBuilder",
    "IncidentBuilder",
    "ReplayBuilder",
    # Metrics
    "RecoveryMetricsCollector",
    "RecoveryMetricRecord",
    # Domain Events
    "FailureDetectedEvent",
    "FailureClassifiedEvent",
    "RootCauseIdentifiedEvent",
    "RecoveryStartedEvent",
    "RecoveryStrategySelectedEvent",
    "RecoveryPlannedEvent",
    "CheckpointRestoredEvent",
    "ReplayStartedEvent",
    "ReplayCompletedEvent",
    "RollbackStartedEvent",
    "RollbackCompletedEvent",
    "CompensationStartedEvent",
    "CompensationCompletedEvent",
    "StateReconciledEvent",
    "DeadLetterCreatedEvent",
    "SelfHealingStartedEvent",
    "SelfHealingCompletedEvent",
    "RecoverySucceededEvent",
    "RecoveryFailedEvent",
    "EscalationTriggeredEvent",
    "IncidentCreatedEvent",
    # Exceptions
    "RecoveryException",
    "FailureClassificationException",
    "UnrecoverableFailureException",
    "CheckpointRestorationException",
    "RollbackCoordinationException",
    "StateInconsistencyException",
    "CircuitBreakerOpenException",
    "BulkheadExhaustionException",
    "EscalationException",
]
