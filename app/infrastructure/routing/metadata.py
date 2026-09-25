"""Routing Metadata Models and Request Specifications."""

from datetime import datetime, timezone
from typing import Dict, List, Optional, Set
from pydantic import BaseModel, Field


class WorkloadRoutingRequest(BaseModel):
    """Specification of a workload routing demand."""

    tenant_id: str
    workload_type: str = "ocr"  # ocr, agent, workflow, model_inference
    required_capabilities: Set[str] = Field(default_factory=set)
    required_compliance: List[str] = Field(default_factory=list)
    target_region: Optional[str] = None
    required_jurisdiction: Optional[str] = None
    min_cpu_cores: float = 1.0
    min_memory_gb: float = 2.0
    labels_selector: Dict[str, str] = Field(default_factory=dict)


class RoutingDecision(BaseModel):
    """Result of an evaluated routing decision."""

    is_routable: bool
    selected_cluster_id: Optional[str] = None
    selected_region_id: Optional[str] = None
    candidate_cluster_ids: List[str] = Field(default_factory=list)
    rejection_reasons: List[str] = Field(default_factory=list)
    evaluated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
