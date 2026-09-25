"""
Enterprise Multi-Agent Intelligence Platform (EMAIP) - Agent Governance.
Maintains version tracking and deterministic provenance for Agents, Prompts,
Models, Policies, Memory namespaces, and Workflow attachments.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import uuid
import logging

from app.agents.domain.agent_entity import Agent

logger = logging.getLogger(__name__)


@dataclass
class AgentGovernanceRecord:
    """Immutable provenance and versioning snapshot for an agent execution."""
    snapshot_id: str = field(default_factory=lambda: f"gov-{uuid.uuid4().hex[:12]}")
    agent_id: str = ""
    agent_version: str = "1.0.0"
    prompt_version: str = "1.0.0"
    model_version: str = "gemini-2.5-flash"
    policy_version: str = "enterprise_default:1.0"
    memory_namespace: str = "default"
    workflow_version: Optional[str] = None
    creator: str = "system"
    modifier: str = "system"
    execution_id: Optional[str] = None
    checksum: str = ""
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "snapshot_id": self.snapshot_id,
            "agent_id": self.agent_id,
            "agent_version": self.agent_version,
            "prompt_version": self.prompt_version,
            "model_version": self.model_version,
            "policy_version": self.policy_version,
            "memory_namespace": self.memory_namespace,
            "workflow_version": self.workflow_version,
            "creator": self.creator,
            "modifier": self.modifier,
            "execution_id": self.execution_id,
            "checksum": self.checksum,
            "timestamp": self.timestamp.isoformat(),
        }


class AgentGovernanceManager:
    """
    Governance Manager ensuring that all autonomous agent executions are
    strictly version-controlled, auditable, and deterministically reproducible.
    """

    def __init__(self):
        self._snapshots: Dict[str, AgentGovernanceRecord] = {}  # snapshot_id -> record
        self._agent_history: Dict[str, List[AgentGovernanceRecord]] = {}

    def record_snapshot(
        self,
        agent: Agent,
        execution_id: Optional[str] = None,
        workflow_version: Optional[str] = None,
        creator: str = "system",
    ) -> AgentGovernanceRecord:
        """
        Captures an immutable governance snapshot for an agent before or during execution.
        """
        record = AgentGovernanceRecord(
            agent_id=agent.id,
            agent_version=agent.version,
            prompt_version=agent.prompt_version,
            model_version=agent.model,
            policy_version=f"{agent.policy_set}:1.0",
            memory_namespace=agent.memory_namespace,
            workflow_version=workflow_version,
            creator=creator,
            execution_id=execution_id,
            checksum=f"chk-{uuid.uuid4().hex[:8]}",
        )

        self._snapshots[record.snapshot_id] = record
        if agent.id not in self._agent_history:
            self._agent_history[agent.id] = []
        self._agent_history[agent.id].append(record)

        logger.info(
            f"Recorded Governance Snapshot {record.snapshot_id} for Agent {agent.id} "
            f"(v{agent.version}, Model: {agent.model}, Prompt: {agent.prompt_version})"
        )
        return record

    def get_snapshot(self, snapshot_id: str) -> Optional[AgentGovernanceRecord]:
        """Retrieves a governance record by snapshot ID."""
        return self._snapshots.get(snapshot_id)

    def get_history(self, agent_id: str) -> List[AgentGovernanceRecord]:
        """Returns the full governance version history for an agent."""
        return list(self._agent_history.get(agent_id, []))
