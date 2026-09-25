from typing import Dict, Optional
from app.platform_verification.lifecycle.context import VerificationExecutionContext
from app.platform_verification.lifecycle.pipeline import verification_pipeline

class CanonicalLifecycleOrchestrator:
    def __init__(self):
        self._executions: Dict[str, VerificationExecutionContext] = {}

    def start_verification(self, definition_id: str, tenant_id: str, initiator: str = "Automated System") -> VerificationExecutionContext:
        ctx = VerificationExecutionContext(definition_id=definition_id, tenant_id=tenant_id, initiator=initiator)
        final_ctx = verification_pipeline.execute_lifecycle(ctx)
        self._executions[final_ctx.execution_id] = final_ctx
        return final_ctx

    def get_execution(self, execution_id: str) -> Optional[VerificationExecutionContext]:
        return self._executions.get(execution_id)

    def reproduce_verification(self, execution_id: str) -> Optional[VerificationExecutionContext]:
        source = self.get_execution(execution_id)
        if not source:
            return None
        repro_ctx = verification_pipeline.reproduce_lifecycle(source)
        self._executions[repro_ctx.execution_id] = repro_ctx
        return repro_ctx

canonical_lifecycle_orchestrator = CanonicalLifecycleOrchestrator()
