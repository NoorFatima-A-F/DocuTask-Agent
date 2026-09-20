"""Local Compute Provider Adapter (Docker Compose / Local Process Execution)."""

import secrets
from typing import Any, Dict, Optional
from ..base import ComputeProvider, ProviderInstanceResult


class LocalComputeProvider(ComputeProvider):
    """Manages Local Docker containers or processes for developer environments."""

    def __init__(self) -> None:
        super().__init__("local")
        self._containers: Dict[str, Dict[str, Any]] = {}

    def create_instance(
        self,
        name: str,
        image: str,
        cpu: float,
        memory_mb: int,
        env_vars: Optional[Dict[str, str]] = None,
    ) -> ProviderInstanceResult:
        cid = f"local-container-{name}-{secrets.token_hex(4)}"
        record = {
            "container_id": cid,
            "name": name,
            "image": image,
            "cpu": cpu,
            "memory_mb": memory_mb,
            "status": "RUNNING",
            "endpoint": f"http://localhost:8000/{name}",
        }
        self._containers[cid] = record
        return ProviderInstanceResult(
            instance_id=cid,
            provider_name="local",
            status="RUNNING",
            endpoint=record["endpoint"],
            metadata=record,
        )

    def terminate_instance(self, instance_id: str) -> bool:
        if instance_id in self._containers:
            self._containers[instance_id]["status"] = "STOPPED"
            return True
        return False

    def get_instance_status(self, instance_id: str) -> str:
        c = self._containers.get(instance_id)
        return c["status"] if c else "NOT_FOUND"

    def health_check(self) -> bool:
        return True
