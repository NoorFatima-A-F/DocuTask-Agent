"""
Stage 13: Certification.
Produces authoritative certification decision with HMAC-SHA256 cryptographic signature.
"""
from app.platform_verification.lifecycle.stages.base_stage import BaseLifecycleStage
from app.platform_verification.lifecycle.context import VerificationExecutionContext, StageResult
from app.platform_verification.lifecycle.states import LifecycleState
from app.platform_verification.shared_kernel.security import HMACSigner
import uuid

class CertificationStage(BaseLifecycleStage):
    @property
    def stage_number(self) -> int:
        return 13

    @property
    def stage_name(self) -> str:
        return "Certification"

    @property
    def target_state(self) -> LifecycleState:
        return LifecycleState.CERTIFIED

    def validate_entry_criteria(self, context: VerificationExecutionContext) -> bool:
        return context.quality_gate_decision.get("gate_passed") is True

    def execute_stage(self, context: VerificationExecutionContext) -> StageResult:
        cert_id = f"cert_{uuid.uuid4().hex[:8]}"
        payload = f"{context.run_id}:{context.tenant_id}:ENTERPRISE_CERTIFIED:{context.created_at}"
        sig = HMACSigner.sign("DocuTask-Enterprise-Root-Key-2026-Immutable", payload)

        cert = {
            "certificate_id": cert_id,
            "level": "ENTERPRISE_CERTIFIED",
            "is_valid": True,
            "hmac_sha256_signature": sig,
            "authority": "DocuTask Enterprise Verification Authority v2.0"
        }
        context.certification_decision = cert
        return StageResult(
            stage_number=self.stage_number,
            stage_name=self.stage_name,
            status="PASSED",
            produced_artifacts=cert
        )

    def validate_exit_criteria(self, context: VerificationExecutionContext, result: StageResult) -> bool:
        return bool(context.certification_decision.get("certificate_id"))
