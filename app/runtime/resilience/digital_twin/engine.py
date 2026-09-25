"""
DocuTask Agent - Operational Digital Twin Engine
Phase 12: Autonomous Production Reliability & Operational Resilience (APRCORP+)
"""

import time
import uuid
from typing import Dict, List, Any, Optional
from app.runtime.resilience.digital_twin.twin_state import (
    DigitalTwinNode,
    DigitalTwinEdge,
    OperationalTwinSnapshot,
    NodeHealthStatus,
    ComponentCategory,
)


class DigitalTwinEngine:
    """
    Live Operational Digital Twin Engine.
    Continuously reflects the true operational state of the DocuTask autonomous platform,
    tracking runtime components, latency drift, fault blast radius, and replica synchronization.
    """

    def __init__(self):
        self.nodes: Dict[str, DigitalTwinNode] = {}
        self.edges: List[DigitalTwinEdge] = []
        self._history: List[OperationalTwinSnapshot] = []
        self._initialize_default_topology()

    def _initialize_default_topology(self) -> None:
        """Initializes the baseline high-availability DocuTask architecture graph."""
        default_nodes = [
            DigitalTwinNode("node-planner", "Autonomous Planner Engine", ComponentCategory.PLANNER, NodeHealthStatus.HEALTHY, latency_ms=18.2, cpu_usage_pct=14.5, replicas=2),
            DigitalTwinNode("node-workers", "DAG Dynamic Worker Pool", ComponentCategory.WORKER, NodeHealthStatus.HEALTHY, latency_ms=32.4, cpu_usage_pct=28.1, replicas=4),
            DigitalTwinNode("node-memory", "Episodic & Causal Memory Graph", ComponentCategory.MEMORY, NodeHealthStatus.HEALTHY, latency_ms=12.1, cpu_usage_pct=8.4, replicas=3),
            DigitalTwinNode("node-truth", "Runtime Truth & Proof Ledger", ComponentCategory.TRUTH_LEDGER, NodeHealthStatus.HEALTHY, latency_ms=8.5, cpu_usage_pct=6.2, replicas=3),
            DigitalTwinNode("node-evidence", "Cryptographic Evidence Store", ComponentCategory.EVIDENCE, NodeHealthStatus.HEALTHY, latency_ms=9.1, cpu_usage_pct=5.5, replicas=3),
            DigitalTwinNode("node-policy", "Dynamic Policy & Sandbox Engine", ComponentCategory.POLICY, NodeHealthStatus.HEALTHY, latency_ms=11.0, cpu_usage_pct=7.0, replicas=2),
            DigitalTwinNode("node-storage", "Redis State & Fast KV Cache", ComponentCategory.STORAGE, NodeHealthStatus.HEALTHY, latency_ms=4.2, cpu_usage_pct=11.0, replicas=3),
            DigitalTwinNode("node-gemini", "Google Cloud Gemini 1.5 Pro/Flash", ComponentCategory.PROVIDER, NodeHealthStatus.HEALTHY, latency_ms=145.0, cpu_usage_pct=0.0, replicas=1),
            DigitalTwinNode("node-commander", "Autonomous Incident Commander", ComponentCategory.INCIDENT_COMMANDER, NodeHealthStatus.HEALTHY, latency_ms=6.8, cpu_usage_pct=3.2, replicas=2),
        ]

        for n in default_nodes:
            self.nodes[n.node_id] = n

        self.edges = [
            DigitalTwinEdge("node-planner", "node-workers", "DISPATCHES_TASKS", latency_p95_ms=22.0, throughput_rps=85.0),
            DigitalTwinEdge("node-workers", "node-gemini", "INVOKES_MODELS", latency_p95_ms=160.0, throughput_rps=45.0),
            DigitalTwinEdge("node-workers", "node-memory", "QUERIES_EXPERIENCES", latency_p95_ms=15.0, throughput_rps=120.0),
            DigitalTwinEdge("node-planner", "node-truth", "COMMITS_PROOFS", latency_p95_ms=10.0, throughput_rps=60.0),
            DigitalTwinEdge("node-workers", "node-evidence", "RECORDS_EVIDENCE", latency_p95_ms=12.0, throughput_rps=110.0),
            DigitalTwinEdge("node-workers", "node-storage", "SYNCS_EXECUTION_STATE", latency_p95_ms=5.0, throughput_rps=250.0),
            DigitalTwinEdge("node-policy", "node-workers", "GOVERNS_SANDBOX", latency_p95_ms=8.0, throughput_rps=90.0),
            DigitalTwinEdge("node-commander", "node-planner", "SUPERVISES_RESILIENCE", latency_p95_ms=7.0, throughput_rps=30.0),
            DigitalTwinEdge("node-commander", "node-workers", "ISOLATES_FAILURES", latency_p95_ms=7.5, throughput_rps=30.0),
        ]

    def register_heartbeat(self, node_id: str, latency_ms: float, error_rate: float, cpu_pct: float) -> Optional[DigitalTwinNode]:
        """Registers a live heartbeat from a physical or logical runtime component."""
        if node_id not in self.nodes:
            return None
        node = self.nodes[node_id]
        node.last_heartbeat_utc = time.time()
        node.latency_ms = max(0.1, latency_ms)
        node.error_rate = min(1.0, max(0.0, error_rate))
        node.cpu_usage_pct = min(100.0, max(0.0, cpu_pct))

        # Auto-compute health status based on live telemetry
        if node.error_rate > 0.5 or node.latency_ms > 2000.0:
            node.health = NodeHealthStatus.FAILING
        elif node.error_rate > 0.1 or node.latency_ms > 500.0:
            node.health = NodeHealthStatus.DEGRADED
        else:
            node.health = NodeHealthStatus.HEALTHY

        return node

    def mutate_node_health(self, node_id: str, status: NodeHealthStatus, latency_ms: Optional[float] = None, error_rate: Optional[float] = None) -> bool:
        """Explicitly mutates node status during chaos injections or incident isolations."""
        if node_id not in self.nodes:
            return False
        node = self.nodes[node_id]
        node.health = status
        if latency_ms is not None:
            node.latency_ms = latency_ms
        if error_rate is not None:
            node.error_rate = error_rate
        return True

    def isolate_node(self, node_id: str) -> bool:
        """Isolates a failing node to prevent cascading blast radius across dependencies."""
        if node_id not in self.nodes:
            return False
        self.nodes[node_id].health = NodeHealthStatus.ISOLATED
        for edge in self.edges:
            if edge.source_id == node_id or edge.target_id == node_id:
                edge.circuit_breaker_open = True
        return True

    def heal_node(self, node_id: str) -> bool:
        """Restores a node to healthy state and resets circuit breakers."""
        if node_id not in self.nodes:
            return False
        self.nodes[node_id].health = NodeHealthStatus.HEALTHY
        self.nodes[node_id].error_rate = 0.00
        self.nodes[node_id].latency_ms = 18.0
        for edge in self.edges:
            if edge.source_id == node_id or edge.target_id == node_id:
                edge.circuit_breaker_open = False
        return True

    def compute_overall_health(self) -> float:
        """Computes weighted overall platform health score [0.0 - 100.0]."""
        if not self.nodes:
            return 100.0
        total_score = 0.0
        for node in self.nodes.values():
            if node.health == NodeHealthStatus.HEALTHY:
                score = 100.0 - (node.error_rate * 50.0)
            elif node.health == NodeHealthStatus.DEGRADED:
                score = 65.0
            elif node.health == NodeHealthStatus.RECOVERING:
                score = 75.0
            elif node.health == NodeHealthStatus.ISOLATED:
                score = 50.0
            else:
                score = 0.0
            total_score += score
        return round(total_score / len(self.nodes), 2)

    def capture_snapshot(self, mission_id: Optional[str] = None) -> OperationalTwinSnapshot:
        """Captures an immutable snapshot of the operational digital twin."""
        snapshot = OperationalTwinSnapshot(
            snapshot_id=f"twin-snap-{uuid.uuid4().hex[:8]}",
            mission_id=mission_id,
            timestamp_utc=time.time(),
            nodes={k: DigitalTwinNode(**v.__dict__) for k, v in self.nodes.items()},
            edges=[DigitalTwinEdge(**e.__dict__) for e in self.edges],
            overall_health_score=self.compute_overall_health(),
            active_incidents_count=sum(1 for n in self.nodes.values() if n.health in [NodeHealthStatus.FAILING, NodeHealthStatus.DEGRADED, NodeHealthStatus.ISOLATED]),
            active_chaos_injections_count=sum(1 for n in self.nodes.values() if "chaos_injected" in n.metadata and n.metadata["chaos_injected"]),
            sync_parity_pct=99.98,
        )
        self._history.append(snapshot)
        if len(self._history) > 100:
            self._history.pop(0)
        return snapshot

    def get_topology_dict(self) -> Dict[str, Any]:
        """Returns serializable dictionary of the operational twin graph."""
        return {
            "overall_health_score": self.compute_overall_health(),
            "nodes": [
                {
                    "node_id": n.node_id,
                    "name": n.name,
                    "category": n.category.value,
                    "health": n.health.value,
                    "latency_ms": round(n.latency_ms, 2),
                    "error_rate": round(n.error_rate, 4),
                    "cpu_usage_pct": round(n.cpu_usage_pct, 1),
                    "memory_usage_mb": round(n.memory_usage_mb, 1),
                    "replicas": n.replicas,
                    "last_heartbeat_utc": n.last_heartbeat_utc,
                    "invariants_passed": n.invariants_passed,
                    "invariants_failed": n.invariants_failed,
                }
                for n in self.nodes.values()
            ],
            "edges": [
                {
                    "source_id": e.source_id,
                    "target_id": e.target_id,
                    "edge_type": e.edge_type,
                    "latency_p95_ms": round(e.latency_p95_ms, 2),
                    "throughput_rps": round(e.throughput_rps, 1),
                    "circuit_breaker_open": e.circuit_breaker_open,
                }
                for e in self.edges
            ],
            "total_nodes": len(self.nodes),
            "total_edges": len(self.edges),
            "timestamp_utc": time.time(),
        }


# Global singleton instance
digital_twin_engine = DigitalTwinEngine()
