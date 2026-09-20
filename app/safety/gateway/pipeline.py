"""Safety Pipeline coordinating Pre-Execution, Tool Guard, and Post-Execution stages."""

from typing import List, Optional
from .context import SafetyContext, ToolContext
from .decision import (
    SafetyDecision,
    SafetyStatus,
    SafetyViolation,
    ViolationSeverity,
    SafetyCategory,
)
from ..input.validator import InputSafetyValidator
from ..injection.scanners import InjectionScanner
from ..jailbreak.detector import JailbreakDetector
from ..privacy.redaction import DataRedactor
from ..privacy.masking import DataMasker
from ..tools.validator import ToolSafetyValidator
from ..output.validator import OutputSafetyValidator
from ..hallucination.detector import HallucinationDetector
from ..risk.scoring import CompositeRiskScorer
from ..risk.assessment import RiskAssessmentEngine
from ..policies.integration import TenantSafetyPolicy


class SafetyPipeline:
    """Orchestrates multi-stage security, privacy, and hallucination guardrails across the AI lifecycle."""

    def __init__(
        self,
        input_validator: Optional[InputSafetyValidator] = None,
        injection_scanner: Optional[InjectionScanner] = None,
        jailbreak_detector: Optional[JailbreakDetector] = None,
        redactor: Optional[DataRedactor] = None,
        masker: Optional[DataMasker] = None,
        tool_validator: Optional[ToolSafetyValidator] = None,
        output_validator: Optional[OutputSafetyValidator] = None,
        hallucination_detector: Optional[HallucinationDetector] = None,
        risk_scorer: Optional[CompositeRiskScorer] = None,
        risk_assessor: Optional[RiskAssessmentEngine] = None,
    ):
        self.input_validator = input_validator or InputSafetyValidator()
        self.injection_scanner = injection_scanner or InjectionScanner()
        self.jailbreak_detector = jailbreak_detector or JailbreakDetector()
        self.redactor = redactor or DataRedactor()
        self.masker = masker or DataMasker()
        self.tool_validator = tool_validator or ToolSafetyValidator()
        self.output_validator = output_validator or OutputSafetyValidator()
        self.hallucination_detector = hallucination_detector or HallucinationDetector()
        self.risk_scorer = risk_scorer or CompositeRiskScorer()
        self.risk_assessor = risk_assessor or RiskAssessmentEngine(self.risk_scorer)

    def guard_input(
        self,
        context: SafetyContext,
        policy: Optional[TenantSafetyPolicy] = None,
    ) -> SafetyDecision:
        """Pre-execution safety pipeline: Input validation, injection, jailbreak, PII, and risk scoring."""
        policy = policy or TenantSafetyPolicy(tenant_id=context.tenant_id)
        violations: List[SafetyViolation] = []
        raw_text = context.raw_input or ""

        # 1. Basic input validation
        is_valid, val_violations = self.input_validator.validate(raw_text)
        violations.extend(val_violations)

        # 2. Injection scanning (Direct & Indirect)
        inj_res = self.injection_scanner.scan_context(context)
        if not inj_res.is_safe:
            violations.extend(inj_res.violations)

        # 3. Jailbreak detection
        is_jb, jb_violations = self.jailbreak_detector.detect(raw_text)
        if is_jb:
            violations.extend(jb_violations)

        # 4. PII Redaction / Masking on input
        sanitized_input = raw_text
        if policy.auto_redact_pii and raw_text:
            redaction_res = self.redactor.redact(raw_text, pseudonymize=False)
            sanitized_input = redaction_res.redacted_text
            context.processed_input = sanitized_input

        # 5. Risk scoring
        has_critical = any(v.severity == ViolationSeverity.CRITICAL for v in violations)
        has_high = any(v.severity == ViolationSeverity.HIGH for v in violations)
        if has_critical:
            input_risk = 0.95
        elif has_high:
            input_risk = 0.60
        elif violations:
            input_risk = 0.20
        else:
            input_risk = 0.05

        component_scores = self.risk_scorer.score_context(context, input_risk=input_risk)
        assessment = self.risk_assessor.assess(component_scores, violations)

        # Check policy blocks
        status = assessment.recommended_status
        if (inj_res.has_direct_injection and policy.block_on_prompt_injection) or (is_jb and policy.block_on_jailbreak):
            status = SafetyStatus.BLOCK

        is_allowed = status not in [SafetyStatus.BLOCK, SafetyStatus.REQUIRE_HUMAN]

        return SafetyDecision(
            status=status,
            is_allowed=is_allowed,
            violations=violations,
            sanitized_content=sanitized_input,
            composite_risk_score=component_scores.composite_risk,
            explanation=assessment.explanation,
            metadata={"component_scores": component_scores.model_dump()},
        )

    def guard_tool(
        self,
        tool_name: str,
        parameters: dict,
        user_role: str = "user",
        is_dry_run: bool = False,
    ) -> SafetyDecision:
        """Tool safety pipeline: Checks permissions, dangerous parameters, and sandboxing requirements."""
        is_safe, violations = self.tool_validator.validate_tool_invocation(
            tool_name=tool_name,
            parameters=parameters,
            user_role=user_role,
            is_dry_run=is_dry_run,
        )

        has_critical = any(v.severity == ViolationSeverity.CRITICAL for v in violations)
        status = SafetyStatus.BLOCK if has_critical else (SafetyStatus.REQUIRE_HUMAN if not is_safe else SafetyStatus.ALLOW)

        return SafetyDecision(
            status=status,
            is_allowed=is_safe,
            violations=violations,
            explanation="Tool invocation validated by safety sandbox" if is_safe else "Tool invocation blocked or restricted by policy",
        )

    def guard_output(
        self,
        context: SafetyContext,
        policy: Optional[TenantSafetyPolicy] = None,
    ) -> SafetyDecision:
        """Post-execution safety pipeline: Toxicity, secret leakage, factuality, hallucination, and grounding."""
        policy = policy or TenantSafetyPolicy(tenant_id=context.tenant_id)
        violations: List[SafetyViolation] = []
        output_text = context.generated_output or ""

        # 1. Output safety (Toxicity, Secret Leakage, PII)
        sys_prompt = context.prompt_context.system_prompt if context.prompt_context else None
        is_safe, out_violations, sanitized_output = self.output_validator.validate_output(
            text=output_text,
            system_prompt=sys_prompt,
            auto_redact_pii=policy.auto_redact_pii,
        )
        violations.extend(out_violations)
        context.sanitized_output = sanitized_output

        # 2. Hallucination & Grounding verification
        if context.knowledge_chunks:
            is_hal, hal_violations, report = self.hallucination_detector.detect(
                output_text=output_text,
                knowledge_chunks=context.knowledge_chunks,
            )
            violations.extend(hal_violations)

        # 3. Output risk scoring (evaluating unmitigated violations)
        unmitigated_critical = any(v.severity == ViolationSeverity.CRITICAL and not v.details.get("mitigated_by_redaction") for v in violations)
        unmitigated_high = any(v.severity == ViolationSeverity.HIGH and not v.details.get("mitigated_by_redaction") for v in violations)
        
        if unmitigated_critical:
            out_risk = 0.95
        elif unmitigated_high:
            out_risk = 0.60
        elif violations:
            out_risk = 0.15
        else:
            out_risk = 0.05

        component_scores = self.risk_scorer.score_context(context, output_risk=out_risk)
        assessment = self.risk_assessor.assess(component_scores, violations)

        is_allowed = assessment.recommended_status not in [SafetyStatus.BLOCK, SafetyStatus.REQUIRE_HUMAN]

        return SafetyDecision(
            status=assessment.recommended_status,
            is_allowed=is_allowed,
            violations=violations,
            sanitized_content=sanitized_output,
            composite_risk_score=component_scores.composite_risk,
            explanation=assessment.explanation,
            metadata={"component_scores": component_scores.model_dump()},
        )
