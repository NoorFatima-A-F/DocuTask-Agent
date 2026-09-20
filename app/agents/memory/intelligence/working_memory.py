"""Tier 2: Working Memory (Active Context).

Maintains current goal state, plan execution pointers, active variables,
and intermediate findings assembled across workflow nodes.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class WorkingMemoryState:
    session_id: str
    goal_id: str = ""
    plan_id: str = ""
    current_task_id: str = ""
    variables: Dict[str, Any] = field(default_factory=dict)
    accumulated_findings: Dict[str, Any] = field(default_factory=dict)
    errors_encountered: List[Dict[str, Any]] = field(default_factory=list)
    last_updated: float = field(default_factory=time.time)


class WorkingMemory:
    """Active execution context for an autonomous agent session."""

    def __init__(self, session_id: str) -> None:
        self.state = WorkingMemoryState(session_id=session_id)

    def set_goal_context(self, goal_id: str, plan_id: str) -> None:
        self.state.goal_id = goal_id
        self.state.plan_id = plan_id
        self.state.last_updated = time.time()

    def set_current_task(self, task_id: str) -> None:
        self.state.current_task_id = task_id
        self.state.last_updated = time.time()

    def update_variable(self, key: str, value: Any) -> None:
        self.state.variables[key] = value
        self.state.last_updated = time.time()

    def get_variable(self, key: str, default: Any = None) -> Any:
        return self.state.variables.get(key, default)

    def record_finding(self, key: str, finding: Any) -> None:
        self.state.accumulated_findings[key] = finding
        self.state.last_updated = time.time()

    def get_findings(self) -> Dict[str, Any]:
        return dict(self.state.accumulated_findings)

    def record_error(self, task_id: str, error_message: str, details: Optional[Dict[str, Any]] = None) -> None:
        self.state.errors_encountered.append({
            "task_id": task_id,
            "error": error_message,
            "details": details or {},
            "timestamp": time.time(),
        })
        self.state.last_updated = time.time()

    def get_errors(self) -> List[Dict[str, Any]]:
        return list(self.state.errors_encountered)

    def export_snapshot(self) -> Dict[str, Any]:
        return {
            "session_id": self.state.session_id,
            "goal_id": self.state.goal_id,
            "plan_id": self.state.plan_id,
            "current_task_id": self.state.current_task_id,
            "variables": self.state.variables,
            "accumulated_findings": self.state.accumulated_findings,
            "errors_encountered": self.state.errors_encountered,
            "last_updated": self.state.last_updated,
        }
