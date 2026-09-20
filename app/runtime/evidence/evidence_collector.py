"""Continuous Evidence Collector.

Hooks into execution runtimes to capture planner choices, tool invocations,
memory lookups, and validation steps as immutable evidence streams.
"""

from __future__ import annotations

import collections
import threading
import time
from typing import Any, Callable, Dict, List, Optional

from app.runtime.evidence.evidence_builder import EvidenceBuilder
from app.runtime.evidence.evidence_graph import EvidenceGraph
from app.runtime.evidence.execution_evidence import EvidenceNode, EvidenceType


class EvidenceCollector:
    def __init__(self, graph: Optional[EvidenceGraph] = None):
        self.graph = graph or EvidenceGraph()
        self._lock = threading.Lock()
        self._last_evidence_hash: Optional[str] = None
        self._event_history: collections.deque = collections.deque(maxlen=1000)
        self._listeners: List[Callable[[EvidenceNode], None]] = []

    def register_listener(self, callback: Callable[[EvidenceNode], None]) -> None:
        self._listeners.append(callback)

    def record_event(
        self,
        evidence_type: EvidenceType,
        source_agent: str,
        inputs: Dict[str, Any],
        outputs: Dict[str, Any],
        metrics: Optional[Dict[str, float]] = None,
        context: Optional[Dict[str, Any]] = None,
        parent_hashes: Optional[List[str]] = None,
    ) -> EvidenceNode:
        """Constructs, seals, stores, and broadcasts an evidence node."""
        with self._lock:
            builder = EvidenceBuilder(evidence_type)
            builder.with_source(source_agent)
            builder.with_inputs(inputs)
            builder.with_outputs(outputs)
            if metrics:
                builder.with_metrics(metrics)
            if context:
                builder.with_context(context)

            # Link to specified parents or chain to the previous hash
            if parent_hashes:
                builder.with_parents(parent_hashes)
            elif self._last_evidence_hash:
                builder.with_parent(self._last_evidence_hash)

            node = builder.build_and_seal()
            self.graph.add_node(node)
            self._last_evidence_hash = node.hash_digest
            self._event_history.append(node)

        # Notify listeners
        for listener in self._listeners:
            try:
                listener(node)
            except Exception:
                pass

        return node

    def get_recent_nodes(self, limit: int = 50) -> List[EvidenceNode]:
        with self._lock:
            nodes = list(self._event_history)
            return nodes[-limit:]

    def get_by_type(self, evidence_type: EvidenceType) -> List[EvidenceNode]:
        with self._lock:
            return [n for n in self.graph.list_nodes() if n.evidence_type == evidence_type]

    def clear(self) -> None:
        with self._lock:
            self.graph = EvidenceGraph()
            self._last_evidence_hash = None
            self._event_history.clear()


# Global runtime singleton
global_evidence_collector = EvidenceCollector()
