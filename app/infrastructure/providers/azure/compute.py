"""Azure Compute Provider Adapter (AKS / VM / Container Apps)."""

import secrets
from typing import Any, Dict, Optional
from ..base import ComputeProvider, ProviderInstanceResult


class AzureComputeProvider(ComputeProvider):
    """Manages Azure Container Apps and AKS workloads."""

    def __init__(self, subscription_id: str = "sub-12345", resource_group: str = "rg-doctask") -> None:
        super().__init__("azure")
        self.subscription_id = subscription_id
        self.resource_group = resource_group
        self._apps: Dict[str, Dict[str, Any]] = {}

    def create_instance(
        self,
        name: str,
        image: str,
        cpu: float,
        memory_mb: int,
        env_vars: Optional[Dict[str, str]] = None,
    ) -> ProviderInstanceResult:
        app_id = f"/subscriptions/{self.subscription_id}/resourceGroups/{self.resource_group}/providers/Microsoft.App/containerApps/{name}-{secrets.token_hex(4)}"
        app_record = {
            "app_id": app_id,
            "name": name,
            "image": image,
            "cpu": cpu,
            "memory_mb": memory_mb,
            "status": "Running",
            "endpoint": f"https://{name}.azurecontainerapps.io",
        }
        self._apps[app_id] = app_record
        return ProviderInstanceResult(
            instance_id=app_id,
            provider_name="azure",
            status="Running",
            endpoint=app_record["endpoint"],
            metadata=app_record,
        )

    def terminate_instance(self, instance_id: str) -> bool:
        if instance_id in self._apps:
            self._apps[instance_id]["status"] = "Stopped"
            return True
        return False

    def get_instance_status(self, instance_id: str) -> str:
        app = self._apps.get(instance_id)
        return app["status"] if app else "NotFound"

    def health_check(self) -> bool:
        return True
