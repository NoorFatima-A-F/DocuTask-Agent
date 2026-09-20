"""
Enterprise Integration Fabric & Universal Connector Platform (EIF-UCP) - Event Normalizer.
Converts heterogeneous vendor event payloads into canonical platform NormalizedEvent records.
"""

from __future__ import annotations

from datetime import datetime, timezone
import logging
from typing import Any, Callable, Dict, Optional
import uuid

from app.connectors.core.models import NormalizedEvent

logger = logging.getLogger(__name__)


class EventNormalizer:
    """
    Translates vendor-specific webhook/polling payloads into canonical platform events.
    """

    def __init__(self):
        self._custom_normalizers: Dict[str, Callable[[Dict[str, Any]], Dict[str, Any]]] = {}

    def register_normalizer(
        self,
        connector_id: str,
        normalizer_fn: Callable[[Dict[str, Any]], Dict[str, Any]],
    ) -> None:
        """Registers a custom payload translation function for a specific connector."""
        self._custom_normalizers[connector_id] = normalizer_fn

    def normalize(
        self,
        connector_id: str,
        raw_event_type: str,
        raw_payload: Dict[str, Any],
        organization_id: str = "org-default",
        workspace_id: str = "ws-default",
        correlation_id: Optional[str] = None,
    ) -> NormalizedEvent:
        """
        Transforms vendor payload into canonical NormalizedEvent structure.
        """
        # Apply custom mapper if registered
        if connector_id in self._custom_normalizers:
            try:
                normalized_payload = self._custom_normalizers[connector_id](raw_payload)
            except Exception as e:
                logger.warning(f"Error in custom normalizer for '{connector_id}': {e}")
                normalized_payload = raw_payload
        else:
            normalized_payload = raw_payload

        # Map canonical event types
        canonical_type = self._map_event_type(connector_id, raw_event_type)

        return NormalizedEvent(
            id=f"evt-{uuid.uuid4().hex[:12]}",
            type=canonical_type,
            source=f"connector.{connector_id}",
            organization=organization_id,
            workspace_id=workspace_id,
            correlation_id=correlation_id or f"corr-{uuid.uuid4().hex[:8]}",
            payload=normalized_payload,
            metadata={
                "raw_event_type": raw_event_type,
                "ingested_at": datetime.now(timezone.utc).isoformat(),
            },
        )

    def _map_event_type(self, connector_id: str, raw_type: str) -> str:
        """Heuristic event type canonicalization."""
        r = raw_type.lower()
        if "email" in r or "mail" in r:
            return "communication.email.received"
        elif "message" in r or "chat" in r:
            return "communication.message.received"
        elif "file" in r or "document" in r or "upload" in r:
            return "storage.file.uploaded"
        elif "pull_request" in r or "pr" in r:
            return "devtools.pull_request.updated"
        elif "invoice" in r or "payment" in r:
            return "finance.invoice.processed"
        elif "contact" in r or "lead" in r or "deal" in r:
            return "crm.record.updated"
        return f"{connector_id}.{raw_type}"
