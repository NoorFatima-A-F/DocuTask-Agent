"""Google Cloud Compute Provider Adapter (GKE / Compute Engine / Cloud Run)."""

import secrets
from typing import Any, Dict, Optional
from ..base import ComputeProvider, ProviderInstanceResult


class GCPComputeProvider(ComputeProvider):
    """Manages GCP Compute workloads (Cloud Run / GKE)."""

    def __init__(self, project_id: str = "doctask-production", region: str = "us-central1") -> None:
        super().__init__("gcp")
        self.project_id = project_id
        self.region = region
        self._services: Dict[str, Dict[str, Any]] = {}

    def create_instance(
        self,
        name: str,
        image: str,
        cpu: float,
        memory_mb: int,
        env_vars: Optional[Dict[str, str]] = None,
    ) -> ProviderInstanceResult:
        service_id = f"projects/{self.project_id}/locations/{self.region}/services/{name}-{secrets.token_hex(4)}"
        svc_record = {
            "service_id": service_id,
            "name": name,
            "image": image,
            "cpu": cpu,
            "memory_mb": memory_mb,
            "status": "READY",
            "endpoint": f"https://{name}-{self.project_id}.a.run.app",
        }
        self._services[service_id] = svc_record
        return ProviderInstanceResult(
            instance_id=service_id,
            provider_name="gcp",
            status="READY",
            endpoint=svc_record["endpoint"],
            metadata=svc_record,
        )

    def terminate_instance(self, instance_id: str) -> bool:
        if instance_id in self._services:
            self._services[instance_id]["status"] = "DELETED"
            return True
        return False

    def get_instance_status(self, instance_id: str) -> str:
        svc = self._services.get(instance_id)
        return svc["status"] if svc else "NOT_FOUND"

    def health_check(self) -> bool:
        return True
