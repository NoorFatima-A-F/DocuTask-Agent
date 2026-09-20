"""
Correlation & Causation Manager.
"""

from typing import Optional
from app.agents.messaging.metadata import CorrelationContext


class CorrelationManager:
    """Correlation context manager for tracing causation across multi-agent workflows."""

    @staticmethod
    def create_child_context(parent: CorrelationContext, new_causation_id: str) -> CorrelationContext:
        """Creates child correlation context with updated causation ID."""
        return CorrelationContext(
            correlation_id=parent.correlation_id,
            causation_id=new_causation_id,
            conversation_id=parent.conversation_id,
            workflow_id=parent.workflow_id,
            execution_id=parent.execution_id,
            session_id=parent.session_id,
            tenant_id=parent.tenant_id
        )
