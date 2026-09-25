"""
Enterprise Knowledge Fabric, Memory Intelligence & Retrieval Platform (EKF-MIRP) - Lifecycle Manager.
Implements the formal 9-state finite state machine governing knowledge objects from ingestion to archival.
"""

from __future__ import annotations

from datetime import datetime, timezone
import logging
from typing import Any, Callable, Dict, List, Optional, Set
from pydantic import BaseModel, Field

from app.knowledge.core.exceptions import InvalidKnowledgeStateError
from app.knowledge.core.models import KnowledgeLifecycleState, KnowledgeObject

logger = logging.getLogger(__name__)


class KnowledgeLifecycleEvent(BaseModel):
    """Immutable audit record emitted during a knowledge object lifecycle state transition."""
    event_id: str
    knowledge_id: str
    from_state: KnowledgeLifecycleState
    to_state: KnowledgeLifecycleState
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    reason: str = ""
    triggered_by: str = "system"
    metadata: Dict[str, Any] = Field(default_factory=dict)


class KnowledgeLifecycleManager:
    """
    Manages and validates state transitions for knowledge objects, maintaining an immutable audit history.
    """

    VALID_TRANSITIONS: Dict[KnowledgeLifecycleState, Set[KnowledgeLifecycleState]] = {
        KnowledgeLifecycleState.CREATED: {
            KnowledgeLifecycleState.INGESTED,
            KnowledgeLifecycleState.ARCHIVED,
        },
        KnowledgeLifecycleState.INGESTED: {
            KnowledgeLifecycleState.VALIDATED,
            KnowledgeLifecycleState.ARCHIVED,
        },
        KnowledgeLifecycleState.VALIDATED: {
            KnowledgeLifecycleState.CLASSIFIED,
            KnowledgeLifecycleState.ARCHIVED,
        },
        KnowledgeLifecycleState.CLASSIFIED: {
            KnowledgeLifecycleState.INDEXED,
            KnowledgeLifecycleState.ARCHIVED,
        },
        KnowledgeLifecycleState.INDEXED: {
            KnowledgeLifecycleState.PUBLISHED,
            KnowledgeLifecycleState.ACTIVE,
            KnowledgeLifecycleState.ARCHIVED,
        },
        KnowledgeLifecycleState.PUBLISHED: {
            KnowledgeLifecycleState.ACTIVE,
            KnowledgeLifecycleState.ARCHIVED,
        },
        KnowledgeLifecycleState.ACTIVE: {
            KnowledgeLifecycleState.INDEXED,  # Re-indexing on update
            KnowledgeLifecycleState.SUPERSEDED,
            KnowledgeLifecycleState.ARCHIVED,
        },
        KnowledgeLifecycleState.SUPERSEDED: {
            KnowledgeLifecycleState.ACTIVE,   # Rollback
            KnowledgeLifecycleState.ARCHIVED,
        },
        KnowledgeLifecycleState.ARCHIVED: {
            KnowledgeLifecycleState.ACTIVE,   # Restoration
            KnowledgeLifecycleState.CREATED,
        },
    }

    def __init__(self, event_listener: Optional[Callable[[KnowledgeLifecycleEvent], None]] = None):
        self._history: Dict[str, List[KnowledgeLifecycleEvent]] = {}
        self._listener = event_listener
        self._metrics: Dict[str, int] = {status.value: 0 for status in KnowledgeLifecycleState}

    def can_transition(self, from_state: KnowledgeLifecycleState | str, to_state: KnowledgeLifecycleState | str) -> bool:
        """Checks if a transition between two lifecycle states is valid."""
        f_state = from_state if isinstance(from_state, KnowledgeLifecycleState) else KnowledgeLifecycleState(from_state)
        t_state = to_state if isinstance(to_state, KnowledgeLifecycleState) else KnowledgeLifecycleState(to_state)
        return t_state in self.VALID_TRANSITIONS.get(f_state, set())

    def transition(
        self,
        knowledge_object: KnowledgeObject,
        target_state: KnowledgeLifecycleState | str,
        reason: str = "",
        triggered_by: str = "system",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> KnowledgeLifecycleEvent:
        """
        Executes a validated state transition on a KnowledgeObject, updates timestamps,
        appends to audit history, and emits lifecycle notifications.
        """
        current_state = knowledge_object.status if isinstance(knowledge_object.status, KnowledgeLifecycleState) else KnowledgeLifecycleState(knowledge_object.status)
        to_state = target_state if isinstance(target_state, KnowledgeLifecycleState) else KnowledgeLifecycleState(target_state)

        if not self.can_transition(current_state, to_state):
            msg = f"Illegal transition for knowledge object '{knowledge_object.id}' from {current_state.value} to {to_state.value}"
            logger.error(msg)
            raise InvalidKnowledgeStateError(msg, knowledge_id=knowledge_object.id)

        import uuid
        event = KnowledgeLifecycleEvent(
            event_id=f"klevt-{uuid.uuid4().hex[:10]}",
            knowledge_id=knowledge_object.id,
            from_state=current_state,
            to_state=to_state,
            reason=reason,
            triggered_by=triggered_by,
            metadata=metadata or {},
        )

        knowledge_object.status = to_state
        knowledge_object.updated_at = datetime.now(timezone.utc)

        if knowledge_object.id not in self._history:
            self._history[knowledge_object.id] = []
        self._history[knowledge_object.id].append(event)

        self._metrics[to_state.value] = self._metrics.get(to_state.value, 0) + 1

        if self._listener:
            try:
                self._listener(event)
            except Exception as e:
                logger.warning(f"Error in knowledge lifecycle listener: {e}")

        logger.info(f"Knowledge object '{knowledge_object.id}' transitioned {current_state.value} -> {to_state.value}: {reason}")
        return event

    def get_history(self, knowledge_id: str) -> List[KnowledgeLifecycleEvent]:
        """Returns the full transition audit trail for a knowledge object."""
        return self._history.get(knowledge_id, [])

    def get_metrics(self) -> Dict[str, int]:
        """Returns transition counts aggregated by lifecycle state."""
        return dict(self._metrics)
