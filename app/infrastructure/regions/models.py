"""Region Domain Models, Enums, and Regional Topology."""

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class RegionStatus(str, Enum):
    PROVISIONING = "PROVISIONING"
    ACTIVE = "ACTIVE"
    DEGRADED = "DEGRADED"
    DRAINING = "DRAINING"
    MAINTENANCE = "MAINTENANCE"
    STANDBY = "STANDBY"
    OFFLINE = "OFFLINE"


class LatencyClass(str, Enum):
    ULTRA_LOW = "ULTRA_LOW"  # < 20ms
    LOW = "LOW"              # < 50ms
    MEDIUM = "MEDIUM"        # < 100ms
    HIGH = "HIGH"            # >= 100ms


class Geography(BaseModel):
    """Geographic and jurisdictional location metadata."""

    continent: str = "North America"
    country: str = "US"
    jurisdiction: str = "US"  # e.g., US, EU, APAC, UK, CA
    un_region_code: str = "021"
    latitude: float = 37.7749
    longitude: float = -122.4194


class Region(BaseModel):
    """First-class governed Region entity."""

    region_id: str
    name: str
    display_name: str
    provider: str = "aws"  # aws, gcp, azure, kubernetes, onprem
    geography: Geography = Field(default_factory=Geography)
    status: RegionStatus = RegionStatus.ACTIVE
    is_primary: bool = False
    routing_priority: int = 100  # Lower number = higher priority
    primary_cluster_id: Optional[str] = None
    failover_region_id: Optional[str] = None
    active_cluster_ids: List[str] = Field(default_factory=list)
    data_residency_jurisdiction: str = "US"
    compliance_certifications: List[str] = Field(
        default_factory=lambda: ["SOC2_TYPE_II", "ISO_27001", "GDPR", "HIPAA"]
    )
    ingress_endpoint: str = "https://ingress.us-east-1.docutask.internal"
    egress_gateways: List[str] = Field(default_factory=list)
    metadata: Dict[str, str] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
