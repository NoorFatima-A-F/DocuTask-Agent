"""
Core World Model Engine for Phase 13.16.
Maintains multi-layer probabilistic entity graphs, dependency graphs, version checkpoints, and state snapshots.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
import hashlib
import json
import math
from typing import Any, Dict, List, Optional
import uuid

from app.runtime.world_model.events.world_model_events import (
    ModelVersion,
    WorldModelEvent,
    WorldModelEventType,
    WorldState,
    world_model_event_bus,
)


@dataclass
class WorldEntityNode:
    entity_id: str
    name: str
    category: str  # service, cluster, database, department, agent, policy, connector, resource
    properties: Dict[str, Any] = field(default_factory=dict)
    state: str = "healthy"
    health_score: float = 0.98
    uncertainty: float = 0.05
    last_updated: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "category": self.category,
            "properties": self.properties,
            "state": self.state,
            "health_score": round(self.health_score, 3),
            "uncertainty": round(self.uncertainty, 4),
            "last_updated": self.last_updated,
        }


@dataclass
class WorldGraphEdge:
    edge_id: str = field(default_factory=lambda: f"edge_{uuid.uuid4().hex[:8]}")
    source_entity_id: str = ""
    target_entity_id: str = ""
    relation_type: str = "depends_on"  # depends_on, calls, manages, scales, allocates, violates
    weight: float = 1.0  # causal/probabilistic weight
    confidence: float = 0.95
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "edge_id": self.edge_id,
            "source_entity_id": self.source_entity_id,
            "target_entity_id": self.target_entity_id,
            "relation_type": self.relation_type,
            "weight": round(self.weight, 3),
            "confidence": round(self.confidence, 4),
            "metadata": self.metadata,
        }


@dataclass
class WorldModelSnapshot:
    snapshot_id: str
    version: ModelVersion = ModelVersion.V1_1_CONTINUOUS
    state: WorldState = WorldState.STABLE
    nodes_count: int = 0
    edges_count: int = 0
    graph_entropy: float = 0.42
    state_signature_sha256: str = ""
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "snapshot_id": self.snapshot_id,
            "version": self.version.value if isinstance(self.version, ModelVersion) else str(self.version),
            "state": self.state.value if isinstance(self.state, WorldState) else str(self.state),
            "nodes_count": self.nodes_count,
            "edges_count": self.edges_count,
            "graph_entropy": round(self.graph_entropy, 4),
            "state_signature_sha256": self.state_signature_sha256,
            "timestamp": self.timestamp,
        }


class WorldEngine:
    """Core multi-layer World Model maintaining entity topologies and causal states."""

    def __init__(self):
        self._nodes: Dict[str, WorldEntityNode] = {}
        self._edges: Dict[str, WorldGraphEdge] = {}
        self._snapshots: List[WorldModelSnapshot] = []
        self._current_state: WorldState = WorldState.STABLE
        self._current_version: ModelVersion = ModelVersion.V1_1_CONTINUOUS
        self._initialize_seed_world()

    def _initialize_seed_world(self) -> None:
        seed_nodes = [
            WorldEntityNode("service_core_api", "Core API Gateway", "service", {"p99_latency": 42.4, "rps": 350}),
            WorldEntityNode("k8s_prod_cluster", "Kubernetes Prod Cluster", "cluster", {"nodes": 48, "region": "us-east-1"}),
            WorldEntityNode("postgres_warehouse", "Postgres Data Warehouse", "database", {"pool_size": 30, "db_load": 0.32}),
            WorldEntityNode("dept_engineering", "Autonomous Engineering Dept", "department", {"budget_monthly": 25000.0}),
            WorldEntityNode("agent_lead_architect", "AI Chief Architect Agent", "agent", {"capability_tier": "T3"}),
            WorldEntityNode("gateway_stripe", "Stripe Payment Gateway", "connector", {"status": "live", "rpm_limit": 150}),
            WorldEntityNode("policy_finance_cap", "Financial Invoicing Threshold Gate", "policy", {"limit_cents": 100000}),
        ]
        for n in seed_nodes:
            self._nodes[n.entity_id] = n

        seed_edges = [
            WorldGraphEdge(source_entity_id="service_core_api", target_entity_id="k8s_prod_cluster", relation_type="deployed_on", weight=0.95),
            WorldGraphEdge(source_entity_id="service_core_api", target_entity_id="postgres_warehouse", relation_type="queries", weight=0.88),
            WorldGraphEdge(source_entity_id="dept_engineering", target_entity_id="agent_lead_architect", relation_type="manages", weight=1.0),
            WorldGraphEdge(source_entity_id="service_core_api", target_entity_id="gateway_stripe", relation_type="calls", weight=0.65),
            WorldGraphEdge(source_entity_id="gateway_stripe", target_entity_id="policy_finance_cap", relation_type="governed_by", weight=1.0),
        ]
        for e in seed_edges:
            self._edges[e.edge_id] = e

        self.create_checkpoint()

    def add_node(self, node: WorldEntityNode) -> WorldEntityNode:
        self._nodes[node.entity_id] = node
        world_model_event_bus.publish(
            WorldModelEvent(
                event_type=WorldModelEventType.GRAPH_NODE_ADDED,
                source="world_engine",
                payload=node.to_dict(),
            )
        )
        return node

    def add_edge(self, edge: WorldGraphEdge) -> WorldGraphEdge:
        self._edges[edge.edge_id] = edge
        world_model_event_bus.publish(
            WorldModelEvent(
                event_type=WorldModelEventType.GRAPH_EDGE_ADDED,
                source="world_engine",
                payload=edge.to_dict(),
            )
        )
        return edge

    def get_node(self, entity_id: str) -> Optional[WorldEntityNode]:
        return self._nodes.get(entity_id)

    def list_nodes(self, category: Optional[str] = None) -> List[WorldEntityNode]:
        nodes = list(self._nodes.values())
        if category:
            nodes = [n for n in nodes if n.category.lower() == category.lower()]
        return nodes

    def list_edges(self) -> List[WorldGraphEdge]:
        return list(self._edges.values())

    def compute_graph_entropy(self) -> float:
        """Calculates degree distribution Shannon entropy: H = -sum(p_i * log2(p_i))."""
        degrees: Dict[str, int] = {nid: 0 for nid in self._nodes}
        for e in self._edges.values():
            if e.source_entity_id in degrees:
                degrees[e.source_entity_id] += 1
            if e.target_entity_id in degrees:
                degrees[e.target_entity_id] += 1

        total_deg = sum(degrees.values())
        if total_deg == 0:
            return 0.0

        entropy = 0.0
        for deg in degrees.values():
            if deg > 0:
                p = deg / total_deg
                entropy -= p * math.log2(p)
        return entropy

    def create_checkpoint(self) -> WorldModelSnapshot:
        sid = f"snap_{uuid.uuid4().hex[:10]}"
        entropy = self.compute_graph_entropy()
        
        # State signature SHA-256
        state_repr = json.dumps(
            {
                "nodes": sorted(list(self._nodes.keys())),
                "edges_count": len(self._edges),
                "entropy": round(entropy, 4),
            },
            sort_keys=True,
        )
        sig = hashlib.sha256(state_repr.encode("utf-8")).hexdigest()

        snapshot = WorldModelSnapshot(
            snapshot_id=sid,
            version=self._current_version,
            state=self._current_state,
            nodes_count=len(self._nodes),
            edges_count=len(self._edges),
            graph_entropy=entropy,
            state_signature_sha256=sig,
        )
        self._snapshots.append(snapshot)

        world_model_event_bus.publish(
            WorldModelEvent(
                event_type=WorldModelEventType.WORLD_CHECKPOINT_CREATED,
                source="world_engine",
                payload=snapshot.to_dict(),
            )
        )
        return snapshot

    def list_snapshots(self) -> List[WorldModelSnapshot]:
        return self._snapshots

    def get_world_summary(self) -> Dict[str, Any]:
        return {
            "current_state": self._current_state.value if isinstance(self._current_state, WorldState) else str(self._current_state),
            "current_version": self._current_version.value if isinstance(self._current_version, ModelVersion) else str(self._current_version),
            "total_nodes": len(self._nodes),
            "total_edges": len(self._edges),
            "graph_entropy": round(self.compute_graph_entropy(), 4),
            "total_snapshots": len(self._snapshots),
            "categories_breakdown": {
                cat: sum(1 for n in self._nodes.values() if n.category == cat)
                for cat in set(n.category for n in self._nodes.values())
            },
        }

    def get_graph(self) -> Dict[str, Any]:
        return {
            "nodes": [n.to_dict() for n in self._nodes.values()],
            "edges": [e.to_dict() for e in self._edges.values()],
            "graph_entropy": round(self.compute_graph_entropy(), 4),
            "snapshots_count": len(self._snapshots),
            "summary": self.get_world_summary(),
        }


# Global Singleton
world_engine = WorldEngine()
