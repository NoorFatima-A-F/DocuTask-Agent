"""
Recovery Workflows & Specialized Disaster Scenarios.

Implements predefined, battle-tested recovery workflows for Region Outages,
Database Corruption, Storage Volume Loss, Queue Loss, and AI Provider Fallbacks.
"""

from __future__ import annotations

import enum
import logging
from typing import Any, Callable, Dict, List, Optional
from pydantic import BaseModel, Field

logger = logging.getLogger("infrastructure.recovery.workflows")


class WorkflowCategory(str, enum.Enum):
    """Disaster and recovery scenario categories."""
    REGION_OUTAGE = "REGION_OUTAGE"
    DATABASE_CORRUPTION = "DATABASE_CORRUPTION"
    STORAGE_LOSS = "STORAGE_LOSS"
    QUEUE_LOSS = "QUEUE_LOSS"
    AI_PROVIDER_FALLBACK = "AI_PROVIDER_FALLBACK"
    CUSTOM = "CUSTOM"


class StepStatus(str, enum.Enum):
    """Execution status of a single recovery step."""
    PENDING = "PENDING"
    EXECUTING = "EXECUTING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    ROLLED_BACK = "ROLLED_BACK"
    SKIPPED = "SKIPPED"


class RecoveryStep(BaseModel):
    """Discrete step within a recovery workflow."""
    step_id: str
    name: str
    description: str = ""
    critical: bool = True
    timeout_seconds: float = 30.0
    status: StepStatus = StepStatus.PENDING
    result_message: str = ""
    error: Optional[str] = None


class RecoveryWorkflow(BaseModel):
    """Specification of a disaster recovery workflow."""
    workflow_id: str
    category: WorkflowCategory
    title: str
    target_entity_id: str
    steps: List[RecoveryStep] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)


def build_region_outage_workflow(workflow_id: str, target_region: str, failover_region: str) -> RecoveryWorkflow:
    """Build standardized Region Outage Recovery Workflow."""
    return RecoveryWorkflow(
        workflow_id=workflow_id,
        category=WorkflowCategory.REGION_OUTAGE,
        title=f"Region Outage Recovery: {target_region} -> {failover_region}",
        target_entity_id=target_region,
        steps=[
            RecoveryStep(step_id="isolate_region", name="Isolate Outage Region", description=f"Drain traffic from {target_region}"),
            RecoveryStep(step_id="revoke_leases", name="Revoke Workload Leases", description="Prevent split-brain double execution"),
            RecoveryStep(step_id="verify_target_capacity", name="Verify Target Capacity", description=f"Ensure {failover_region} has sufficient compute"),
            RecoveryStep(step_id="promote_target_region", name="Promote Target Region", description=f"Activate primary services in {failover_region}"),
            RecoveryStep(step_id="shift_dns_routes", name="Update Traffic Routes", description=f"Shift DNS/Gateway to {failover_region}"),
            RecoveryStep(step_id="verify_service_health", name="Verify End-to-End Health", description="Run readiness probes on new primary"),
        ],
        metadata={"source": target_region, "target": failover_region},
    )


def build_database_corruption_workflow(workflow_id: str, database_id: str, checkpoint_id: str) -> RecoveryWorkflow:
    """Build Database Corruption Recovery Workflow."""
    return RecoveryWorkflow(
        workflow_id=workflow_id,
        category=WorkflowCategory.DATABASE_CORRUPTION,
        title=f"Database Corruption Recovery for {database_id}",
        target_entity_id=database_id,
        steps=[
            RecoveryStep(step_id="quarantine_db", name="Quarantine Corrupted Database", description="Block write traffic immediately"),
            RecoveryStep(step_id="fetch_checkpoint", name="Fetch Last Known Good Checkpoint", description=f"Load snapshot {checkpoint_id}"),
            RecoveryStep(step_id="restore_data", name="Restore Snapshot Data", description="Populate secondary database instance"),
            RecoveryStep(step_id="replay_tx_logs", name="Replay Transaction Logs", description="Replay idempotent mutation logs up to point-of-failure"),
            RecoveryStep(step_id="verify_integrity", name="Verify Restored Data Integrity", description="Validate checksums and foreign keys"),
            RecoveryStep(step_id="reconnect_services", name="Reconnect Application Pool", description="Resume read/write traffic"),
        ],
        metadata={"database_id": database_id, "checkpoint_id": checkpoint_id},
    )


def build_storage_loss_workflow(workflow_id: str, volume_id: str, replica_volume_id: str) -> RecoveryWorkflow:
    """Build Object/Block Storage Loss Recovery Workflow."""
    return RecoveryWorkflow(
        workflow_id=workflow_id,
        category=WorkflowCategory.STORAGE_LOSS,
        title=f"Storage Loss Recovery for {volume_id}",
        target_entity_id=volume_id,
        steps=[
            RecoveryStep(step_id="detach_failed_volume", name="Detach Failed Storage Volume", description=f"Unmount {volume_id}"),
            RecoveryStep(step_id="attach_replica", name="Attach Cross-Region Replica", description=f"Mount replica {replica_volume_id}"),
            RecoveryStep(step_id="verify_filesystem", name="Verify File System & Hashes", description="Run fsck and checksum verification"),
            RecoveryStep(step_id="remount_services", name="Remount Storage to Workers", description="Resume worker file processing"),
        ],
        metadata={"volume_id": volume_id, "replica_id": replica_volume_id},
    )


def build_queue_loss_workflow(workflow_id: str, queue_id: str) -> RecoveryWorkflow:
    """Build Message Queue Loss Recovery Workflow."""
    return RecoveryWorkflow(
        workflow_id=workflow_id,
        category=WorkflowCategory.QUEUE_LOSS,
        title=f"Queue Infrastructure Recovery for {queue_id}",
        target_entity_id=queue_id,
        steps=[
            RecoveryStep(step_id="provision_fresh_queue", name="Provision Fallback Queue", description="Spin up secondary broker partition"),
            RecoveryStep(step_id="rehydrate_unacked_tasks", name="Rehydrate Unacked Workloads", description="Query execution lease registry for in-flight tasks"),
            RecoveryStep(step_id="republish_messages", name="Republish Workload Messages", description="Enqueue recovered workloads with idempotency keys"),
            RecoveryStep(step_id="resume_consumers", name="Resume Worker Consumer Groups", description="Enable worker task pulling"),
        ],
        metadata={"queue_id": queue_id},
    )


def build_ai_provider_fallback_workflow(workflow_id: str, primary_provider: str, secondary_provider: str) -> RecoveryWorkflow:
    """Build AI Provider Fallback Recovery Workflow."""
    return RecoveryWorkflow(
        workflow_id=workflow_id,
        category=WorkflowCategory.AI_PROVIDER_FALLBACK,
        title=f"AI Provider Fallback: {primary_provider} -> {secondary_provider}",
        target_entity_id=primary_provider,
        steps=[
            RecoveryStep(step_id="trip_circuit_breaker", name="Trip Primary Provider Circuit Breaker", description=f"Block calls to {primary_provider}"),
            RecoveryStep(step_id="switch_model_router", name="Switch Model Router to Secondary", description=f"Route inference to {secondary_provider}"),
            RecoveryStep(step_id="warmup_secondary", name="Warmup Secondary Model Endpoints", description="Execute test inference prompt"),
            RecoveryStep(step_id="verify_inference_quality", name="Verify Output Contract", description="Verify token generation matches schema requirements"),
        ],
        metadata={"primary": primary_provider, "secondary": secondary_provider},
    )
