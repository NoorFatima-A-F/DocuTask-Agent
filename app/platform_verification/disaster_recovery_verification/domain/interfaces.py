"""
Domain interfaces for Disaster Recovery Architecture Verification (Part 3G.1).
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any
from app.platform_verification.disaster_recovery_verification.domain.models import (
    DRServiceInventory,
    ComponentCriticalityEntry,
    BusinessImpactAnalysisEntry,
    RecoveryDependencyGraph,
    DataRecoveryValidationReport,
    DRTestScenarioResult,
    DRSecurityValidationReport,
    DRCertificationScorecard,
    DRMetadata,
    DRScenarioType,
)


class IDRArchitectureDiscovery(ABC):
    @abstractmethod
    def discover_inventory(self) -> DRServiceInventory:
        pass

    @abstractmethod
    def classify_components(self) -> Dict[str, ComponentCriticalityEntry]:
        pass

    @abstractmethod
    def generate_bia(self) -> List[BusinessImpactAnalysisEntry]:
        pass


class IRecoveryDependencyGraphEngine(ABC):
    @abstractmethod
    def build_dependency_graph(self) -> RecoveryDependencyGraph:
        pass

    @abstractmethod
    def validate_recovery_order(self, proposed_order: List[str]) -> bool:
        pass


class IDataRecoveryValidator(ABC):
    @abstractmethod
    def validate_data_recovery(
        self,
        original_hash: str,
        restored_hash: str,
        expected_count: int,
        restored_count: int,
    ) -> DataRecoveryValidationReport:
        pass


class IDRSecurityValidator(ABC):
    @abstractmethod
    def validate_dr_security(self) -> DRSecurityValidationReport:
        pass


class IDRTestHarness(ABC):
    __test__ = False
    @abstractmethod
    def execute_scenario(self, scenario: DRScenarioType) -> DRTestScenarioResult:
        pass

    @abstractmethod
    def execute_all_scenarios(self) -> List[DRTestScenarioResult]:
        pass


class IDRCertificationEngine(ABC):
    @abstractmethod
    def compute_certification(
        self,
        scenarios: List[DRTestScenarioResult],
        data_report: DataRecoveryValidationReport,
        sec_report: DRSecurityValidationReport,
        dep_graph: RecoveryDependencyGraph,
    ) -> DRCertificationScorecard:
        pass


class IDREvidenceStore(ABC):
    @abstractmethod
    def persist_all_evidence(
        self,
        inventory: DRServiceInventory,
        criticality: Dict[str, ComponentCriticalityEntry],
        scenarios: List[DRTestScenarioResult],
        dep_graph: RecoveryDependencyGraph,
        backup_report: Dict[str, Any],
        rto_rpo_report: Dict[str, Any],
        integrity_report: DataRecoveryValidationReport,
        security_report: DRSecurityValidationReport,
        metadata: DRMetadata,
    ) -> Dict[str, str]:
        pass
