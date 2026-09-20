"""Traffic Splitting (Canary, Blue-Green, Shadow/Mirror)."""

from __future__ import annotations

import random
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional

from ..mesh.data_plane import MeshRequest, MeshResponse


class SplitType(str, Enum):
    WEIGHTED = "WEIGHTED"
    CANARY = "CANARY"
    BLUE_GREEN = "BLUE_GREEN"
    SHADOW = "SHADOW"


@dataclass
class VersionSplit:
    version: str
    weight: int  # 0 to 100
    description: str = ""


@dataclass
class TrafficSplitConfig:
    split_id: str
    service_name: str
    namespace: str = "default"
    split_type: SplitType = SplitType.WEIGHTED
    splits: List[VersionSplit] = field(default_factory=list)
    shadow_version: Optional[str] = None
    shadow_percentage: float = 0.0  # 0.0 to 100.0
    active: bool = True


class TrafficSplitter:
    """Manages progressive delivery traffic splits and non-blocking shadow traffic mirroring."""

    def __init__(self):
        self._configs: Dict[str, TrafficSplitConfig] = {}
        self._shadow_records: List[Dict[str, Any]] = []

    def set_split_config(self, config: TrafficSplitConfig) -> None:
        key = f"{config.namespace}/{config.service_name}"
        self._configs[key] = config

    def get_split_config(self, service_name: str, namespace: str = "default") -> Optional[TrafficSplitConfig]:
        key = f"{namespace}/{service_name}"
        return self._configs.get(key)

    def remove_split_config(self, service_name: str, namespace: str = "default") -> bool:
        key = f"{namespace}/{service_name}"
        if key in self._configs:
            del self._configs[key]
            return True
        return False

    def select_version(self, service_name: str, namespace: str = "default") -> str:
        """Select a destination version according to configured weights."""
        cfg = self.get_split_config(service_name, namespace)
        if not cfg or not cfg.active or not cfg.splits:
            return "v1"

        total_weight = sum(s.weight for s in cfg.splits)
        if total_weight <= 0:
            return cfg.splits[0].version

        rand_val = random.uniform(0, total_weight)
        current = 0.0
        for s in cfg.splits:
            current += s.weight
            if rand_val <= current:
                return s.version

        return cfg.splits[-1].version

    def should_mirror_shadow(self, service_name: str, namespace: str = "default") -> tuple[bool, Optional[str]]:
        """Determine if request should be shadowed/mirrored to a candidate version."""
        cfg = self.get_split_config(service_name, namespace)
        if not cfg or not cfg.active or not cfg.shadow_version or cfg.shadow_percentage <= 0:
            return False, None

        if random.uniform(0, 100) <= cfg.shadow_percentage:
            return True, cfg.shadow_version
        return False, None

    def record_shadow_execution(
        self,
        request: MeshRequest,
        shadow_version: str,
        shadow_response: MeshResponse,
    ) -> None:
        """Record shadow execution telemetry asynchronously."""
        self._shadow_records.append({
            "request_id": request.request_id,
            "target_service": request.target_service,
            "shadow_version": shadow_version,
            "status_code": shadow_response.status_code,
            "duration_ms": shadow_response.duration_ms,
            "timestamp": time.time(),
        })
        # Keep capped
        if len(self._shadow_records) > 200:
            self._shadow_records.pop(0)

    def get_shadow_records(self) -> List[Dict[str, Any]]:
        return list(self._shadow_records)
