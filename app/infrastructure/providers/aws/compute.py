"""AWS Compute Provider Adapter (ECS / EKS / EC2 / Lambda)."""

import secrets
from typing import Any, Dict, Optional
from ..base import ComputeProvider, ProviderInstanceResult


class AWSComputeProvider(ComputeProvider):
    """Manages AWS Compute Workloads (ECS Task / EC2 / Lambda)."""

    def __init__(self, region: str = "us-east-1") -> None:
        super().__init__("aws")
        self.region = region
        self._tasks: Dict[str, Dict[str, Any]] = {}

    def create_instance(
        self,
        name: str,
        image: str,
        cpu: float,
        memory_mb: int,
        env_vars: Optional[Dict[str, str]] = None,
    ) -> ProviderInstanceResult:
        arn = f"arn:aws:ecs:{self.region}:123456789012:task/{name}/{secrets.token_hex(16)}"
        task_record = {
            "task_arn": arn,
            "name": name,
            "image": image,
            "cpu": cpu,
            "memory_mb": memory_mb,
            "status": "RUNNING",
            "endpoint": f"http://{name}.ecs.{self.region}.amazonaws.com",
        }
        self._tasks[arn] = task_record
        return ProviderInstanceResult(
            instance_id=arn,
            provider_name="aws",
            status="RUNNING",
            endpoint=task_record["endpoint"],
            metadata=task_record,
        )

    def terminate_instance(self, instance_id: str) -> bool:
        if instance_id in self._tasks:
            self._tasks[instance_id]["status"] = "STOPPED"
            return True
        return False

    def get_instance_status(self, instance_id: str) -> str:
        task = self._tasks.get(instance_id)
        return task["status"] if task else "UNKNOWN"

    def health_check(self) -> bool:
        return True
