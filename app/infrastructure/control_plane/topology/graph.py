"""Topology Graph Representation for Multi-Region Multi-Cluster Mesh."""

from enum import Enum
import threading
from typing import Dict, List, Optional, Set, Tuple
from pydantic import BaseModel, Field


class NodeType(str, Enum):
    REGION = "REGION"
    CLUSTER = "CLUSTER"
    GATEWAY = "GATEWAY"


class TopologyNode(BaseModel):
    node_id: str
    node_type: NodeType
    properties: Dict[str, str] = Field(default_factory=dict)


class TopologyEdge(BaseModel):
    source_id: str
    target_id: str
    latency_ms: float = 10.0
    bandwidth_gbps: float = 100.0
    is_healthy: bool = True
    edge_type: str = "REGIONAL_LINK"  # REGIONAL_LINK, CLUSTER_LINK, FAILOVER_LINK


class TopologyGraph:
    """Thread-safe graph representation of the global topology."""

    def __init__(self):
        self._nodes: Dict[str, TopologyNode] = {}
        self._edges: Dict[Tuple[str, str], TopologyEdge] = {}
        self._adjacency: Dict[str, Set[str]] = {}
        self._lock = threading.RLock()

    def add_node(self, node_id: str, node_type: NodeType, properties: Optional[Dict[str, str]] = None) -> TopologyNode:
        """Add a node (Region, Cluster, or Gateway) to the topology graph."""
        with self._lock:
            node = TopologyNode(node_id=node_id, node_type=node_type, properties=properties or {})
            self._nodes[node_id] = node
            if node_id not in self._adjacency:
                self._adjacency[node_id] = set()
            return node

    def add_edge(
        self,
        source_id: str,
        target_id: str,
        latency_ms: float = 10.0,
        bandwidth_gbps: float = 100.0,
        edge_type: str = "REGIONAL_LINK",
    ) -> TopologyEdge:
        """Add a bidirectional edge between two nodes in the topology."""
        with self._lock:
            # Ensure nodes exist
            if source_id not in self._nodes:
                self.add_node(source_id, NodeType.REGION)
            if target_id not in self._nodes:
                self.add_node(target_id, NodeType.REGION)

            edge = TopologyEdge(
                source_id=source_id,
                target_id=target_id,
                latency_ms=latency_ms,
                bandwidth_gbps=bandwidth_gbps,
                edge_type=edge_type,
            )
            self._edges[(source_id, target_id)] = edge
            self._edges[(target_id, source_id)] = TopologyEdge(
                source_id=target_id,
                target_id=source_id,
                latency_ms=latency_ms,
                bandwidth_gbps=bandwidth_gbps,
                edge_type=edge_type,
            )
            self._adjacency[source_id].add(target_id)
            self._adjacency[target_id].add(source_id)
            return edge

    def get_node(self, node_id: str) -> Optional[TopologyNode]:
        with self._lock:
            return self._nodes.get(node_id)

    def get_edge(self, source_id: str, target_id: str) -> Optional[TopologyEdge]:
        with self._lock:
            return self._edges.get((source_id, target_id))

    def get_neighbors(self, node_id: str) -> List[str]:
        with self._lock:
            return list(self._adjacency.get(node_id, set()))

    def list_nodes(self, node_type: Optional[NodeType] = None) -> List[TopologyNode]:
        with self._lock:
            nodes = list(self._nodes.values())
            if node_type:
                nodes = [n for n in nodes if n.node_type == node_type]
            return nodes

    def find_shortest_latency_path(self, start_id: str, target_id: str) -> Tuple[List[str], float]:
        """Dijkstra's shortest path based on latency_ms."""
        with self._lock:
            if start_id not in self._nodes or target_id not in self._nodes:
                return [], float("inf")
            if start_id == target_id:
                return [start_id], 0.0

            import heapq
            distances = {n: float("inf") for n in self._nodes}
            previous = {n: None for n in self._nodes}
            distances[start_id] = 0.0

            pq = [(0.0, start_id)]
            while pq:
                curr_dist, curr_node = heapq.heappop(pq)
                if curr_dist > distances[curr_node]:
                    continue
                if curr_node == target_id:
                    break

                for neighbor in self._adjacency.get(curr_node, set()):
                    edge = self._edges.get((curr_node, neighbor))
                    if not edge or not edge.is_healthy:
                        continue
                    new_dist = curr_dist + edge.latency_ms
                    if new_dist < distances[neighbor]:
                        distances[neighbor] = new_dist
                        previous[neighbor] = curr_node
                        heapq.heappush(pq, (new_dist, neighbor))

            if distances[target_id] == float("inf"):
                return [], float("inf")

            path = []
            curr = target_id
            while curr:
                path.append(curr)
                curr = previous[curr]
            path.reverse()
            return path, distances[target_id]
