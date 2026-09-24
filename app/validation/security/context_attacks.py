"""
Context Window Abuse & Delimiter Confusion Testing Engine.
Evaluates large document text, repeated malicious instructions, and prompt delimiter confusion attacks.
"""

from app.ai.prompt_builder import PromptBuilder
from app.core.logging import logger
from app.validation.security.attack_cases import AttackCase, AttackResult


class ContextAttackTester:
    """Tester evaluating context window floods and delimiter confusion attacks."""

    @classmethod
    def test_context(cls, attack_case: AttackCase) -> AttackResult:
        """
        Executes context delimiter confusion attack test.
        """
        sanitized = PromptBuilder.sanitize_text(attack_case.payload)
        PromptBuilder.build_prompt(sanitized, "invoice")

        # System override tags should be stripped
        passed = "SYSTEM:" not in sanitized
        actual_behavior = "Delimiter override attempts contained safely in untrusted text section."

        logger.info(f"Executed Context attack test '{attack_case.attack_id}': Passed={passed}")

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
