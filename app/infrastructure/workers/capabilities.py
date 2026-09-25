"""Worker Capability Registry and Dynamic Matching Engine."""

import threading
from typing import Dict, List, Optional, Set


class StandardWorkerCapabilities:
    """Standardized capability identifiers across worker types."""

    WORKFLOW_EXECUTE = "workflow.execute"
    AGENT_REASONING = "agent.reasoning"
    CONNECTOR_HTTP = "connector.http"
    DOCUMENT_OCR = "document.ocr"
    EMBEDDING_GENERATE = "embedding.generate"
    GPU_CUDA = "gpu.cuda"
    GPU_A100 = "gpu.a100"
    GPU_T4 = "gpu.t4"
    MEMORY_HIGH = "memory.high"
    NETWORK_EXTERNAL = "network.external"
    COMPLIANCE_HIPAA = "compliance.hipaa"
    COMPLIANCE_SOC2 = "compliance.soc2"


class WorkerCapabilityRegistry:
    """Indexes and queries worker capabilities across all registered workers."""

    def __init__(self) -> None:
        self._capabilities: Dict[str, Set[str]] = {}  # worker_id -> capabilities
        self._lock = threading.RLock()

    def register_capabilities(self, worker_id: str, capabilities: Set[str]) -> None:
        with self._lock:
            self._capabilities[worker_id] = set(capabilities)

    def add_capability(self, worker_id: str, capability: str) -> None:
        with self._lock:
            if worker_id not in self._capabilities:
                self._capabilities[worker_id] = set()
            self._capabilities[worker_id].add(capability)

    def remove_capability(self, worker_id: str, capability: str) -> None:
        with self._lock:
            if worker_id in self._capabilities:
                self._capabilities[worker_id].discard(capability)

    def get_capabilities(self, worker_id: str) -> Set[str]:
        with self._lock:
            return set(self._capabilities.get(worker_id, set()))

    def satisfies_capabilities(
        self,
        worker_id: str,
        mandatory: Set[str],
        optional: Optional[Set[str]] = None,
    ) -> bool:
        """Check if worker satisfies mandatory capabilities."""
        with self._lock:
            worker_caps = self.get_capabilities(worker_id)
            return mandatory.issubset(worker_caps)

    def calculate_capability_match_score(
        self,
        worker_id: str,
        mandatory: Set[str],
        optional: Optional[Set[str]] = None,
    ) -> float:
        """Compute matching score (0.0 to 1.0) with bonus for satisfying optional capabilities."""
        with self._lock:
            worker_caps = self.get_capabilities(worker_id)
            if not mandatory.issubset(worker_caps):
                return 0.0

            if not optional:
                return 1.0

            matched_opt = len(optional.intersection(worker_caps))
            return 1.0 + (matched_opt / len(optional)) * 0.5

    def query_workers(
        self,
        mandatory: Set[str],
        optional: Optional[Set[str]] = None,
    ) -> List[str]:
        """Find all worker IDs satisfying mandatory capabilities."""
        with self._lock:
            return [
                w_id for w_id in self._capabilities.keys()
                if self.satisfies_capabilities(w_id, mandatory, optional)
            ]
