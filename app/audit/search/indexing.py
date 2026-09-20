"""Audit Inverted Index for Full-Text Search."""

import re
from typing import Dict, Set, List
from ..core.events import AuditEvent


class AuditInvertedIndex:
    """Inverted token index providing fast keyword lookups over audit events."""

    def __init__(self):
        # term -> set of event_ids
        self._index: Dict[str, Set[str]] = {}

    def _tokenize(self, text: str) -> List[str]:
        if not text:
            return []
        tokens = re.findall(r"\b\w{2,}\b", text.lower())
        return tokens

    def index_event(self, event: AuditEvent) -> None:
        fields_to_index = [
            event.event_type,
            event.action,
            event.resource_type,
            event.resource_id,
            event.resource_name or "",
            event.actor_id,
            event.actor_name or "",
            event.payload_summary or "",
            str(event.metadata),
        ]
        combined = " ".join(fields_to_index)
        tokens = self._tokenize(combined)

        for token in tokens:
            if token not in self._index:
                self._index[token] = set()
            self._index[token].add(event.event_id)

    def search_terms(self, query: str) -> Set[str]:
        tokens = self._tokenize(query)
        if not tokens:
            return set()

        matching_event_ids: Set[str] = set()
        first = True
        for token in tokens:
            ids = self._index.get(token, set())
            if first:
                matching_event_ids = set(ids)
                first = False
            else:
                matching_event_ids.intersection_update(ids)

        return matching_event_ids
