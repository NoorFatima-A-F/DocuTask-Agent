"""
Phase 13.18: Service Discovery & Multi-Region Fabric Router
Geographic latency-aware task routing across global cloud regions (US, EU, Asia, PK).
"""

from __future__ import annotations
from typing import Dict, List, Optional, Any
from app.runtime.distributed.models.schemas import RegionName, WorkerNode


class RegionRouter:
    """Calculates cross-region latency matrices and routes tasks to optimal geographic endpoints."""

    # Approximate inter-region latency matrix in ms
    LATENCY_MATRIX: Dict[str, Dict[str, float]] = {
        RegionName.US_EAST.value: {
            RegionName.US_EAST.value: 8.0,
            RegionName.US_WEST.value: 65.0,
            RegionName.EU_CENTRAL.value: 85.0,
            RegionName.ASIA_EAST.value: 180.0,
            RegionName.PK_SOUTH.value: 210.0,
        },
        RegionName.EU_CENTRAL.value: {
            RegionName.US_EAST.value: 85.0,
            RegionName.US_WEST.value: 135.0,
            RegionName.EU_CENTRAL.value: 10.0,
            RegionName.ASIA_EAST.value: 140.0,
            RegionName.PK_SOUTH.value: 110.0,
        },
        RegionName.ASIA_EAST.value: {
            RegionName.US_EAST.value: 180.0,
            RegionName.US_WEST.value: 115.0,
            RegionName.EU_CENTRAL.value: 140.0,
            RegionName.ASIA_EAST.value: 12.0,
            RegionName.PK_SOUTH.value: 75.0,
        },
        RegionName.PK_SOUTH.value: {
            RegionName.US_EAST.value: 210.0,
            RegionName.US_WEST.value: 240.0,
            RegionName.EU_CENTRAL.value: 110.0,
            RegionName.ASIA_EAST.value: 75.0,
            RegionName.PK_SOUTH.value: 6.0,
        },
    }

    @classmethod
    def get_latency(cls, source_region: RegionName, target_region: RegionName) -> float:
        src = source_region.value if isinstance(source_region, RegionName) else source_region
        tgt = target_region.value if isinstance(target_region, RegionName) else target_region
        return cls.LATENCY_MATRIX.get(src, {}).get(tgt, 150.0)

    @classmethod
    def get_region_topology(cls) -> List[Dict[str, Any]]:
        return [
            {"region": RegionName.US_EAST.value, "location": "N. Virginia (GCP us-east4 / AWS us-east-1)", "status": "ONLINE", "avg_latency_ms": 8.5},
            {"region": RegionName.US_WEST.value, "location": "Oregon (GCP us-west1 / AWS us-west-2)", "status": "ONLINE", "avg_latency_ms": 65.0},
            {"region": RegionName.EU_CENTRAL.value, "location": "Frankfurt (GCP europe-west3 / AWS eu-central-1)", "status": "ONLINE", "avg_latency_ms": 10.2},
            {"region": RegionName.ASIA_EAST.value, "location": "Tokyo (GCP asia-northeast1 / AWS ap-northeast-1)", "status": "ONLINE", "avg_latency_ms": 12.0},
            {"region": RegionName.PK_SOUTH.value, "location": "Karachi Edge (Hybrid Node Cluster)", "status": "ONLINE", "avg_latency_ms": 6.0},
        ]
