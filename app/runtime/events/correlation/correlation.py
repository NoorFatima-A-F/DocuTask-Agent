"""
DocuTask Agent - Distributed Correlation Tracker
Phase 13.1: Autonomous Runtime Observability & Domain Event Platform (ARODP)
"""

from typing import Dict, List, Any, Optional
from app.runtime.events.models.event import DomainEvent


class CorrelationTracker:
    """
    Tracks distributed correlation chains spanning multiple micro-engines and DAG workers.
    """

    def __init__(self):
        self._chains: Dict[str, List[DomainEvent]] = {}

    def track(self, event: DomainEvent) -> None:
        """Appends an event to its distributed correlation chain."""
        corr_id = event.correlation_id
        if corr_id not in self._chains:
            self._chains[corr_id] = []
        self._chains[corr_id].append(event)

    def get_correlation_trace(self, correlation_id: str) -> List[DomainEvent]:
        """Returns ordered sequence of events associated with a correlation trace."""
        return self._chains.get(correlation_id, [])

    def get_active_traces_count(self) -> int:
        return len(self._chains)


# Global singleton correlation tracker
correlation_tracker = CorrelationTracker()
