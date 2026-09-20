"""Mesh Control Plane Controller and Topology Management."""

from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Set


class MeshState(str, Enum):
    INITIALIZING = "INITIALIZING"
    ACTIVE = "ACTIVE"
    DEGRADED = "DEGRADED"
    DRAINING = "DRAINING"
    TERMINATED = "TERMINATED"


class ProtocolType(str, Enum):
    HTTP_1_1 = "HTTP_1_1"
    HTTP_2 = "HTTP_2"
    GRPC = "GRPC"
    WEBSOCKET = "WEBSOCKET"
    TCP = "TCP"


@dataclass
class MeshNode:
    node_id: str
    service_name: str
    namespace: str
    cluster_id: str
    region: str
    ip_address: str
    port: int
    protocol: ProtocolType = ProtocolType.HTTP_2
    version: str = "v1.0.0"
    tags: Dict[str, str] = field(default_factory=dict)
    weight: int = 100
    healthy: bool = True
    last_heartbeat: float = field(default_factory=time.time)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class MeshServiceSpec:
    service_name: str
    namespace: str = "default"
    display_name: str = ""
    description: str = ""
    protocols: List[ProtocolType] = field(default_factory=lambda: [ProtocolType.HTTP_2, ProtocolType.GRPC])
    min_instances: int = 1
    max_instances: int = 10
    mtls_required: bool = True
    zero_trust_strict: bool = True
    timeout_ms: int = 5000
    retry_max_attempts: int = 3
    tags: Dict[str, str] = field(default_factory=dict)
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)


@dataclass
class MeshConfigVersion:
    version_id: str
    version_number: int
    generated_at: float
    service_count: int
    node_count: int
    checksum: str
    configs: Dict[str, Any] = field(default_factory=dict)


@dataclass
class MeshTopology:
    mesh_id: str
    name: str
    state: MeshState = MeshState.ACTIVE
    services: Dict[str, MeshServiceSpec] = field(default_factory=dict)
    nodes: Dict[str, MeshNode] = field(default_factory=dict)
    active_version: int = 1
    config_history: List[MeshConfigVersion] = field(default_factory=list)


class ServiceMeshController:
    """Central Control Plane Controller for the Service Mesh."""

    def __init__(self, mesh_id: Optional[str] = None, name: str = "docutask-mesh"):
        self.mesh_id = mesh_id or f"mesh-{uuid.uuid4().hex[:8]}"
        self.name = name
        self._topology = MeshTopology(mesh_id=self.mesh_id, name=self.name)
        self._listeners: List[Any] = []
        self._version_counter = 1

    @property
    def topology(self) -> MeshTopology:
        return self._topology

    def register_service(self, spec: MeshServiceSpec) -> MeshServiceSpec:
        """Register a new service specification in the mesh control plane."""
        key = f"{spec.namespace}/{spec.service_name}"
        spec.updated_at = time.time()
        self._topology.services[key] = spec
        self._bump_version(f"register_service:{key}")
        return spec

    def deregister_service(self, service_name: str, namespace: str = "default") -> bool:
        """Remove a service specification from the mesh control plane."""
        key = f"{namespace}/{service_name}"
        if key in self._topology.services:
            del self._topology.services[key]
            # Also clean up nodes belonging to this service
            nodes_to_remove = [
                node_id for node_id, node in self._topology.nodes.items()
                if node.service_name == service_name and node.namespace == namespace
            ]
            for n_id in nodes_to_remove:
                del self._topology.nodes[n_id]
            self._bump_version(f"deregister_service:{key}")
            return True
        return False

    def get_service(self, service_name: str, namespace: str = "default") -> Optional[MeshServiceSpec]:
        key = f"{namespace}/{service_name}"
        return self._topology.services.get(key)

    def list_services(self, namespace: Optional[str] = None) -> List[MeshServiceSpec]:
        if namespace:
            return [s for s in self._topology.services.values() if s.namespace == namespace]
        return list(self._topology.services.values())

    def register_node(self, node: MeshNode) -> MeshNode:
        """Register an active instance node belonging to a service."""
        node.last_heartbeat = time.time()
        self._topology.nodes[node.node_id] = node
        self._bump_version(f"register_node:{node.node_id}")
        return node

    def deregister_node(self, node_id: str) -> bool:
        """Remove an instance node from the mesh."""
        if node_id in self._topology.nodes:
            del self._topology.nodes[node_id]
            self._bump_version(f"deregister_node:{node_id}")
            return True
        return False

    def get_node(self, node_id: str) -> Optional[MeshNode]:
        return self._topology.nodes.get(node_id)

    def list_nodes(
        self,
        service_name: Optional[str] = None,
        namespace: Optional[str] = None,
        healthy_only: bool = False,
    ) -> List[MeshNode]:
        nodes = list(self._topology.nodes.values())
        if service_name:
            nodes = [n for n in nodes if n.service_name == service_name]
        if namespace:
            nodes = [n for n in nodes if n.namespace == namespace]
        if healthy_only:
            nodes = [n for n in nodes if n.healthy]
        return nodes

    def heartbeat_node(self, node_id: str, healthy: bool = True) -> bool:
        """Update node heartbeat and health state."""
        node = self._topology.nodes.get(node_id)
        if node:
            node.last_heartbeat = time.time()
            node.healthy = healthy
            return True
        return False

    def get_active_config(self) -> Dict[str, Any]:
        """Fetch current distributed mesh configuration snapshot."""
        return {
            "mesh_id": self.mesh_id,
            "version": self._topology.active_version,
            "state": self._topology.state.value,
            "services_count": len(self._topology.services),
            "nodes_count": len(self._topology.nodes),
            "services": [
                {"name": s.service_name, "namespace": s.namespace, "protocols": [p.value for p in s.protocols]}
                for s in self._topology.services.values()
            ],
            "healthy_nodes": len([n for n in self._topology.nodes.values() if n.healthy]),
        }

    def _bump_version(self, reason: str) -> None:
        self._version_counter += 1
        self._topology.active_version = self._version_counter
        cfg = MeshConfigVersion(
            version_id=f"v-{self._version_counter}-{uuid.uuid4().hex[:6]}",
            version_number=self._version_counter,
            generated_at=time.time(),
            service_count=len(self._topology.services),
            node_count=len(self._topology.nodes),
            checksum=f"chk-{self._version_counter}-{len(self._topology.nodes)}",
            configs={"reason": reason},
        )
        self._topology.config_history.append(cfg)
        # Keep config history capped at 50 entries
        if len(self._topology.config_history) > 50:
            self._topology.config_history.pop(0)
