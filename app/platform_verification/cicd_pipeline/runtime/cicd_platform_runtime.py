"""
Enterprise CI/CD Platform Runtime facade.
"""
from __future__ import annotations
from app.platform_verification.cicd_pipeline.core.artifact_registry import EnterpriseArtifactRegistry
from app.platform_verification.cicd_pipeline.core.change_detector import EnterpriseChangeDetector
from app.platform_verification.cicd_pipeline.core.observability_engine import EnterprisePipelineObservabilityEngine
from app.platform_verification.cicd_pipeline.core.pipeline_orchestrator import EnterprisePipelineOrchestrator
from app.platform_verification.cicd_pipeline.core.promotion_engine import EnterpriseEnvironmentPromotionEngine
from app.platform_verification.cicd_pipeline.core.rollback_engine import EnterpriseRollbackEngine
from app.platform_verification.cicd_pipeline.core.stage_runner import EnterpriseStageRunner
from app.platform_verification.cicd_pipeline.core.supply_chain_verifier import EnterpriseSupplyChainVerifier


class EnterpriseCICDPlatformRuntime:
    """Unified runtime connecting all CI/CD continuous verification engines."""

    def __init__(self):
        self.change_detector = EnterpriseChangeDetector()
        self.stage_runner = EnterpriseStageRunner()
        self.orchestrator = EnterprisePipelineOrchestrator(stage_runner=self.stage_runner)
        self.promotion_engine = EnterpriseEnvironmentPromotionEngine()
        self.rollback_engine = EnterpriseRollbackEngine()
        self.artifact_registry = EnterpriseArtifactRegistry()
        self.supply_chain_verifier = EnterpriseSupplyChainVerifier()
        self.observability = EnterprisePipelineObservabilityEngine()
