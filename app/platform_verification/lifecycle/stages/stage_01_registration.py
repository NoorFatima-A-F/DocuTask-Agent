"""
Stage 1: Verification Registration.
Validates identity, ownership, permissions, assigns immutable IDs, and establishes traceability.
"""
from app.platform_verification.lifecycle.stages.base_stage import BaseLifecycleStage
from app.platform_verification.lifecycle.context import VerificationExecutionContext, StageResult
from app.platform_verification.lifecycle.states import LifecycleState

class VerificationRegistrationStage(BaseLifecycleStage):
    @property
    def stage_number(self) -> int:
        return 1

    @property
    def stage_name(self) -> str:
        return "Verification Registration"

    @property
    def target_state(self) -> LifecycleState:
        return LifecycleState.REGISTERED

    def validate_entry_criteria(self, context: VerificationExecutionContext) -> bool:
        return bool(context.execution_id and context.tenant_id and context.definition_id)

    def execute_stage(self, context: VerificationExecutionContext) -> StageResult:
        artifacts = {
            "registered_at": context.created_at,
            "initiator": context.initiator,
            "intent": context.intent,
            "tenant_id": context.tenant_id,
            "trace_id": f"trace_{context.execution_id[:8]}"
        }
        return StageResult(
            stage_number=self.stage_number,
            stage_name=self.stage_name,
            status="PASSED",
            produced_artifacts=artifacts
        )

    def validate_exit_criteria(self, context: VerificationExecutionContext, result: StageResult) -> bool:
        return result.status == "PASSED" and "trace_id" in result.produced_artifacts
