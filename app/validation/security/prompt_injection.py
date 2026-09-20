"""
Prompt Injection Security Testing Engine.
Executes direct prompt injections, role manipulation, instruction hierarchy override tests,
and document-based injection benchmarks.
"""

from typing import List
from app.ai.prompt_builder import PromptBuilder
from app.core.logging import logger
from app.validation.security.attack_cases import AttackCase, AttackResult


class PromptInjectionTester:
    """Tester evaluating prompt injection resistance."""

    @classmethod
    def test_injection(cls, attack_case: AttackCase) -> AttackResult:
        """
        Executes a prompt injection attack against PromptBuilder.sanitize_text.
        """
        sanitized = PromptBuilder.sanitize_text(attack_case.payload)
        user_prompt = PromptBuilder.build_prompt(attack_case.payload, "invoice")

        # System override tags should be neutralized
        tag_blocked = "SYSTEM:" not in sanitized and "USER:" not in sanitized
        delim_blocked = "<|im_start|>" not in sanitized and "<|im_end|>" not in sanitized

        passed = tag_blocked and delim_blocked
        actual_behavior = f"Sanitized payload: '{sanitized[:80]}...'. Direct system override tags neutralized." if passed else "System tags persisted in prompt."

        logger.info(f"Executed prompt injection test '{attack_case.attack_id}': Passed={passed}")

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
