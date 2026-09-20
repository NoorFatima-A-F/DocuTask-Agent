"""Centralized Audit Collection Gateway."""

from typing import Dict, Any, List, Optional, Union
from ..core.events import AuditEvent
from ..storage.repository import AuditRepository
from .normalizer import EventNormalizer
from .processors import BaseAuditProcessor, EnvironmentSecurityEnricher, AIContextProcessor


class AuditCollectorGateway:
    """Centralized ingestion gateway for all platform audit events."""

    def __init__(
        self,
        repository: Optional[AuditRepository] = None,
        processors: Optional[List[BaseAuditProcessor]] = None,
    ):
        self.repository = repository or AuditRepository()
        self.processors = processors or [
            EnvironmentSecurityEnricher(),
            AIContextProcessor(),
        ]
        self.normalizer = EventNormalizer()

    def record(
        self,
        event_or_dict: Optional[Union[AuditEvent, Dict[str, Any]]] = None,
        **kwargs,
    ) -> AuditEvent:
        """
        Records an audit event into the immutable repository after normalization and enrichment.
        Supports passing an AuditEvent, a dict, or keyword arguments.
        """
        payload: Dict[str, Any] = {}
        if isinstance(event_or_dict, AuditEvent):
            event = event_or_dict
        elif isinstance(event_or_dict, dict):
            payload = dict(event_or_dict)
            payload.update(kwargs)
            event = self.normalizer.normalize(payload)
        else:
            payload = dict(kwargs)
            event = self.normalizer.normalize(payload)

        # Run processors in sequence
        for processor in self.processors:
            event = processor.process(event)

        # Append to immutable repository
        return self.repository.record(event)

    def record_batch(self, events: List[Union[AuditEvent, Dict[str, Any]]]) -> List[AuditEvent]:
        recorded: List[AuditEvent] = []
        for e in events:
            rec = self.record(e)
            recorded.append(rec)
        return recorded
