"""
Parallel Workflow Engine.
Executes concurrent workflow branches and coordinates barrier join synchronization.
"""

from typing import Any, Dict, List
from uuid import UUID
from pydantic import BaseModel, Field


class ParallelBranchResult(BaseModel):
    branch_id: str
    outputs: Dict[str, Any] = Field(default_factory=dict)
    success: bool = True

    model_config = {"frozen": True}


class ParallelWorkflowEngine:
    """Manages parallel branch splits and synchronization joins."""

    def evaluate_join(self, branch_results: List[ParallelBranchResult]) -> Dict[str, Any]:
        """Merges concurrent branch outputs and verifies all completed successfully."""
        merged: Dict[str, Any] = {}
        all_ok = True

        for b in branch_results:
            merged.update(b.outputs)
            if not b.success:
                all_ok = False

        return {
            "all_branches_successful": all_ok,
            "merged_outputs": merged,
            "total_branches": len(branch_results)
        }
