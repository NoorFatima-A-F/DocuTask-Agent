"""
Task Execution and Mutation History for Persistent Task Graph Intelligence.
Maintains granular audit records of execution attempts, runtime mutations, and failure roots.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4


@dataclass
class TaskExecutionRecord:
    """Execution metrics for an individual task execution pass."""

    record_id: UUID = field(default_factory=uuid4)
    task_id: str = ""
    attempt: int = 1
    agent_id: str = ""
    tools_used: List[str] = field(default_factory=list)
    started_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    completed_at: Optional[datetime] = None
    duration_ms: float = 0.0
    success: bool = False
    error_message: str = ""
    output_summary: str = ""


@dataclass
class MutationRecord:
    """Detailed record of an in-flight DAG modification."""

    mutation_id: UUID = field(default_factory=uuid4)
    plan_id: str = ""
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    mutation_type: str = ""
    trigger_reason: str = ""
    target_node_id: str = ""
    inserted_node_ids: List[str] = field(default_factory=list)
    replaced_node_ids: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


class TaskExecutionHistory:
    """Chronological ledger of task attempts and graph topology mutations."""

    def __init__(self, plan_id: str = "") -> None:
        self.plan_id = plan_id
        self._execution_records: List[TaskExecutionRecord] = []
        self._mutation_records: List[MutationRecord] = []

    def record_attempt(
        self,
        task_id: str,
        attempt: int,
        agent_id: str,
        tools_used: List[str],
        duration_ms: float,
        success: bool,
        error_message: str = "",
        output_summary: str = "",
    ) -> TaskExecutionRecord:
        rec = TaskExecutionRecord(
            task_id=task_id,
            attempt=attempt,
            agent_id=agent_id,
            tools_used=tools_used,
            duration_ms=duration_ms,
            success=success,
            error_message=error_message,
            output_summary=output_summary,
            completed_at=datetime.now(timezone.utc),
        )
        self._execution_records.append(rec)
        return rec

    def record_mutation(
        self,
        mutation_type: str,
        trigger_reason: str,
        target_node_id: str = "",
        inserted_node_ids: Optional[List[str]] = None,
        replaced_node_ids: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> MutationRecord:
        mut = MutationRecord(
            plan_id=self.plan_id,
            mutation_type=mutation_type,
            trigger_reason=trigger_reason,
            target_node_id=target_node_id,
            inserted_node_ids=inserted_node_ids or [],
            replaced_node_ids=replaced_node_ids or [],
            metadata=metadata or {},
        )
        self._mutation_records.append(mut)
        return mut

    def get_task_attempts(self, task_id: str) -> List[TaskExecutionRecord]:
        return [r for r in self._execution_records if r.task_id == task_id]

    def get_all_records(self) -> List[TaskExecutionRecord]:
        return list(self._execution_records)

    def get_all_mutations(self) -> List[MutationRecord]:
        return list(self._mutation_records)
