"""
AOIS-HROP Phase 13.7 - Recovery Engine
Master recovery coordinator orchestrating checkpoint restoration, policy rollbacks, re-optimization, and mission continuation.
"""

from typing import Any, Dict, List, Optional
import uuid
from app.runtime.operations.recovery.recovery_orchestrators import (
    CheckpointRecoveryOrchestrator,
    PolicyRecoveryOrchestrator,
    OptimizationRecoveryOrchestrator,
    MissionContinuationEngine,
    RecoveryVerifier,
    RecoveryPlan,
    RecoveryExecutionResult,
)


class RecoveryEngine:
    """
    Master coordinator for multi-tier autonomous recovery operations.
    """

    def __init__(self):
        self.checkpoint_orchestrator = CheckpointRecoveryOrchestrator()
        self.policy_orchestrator = PolicyRecoveryOrchestrator()
        self.optimization_orchestrator = OptimizationRecoveryOrchestrator()
        self.continuation_engine = MissionContinuationEngine()
        self.verifier = RecoveryVerifier()
        self._history: List[RecoveryExecutionResult] = []

    def plan_recovery(
        self,
        mission_id: str,
        strategy: str = "CHECKPOINT_ROLLBACK",
        snapshot_id: Optional[str] = "snap_step_004",
    ) -> RecoveryPlan:
        steps = [
            f"1. Freeze active threads for mission {mission_id}",
            f"2. Restore immutable state from checkpoint {snapshot_id}",
            "3. Recompute DAG wavefront invariants",
            "4. Verify Truth Ledger cryptographic consistency",
            "5. Resume execution with verified continuation engine",
        ]

        return RecoveryPlan(
            plan_id=f"plan-rec-{uuid.uuid4().hex[:8]}",
            target_mission_id=mission_id,
            recovery_strategy=strategy,
            checkpoint_snapshot_id=snapshot_id,
            steps=steps,
        )

    def execute_recovery(
        self,
        mission_id: str,
        strategy: str = "CHECKPOINT_ROLLBACK",
        snapshot_id: Optional[str] = "snap_step_004",
    ) -> Dict[str, Any]:
        if strategy == "POLICY_FALLBACK":
            result = self.policy_orchestrator.rollback_policy(mission_id)
        elif strategy == "OPTIMIZATION_RETRY":
            result = self.optimization_orchestrator.reoptimize_execution(mission_id)
        else:
            result = self.checkpoint_orchestrator.restore_from_snapshot(mission_id, snapshot_id or "snap_step_004")

        is_verified = self.verifier.verify_consistency(mission_id, result.restored_step_index)
        continuation = self.continuation_engine.resume_mission(mission_id, result.restored_step_index)

        self._history.append(result)

        return {
            "recovery_id": result.recovery_id,
            "target_mission_id": result.target_mission_id,
            "strategy": result.strategy,
            "status": "COMPLETED" if result.status == "SUCCESS" and is_verified else "FAILED",
            "restored_step": result.restored_step_index,
            "invariants_restored": result.restored_invariants_count,
            "elapsed_ms": result.elapsed_ms,
            "consistency_verified": is_verified,
            "continuation": continuation,
            "timestamp": result.executed_at,
        }

    def get_recovery_history(self) -> List[Dict[str, Any]]:
        return [
            {
                "recovery_id": r.recovery_id,
                "mission_id": r.target_mission_id,
                "strategy": r.strategy,
                "status": r.status,
                "restored_step": r.restored_step_index,
                "elapsed_ms": r.elapsed_ms,
                "timestamp": r.executed_at,
            }
            for r in self._history
        ]


_GLOBAL_RECOVERY_ENGINE: Optional[RecoveryEngine] = None


def get_recovery_engine() -> RecoveryEngine:
    global _GLOBAL_RECOVERY_ENGINE
    if _GLOBAL_RECOVERY_ENGINE is None:
        _GLOBAL_RECOVERY_ENGINE = RecoveryEngine()
    return _GLOBAL_RECOVERY_ENGINE
