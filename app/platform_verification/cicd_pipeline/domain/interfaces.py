"""
Abstract interfaces for Enterprise Continuous Verification CI/CD Pipeline.
"""
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from app.platform_verification.cicd_pipeline.domain.models import (
    EnvironmentPromotionRecord,
    PipelineArtifactMetadata,
    PipelineChangeContext,
    PipelineExecutionRecord,
    PipelineObservabilityMetrics,
    PipelineStageType,
    RollbackEventRecord,
    RollbackTriggerReason,
    StageExecutionRecord,
    SupplyChainSecurityReport,
    TargetEnvironment,
)


class IChangeDetector(ABC):
    """Analyzes source control changes, classifies risk, and determines required pipeline stages."""

    @abstractmethod
    def analyze_changes(
        self,
        change_id: str,
        commit_sha: str,
        branch: str,
        author: str,
        changed_paths: List[str],
    ) -> PipelineChangeContext:
        """Analyzes commit changes and outputs adaptive execution plan."""
        pass


class IStageRunner(ABC):
    """Executes a single pipeline verification stage."""

    @abstractmethod
    def execute_stage(
        self,
        stage_type: PipelineStageType,
        change_context: PipelineChangeContext,
        previous_stage_outputs: Dict[str, Any],
    ) -> StageExecutionRecord:
        """Executes a verification stage and returns execution record with metrics."""
        pass


class IPipelineOrchestrator(ABC):
    """Coordinates full end-to-end continuous verification pipeline execution."""

    @abstractmethod
    def trigger_pipeline(
        self,
        change_context: PipelineChangeContext,
        target_env: TargetEnvironment = TargetEnvironment.STAGING,
    ) -> PipelineExecutionRecord:
        """Triggers pipeline run, evaluates stages sequentially, and returns full record."""
        pass

    @abstractmethod
    def get_pipeline_status(self, pipeline_id: str) -> Optional[PipelineExecutionRecord]:
        """Retrieves pipeline execution status by ID."""
        pass


class IPromotionEngine(ABC):
    """Governs environment progression (Dev -> Int -> Staging -> Shadow -> Prod)."""

    @abstractmethod
    def evaluate_and_promote(
        self,
        pipeline_record: PipelineExecutionRecord,
        target_env: TargetEnvironment,
        approved_by: str,
    ) -> EnvironmentPromotionRecord:
        """Evaluates certification gate and promotes build to target environment."""
        pass


class IRollbackEngine(ABC):
    """Handles automated rollbacks upon incident detection or health degradation."""

    @abstractmethod
    def execute_rollback(
        self,
        pipeline_id: str,
        target_env: TargetEnvironment,
        reason: RollbackTriggerReason,
        failed_version: str,
        previous_stable_version: str,
    ) -> RollbackEventRecord:
        """Halts deployment, restores previous version, and invalidates certificate."""
        pass


class IArtifactRegistry(ABC):
    """Stores, hashes, verifies, and certifies build, model, and dataset artifacts."""

    @abstractmethod
    def register_artifact(
        self,
        name: str,
        version: str,
        artifact_type: str,
        content_bytes: bytes,
    ) -> PipelineArtifactMetadata:
        """Registers and computes SHA-256 for a release artifact."""
        pass

    @abstractmethod
    def verify_artifact_integrity(self, artifact_id: str) -> bool:
        """Verifies artifact checksum."""
        pass


class ISupplyChainVerifier(ABC):
    """Performs security supply chain validation (dependencies, CVEs, secrets, SBOM)."""

    @abstractmethod
    def scan_pipeline_artifacts(
        self,
        pipeline_id: str,
        artifacts: List[PipelineArtifactMetadata],
    ) -> SupplyChainSecurityReport:
        """Scans artifacts for vulnerabilities and compliance violations."""
        pass


class IPipelineObservability(ABC):
    """Collects and aggregates DORA and AI quality pipeline observability metrics."""

    @abstractmethod
    def record_pipeline_run(self, record: PipelineExecutionRecord) -> None:
        """Ingests a completed pipeline run into metrics store."""
        pass

    @abstractmethod
    def get_metrics(self) -> PipelineObservabilityMetrics:
        """Returns consolidated observability metrics."""
        pass
