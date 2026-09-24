"""
Fluent Builders Suite for Recovery Subsystem.
Provides RecoveryRequestBuilder, RecoverySessionBuilder, RecoveryStrategyBuilder,
FailureBuilder, IncidentBuilder, CheckpointRestoreBuilder, and ReplayBuilder.
"""

from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4
from app.agents.recovery.context import RecoveryContext, RecoveryRequest
from app.agents.recovery.failure import (
    Failure,
    FailureCategory,
    FailureEvidence,
    FailureIdentity,
    FailureSeverity,
)
from app.agents.recovery.incident import Incident, IncidentSeverity
from app.agents.recovery.recovery_strategy import RecoveryStrategy, RecoveryStrategyDefinition
from app.agents.recovery.replay import ReplayInstruction


class FailureBuilder:
    """Fluent builder for Failure entity."""

    def __init__(self, execution_id: UUID):
        self._execution_id = execution_id
        self._node_id: Optional[str] = None
        self._tool_name: Optional[str] = None
        self._error_type = "RuntimeError"
        self._error_msg = "Task execution failed"
        self._category = FailureCategory.EXECUTION_FAILURE
        self._severity = FailureSeverity.MEDIUM

    def on_node(self, node_id: str) -> "FailureBuilder":
        self._node_id = node_id
        return self

    def with_tool(self, tool_name: str) -> "FailureBuilder":
        self._tool_name = tool_name
        return self

    def with_error(self, error_type: str, error_msg: str) -> "FailureBuilder":
        self._error_type = error_type
        self._error_msg = error_msg
        return self

    def with_category(self, category: FailureCategory) -> "FailureBuilder":
        self._category = category
        return self

    def with_severity(self, severity: FailureSeverity) -> "FailureBuilder":
        self._severity = severity
        return self

    def build(self) -> Failure:
        identity = FailureIdentity(
            execution_id=self._execution_id,
            node_id=self._node_id,
            tool_name=self._tool_name
        )
        evidence = FailureEvidence(
            error_type=self._error_type,
            error_message=self._error_msg
        )
        return Failure(
            identity=identity,
            category=self._category,
            severity=self._severity,
            evidence=evidence
        )


class RecoveryRequestBuilder:
    """Fluent builder for RecoveryRequest."""

    def __init__(self, failure: Failure):
        self._failure = failure
        self._context = RecoveryContext()

    def with_context(self, context: RecoveryContext) -> "RecoveryRequestBuilder":
        self._context = context
        return self

    def build(self) -> RecoveryRequest:
        return RecoveryRequest(failure=self._failure, context=self._context)


class RecoveryStrategyBuilder:
    """Fluent builder for RecoveryStrategyDefinition."""

    def __init__(self, strategy: RecoveryStrategy):
        self._strategy = strategy
        self._params: Dict[str, Any] = {}
        self._cost = 0.0
        self._human_gate = False

    def with_param(self, key: str, value: Any) -> "RecoveryStrategyBuilder":
        self._params[key] = value
        return self

    def with_cost(self, cost_usd: float) -> "RecoveryStrategyBuilder":
        self._cost = cost_usd
        return self

    def require_human_gate(self, required: bool = True) -> "RecoveryStrategyBuilder":
        self._human_gate = required
        return self

    def build(self) -> RecoveryStrategyDefinition:
        return RecoveryStrategyDefinition(
            strategy=self._strategy,
            parameters=self._params,
            estimated_cost_usd=self._cost,
            requires_human_gate=self._human_gate
        )


class IncidentBuilder:
    """Fluent builder for Incident."""

    def __init__(self, execution_id: UUID, failure_id: UUID, title: str):
        self._execution_id = execution_id
        self._failure_id = failure_id
        self._title = title
        self._description = ""
        self._severity = IncidentSeverity.SEV3

    def with_description(self, description: str) -> "IncidentBuilder":
        self._description = description
        return self

    def with_severity(self, severity: IncidentSeverity) -> "IncidentBuilder":
        self._severity = severity
        return self

    def build(self) -> Incident:
        return Incident(
            execution_id=self._execution_id,
            failure_id=self._failure_id,
            title=self._title,
            description=self._description,
            severity=self._severity
        )


class ReplayBuilder:
    """Fluent builder for ReplayInstruction."""

    def __init__(self, execution_id: UUID, node_ids: List[str]):
        self._execution_id = execution_id
        self._node_ids = list(node_ids)
        self._inputs: Dict[str, Any] = {}

    def with_input(self, key: str, value: Any) -> "ReplayBuilder":
        self._inputs[key] = value
        return self

    def build(self) -> ReplayInstruction:
        return ReplayInstruction(
            replay_id=f"replay_{uuid4().hex[:8]}",
            execution_id=self._execution_id,
            node_ids=self._node_ids,
            inputs=self._inputs
        )
