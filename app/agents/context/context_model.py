"""
Agent Context Domain Model.
Provides immutable, strongly typed context objects for tracking agent execution state,
request identifiers, document references, shared variables, and execution history.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List
from uuid import UUID, uuid4


@dataclass(frozen=True)
class ExecutionMetadata:
    """Immutable execution metadata for auditing and tracing."""

    execution_id: UUID = field(default_factory=uuid4)
    request_id: str = field(default_factory=lambda: str(uuid4()))
    correlation_id: str = field(default_factory=lambda: str(uuid4()))
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class SharedVariables:
    """Thread-safe mutable dictionary for inter-component agent variables."""

    _store: Dict[str, Any] = field(default_factory=dict)

    def get(self, key: str, default: Any = None) -> Any:
        return self._store.get(key, default)

    def set(self, key: str, value: Any) -> None:
        self._store[key] = value

    def contains(self, key: str) -> bool:
        return key in self._store

    def to_dict(self) -> Dict[str, Any]:
        return dict(self._store)


@dataclass(frozen=True)
class AgentContext:
    """
    Immutable Agent Execution Context.
    Tracks document reference, user identity, execution state, and history.
    """

    document_id: UUID
    user_id: UUID
    agent_name: str = "DocumentAgent"
    metadata: ExecutionMetadata = field(default_factory=ExecutionMetadata)
    configuration: Dict[str, Any] = field(default_factory=dict)
    execution_history: List[Dict[str, Any]] = field(default_factory=list)
    variables: SharedVariables = field(default_factory=SharedVariables)

    def with_history_entry(self, stage: str, details: Dict[str, Any]) -> "AgentContext":
        """Returns a new AgentContext instance with the updated execution history entry."""
        new_history = list(self.execution_history)
        new_history.append({
            "stage": stage,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "details": details
        })
        return AgentContext(
            document_id=self.document_id,
            user_id=self.user_id,
            agent_name=self.agent_name,
            metadata=self.metadata,
            configuration=self.configuration,
            execution_history=new_history,
            variables=self.variables
        )
