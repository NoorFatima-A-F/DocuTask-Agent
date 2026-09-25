"""
Structured Contextual Agent Logging Hook.
Injects execution_id, request_id, document_id, state, duration, agent_name, and correlation_id.
"""

from typing import Any, Dict
from app.core.logging import logger
from app.agents.context import AgentContext
from app.agents.state import AgentState


class AgentLogger:
    """Structured logger wrapper for contextual agent logging."""

    def __init__(self, agent_name: str = "DocumentAgent"):
        self.agent_name = agent_name

    def log(
        self,
        level: str,
        message: str,
        context: AgentContext,
        state: AgentState | None = None,
        duration_ms: float | None = None,
        extra: Dict[str, Any] | None = None
    ) -> None:
        """Emits structured log message with context attributes."""
        payload = {
            "agent_name": self.agent_name,
            "execution_id": str(context.metadata.execution_id),
            "request_id": context.metadata.request_id,
            "correlation_id": context.metadata.correlation_id,
            "document_id": str(context.document_id),
            "state": state.value if state else "N/A",
            "duration_ms": duration_ms,
            "details": extra or {}
        }
        log_msg = f"[{self.agent_name}] [{payload['state']}] {message} | ExecID={payload['execution_id']} | DocID={payload['document_id']}"

        log_func = getattr(logger, level.lower(), logger.info)
        log_func(log_msg)
