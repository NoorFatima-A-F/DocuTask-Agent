"""Safety Runtime Developer SDK & Decorators."""

import functools
from typing import Optional, Dict, Any, List, Callable
from ..gateway.context import (
    SafetyContext,
    SourceTrustLevel,
    ModelContext,
    PromptContext,
    KnowledgeChunk,
)
from ..gateway.decision import SafetyDecision
from ..gateway.runtime import SafetyGateway
from ..privacy.redaction import DataRedactor, RedactionResult
from ..privacy.masking import DataMasker
from ..hallucination.grounding import GroundingVerifier, GroundingReport


class SafetyRuntimeSDK:
    """Developer SDK client providing high-level safety guardrails for AI applications."""

    def __init__(self, gateway: Optional[SafetyGateway] = None):
        self.gateway = gateway or SafetyGateway()
        self.redactor = DataRedactor()
        self.masker = DataMasker()
        self.grounding_verifier = GroundingVerifier()

    def guard_input(
        self,
        raw_input: str,
        tenant_id: str,
        user_id: Optional[str] = None,
        agent_id: Optional[str] = None,
        source_trust: SourceTrustLevel = SourceTrustLevel.USER,
        model_id: Optional[str] = None,
        knowledge_chunks: Optional[List[KnowledgeChunk]] = None,
    ) -> SafetyDecision:
        context = SafetyContext(
            tenant_id=tenant_id,
            user_id=user_id,
            agent_id=agent_id,
            raw_input=raw_input,
            source_trust=source_trust,
            model_context=ModelContext(model_id=model_id) if model_id else None,
            knowledge_chunks=knowledge_chunks or [],
        )
        return self.gateway.inspect_input(context)

    def guard_output(
        self,
        generated_output: str,
        tenant_id: str,
        system_prompt: Optional[str] = None,
        knowledge_chunks: Optional[List[KnowledgeChunk]] = None,
    ) -> SafetyDecision:
        context = SafetyContext(
            tenant_id=tenant_id,
            generated_output=generated_output,
            prompt_context=PromptContext(system_prompt=system_prompt) if system_prompt else None,
            knowledge_chunks=knowledge_chunks or [],
        )
        return self.gateway.inspect_output(context)

    def validate_tool_call(
        self,
        tool_name: str,
        parameters: Dict[str, Any],
        user_role: str = "user",
        is_dry_run: bool = False,
        tenant_id: str = "default",
    ) -> SafetyDecision:
        context = SafetyContext(tenant_id=tenant_id)
        return self.gateway.inspect_tool(
            context=context,
            tool_name=tool_name,
            parameters=parameters,
            user_role=user_role,
            is_dry_run=is_dry_run,
        )

    def verify_grounding(
        self,
        output_text: str,
        knowledge_chunks: List[KnowledgeChunk],
    ) -> GroundingReport:
        return self.grounding_verifier.verify_grounding(output_text, knowledge_chunks)

    def redact_pii(self, text: str, pseudonymize: bool = False) -> RedactionResult:
        return self.redactor.redact(text, pseudonymize=pseudonymize)

    def mask_pii(self, text: str) -> str:
        return self.masker.mask_text(text)


def safety_guard(
    tenant_id: str = "default",
    sdk: Optional[SafetyRuntimeSDK] = None,
    block_action: str = "raise",  # "raise" or "return_error"
):
    """Function decorator that automatically executes pre- and post-inference safety guardrails."""
    safety_client = sdk or SafetyRuntimeSDK()

    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # 1. Pre-execution guard
            raw_input = kwargs.get("prompt") or kwargs.get("input_text") or (args[0] if args else "")
            if isinstance(raw_input, str) and raw_input:
                input_decision = safety_client.guard_input(raw_input=raw_input, tenant_id=tenant_id)
                if not input_decision.is_allowed:
                    if block_action == "raise":
                        raise PermissionError(f"Safety guardrail blocked input: {input_decision.explanation}")
                    return {"error": "SAFETY_BLOCKED", "decision": input_decision.model_dump()}

            # 2. Invoke actual function
            result = func(*args, **kwargs)

            # 3. Post-execution guard
            if isinstance(result, str) and result:
                output_decision = safety_client.guard_output(generated_output=result, tenant_id=tenant_id)
                if not output_decision.is_allowed:
                    if block_action == "raise":
                        raise PermissionError(f"Safety guardrail blocked output: {output_decision.explanation}")
                    return {"error": "SAFETY_BLOCKED", "decision": output_decision.model_dump()}
                if output_decision.sanitized_content:
                    return output_decision.sanitized_content

            return result
        return wrapper
    return decorator
