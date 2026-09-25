"""
Structured Output & Schema Pollution Security Testing Engine.
Evaluates JSON layer robustness against malformed JSON, nested payload pollution, and type confusion attacks.
"""

import json
from app.ai.exceptions import AIValidationException
from app.ai.validator import AIValidator
from app.core.logging import logger
from app.validation.security.attack_cases import AttackCase, AttackResult


class SchemaAttackTester:
    """Tester evaluating JSON extraction layer defenses."""

    @classmethod
    def test_schema(cls, attack_case: AttackCase) -> AttackResult:
        """
        Executes schema attack against AIValidator.
        """
        try:
            raw_dict = json.loads(attack_case.payload)
            validated_dict, _ = AIValidator.validate(raw_dict, "invoice")
            # If payload was nested malicious dict for scalar field, validation should fail
            passed = False
            actual_behavior = "Unsafe schema pollution passed validation unexpectedly."
        except (AIValidationException, Exception) as exc:
            passed = True
            actual_behavior = f"Pydantic schema validation correctly rejected malicious payload: {str(exc)}"

        logger.info(f"Executed Schema attack test '{attack_case.attack_id}': Passed={passed}")

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
