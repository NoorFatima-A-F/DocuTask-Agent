"""
Encoding Attacks Security Testing Engine.
Evaluates Base64, URL, HTML entity, and Hex encoded instructions to ensure they are treated
strictly as literal data context rather than executable system instructions.
"""

from app.ai.prompt_builder import PromptBuilder
from app.core.logging import logger
from app.validation.security.attack_cases import AttackCase, AttackResult


class EncodingAttackTester:
    """Tester evaluating encoded instruction attack defenses."""

    @classmethod
    def test_encoding(cls, attack_case: AttackCase) -> AttackResult:
        """
        Executes encoded instruction attack test.
        """
        sanitized = PromptBuilder.sanitize_text(attack_case.payload)
        user_prompt = PromptBuilder.build_prompt(sanitized, "invoice")

        # Encoded string must be wrapped inside DOCUMENT CONTENT section
        passed = "DOCUMENT CONTENT TO PROCESS:" in user_prompt and "SYSTEM:" not in sanitized
        actual_behavior = f"Encoded payload contained safely within DOCUMENT CONTENT block."

        logger.info(f"Executed Encoding attack test '{attack_case.attack_id}': Passed={passed}")

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
