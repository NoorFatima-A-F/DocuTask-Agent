"""Comprehensive Output Safety Validator."""

from typing import List, Tuple, Optional
from ..gateway.decision import SafetyCategory, ViolationSeverity, SafetyViolation
from ..privacy.redaction import DataRedactor
from .toxicity import ToxicityDetector
from .leakage import DataLeakageDetector
from .factuality import FactualityChecker


class OutputSafetyValidator:
    """Master validator inspecting AI outputs for toxicity, leakage, factuality, and PII."""

    def __init__(
        self,
        toxicity_detector: Optional[ToxicityDetector] = None,
        leakage_detector: Optional[DataLeakageDetector] = None,
        factuality_checker: Optional[FactualityChecker] = None,
        redactor: Optional[DataRedactor] = None,
    ):
        self.toxicity_detector = toxicity_detector or ToxicityDetector()
        self.leakage_detector = leakage_detector or DataLeakageDetector()
        self.factuality_checker = factuality_checker or FactualityChecker()
        self.redactor = redactor or DataRedactor()

    def validate_output(
        self,
        text: str,
        system_prompt: Optional[str] = None,
        auto_redact_pii: bool = True,
    ) -> Tuple[bool, List[SafetyViolation], str]:
        violations: List[SafetyViolation] = []
        sanitized_text = text or ""

        if not text:
            return True, violations, sanitized_text

        # 1. Toxicity check
        is_toxic, tox_viols, _ = self.toxicity_detector.scan(text)
        violations.extend(tox_viols)

        # 2. Leakage check
        is_leaking, leak_viols = self.leakage_detector.scan(text, system_prompt=system_prompt)

        # 3. Factuality check
        is_consistent, fact_viols = self.factuality_checker.check(text)
        violations.extend(fact_viols)

        # 4. Optional auto-redaction of PII in output
        if auto_redact_pii:
            redact_res = self.redactor.redact(sanitized_text)
            sanitized_text = redact_res.redacted_text
            # Demote or mark PII violations as mitigated
            for v in leak_viols:
                if v.category == SafetyCategory.PII_LEAKAGE:
                    v.severity = ViolationSeverity.LOW
                    v.details["mitigated_by_redaction"] = True
            violations.extend(leak_viols)
        else:
            violations.extend(leak_viols)

        # Safe if no remaining critical / high severity violations
        unmitigated_high_or_critical = [
            v for v in violations
            if v.severity in [ViolationSeverity.CRITICAL, ViolationSeverity.HIGH]
            and not v.details.get("mitigated_by_redaction", False)
        ]
        is_safe = len(unmitigated_high_or_critical) == 0

        return is_safe, violations, sanitized_text
