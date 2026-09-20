"""Regional Control Plane State Models."""

from datetime import datetime, timezone
from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class RegionalControlPlaneState(BaseModel):
    """Snapshot of a Regional Control Plane state."""

    region_id: str
    control_plane_id: str
    is_active: bool = True
    local_clusters_count: int = 0
    active_clusters_count: int = 0
    degraded_clusters_count: int = 0
    last_heartbeat: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    synced_epoch: int = 1
    metadata: Dict[str, str] = Field(default_factory=dict)
