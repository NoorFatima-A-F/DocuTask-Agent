"""Cluster Capability Registry and Query Engine."""

from typing import Dict, List, Set


class StandardCapabilities:
    GPU_ENABLED = "gpu.enabled"
    VECTOR_SEARCH_ENABLED = "vector-search.enabled"
    OCR_ENABLED = "ocr.enabled"
    HIGH_MEMORY_ENABLED = "high-memory.enabled"
    COMPLIANCE_HIPAA = "compliance.hipaa"
    COMPLIANCE_PCI = "compliance.pci"
    REGION_PRIVATE = "region.private"
    STORAGE_LOCALITY = "storage.locality"
    ARM64_ARCH = "arch.arm64"
    X86_64_ARCH = "arch.x86_64"


class ClusterCapabilityRegistry:
    """Indexes and queries cluster capabilities across all registered clusters."""

    def __init__(self) -> None:
        self._cluster_capabilities: Dict[str, Set[str]] = {}

    def register_capabilities(self, cluster_id: str, capabilities: Set[str]) -> None:
        self._cluster_capabilities[cluster_id] = set(capabilities)

    def add_capability(self, cluster_id: str, capability: str) -> None:
        if cluster_id not in self._cluster_capabilities:
            self._cluster_capabilities[cluster_id] = set()
        self._cluster_capabilities[cluster_id].add(capability)

    def remove_capability(self, cluster_id: str, capability: str) -> None:
        if cluster_id in self._cluster_capabilities:
            self._cluster_capabilities[cluster_id].discard(capability)

    def get_capabilities(self, cluster_id: str) -> Set[str]:
        return set(self._cluster_capabilities.get(cluster_id, set()))

    def satisfies_capabilities(self, cluster_id: str, required_capabilities: Set[str]) -> bool:
        cluster_caps = self.get_capabilities(cluster_id)
        return required_capabilities.issubset(cluster_caps)

    def has_capabilities(self, cluster_id: str, required_capabilities: Set[str]) -> bool:
        return self.satisfies_capabilities(cluster_id, required_capabilities)

    def find_clusters_with_capabilities(self, required_capabilities: Set[str]) -> List[str]:
        return [
            cid for cid, caps in self._cluster_capabilities.items()
            if required_capabilities.issubset(caps)
        ]

    def query_clusters(self, required_capabilities: Set[str]) -> List[str]:
        return self.find_clusters_with_capabilities(required_capabilities)
