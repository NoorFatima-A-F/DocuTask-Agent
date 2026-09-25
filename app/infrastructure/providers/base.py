"""Neutral Provider Interfaces for Cloud and Infrastructure Abstraction."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from pydantic import BaseModel


class ProviderInstanceResult(BaseModel):
    """Result of a compute provider operation."""

    instance_id: str
    provider_name: str
    status: str
    endpoint: Optional[str] = None
    metadata: Dict[str, Any] = {}


class ComputeProvider(ABC):
    """Abstract Compute Provider contract."""

    def __init__(self, provider_name: str) -> None:
        self.provider_name = provider_name

    @abstractmethod
    def create_instance(self, name: str, image: str, cpu: float, memory_mb: int, env_vars: Optional[Dict[str, str]] = None) -> ProviderInstanceResult:
        pass

    @abstractmethod
    def terminate_instance(self, instance_id: str) -> bool:
        pass

    @abstractmethod
    def get_instance_status(self, instance_id: str) -> str:
        pass

    @abstractmethod
    def health_check(self) -> bool:
        pass


class StorageProvider(ABC):
    """Abstract Storage Provider contract."""

    def __init__(self, provider_name: str) -> None:
        self.provider_name = provider_name

    @abstractmethod
    def provision_bucket(self, bucket_name: str, region: str) -> bool:
        pass

    @abstractmethod
    def delete_bucket(self, bucket_name: str) -> bool:
        pass


class NetworkProvider(ABC):
    """Abstract Network Provider contract."""

    def __init__(self, provider_name: str) -> None:
        self.provider_name = provider_name

    @abstractmethod
    def create_load_balancer(self, name: str, ports: List[int], target_service: str) -> str:
        pass

    @abstractmethod
    def delete_load_balancer(self, lb_id: str) -> bool:
        pass


class SecretProvider(ABC):
    """Abstract Secret Provider contract (isolated from app logic)."""

    def __init__(self, provider_name: str) -> None:
        self.provider_name = provider_name

    @abstractmethod
    def get_secret(self, secret_name: str) -> Optional[str]:
        pass

    @abstractmethod
    def set_secret(self, secret_name: str, secret_value: str) -> bool:
        pass

    @abstractmethod
    def delete_secret(self, secret_name: str) -> bool:
        pass
