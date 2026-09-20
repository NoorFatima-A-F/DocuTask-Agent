"""
Branching Planner Subsystem.
Plans conditional, retry, and rollback branches for generated plans.
"""

from typing import List
from app.agents.planning.branching import BranchCondition, ConditionalBranch


class BranchPlanner:
    """Plans decision and error-recovery branching structures."""

    def plan_branches(self) -> List[ConditionalBranch]:
        return [
            ConditionalBranch(
                branch_id="br_confidence_check",
                condition=BranchCondition(condition_id="c_conf", expression="confidence >= 0.85"),
                target_node_id="t3_validate",
                fallback_node_id="t1_ocr"
            )
        ]
