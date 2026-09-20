"""Global Control Plane State Models."""

from datetime import datetime, timezone
from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class GlobalControlPlaneState(BaseModel):
    """Snapshot of Global Control Plane state."""

    control_plane_id: str = "gcp_global_primary"
    version: str = "3.1.0"
    is_leader: bool = True
    active_regions_count: int = 0
    total_clusters_count: int = 0
    healthy_clusters_count: int = 0
    synced_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    epoch: int = 1
    metadata: Dict[str, str] = Field(default_factory=dict)
