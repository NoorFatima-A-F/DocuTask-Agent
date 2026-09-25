"""
Enterprise Integration Fabric & Universal Connector Platform (EIF-UCP) - Connector Lifecycle Manager.
Implements the formal 10-state lifecycle finite state machine for installable connectors.
"""

from __future__ import annotations

from datetime import datetime, timezone
import logging
from typing import Any, Callable, Dict, List, Optional, Set
from pydantic import BaseModel, Field

from app.connectors.core.exceptions import InvalidConnectorStateError
from app.connectors.core.models import Connector, ConnectorStatus

logger = logging.getLogger(__name__)


class ConnectorLifecycleEvent(BaseModel):
    """Immutable audit record emitted during a connector lifecycle state transition."""
    event_id: str
    connector_id: str
    from_state: ConnectorStatus
    to_state: ConnectorStatus
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    reason: str = ""
    triggered_by: str = "system"
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ConnectorLifecycleManager:
    """
    Orchestrates connector lifecycle state transitions, validates permissible edges,
    maintains an immutable audit ledger, and publishes transition events.
    """

    VALID_TRANSITIONS: Dict[ConnectorStatus, Set[ConnectorStatus]] = {
        ConnectorStatus.DISCOVERED: {
            ConnectorStatus.INSTALLED,
            ConnectorStatus.REMOVED,
        },
        ConnectorStatus.INSTALLED: {
            ConnectorStatus.CONFIGURED,
            ConnectorStatus.DISABLED,
            ConnectorStatus.REMOVED,
        },
        ConnectorStatus.CONFIGURED: {
            ConnectorStatus.AUTHENTICATED,
            ConnectorStatus.DISABLED,
            ConnectorStatus.REMOVED,
        },
        ConnectorStatus.AUTHENTICATED: {
            ConnectorStatus.VALIDATED,
            ConnectorStatus.CONFIGURED,
            ConnectorStatus.DISABLED,
            ConnectorStatus.REMOVED,
        },
        ConnectorStatus.VALIDATED: {
            ConnectorStatus.READY,
            ConnectorStatus.CONFIGURED,
            ConnectorStatus.AUTHENTICATED,
            ConnectorStatus.DISABLED,
            ConnectorStatus.REMOVED,
        },
        ConnectorStatus.READY: {
            ConnectorStatus.ACTIVE,
            ConnectorStatus.DISABLED,
            ConnectorStatus.UPDATING,
            ConnectorStatus.REMOVED,
        },
        ConnectorStatus.ACTIVE: {
            ConnectorStatus.UPDATING,
            ConnectorStatus.DISABLED,
            ConnectorStatus.READY,
            ConnectorStatus.REMOVED,
        },
        ConnectorStatus.UPDATING: {
            ConnectorStatus.VALIDATED,
            ConnectorStatus.READY,
            ConnectorStatus.ACTIVE,
            ConnectorStatus.DISABLED,
            ConnectorStatus.REMOVED,
        },
        ConnectorStatus.DISABLED: {
            ConnectorStatus.CONFIGURED,
            ConnectorStatus.AUTHENTICATED,
            ConnectorStatus.READY,
            ConnectorStatus.ACTIVE,
            ConnectorStatus.REMOVED,
        },
        ConnectorStatus.REMOVED: set(),
    }

    def __init__(self, event_listener: Optional[Callable[[ConnectorLifecycleEvent], None]] = None):
        self._history: Dict[str, List[ConnectorLifecycleEvent]] = {}
        self._listener = event_listener
        self._metrics: Dict[str, int] = {status.value: 0 for status in ConnectorStatus}

    def can_transition(self, from_state: ConnectorStatus | str, to_state: ConnectorStatus | str) -> bool:
        """Determines whether a transition between two lifecycle states is allowed."""
        f_state = from_state if isinstance(from_state, ConnectorStatus) else ConnectorStatus(from_state)
        t_state = to_state if isinstance(to_state, ConnectorStatus) else ConnectorStatus(to_state)
        return t_state in self.VALID_TRANSITIONS.get(f_state, set())

    def transition(
        self,
        connector: Connector,
        target_state: ConnectorStatus | str,
        reason: str = "",
        triggered_by: str = "system",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> ConnectorLifecycleEvent:
        """
        Executes a validated state transition, updates the connector entity,
        records an audit entry, updates metrics, and dispatches a lifecycle event.
        """
        current_state = connector.status if isinstance(connector.status, ConnectorStatus) else ConnectorStatus(connector.status)
        to_state = target_state if isinstance(target_state, ConnectorStatus) else ConnectorStatus(target_state)

        if not self.can_transition(current_state, to_state):
            msg = f"Illegal transition for connector '{connector.id}' from {current_state.value} to {to_state.value}"
            logger.error(msg)
            raise InvalidConnectorStateError(msg, connector_id=connector.id)

        import uuid
        event = ConnectorLifecycleEvent(
            event_id=f"clevt-{uuid.uuid4().hex[:10]}",
            connector_id=connector.id,
            from_state=current_state,
            to_state=to_state,
            reason=reason,
            triggered_by=triggered_by,
            metadata=metadata or {},
        )

        # Update connector state
        connector.status = to_state
        connector.updated_at = datetime.now(timezone.utc)

        # Record audit trail
        if connector.id not in self._history:
            self._history[connector.id] = []
        self._history[connector.id].append(event)

        # Update metrics
        self._metrics[to_state.value] = self._metrics.get(to_state.value, 0) + 1

        # Emit event
        if self._listener:
            try:
                self._listener(event)
            except Exception as e:
                logger.warning(f"Error in connector lifecycle listener: {e}")

        logger.info(f"Connector '{connector.id}' transitioned {current_state.value} -> {to_state.value}: {reason}")
        return event

    def get_history(self, connector_id: str) -> List[ConnectorLifecycleEvent]:
        """Retrieves the complete lifecycle audit history for a connector."""
        return self._history.get(connector_id, [])

    def get_metrics(self) -> Dict[str, int]:
        """Returns the transition counts aggregated by lifecycle state."""
        return dict(self._metrics)
