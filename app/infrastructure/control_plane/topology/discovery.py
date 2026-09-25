"""Topology Discovery Service synchronizing graph topology from registries."""

from typing import Optional
from app.infrastructure.clusters.registry import ClusterRegistry
from app.infrastructure.regions.registry import RegionRegistry
from app.infrastructure.control_plane.topology.graph import NodeType, TopologyGraph


class TopologyDiscoveryService:
    """Discovers and synchronizes the global topology graph from active registries."""

    def __init__(
        self,
        cluster_registry: ClusterRegistry,
        region_registry: RegionRegistry,
        graph: Optional[TopologyGraph] = None,
    ):
        self.cluster_registry = cluster_registry
        self.region_registry = region_registry
        self.graph = graph or TopologyGraph()

    def discover_and_sync(self) -> TopologyGraph:
        """Populate and synchronize the topology graph with all registered regions and clusters."""
        regions = self.region_registry.list_regions()
        clusters = self.cluster_registry.list_clusters()

        # Add region nodes
        for r in regions:
            self.graph.add_node(
                node_id=r.region_id,
                node_type=NodeType.REGION,
                properties={
                    "name": r.name,
                    "jurisdiction": r.data_residency_jurisdiction,
                    "status": r.status.value,
                },
            )

        # Add cluster nodes and cluster-region edges
        for c in clusters:
            self.graph.add_node(
                node_id=c.cluster_id,
                node_type=NodeType.CLUSTER,
                properties={
                    "name": c.name,
                    "provider": c.provider,
                    "status": c.status.value,
                    "health": c.health_status,
                },
            )
            # Link cluster to its host region (low latency intra-region link, ~1.5ms)
            self.graph.add_edge(
                source_id=c.cluster_id,
                target_id=c.region_id,
                latency_ms=1.5,
                bandwidth_gbps=100.0,
                edge_type="CLUSTER_LINK",
            )

        # Add inter-region backbone links
        for i, r1 in enumerate(regions):
            for r2 in regions[i + 1:]:
                # Regional inter-connect latency model
                est_latency = 35.0 if r1.geography.continent == r2.geography.continent else 95.0
                self.graph.add_edge(
                    source_id=r1.region_id,
                    target_id=r2.region_id,
                    latency_ms=est_latency,
                    bandwidth_gbps=40.0,
                    edge_type="REGIONAL_LINK",
                )

        return self.graph
