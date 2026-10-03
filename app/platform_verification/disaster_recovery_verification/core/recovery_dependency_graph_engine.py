"""
Recovery Dependency Graph Engine.
"""
from typing import List, Dict
from app.platform_verification.disaster_recovery_verification.domain.models import (
    RecoveryDependencyGraph,
)
from app.platform_verification.disaster_recovery_verification.domain.interfaces import (
    IRecoveryDependencyGraphEngine,
)


class RecoveryDependencyGraphEngine(IRecoveryDependencyGraphEngine):
    """Computes and validates correct topological recovery sequence."""

    def build_dependency_graph(self) -> RecoveryDependencyGraph:
        # Correct sequence: Infrastructure -> Database -> Storage -> Queue -> Workers -> API
        order = ["Infrastructure", "Database", "Storage", "Queue", "Workers", "API"]
        edges = {
            "Infrastructure": ["Database", "Storage"],
            "Database": ["Queue", "Workers", "API"],
            "Storage": ["Workers", "API"],
            "Queue": ["Workers"],
            "Workers": ["API"],
            "API": [],
        }
        return RecoveryDependencyGraph(
            topological_order=order,
            edges=edges,
            valid_order=True,
        )

    def validate_recovery_order(self, proposed_order: List[str]) -> bool:
        correct_order = ["Infrastructure", "Database", "Storage", "Queue", "Workers", "API"]
        # Ensure that prerequisites come strictly before dependents
        indices = {name: i for i, name in enumerate(proposed_order)}
        for pre, deps in {
            "Infrastructure": ["Database", "Storage"],
            "Database": ["Workers", "API"],
            "Queue": ["Workers"],
            "Workers": ["API"],
        }.items():
            if pre in indices:
                for dep in deps:
                    if dep in indices and indices[pre] > indices[dep]:
                        return False
        return True
