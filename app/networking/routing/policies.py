"""Routing Policies and Connection Management."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional


class LoadBalancingAlgorithm(str, Enum):
    ROUND_ROBIN = "ROUND_ROBIN"
    WEIGHTED_ROUND_ROBIN = "WEIGHTED_ROUND_ROBIN"
    LEAST_REQUEST = "LEAST_REQUEST"
    CONSISTENT_HASH = "CONSISTENT_HASH"
    LOCALITY_PRIORITIZED = "LOCALITY_PRIORITIZED"


@dataclass
class ConnectionPoolSettings:
    max_connections: int = 1024
    max_pending_requests: int = 512
    max_requests_per_connection: int = 100
    idle_timeout_seconds: float = 60.0
    connect_timeout_ms: float = 1000.0


@dataclass
class OutlierDetectionSettings:
    consecutive_5xx_errors: int = 5
    interval_seconds: float = 10.0
    base_ejection_time_seconds: float = 30.0
    max_ejection_percent: int = 50


@dataclass
class TrafficPolicy:
    policy_id: str
    service_name: str
    namespace: str = "default"
    load_balancing: LoadBalancingAlgorithm = LoadBalancingAlgorithm.ROUND_ROBIN
    connection_pool: ConnectionPoolSettings = field(default_factory=ConnectionPoolSettings)
    outlier_detection: OutlierDetectionSettings = field(default_factory=OutlierDetectionSettings)
    cookie_affinity_name: Optional[str] = None
    header_rewrites: Dict[str, str] = field(default_factory=dict)
    mirror_percentage: float = 0.0
    mirror_service: Optional[str] = None


class RoutingPolicyEngine:
    """Manages service-level traffic policies and transforms requests according to policy rules."""

    def __init__(self):
        self._policies: Dict[str, TrafficPolicy] = {}

    def set_policy(self, policy: TrafficPolicy) -> None:
        key = f"{policy.namespace}/{policy.service_name}"
        self._policies[key] = policy

    def get_policy(self, service_name: str, namespace: str = "default") -> Optional[TrafficPolicy]:
        key = f"{namespace}/{service_name}"
        return self._policies.get(key)

    def remove_policy(self, service_name: str, namespace: str = "default") -> bool:
        key = f"{namespace}/{service_name}"
        if key in self._policies:
            del self._policies[key]
            return True
        return False

    def list_policies(self) -> List[TrafficPolicy]:
        return list(self._policies.values())
