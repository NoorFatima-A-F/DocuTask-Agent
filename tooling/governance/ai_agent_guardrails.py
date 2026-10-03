import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from dataclasses import dataclass
from typing import List
from tooling.governance.shared_kernel_validator import validate_shared_kernel
from tooling.governance.naming_standards_validator import validate_naming

@dataclass(frozen=True)
class GuardrailValidationResult:
    passed: bool
    violations: List[str]
    compliance_score: float

class AiAgentGuardrails:
    @staticmethod
    def run_all_guardrails(base_dir: str = ".") -> GuardrailValidationResult:
        violations = []
        naming_errs = validate_naming(base_dir)
        violations.extend(naming_errs)

        sk_exit = validate_shared_kernel()
        if sk_exit != 0:
            violations.append("Shared Kernel invariant validation failed")

        passed = len(violations) == 0
        score = 1.0 if passed else max(0.0, 1.0 - (len(violations) * 0.2))

        return GuardrailValidationResult(
            passed=passed,
            violations=violations,
            compliance_score=score
        )

if __name__ == "__main__":
    res = AiAgentGuardrails.run_all_guardrails()
    print(f"AI Guardrails check: Passed={res.passed}, Score={res.compliance_score * 100:.1f}%")
