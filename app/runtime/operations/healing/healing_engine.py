"""
AOIS-HROP Phase 13.7 - Healing Engine
Master self-healing coordinator orchestrating strategy selection, execution actuators, validation, and audit recording.
"""

from typing import Any, Dict, List, Optional
import uuid
from app.runtime.operations.healing.strategy_selector import HealingStrategySelector
from app.runtime.operations.healing.domain_actuators import (
    WorkerRecoveryActuator,
    PlannerRecoveryActuator,
    ResourceRecoveryActuator,
    MemoryRecoveryActuator,
    HealingExecutionResult,
)
from app.runtime.operations.healing.healing_validator import HealingValidator
from app.runtime.operations.healing.healing_audit import HealingAuditLedger, HealingAuditRecord
from app.runtime.operations.events.operation_events import HealingActionType, OperationalSeverity, SubsystemType


class HealingEngine:
    """
    Master self-healing coordinator executing automated remediations for detected runtime anomalies.
    """

    def __init__(self):
        self.strategy_selector = HealingStrategySelector()
        self.worker_actuator = WorkerRecoveryActuator()
        self.planner_actuator = PlannerRecoveryActuator()
        self.resource_actuator = ResourceRecoveryActuator()
        self.memory_actuator = MemoryRecoveryActuator()
        self.validator = HealingValidator()
        self.audit_ledger = HealingAuditLedger()

    def execute_healing(
        self,
        incident_id: str,
        subsystem: SubsystemType,
        error_type: str = "WORKER_CRASH",
        severity: OperationalSeverity = OperationalSeverity.MEDIUM,
        target_resource: str = "worker-thread-01",
        manual_override_action: Optional[HealingActionType] = None,
    ) -> Dict[str, Any]:
        healing_id = f"heal-{uuid.uuid4().hex[:8]}"
        action = manual_override_action or self.strategy_selector.select_strategy(subsystem, error_type, severity)

        # Actuate remediation
        if action == HealingActionType.WORKER_RESTART:
            result = self.worker_actuator.restart_worker(target_resource)
        elif action == HealingActionType.WORKER_REPLACE:
            result = self.worker_actuator.replace_worker(target_resource)
        elif action == HealingActionType.PLANNER_REPLAN:
            result = self.planner_actuator.trigger_replan(target_resource, reason=error_type)
        elif action == HealingActionType.PLANNER_ROLLBACK:
            result = self.planner_actuator.trigger_rollback(target_resource)
        elif action == HealingActionType.MEMORY_REPAIR:
            result = self.memory_actuator.repair_cache(target_resource)
        elif action == HealingActionType.FALLBACK_MODEL_ENGAGE:
            result = self.resource_actuator.engage_fallback_model(target_resource)
        else:
            result = self.resource_actuator.reallocate_concurrency(target_resource, new_concurrency=12)

        is_valid = self.validator.validate_healing(
            action_type=action.value,
            target_subsystem=subsystem.value,
        )

        audit_rec = self.audit_ledger.record_healing_event(
            healing_id=healing_id,
            incident_id=incident_id,
            action_type=action.value,
            target=target_resource,
            success=result.status == "SUCCESS" and is_valid,
        )

        return {
            "healing_id": healing_id,
            "incident_id": incident_id,
            "action_type": action.value,
            "target": target_resource,
            "status": "COMPLETED" if result.status == "SUCCESS" and is_valid else "FAILED",
            "execution_time_ms": result.execution_time_ms,
            "validation_passed": is_valid,
            "audit_hash": audit_rec.sha256_hash,
            "details": result.details,
            "timestamp": audit_rec.timestamp_utc,
        }

    def get_healing_history(self) -> List[Dict[str, Any]]:
        return [
            {
                "audit_id": r.audit_id,
                "healing_id": r.healing_id,
                "incident_id": r.incident_id,
                "action_type": r.action_type,
                "target": r.target,
                "success": r.success,
                "hash": r.sha256_hash,
                "timestamp": r.timestamp_utc,
            }
            for r in self.audit_ledger.get_all_records()
        ]


_GLOBAL_HEALING_ENGINE: Optional[HealingEngine] = None


def get_healing_engine() -> HealingEngine:
    global _GLOBAL_HEALING_ENGINE
    if _GLOBAL_HEALING_ENGINE is None:
        _GLOBAL_HEALING_ENGINE = HealingEngine()
    return _GLOBAL_HEALING_ENGINE
