"""
Phase 13.19: Enterprise Business Goal & OKR Manager.
Translates enterprise goals into executable process workflows and tracks quantitative Key Results (KRs).
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
from app.runtime.business.models.schemas import (
    BusinessGoal,
    OKRKeyResult,
    GoalStatus,
)


class BusinessGoalManager:
    def __init__(self):
        self._goals: Dict[str, BusinessGoal] = {}
        self._seed_default_goals()

    def _seed_default_goals(self) -> None:
        """Seeds enterprise OKRs."""
        goal1 = BusinessGoal(
            goal_id="goal_invoice_velocity",
            title="Accelerate Global Invoice Turnaround by 50%",
            category="EFFICIENCY",
            target_department="dept_finance",
            status=GoalStatus.IN_PROGRESS,
            progress_pct=68.5,
            key_results=[
                OKRKeyResult(
                    kr_id="kr_cycle_time",
                    description="Reduce end-to-end invoice cycle time from 4 days to < 4 hours",
                    target_value=4.0,
                    current_value=1.8,
                    unit="hours",
                    achieved=True,
                ),
                OKRKeyResult(
                    kr_id="kr_straight_through",
                    description="Achieve 85% Straight-Through-Processing (STP) rate",
                    target_value=85.0,
                    current_value=78.2,
                    unit="%",
                    achieved=False,
                ),
            ],
            aligned_process_ids=["proc_invoice_enterprise_01"],
        )

        goal2 = BusinessGoal(
            goal_id="goal_cost_reduction",
            title="Reduce Processing Cost Per Invoice to under $1.50",
            category="EFFICIENCY",
            target_department="dept_finance",
            status=GoalStatus.IN_PROGRESS,
            progress_pct=82.0,
            key_results=[
                OKRKeyResult(
                    kr_id="kr_unit_cost",
                    description="Lower cost per invoice transaction",
                    target_value=1.50,
                    current_value=1.35,
                    unit="USD",
                    achieved=True,
                ),
            ],
            aligned_process_ids=["proc_invoice_enterprise_01"],
        )

        self._goals[goal1.goal_id] = goal1
        self._goals[goal2.goal_id] = goal2

    def create_goal(self, goal: BusinessGoal) -> BusinessGoal:
        goal.created_at = datetime.now(timezone.utc).isoformat()
        self._goals[goal.goal_id] = goal
        return goal

    def get_goal(self, goal_id: str) -> Optional[BusinessGoal]:
        return self._goals.get(goal_id)

    def list_goals(self, department: Optional[str] = None) -> List[BusinessGoal]:
        if department:
            return [g for g in self._goals.values() if g.target_department == department]
        return list(self._goals.values())

    def update_goal_progress(self, goal_id: str, new_progress_pct: float) -> BusinessGoal:
        goal = self._goals.get(goal_id)
        if not goal:
            raise ValueError(f"Goal {goal_id} not found")
        goal.progress_pct = max(0.0, min(100.0, new_progress_pct))
        if goal.progress_pct >= 100.0:
            goal.status = GoalStatus.ACHIEVED
        return goal

    def decompose_goal_to_action_plan(self, goal_id: str) -> Dict[str, Any]:
        """Performs HTN decomposition from high-level goal to recommended workflow actions."""
        goal = self._goals.get(goal_id)
        if not goal:
            raise ValueError(f"Goal {goal_id} not found")

        return {
            "goal_id": goal_id,
            "goal_title": goal.title,
            "recommended_actions": [
                {
                    "action_id": "act_parallelize_ocr_tax",
                    "type": "WORKFLOW_MODIFICATION",
                    "description": "Execute OCR extraction and vendor master lookup in parallel",
                    "estimated_impact": "+18% throughput",
                },
                {
                    "action_id": "act_raise_approval_floor",
                    "type": "POLICY_RELAXATION",
                    "description": "Increase auto-approval threshold for verified recurring vendors up to $15,000",
                    "estimated_impact": "-35% human touchpoints",
                },
            ],
        }
