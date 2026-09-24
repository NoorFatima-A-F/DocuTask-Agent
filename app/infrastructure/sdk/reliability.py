"""
Unified High-Level Reliability & Disaster Recovery SDK.

Provides clean, enterprise-grade programmatic interfaces for interacting with
probes, health evaluations, failover plans, disaster recovery workflows, replication, and incidents.
"""

from __future__ import annotations

from typing import Any, Callable, List, Optional

from app.infrastructure.failover.orchestrator import FailoverExecutionResult, FailoverOrchestrator
from app.infrastructure.failover.planner import FailoverPlan, FailoverScope, FailoverType
from app.infrastructure.health.aggregator import HealthAggregatorService, SystemHealthMatrix
from app.infrastructure.health.evaluator import HealthScore
from app.infrastructure.health.heartbeat import HeartbeatSignal, HeartbeatStatus
from app.infrastructure.health.probes import HealthProbe, ProbeResult, ProbeType
from app.infrastructure.incidents.manager import IncidentManager
from app.infrastructure.incidents.models import Incident
from app.infrastructure.recovery.checkpoints import Checkpoint, CheckpointManager, CheckpointType
from app.infrastructure.recovery.executor import RecoveryWorkflowExecutor, WorkflowExecutionReport
from app.infrastructure.recovery.verification import RecoveryVerifier
from app.infrastructure.recovery.workflows import RecoveryWorkflow
from app.infrastructure.reliability.manager import ReliabilityManager
from app.infrastructure.reliability.models import (
    SeverityLevel,
)
from app.infrastructure.replication.conflict_resolution import (
    ConflictResolutionStrategy,
    ConflictResolver,
    ReplicationConflict,
    ResolutionResult,
)
from app.infrastructure.replication.models import ReplicationLagMetric
from app.infrastructure.replication.replication_manager import ReplicationManager
from app.infrastructure.replication.sync import SyncCoordinator


class ReliabilitySDK:
    """
    Unified platform SDK for enterprise reliability, health, failover, recovery, and incidents.
    """

    def __init__(
        self,
        reliability_manager: Optional[ReliabilityManager] = None,
        health_aggregator: Optional[HealthAggregatorService] = None,
        failover_orchestrator: Optional[FailoverOrchestrator] = None,
        checkpoint_manager: Optional[CheckpointManager] = None,
        recovery_executor: Optional[RecoveryWorkflowExecutor] = None,
        recovery_verifier: Optional[RecoveryVerifier] = None,
        replication_manager: Optional[ReplicationManager] = None,
        sync_coordinator: Optional[SyncCoordinator] = None,
        conflict_resolver: Optional[ConflictResolver] = None,
        incident_manager: Optional[IncidentManager] = None,
    ) -> None:
        self.reliability_manager = reliability_manager or ReliabilityManager()
        self.health_aggregator = health_aggregator or HealthAggregatorService()
        self.failover_orchestrator = failover_orchestrator or FailoverOrchestrator()
        self.checkpoint_manager = checkpoint_manager or CheckpointManager()
        self.recovery_executor = recovery_executor or RecoveryWorkflowExecutor()
        self.recovery_verifier = recovery_verifier or RecoveryVerifier()
        self.replication_manager = replication_manager or ReplicationManager()
        self.sync_coordinator = sync_coordinator or SyncCoordinator()
        self.conflict_resolver = conflict_resolver or ConflictResolver()
        self.incident_manager = incident_manager or IncidentManager()

    # --- Health & Probing ---
    def register_probe(
        self,
        probe_id: str,
        component_id: str,
        probe_type: ProbeType = ProbeType.LIVENESS,
        interval_seconds: float = 10.0,
        timeout_seconds: float = 3.0,
        handler: Optional[Callable[[], Any]] = None,
    ) -> HealthProbe:
        probe = HealthProbe(
            probe_id=probe_id,
            component_id=component_id,
            probe_type=probe_type,
            interval_seconds=interval_seconds,
            timeout_seconds=timeout_seconds,
        )
        self.health_aggregator.probe_registry.register_probe(probe, handler=handler)
        return probe

    def execute_probe(self, probe_id: str) -> ProbeResult:
        return self.health_aggregator.probe_registry.execute_probe_sync(probe_id)

    def get_component_health(self, component_id: str) -> HealthScore:
        return self.health_aggregator.get_component_health(component_id)

    def get_system_health(self) -> SystemHealthMatrix:
        return self.health_aggregator.get_system_health_matrix()

    def record_heartbeat(self, entity_id: str, entity_type: str = "service", **kwargs: Any) -> HeartbeatStatus:
        signal = HeartbeatSignal(entity_id=entity_id, entity_type=entity_type, **kwargs)
        return self.health_aggregator.heartbeat_aggregator.record_heartbeat(signal)

    # --- Failover & Routing ---
    def plan_failover(
        self,
        plan_id: str,
        source_region: str,
        target_region: str,
        failover_type: FailoverType = FailoverType.AUTOMATIC,
        scope: FailoverScope = FailoverScope.REGION,
        affected_services: Optional[List[str]] = None,
        reason: str = "Reliability threshold breach",
    ) -> FailoverPlan:
        return self.failover_orchestrator.planner.create_plan(
            plan_id=plan_id,
            source_region=source_region,
            target_region=target_region,
            failover_type=failover_type,
            scope=scope,
            affected_services=affected_services,
            reason=reason,
        )

    def execute_failover(self, plan_id: str) -> FailoverExecutionResult:
        return self.failover_orchestrator.execute_failover(plan_id)

    # --- Checkpoints & Recovery ---
    def create_checkpoint(
        self,
        checkpoint_id: str,
        checkpoint_type: CheckpointType,
        entity_id: str,
        region_id: str,
        payload_data: Any,
    ) -> Checkpoint:
        return self.checkpoint_manager.create_checkpoint(
            checkpoint_id=checkpoint_id,
            checkpoint_type=checkpoint_type,
            entity_id=entity_id,
            region_id=region_id,
            payload_data=payload_data,
        )

    def execute_recovery_workflow(self, workflow: RecoveryWorkflow) -> WorkflowExecutionReport:
        return self.recovery_executor.execute_workflow(workflow)

    # --- Replication & Conflicts ---
    def record_replication_lag(
        self,
        stream_id: str,
        lag_seconds: float,
        byte_lag: int = 0,
        unapplied_mutations: int = 0,
    ) -> ReplicationLagMetric:
        if not self.replication_manager.get_stream(stream_id):
            self.replication_manager.register_stream(
                stream_id=stream_id,
                source_region="us-east-1",
                target_region="us-west-2",
                dataset_name="default",
            )
        return self.replication_manager.record_lag(
            stream_id=stream_id,
            lag_seconds=lag_seconds,
            byte_lag=byte_lag,
            unapplied_mutations=unapplied_mutations,
        )

    def resolve_conflict(
        self,
        conflict: ReplicationConflict,
        strategy: ConflictResolutionStrategy = ConflictResolutionStrategy.LAST_WRITE_WINS,
    ) -> ResolutionResult:
        return self.conflict_resolver.resolve(conflict, strategy)

    # --- Incidents ---
    def create_incident(
        self,
        incident_id: str,
        title: str,
        severity: SeverityLevel = SeverityLevel.WARNING,
        impacted_components: Optional[List[str]] = None,
        lead_responder: Optional[str] = None,
    ) -> Incident:
        return self.incident_manager.create_incident(
            incident_id=incident_id,
            title=title,
            severity=severity,
            impacted_components=impacted_components,
            lead_responder=lead_responder,
        )

    def list_active_incidents(self) -> List[Incident]:
        return self.incident_manager.list_active_incidents()
