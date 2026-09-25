"""
DocuTask Agent - Causation DAG Builder & Trace Engine
Phase 13.1: Autonomous Runtime Observability & Domain Event Platform (ARODP)
"""

from typing import Dict, List, Any
from app.runtime.events.models.event import DomainEvent


class CausationDAGBuilder:
    """
    Builds a directed acyclic graph of event causation.
    Traces parent-child and cause-effect lineages between events.
    """

    @staticmethod
    def build_causation_tree(events: List[DomainEvent]) -> Dict[str, Any]:
        """
        Constructs a tree representation of parent-child event causation.
        """
        nodes: Dict[str, Dict[str, Any]] = {}
        roots: List[Dict[str, Any]] = []

        for e in events:
            node = {
                "event_id": e.event_id,
                "event_type": e.event_type.value if hasattr(e.event_type, "value") else str(e.event_type),
                "subsystem": e.subsystem.value if hasattr(e.subsystem, "value") else str(e.subsystem),
                "timestamp_utc": e.timestamp_utc,
                "actor": e.actor.actor_id,
                "parent_id": e.parent_event_id,
                "causation_id": e.causation_id,
                "children": [],
            }
            nodes[e.event_id] = node

        # Link parent -> child
        for node in nodes.values():
            parent_id = node["parent_id"]
            if parent_id and parent_id in nodes:
                nodes[parent_id]["children"].append(node)
            else:
                roots.append(node)

        return {
            "total_nodes": len(nodes),
            "root_events_count": len(roots),
            "tree": roots,
        }
