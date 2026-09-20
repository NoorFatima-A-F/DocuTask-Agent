"""
AWM-PSDTIP Phase 13.10 - Temporal Knowledge Graph
Time-aware knowledge graph supporting historical traversal, evolutionary state transitions, and projected future branches.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
import hashlib
from typing import Any, Dict, List, Optional
import uuid


@dataclass
class TemporalGraphNode:
    node_id: str
    label: str
    entity_type: str  # 'MISSION_STATE', 'POLICY_VERSION', 'SWARM_TOPOLOGY', 'PREDICTED_FUTURE'
    valid_from: str
    valid_to: Optional[str] = None
    properties: Dict[str, Any] = field(default_factory=dict)
    is_projected_future: bool = False


@dataclass
class TemporalGraphEdge:
    edge_id: str
    source_id: str
    target_id: str
    relation: str  # 'TRANSITIONED_TO', 'BRANCHED_INTO', 'PREDICTS', 'DERIVED_FROM'
    valid_at: str
    weight: float = 1.0


class TemporalKnowledgeGraph:
    """
    Maintains a 4D spatio-temporal graph linking past, present, and predicted future states.
    """

    def __init__(self):
        self._nodes: Dict[str, TemporalGraphNode] = {}
        self._edges: Dict[str, TemporalGraphEdge] = {}
        self._seed_default_temporal_graph()

    def add_node(
        self,
        label: str,
        entity_type: str,
        valid_from: Optional[str] = None,
        valid_to: Optional[str] = None,
        properties: Optional[Dict[str, Any]] = None,
        is_projected_future: bool = False,
    ) -> TemporalGraphNode:
        nid = f"tnode-{uuid.uuid4().hex[:8]}"
        now = datetime.now(timezone.utc).isoformat()
        node = TemporalGraphNode(
            node_id=nid,
            label=label,
            entity_type=entity_type,
            valid_from=valid_from or now,
            valid_to=valid_to,
            properties=properties or {},
            is_projected_future=is_projected_future,
        )
        self._nodes[nid] = node
        return node

    def add_edge(
        self,
        source_id: str,
        target_id: str,
        relation: str,
        valid_at: Optional[str] = None,
        weight: float = 1.0,
    ) -> TemporalGraphEdge:
        eid = f"tedge-{uuid.uuid4().hex[:8]}"
        edge = TemporalGraphEdge(
            edge_id=eid,
            source_id=source_id,
            target_id=target_id,
            relation=relation,
            valid_at=valid_at or datetime.now(timezone.utc).isoformat(),
            weight=weight,
        )
        self._edges[eid] = edge
        return edge

    def query_state_at_time(self, timestamp_iso: str) -> List[TemporalGraphNode]:
        res = []
        for n in self._nodes.values():
            if n.valid_from <= timestamp_iso:
                if n.valid_to is None or n.valid_to >= timestamp_iso:
                    res.append(n)
        return res

    def get_future_projections(self) -> List[TemporalGraphNode]:
        return [n for n in self._nodes.values() if n.is_projected_future]

    def get_summary(self) -> Dict[str, Any]:
        return {
            "total_nodes": len(self._nodes),
            "total_edges": len(self._edges),
            "historical_nodes_count": len([n for n in self._nodes.values() if not n.is_projected_future]),
            "projected_nodes_count": len([n for n in self._nodes.values() if n.is_projected_future]),
            "nodes": [n.__dict__ for n in self._nodes.values()],
            "edges": [e.__dict__ for e in self._edges.values()],
        }

    def _seed_default_temporal_graph(self):
        n1 = self.add_node(
            label="Legacy Sequential APDLE DAG (T-24h)",
            entity_type="MISSION_STATE",
            valid_from="2026-09-11T00:00:00Z",
            valid_to="2026-09-12T00:00:00Z",
            properties={"mean_latency_ms": 380.0},
        )
        n2 = self.add_node(
            label="Dynamic Fan-Out DAG + Cache (Present)",
            entity_type="MISSION_STATE",
            valid_from="2026-09-12T00:00:00Z",
            properties={"mean_latency_ms": 180.0},
        )
        n3 = self.add_node(
            label="Projected Autonomous Strike Swarm (T+48h)",
            entity_type="PREDICTED_FUTURE",
            valid_from="2026-09-14T00:00:00Z",
            properties={"predicted_latency_ms": 95.0, "confidence": 0.985},
            is_projected_future=True,
        )

        self.add_edge(n1.node_id, n2.node_id, "TRANSITIONED_TO")
        self.add_edge(n2.node_id, n3.node_id, "PREDICTS")
