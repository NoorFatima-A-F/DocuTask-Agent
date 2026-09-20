"""
Interfaces and Abstract Base Classes for Backup Architecture Verification Framework (Part 3G.2A).
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional

from app.platform_verification.backup_architecture_verification.domain.models import (
    AssetInventoryItem,
    ClassificationEntry,
    BackupStrategyConfig,
    StrategyValidationResult,
    BackupDependencyGraph,
    CoverageReport,
    RetentionPolicyConfig,
    RetentionValidationResult,
    LifecycleValidationReport,
    BackupOwnershipRecord,
    BackupMetadataEntry,
    PolicyValidationResult,
    ArchitectureConsistencyReport,
    BackupMetricsReport,
    BackupReadinessScorecard,
)


class IAssetDiscoveryEngine(ABC):
    """Part 1: Automatically inventories all platform assets."""
    @abstractmethod
    def discover_assets(self) -> List[AssetInventoryItem]:
        pass


class IClassificationEngine(ABC):
    """Part 2: Classifies assets into Tier 0 to Tier 3 with RPO/RTO parameters."""
    @abstractmethod
    def classify_assets(self, assets: List[AssetInventoryItem]) -> Dict[str, ClassificationEntry]:
        pass


class IStrategyValidationEngine(ABC):
    """Part 3: Verifies backup strategy matches asset importance and requirements."""
    @abstractmethod
    def validate_strategies(
        self,
        assets: List[AssetInventoryItem],
        classifications: Dict[str, ClassificationEntry],
        strategies: Dict[str, BackupStrategyConfig],
    ) -> List[StrategyValidationResult]:
        pass


class IDependencyGraphEngine(ABC):
    """Part 4: Generates recovery dependency DAG and checks for circular dependencies."""
    @abstractmethod
    def build_and_validate_graph(self, assets: List[AssetInventoryItem]) -> BackupDependencyGraph:
        pass


class ICoverageAnalysisEngine(ABC):
    """Part 5: Analyzes coverage matrix across Tier 0-3 assets."""
    @abstractmethod
    def analyze_coverage(
        self,
        assets: List[AssetInventoryItem],
        strategies: Dict[str, BackupStrategyConfig],
        retentions: Dict[str, RetentionPolicyConfig],
    ) -> CoverageReport:
        pass


class IRetentionVerificationEngine(ABC):
    """Part 6: Validates retention policies, legal holds, and detects infinite/missing retention."""
    @abstractmethod
    def verify_retention_policies(
        self,
        assets: List[AssetInventoryItem],
        retentions: Dict[str, RetentionPolicyConfig],
    ) -> List[RetentionValidationResult]:
        pass


class ILifecycleValidationEngine(ABC):
    """Part 7: Validates 8-stage backup lifecycle, detects orphaned or unexpired backups."""
    @abstractmethod
    def validate_lifecycles(self, assets: List[AssetInventoryItem]) -> List[LifecycleValidationReport]:
        pass


class IOwnershipModelEngine(ABC):
    """Part 8: Enforces ownership model across all protected assets."""
    @abstractmethod
    def verify_ownership(self, assets: List[AssetInventoryItem]) -> List[BackupOwnershipRecord]:
        pass


class IMetadataEngine(ABC):
    """Part 9: Generates cryptographically verifiable metadata for backups."""
    @abstractmethod
    def generate_metadata_registry(self, assets: List[AssetInventoryItem]) -> List[BackupMetadataEntry]:
        pass


class IPolicyValidationEngine(ABC):
    """Part 10: Validates backup policy schedules, encryption, and notifications."""
    @abstractmethod
    def validate_policies(self, policies: List[Dict[str, Any]]) -> List[PolicyValidationResult]:
        pass


class IArchitectureConsistencyEngine(ABC):
    """Part 11: Validates referential integrity and consistency across the backup architecture."""
    @abstractmethod
    def verify_consistency(
        self,
        assets: List[AssetInventoryItem],
        strategies: Dict[str, BackupStrategyConfig],
        retentions: Dict[str, RetentionPolicyConfig],
        ownerships: List[BackupOwnershipRecord],
        dep_graph: BackupDependencyGraph,
    ) -> ArchitectureConsistencyReport:
        pass


class IObservabilityEngine(ABC):
    """Part 12: Collects metrics and exposes Prometheus, OpenTelemetry, and Grafana exports."""
    @abstractmethod
    def generate_metrics_report(
        self,
        coverage: CoverageReport,
        metadata_list: List[BackupMetadataEntry],
    ) -> BackupMetricsReport:
        pass


class IEvidenceManifestEngine(ABC):
    """Part 13: Emits all 14 machine-readable audit artifacts."""
    @abstractmethod
    def export_evidence_artifacts(
        self,
        verification_data: Dict[str, Any],
        output_dir: Optional[str] = None,
    ) -> Dict[str, str]:
        pass


class IReadinessScoringEngine(ABC):
    """Part 14: Computes weighted readiness score and certification tier."""
    @abstractmethod
    def calculate_readiness_score(
        self,
        discovery_score: float,
        classification_score: float,
        strategy_score: float,
        coverage_score: float,
        retention_score: float,
        lifecycle_score: float,
        metadata_score: float,
        observability_score: float,
        policy_score: float,
        execution_duration_ms: float,
    ) -> BackupReadinessScorecard:
        pass
