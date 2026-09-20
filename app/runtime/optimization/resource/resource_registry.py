"""
Resource Registry & Inventory for Phase 13.6 (ARIA-EOP).
Tracks active worker pools, LLM quotas, OCR nodes, GPU acceleration, and cache layers.
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class ResourceNode(BaseModel):
    resource_id: str
    resource_type: str  # WORKER_POOL | LLM_QUOTA | OCR_ENGINE | GPU_NODE | CACHE_STORE
    name: str
    total_capacity: int
    available_units: int
    allocated_units: int = 0
    utilization_rate: float = 0.0
    status: str = "HEALTHY"  # HEALTHY | DEGRADED | EXHAUSTED


class ResourceRegistry:
    """
    Catalog of enterprise compute, model, and worker resources.
    """

    def __init__(self):
        self._nodes: Dict[str, ResourceNode] = {}
        self._seed_default_resources()

    def _seed_default_resources(self):
        self._nodes["res-pool-worker-01"] = ResourceNode(
            resource_id="res-pool-worker-01",
            resource_type="WORKER_POOL",
            name="General Async Worker Pool",
            total_capacity=16,
            available_units=10,
            allocated_units=6,
            utilization_rate=0.375,
            status="HEALTHY",
        )
        self._nodes["res-llm-gemini-flash"] = ResourceNode(
            resource_id="res-llm-gemini-flash",
            resource_type="LLM_QUOTA",
            name="Gemini 1.5 Flash Quota (RPM)",
            total_capacity=1000,
            available_units=850,
            allocated_units=150,
            utilization_rate=0.150,
            status="HEALTHY",
        )
        self._nodes["res-ocr-tesseract"] = ResourceNode(
            resource_id="res-ocr-tesseract",
            resource_type="OCR_ENGINE",
            name="Local Tesseract OCR Cluster",
            total_capacity=8,
            available_units=5,
            allocated_units=3,
            utilization_rate=0.375,
            status="HEALTHY",
        )
        self._nodes["res-gpu-v100"] = ResourceNode(
            resource_id="res-gpu-v100",
            resource_type="GPU_NODE",
            name="NVIDIA V100 Acceleration Node",
            total_capacity=4,
            available_units=3,
            allocated_units=1,
            utilization_rate=0.250,
            status="HEALTHY",
        )

    def list_resources(self) -> List[ResourceNode]:
        return list(self._nodes.values())

    def get_resource(self, resource_id: str) -> Optional[ResourceNode]:
        return self._nodes.get(resource_id)


resource_registry = ResourceRegistry()
