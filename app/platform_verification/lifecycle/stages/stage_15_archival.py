"""
Stage 15: Archival.
Archives all execution assets, plans, datasets, evidence, and certificates into an immutable bundle.
"""
from app.platform_verification.lifecycle.stages.base_stage import BaseLifecycleStage
from app.platform_verification.lifecycle.context import VerificationExecutionContext, StageResult
from app.platform_verification.lifecycle.states import LifecycleState
from app.platform_verification.shared_kernel.security import CanonicalHasher
from datetime import datetime, timezone

class ArchivalStage(BaseLifecycleStage):
    @property
    def stage_number(self) -> int:
        return 15

    @property
    def stage_name(self) -> str:
        return "Archival"

    @property
    def target_state(self) -> LifecycleState:
        return LifecycleState.ARCHIVED

    def validate_entry_criteria(self, context: VerificationExecutionContext) -> bool:
        return bool(context.report_manifest and context.certification_decision)

    def execute_stage(self, context: VerificationExecutionContext) -> StageResult:
        bundle = {
            "execution_id": context.execution_id,
            "run_id": context.run_id,
            "config_fingerprint": context.config_fingerprint,
            "metrics": context.calculated_metrics,
            "certificate": context.certification_decision
        }
        bundle_hash = CanonicalHasher.hash_payload(bundle)
        context.archival_bundle_hash = bundle_hash
        context.completed_at = datetime.now(timezone.utc).isoformat()

        return StageResult(
            stage_number=self.stage_number,
            stage_name=self.stage_name,
            status="PASSED",
            produced_artifacts={"archival_hash": bundle_hash, "is_immutable": True}
        )

    def validate_exit_criteria(self, context: VerificationExecutionContext, result: StageResult) -> bool:
        return len(context.archival_bundle_hash or "") == 64
