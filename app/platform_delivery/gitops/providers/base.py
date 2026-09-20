"""GitOps Provider Abstraction (Req 26)."""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class GitOpsSyncResult:
    sync_status: str  # "Synced" or "OutOfSync"
    health_status: str  # "Healthy", "Degraded", "Progressing"
    revision: str
    message: str


class GitOpsProvider(ABC):
    """Vendor-neutral GitOps Provider Interface."""

    @property
    @abstractmethod
    def provider_name(self) -> str:
        pass

    @abstractmethod
    def sync_application(self, app_name: str, revision: str, prune: bool = True) -> GitOpsSyncResult:
        pass

    @abstractmethod
    def get_sync_status(self, app_name: str) -> GitOpsSyncResult:
        pass
