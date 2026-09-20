"""Service Health Monitoring and Operational Diagnostics."""

from datetime import datetime, timezone
from enum import Enum
from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class HealthStatus(str, Enum):
    HEALTHY = "HEALTHY"
    DEGRADED = "DEGRADED"
    UNHEALTHY = "UNHEALTHY"
    UNKNOWN = "UNKNOWN"


class ServiceHealth(BaseModel):
    """Detailed health record for a service."""

    service_id: str
    status: HealthStatus = HealthStatus.HEALTHY
    version: str = "1.0.0"
    cpu_percent: float = 15.0
    memory_mb: float = 256.0
    latency_p95_ms: float = 12.5
    errors_per_minute: int = 0
    last_check: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    region: str = "us-east-1"
    cluster: str = "k8s-prod-cluster-01"


class ServiceHealthMonitor:
    """Collects, assesses, and queries service health states across clusters."""

    def __init__(self) -> None:
        self._health_records: Dict[str, ServiceHealth] = {}

    def record_health(
        self,
        service_id: str,
        status: HealthStatus = HealthStatus.HEALTHY,
        cpu_percent: float = 15.0,
        memory_mb: float = 256.0,
        latency_p95_ms: float = 12.5,
        errors_per_minute: int = 0,
        region: str = "us-east-1",
        cluster: str = "k8s-prod-cluster-01",
    ) -> ServiceHealth:
        record = ServiceHealth(
            service_id=service_id,
            status=status,
            cpu_percent=cpu_percent,
            memory_mb=memory_mb,
            latency_p95_ms=latency_p95_ms,
            errors_per_minute=errors_per_minute,
            region=region,
            cluster=cluster,
            last_check=datetime.now(timezone.utc),
        )
        self._health_records[service_id] = record
        return record

    def get_health(self, service_id: str) -> ServiceHealth:
        return self._health_records.get(
            service_id,
            ServiceHealth(service_id=service_id, status=HealthStatus.UNKNOWN),
        )

    def list_unhealthy_services(self) -> List[ServiceHealth]:
        return [
            h for h in self._health_records.values()
            if h.status in [HealthStatus.DEGRADED, HealthStatus.UNHEALTHY]
        ]
