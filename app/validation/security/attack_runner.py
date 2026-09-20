"""
Security Attack Suite Orchestrator & Execution Runner.
Orchestrates automated execution across prompt injection, Unicode, encoding, context,
and schema attack suites.
"""

from typing import Dict, List
from app.core.logging import logger
from app.validation.security.attack_cases import AttackCase, AttackRepository, AttackResult
from app.validation.security.context_attacks import ContextAttackTester
from app.validation.security.encoding_attacks import EncodingAttackTester
from app.validation.security.prompt_injection import PromptInjectionTester
from app.validation.security.schema_attacks import SchemaAttackTester
from app.validation.security.unicode_attacks import UnicodeAttackTester


class SecurityAttackRunner:
    """Runner executing adversarial security test suites."""

    @classmethod
    def run_all_attacks(cls) -> List[AttackResult]:
        """
        Executes complete security attack benchmark suite.
        """
        attack_cases = AttackRepository.get_attack_cases()
        results: List[AttackResult] = []

        logger.info(f"Starting Security Attack Benchmark: Total Cases={len(attack_cases)}")

        for case in attack_cases:
            if case.category == "prompt_injection":
                res = PromptInjectionTester.test_injection(case)
            elif case.category == "unicode":
                res = UnicodeAttackTester.test_unicode(case)
            elif case.category == "encoding":
                res = EncodingAttackTester.test_encoding(case)
            elif case.category == "context":
                res = ContextAttackTester.test_context(case)
            elif case.category == "schema":
                res = SchemaAttackTester.test_schema(case)
            else:
                res = PromptInjectionTester.test_injection(case)

            results.append(res)

        passed_count = sum(1 for r in results if r.passed)
        success_rate = (passed_count / len(results)) * 100.0 if results else 100.0

        logger.info(f"Completed Security Benchmark: Passed={passed_count}/{len(results)} ({success_rate:.1f}%)")

        return results
