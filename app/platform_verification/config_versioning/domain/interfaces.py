"""
Domain Interfaces for Configuration & Dependency Management.
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from app.platform_verification.config_versioning.domain.models import (
    ConfigurationSnapshot, DependencyItem, DriftReport,
    ChangeRequest, RollbackRecord
)

class ConfigurationRegistryInterface(ABC):
    @abstractmethod
    def store_snapshot(self, snapshot: ConfigurationSnapshot) -> ConfigurationSnapshot:
        pass

    @abstractmethod
    def get_snapshot(self, snapshot_id: str) -> Optional[ConfigurationSnapshot]:
        pass

    @abstractmethod
    def list_snapshots(self, tenant_id: str = "default-tenant") -> List[ConfigurationSnapshot]:
        pass


class DependencyRegistryInterface(ABC):
    @abstractmethod
    def register_dependency(self, item: DependencyItem) -> DependencyItem:
        pass

    @abstractmethod
    def list_dependencies(self) -> List[DependencyItem]:
        pass

    @abstractmethod
    def get_dependency(self, name: str) -> Optional[DependencyItem]:
        pass


class DriftDetectorInterface(ABC):
    @abstractmethod
    def detect_drift(self, baseline_snapshot_id: str, current_config: Dict[str, Any]) -> DriftReport:
        pass


class ChangeTrackerInterface(ABC):
    @abstractmethod
    def submit_change_request(self, request: ChangeRequest) -> ChangeRequest:
        pass

    @abstractmethod
    def approve_change_request(self, change_id: str, approver: str) -> ChangeRequest:
        pass

    @abstractmethod
    def execute_rollback(self, change_id: str, to_snapshot_id: str, reason: str) -> RollbackRecord:
        pass
