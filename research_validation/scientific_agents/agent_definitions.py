"""
Scientific Agent Definitions (Phase 94C)
========================================
Defines the 10 specialized autonomous scientific agents and their domain responsibilities.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict


class ScientificAgentRole(str, Enum):
    PLANNER = "PLANNER_AGENT"
    EVIDENCE = "EVIDENCE_AGENT"
    BENCHMARK = "BENCHMARK_AGENT"
    STATISTICS = "STATISTICS_AGENT"
    PUBLICATION = "PUBLICATION_AGENT"
    REVIEWER = "REVIEWER_AGENT"
    GOVERNANCE = "GOVERNANCE_AGENT"
    MEMORY = "MEMORY_AGENT"
    REFLECTION = "REFLECTION_AGENT"
    COORDINATOR = "COORDINATOR_AGENT"


@dataclass(frozen=True)
class ScientificAgentMessage:
    """Strongly-typed message passed between autonomous scientific agents."""
    message_id: str
    sender_role: ScientificAgentRole
    recipient_role: ScientificAgentRole
    action: str
    payload: Dict[str, Any]
    timestamp_utc: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass(frozen=True)
class ScientificAgentState:
    """State record for an individual scientific agent."""
    role: ScientificAgentRole
    tasks_completed: int
    active_status: str  # "IDLE", "PROCESSING", "AWAITING_CONSENSUS"
    last_action_timestamp_utc: str
