"""
Mutation Testing Harness.
Evaluates test suite robustness by verifying tests fail when code mutations are introduced.
"""
from dataclasses import dataclass
from typing import List, Callable, Any

@dataclass(frozen=True)
class MutationScoreResult:
    target_module: str
    mutations_generated: int
    mutations_killed: int
    mutations_survived: int
    mutation_score: float

    @property
    def passed_threshold(self) -> bool:
        return self.mutation_score >= 0.80

class MutationTestingHarness:
    """Executes code mutations and validates test sensitivity."""
    def evaluate_test_strength(
        self,
        target_name: str,
        test_fn: Callable[[Any], bool],
        clean_inputs: List[Any],
        mutated_inputs: List[Any]
    ) -> MutationScoreResult:
        killed = 0
        survived = 0

        for m_inp in mutated_inputs:
            # If the test function returns False or raises, mutation is caught/killed
            try:
                passed = test_fn(m_inp)
                if not passed:
                    killed += 1
                else:
                    survived += 1
            except Exception:
                killed += 1

        total = len(mutated_inputs)
        score = killed / max(1, total)

        return MutationScoreResult(
            target_module=target_name,
            mutations_generated=total,
            mutations_killed=killed,
            mutations_survived=survived,
            mutation_score=score
        )
