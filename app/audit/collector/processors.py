"""Audit Event Enrichment Processors."""

from abc import ABC, abstractmethod
from ..core.events import AuditEvent


class BaseAuditProcessor(ABC):
    @abstractmethod
    def process(self, event: AuditEvent) -> AuditEvent:
        pass


class EnvironmentSecurityEnricher(BaseAuditProcessor):
    """Enriches audit events with host, runtime, and security posture metadata."""

    def __init__(self, default_environment: str = "production"):
        self.default_environment = default_environment

    def process(self, event: AuditEvent) -> AuditEvent:
        if not event.environment:
            event.environment = self.default_environment
        
        # Add basic runtime tag if missing
        if "collector_version" not in event.metadata:
            event.metadata["collector_version"] = "8G.1.0"
        return event


class AIContextProcessor(BaseAuditProcessor):
    """Ensures AI-specific events contain model, prompt, or grounding tags."""

    def process(self, event: AuditEvent) -> AuditEvent:
        if event.category.value == "AI" or "ai" in event.event_type.lower():
            if "ai_trace_enabled" not in event.metadata:
                event.metadata["ai_trace_enabled"] = True
        return event
