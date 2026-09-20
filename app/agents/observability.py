"""
Agent Observability Hooks Interface.
Provides abstraction hooks for OpenTelemetry distributed tracing,
Google Cloud Logging, and Cloud Monitoring integration.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict
from app.agents.context import AgentContext
from app.agents.events import AgentEvent


class AgentObservabilityHook(ABC):
    """Abstract observability hook for tracing, logging, and APM platforms."""

    @abstractmethod
    def start_span(self, span_name: str, context: AgentContext) -> Any:
        """Starts a distributed tracing span."""
        pass

    @abstractmethod
    def end_span(self, span: Any, status_code: str = "OK") -> None:
        """Ends a distributed tracing span."""
        pass

    @abstractmethod
    def record_event(self, event: AgentEvent) -> None:
        """Emits an observable domain event to Cloud Logging / OpenTelemetry."""
        pass

    @abstractmethod
    def inject_context(self, carrier: Dict[str, str], context: AgentContext) -> Dict[str, str]:
        """Injects W3C trace context into HTTP or event headers."""
        pass


class NoOpAgentObservabilityHook(AgentObservabilityHook):
    """Default non-operational observability hook implementation."""

    def start_span(self, span_name: str, context: AgentContext) -> Any:
        return None

    def end_span(self, span: Any, status_code: str = "OK") -> None:
        pass

    def record_event(self, event: AgentEvent) -> None:
        pass

    def inject_context(self, carrier: Dict[str, str], context: AgentContext) -> Dict[str, str]:
        carrier["x-execution-id"] = str(context.metadata.execution_id)
        carrier["x-request-id"] = context.metadata.request_id
        carrier["x-correlation-id"] = context.metadata.correlation_id
        return carrier
