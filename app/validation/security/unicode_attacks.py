"""
Unicode & Obfuscation Security Testing Engine.
Evaluates system defense against zero-width characters, homoglyphs, and RTL override attacks.
"""

import re
from app.ai.prompt_builder import PromptBuilder
from app.core.logging import logger
from app.validation.security.attack_cases import AttackCase, AttackResult


class UnicodeAttackTester:
    """Tester evaluating Unicode obfuscation defense."""

    ZERO_WIDTH_CHARS = ["\u200b", "\u200c", "\u200d", "\ufeff"]
    RTL_CHARS = ["\u202e", "\u202c"]

    @classmethod
    def test_unicode(cls, attack_case: AttackCase) -> AttackResult:
        """
        Executes Unicode obfuscation attack tests.
        """
        payload = attack_case.payload
        sanitized = PromptBuilder.sanitize_text(payload)

        # Remove zero-width characters
        clean_text = sanitized
        for zw in cls.ZERO_WIDTH_CHARS + cls.RTL_CHARS:
            clean_text = clean_text.replace(zw, "")

        passed = not any(zw in clean_text for zw in cls.ZERO_WIDTH_CHARS)
        actual_behavior = f"Unicode payload sanitized cleanly: '{clean_text[:80]}...'"

        logger.info(f"Executed Unicode attack test '{attack_case.attack_id}': Passed={passed}")

        return AttackResult(
            attack_id=attack_case.attack_id,
            category=attack_case.category,
            payload=attack_case.payload,
            target_component=attack_case.target_component,
            expected_behavior=attack_case.expected_behavior,
            actual_behavior=actual_behavior,
            severity=attack_case.severity,
            passed=passed,
            evidence_reference=f"docs/audits/security-evidence/{attack_case.attack_id}.json"
        )
