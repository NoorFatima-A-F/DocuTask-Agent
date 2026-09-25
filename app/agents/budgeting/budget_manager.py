"""
Enterprise Multi-Agent Intelligence Platform (EMAIP) - Budget Manager.
Tracks resource consumption (tokens, cost, tool calls, execution duration)
and enforces automated budget actions (Continue, Warn, Reduce Capability, Require Approval, Terminate).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, Optional
import logging

logger = logging.getLogger(__name__)


class BudgetAction(str, Enum):
    """Enforcement actions triggered by budget threshold breaches."""
    CONTINUE = "CONTINUE"
    WARN = "WARN"
    REDUCE_CAPABILITY = "REDUCE_CAPABILITY"
    REQUIRE_APPROVAL = "REQUIRE_APPROVAL"
    TERMINATE = "TERMINATE"


@dataclass
class AgentResourceUsage:
    """Tracks cumulative resource usage for an agent or execution."""
    agent_id: str
    total_tokens: int = 0
    total_cost_usd: float = 0.0
    total_execution_time_seconds: float = 0.0
    total_tool_calls: int = 0
    total_api_calls: int = 0
    last_updated: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "agent_id": self.agent_id,
            "total_tokens": self.total_tokens,
            "total_cost_usd": self.total_cost_usd,
            "total_execution_time_seconds": self.total_execution_time_seconds,
            "total_tool_calls": self.total_tool_calls,
            "total_api_calls": self.total_api_calls,
            "last_updated": self.last_updated.isoformat(),
        }


class BudgetManager:
    """
    Manages and bounds resource budgets for autonomous agents across executions.
    """

    def __init__(self):
        self._usage: Dict[str, AgentResourceUsage] = {}

    def get_or_create_usage(self, agent_id: str) -> AgentResourceUsage:
        if agent_id not in self._usage:
            self._usage[agent_id] = AgentResourceUsage(agent_id=agent_id)
        return self._usage[agent_id]

    def record_consumption(
        self,
        agent_id: str,
        tokens: int = 0,
        cost_usd: float = 0.0,
        execution_time_seconds: float = 0.0,
        tool_calls: int = 0,
        api_calls: int = 0,
    ) -> AgentResourceUsage:
        """Records incremental resource consumption."""
        u = self.get_or_create_usage(agent_id)
        u.total_tokens += tokens
        u.total_cost_usd += cost_usd
        u.total_execution_time_seconds += execution_time_seconds
        u.total_tool_calls += tool_calls
        u.total_api_calls += api_calls
        u.last_updated = datetime.now(timezone.utc)
        return u

    def evaluate_budget(
        self,
        agent_id: str,
        budget_spec: Optional[Dict[str, Any]] = None
    ) -> BudgetAction:
        """
        Evaluates current consumption against budget constraints and returns the
        mandated BudgetAction.
        """
        u = self.get_or_create_usage(agent_id)
        spec = budget_spec or {}

        max_cost = float(spec.get("max_cost_usd", 1.0))
        max_tokens = int(spec.get("max_tokens", 100000))
        max_time = float(spec.get("max_execution_time_seconds", 300))

        # Check hard termination
        if u.total_cost_usd >= max_cost or u.total_tokens >= max_tokens or u.total_execution_time_seconds >= max_time:
            logger.warning(
                f"Budget TERMINATE triggered for Agent '{agent_id}': "
                f"Cost=${u.total_cost_usd}/${max_cost}, Tokens={u.total_tokens}/{max_tokens}"
            )
            return BudgetAction.TERMINATE

        # Check approval requirement threshold (e.g. 80%)
        if u.total_cost_usd >= (max_cost * 0.8) or u.total_tokens >= (max_tokens * 0.8):
            return BudgetAction.REQUIRE_APPROVAL

        # Check warning threshold (e.g. 60%)
        if u.total_cost_usd >= (max_cost * 0.6) or u.total_tokens >= (max_tokens * 0.6):
            return BudgetAction.WARN

        return BudgetAction.CONTINUE
