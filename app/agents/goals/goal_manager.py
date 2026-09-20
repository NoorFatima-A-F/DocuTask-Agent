"""
Enterprise Multi-Agent Intelligence Platform (EMAIP) - Goal Management System.
Implements hierarchical goal creation, subgoal tree linking, constraint validation,
and goal status tracking.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import uuid
import logging

from app.agents.domain.agent_entity import GoalModel

logger = logging.getLogger(__name__)


class GoalNotFoundError(Exception):
    """Raised when a goal ID cannot be resolved."""
    pass


class GoalManager:
    """
    Manages high-level enterprise business goals, decomposing them into
    subgoals, tasks, actions, and measurable success criteria.
    """

    def __init__(self):
        self._goals: Dict[str, GoalModel] = {}
        self._subgoal_tree: Dict[str, List[str]] = {}  # parent_id -> list of child_ids
        self._parent_map: Dict[str, str] = {}          # child_id -> parent_id

    def create_goal(
        self,
        description: str,
        priority: str = "HIGH",
        deadline: Optional[datetime] = None,
        constraints: Optional[List[str]] = None,
        budget: Optional[Dict[str, Any]] = None,
        success_conditions: Optional[List[str]] = None,
        failure_conditions: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        goal_id: Optional[str] = None,
    ) -> GoalModel:
        """Creates and registers a top-level enterprise goal."""
        gid = goal_id or f"goal-{uuid.uuid4().hex[:12]}"
        goal = GoalModel(
            id=gid,
            description=description,
            priority=priority,
            deadline=deadline,
            constraints=constraints or [],
            budget=budget or {"max_cost_usd": 1.0, "max_time_seconds": 300},
            success_conditions=success_conditions or [],
            failure_conditions=failure_conditions or [],
            status="CREATED",
            metadata=metadata or {},
            created_at=datetime.now(timezone.utc),
        )
        self._goals[gid] = goal
        self._subgoal_tree[gid] = []
        logger.info(f"Created Goal: {gid} - '{description}' [Priority: {priority}]")
        return goal

    def add_subgoal(
        self,
        parent_goal_id: str,
        description: str,
        priority: Optional[str] = None,
        constraints: Optional[List[str]] = None,
        budget: Optional[Dict[str, Any]] = None,
        success_conditions: Optional[List[str]] = None,
    ) -> GoalModel:
        """Attaches a child subgoal to an existing parent goal."""
        parent = self._goals.get(parent_goal_id)
        if not parent:
            raise GoalNotFoundError(f"Parent goal {parent_goal_id} not found.")

        subgoal = self.create_goal(
            description=description,
            priority=priority or parent.priority,
            constraints=constraints or list(parent.constraints),
            budget=budget or dict(parent.budget),
            success_conditions=success_conditions or [],
        )

        parent.subgoals.append(subgoal.id)
        self._subgoal_tree[parent_goal_id].append(subgoal.id)
        self._parent_map[subgoal.id] = parent_goal_id

        logger.info(f"Attached Subgoal {subgoal.id} to Parent {parent_goal_id}")
        return subgoal

    def get_goal(self, goal_id: str) -> Optional[GoalModel]:
        """Retrieves a goal by its ID."""
        return self._goals.get(goal_id)

    def get_hierarchy(self, goal_id: str) -> Dict[str, Any]:
        """Returns the full hierarchical tree representation of a goal and its subgoals."""
        root = self._goals.get(goal_id)
        if not root:
            raise GoalNotFoundError(f"Goal {goal_id} not found.")

        def build_tree(gid: str) -> Dict[str, Any]:
            g = self._goals[gid]
            children = [build_tree(cid) for cid in self._subgoal_tree.get(gid, []) if cid in self._goals]
            return {
                "goal": g.to_dict(),
                "children": children,
            }

        return build_tree(goal_id)

    def update_status(self, goal_id: str, status: str) -> GoalModel:
        """Updates the operational status of a goal."""
        goal = self._goals.get(goal_id)
        if not goal:
            raise GoalNotFoundError(f"Goal {goal_id} not found.")
        goal.status = status
        return goal

    def list_goals(self, status: Optional[str] = None) -> List[GoalModel]:
        """Lists all goals, optionally filtered by status."""
        if status:
            return [g for g in self._goals.values() if g.status == status]
        return list(self._goals.values())
