"""
Abstract Interfaces for Multi-Region & Cloud Failover Framework (Part 3G.6).
"""
from abc import ABC, abstractmethod
from app.platform_verification.multi_region_failover.domain.models import (
    MultiRegionArchitectureReport,
    CloudPortabilityReport,
    DatabaseReplicationReport,
    StorageReplicationReport,
    TrafficFailoverReport,
    WorkflowCheckpointReport,
    ChaosOutageReport,
    AvailabilityMetricsReport,
    MultiRegionScorecard,
)


class IMultiRegionArchitectureValidator(ABC):
    @abstractmethod
    def validate_architecture(self) -> MultiRegionArchitectureReport:
        pass


class ICloudPortabilityVerifier(ABC):
    @abstractmethod
    def verify_portability(self) -> CloudPortabilityReport:
        pass


class IDatabaseReplicationVerifier(ABC):
    @abstractmethod
    def verify_database_replication(self) -> DatabaseReplicationReport:
        pass


class IStorageReplicationVerifier(ABC):
    @abstractmethod
    def verify_storage_replication(self) -> StorageReplicationReport:
        pass


class ITrafficFailoverEngine(ABC):
    @abstractmethod
    def verify_traffic_failover(self) -> TrafficFailoverReport:
        pass


class IWorkflowCheckpointVerifier(ABC):
    @abstractmethod
    def verify_workflow_checkpoints(self) -> WorkflowCheckpointReport:
        pass


class IChaosOutageSimulator(ABC):
    @abstractmethod
    def simulate_regional_outages(self) -> ChaosOutageReport:
        pass


class IAvailabilityMetricsEngine(ABC):
    @abstractmethod
    def calculate_availability_metrics(self) -> AvailabilityMetricsReport:
        pass


class IMultiRegionScoreEngine(ABC):
    @abstractmethod
    def calculate_scorecard(
        self,
        arch: MultiRegionArchitectureReport,
        portability: CloudPortabilityReport,
        db_rep: DatabaseReplicationReport,
        storage_rep: StorageReplicationReport,
        traffic: TrafficFailoverReport,
        workflow: WorkflowCheckpointReport,
        chaos: ChaosOutageReport,
        avail: AvailabilityMetricsReport,
    ) -> MultiRegionScorecard:
        pass
