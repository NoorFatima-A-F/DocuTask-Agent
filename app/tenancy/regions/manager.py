"""Regional Deployment & Residency Manager (ESP-MOOS).

Governs geographical deployment targets and data residency boundaries across US, EU, Asia, Middle East, and Private Cloud.
"""

from __future__ import annotations

from typing import Dict, List, Optional
from app.tenancy.core.models import Region


class RegionManager:
    """Manages available infrastructure regions and regional latency routing."""

    REGION_METADATA: Dict[Region, Dict[str, any]] = {
        Region.US_EAST: {"name": "US East (N. Virginia)", "cloud": "AWS/GCP", "jurisdiction": "USA"},
        Region.US_WEST: {"name": "US West (Oregon)", "cloud": "AWS/GCP", "jurisdiction": "USA"},
        Region.EU_WEST: {"name": "EU West (Ireland)", "cloud": "AWS/GCP", "jurisdiction": "European Union"},
        Region.EU_CENTRAL: {"name": "EU Central (Frankfurt)", "cloud": "AWS/GCP", "jurisdiction": "European Union"},
        Region.ASIA_PACIFIC: {"name": "Asia Pacific (Singapore)", "cloud": "AWS/GCP", "jurisdiction": "Singapore"},
        Region.MIDDLE_EAST: {"name": "Middle East (UAE)", "cloud": "AWS/GCP", "jurisdiction": "UAE"},
        Region.PRIVATE_CLOUD: {"name": "On-Premises / Dedicated VPC", "cloud": "Self-Hosted", "jurisdiction": "Custom"},
    }

    def list_regions(self) -> List[Dict[str, any]]:
        """List all supported platform deployment regions."""
        return [
            {"region": r.value, **meta} for r, meta in self.REGION_METADATA.items()
        ]

    def get_region_metadata(self, region: Region) -> Dict[str, any]:
        """Get metadata for a specific region."""
        return self.REGION_METADATA.get(region, {"name": region.value, "jurisdiction": "Unknown"})
