"""
Intelligent Change Classification and Risk Impact Engine.
"""
from __future__ import annotations
from typing import List
from app.platform_verification.cicd_pipeline.domain.interfaces import IChangeDetector
from app.platform_verification.cicd_pipeline.domain.models import (
    ChangedFile,
    ChangeRiskLevel,
    PipelineChangeContext,
    PipelineChangeType,
    PipelineStageType,
)


class EnterpriseChangeDetector(IChangeDetector):
    """Classifies repository changes into adaptive verification execution plans."""

    def analyze_changes(
        self,
        change_id: str,
        commit_sha: str,
        branch: str,
        author: str,
        changed_paths: List[str],
    ) -> PipelineChangeContext:
        changed_files: List[ChangedFile] = []
        has_model = False
        has_prompt = False
        has_dataset = False
        has_infra = False
        has_code = False
        has_docs_only = True

        for path in changed_paths:
            path_lower = path.lower()
            if "prompt" in path_lower or "templates" in path_lower:
                ctype = PipelineChangeType.PROMPT
                has_prompt = True
                has_docs_only = False
            elif "model" in path_lower or "weights" in path_lower or "checkpoints" in path_lower:
                ctype = PipelineChangeType.MODEL
                has_model = True
                has_docs_only = False
            elif "dataset" in path_lower or "data/" in path_lower or "schemas" in path_lower:
                ctype = PipelineChangeType.DATASET
                has_dataset = True
                has_docs_only = False
            elif "docker" in path_lower or "k8s" in path_lower or "helm" in path_lower or "terraform" in path_lower:
                ctype = PipelineChangeType.INFRASTRUCTURE
                has_infra = True
                has_docs_only = False
            elif path_lower.endswith((".py", ".ts", ".js", ".go", ".rs", ".sql")):
                ctype = PipelineChangeType.CODE
                has_code = True
                has_docs_only = False
            elif path_lower.endswith((".md", ".txt", ".rst", ".png", ".jpg")):
                ctype = PipelineChangeType.DOCUMENTATION
            else:
                ctype = PipelineChangeType.CONFIGURATION
                has_docs_only = False

            changed_files.append(ChangedFile(file_path=path, change_type=ctype))

        # Determine Primary Change Type & Risk Level
        if has_model:
            primary_type = PipelineChangeType.MODEL
            risk_level = ChangeRiskLevel.CRITICAL
            affected_components = ["AIModelInference", "AgentCore", "EmbeddingEngine"]
            required_stages = [
                PipelineStageType.STAGE_1_SOURCE_VALIDATION,
                PipelineStageType.STAGE_2_BUILD_VERIFICATION,
                PipelineStageType.STAGE_3_UNIT_VERIFICATION,
                PipelineStageType.STAGE_4_COMPONENT_VERIFICATION,
                PipelineStageType.STAGE_6_AI_EVALUATION,
                PipelineStageType.STAGE_7_SECURITY_VERIFICATION,
                PipelineStageType.STAGE_8_PERFORMANCE_VERIFICATION,
                PipelineStageType.STAGE_9_CERTIFICATION_VALIDATION,
            ]
        elif has_prompt:
            primary_type = PipelineChangeType.PROMPT
            risk_level = ChangeRiskLevel.HIGH
            affected_components = ["PromptTemplates", "AgentReasoning", "ExtractionPipeline"]
            required_stages = [
                PipelineStageType.STAGE_1_SOURCE_VALIDATION,
                PipelineStageType.STAGE_3_UNIT_VERIFICATION,
                PipelineStageType.STAGE_6_AI_EVALUATION,
                PipelineStageType.STAGE_7_SECURITY_VERIFICATION,
                PipelineStageType.STAGE_9_CERTIFICATION_VALIDATION,
            ]
        elif has_code:
            primary_type = PipelineChangeType.CODE
            risk_level = ChangeRiskLevel.MEDIUM
            affected_components = ["BackendServices", "APIEndpoints", "WorkerPool"]
            required_stages = [
                PipelineStageType.STAGE_1_SOURCE_VALIDATION,
                PipelineStageType.STAGE_2_BUILD_VERIFICATION,
                PipelineStageType.STAGE_3_UNIT_VERIFICATION,
                PipelineStageType.STAGE_4_COMPONENT_VERIFICATION,
                PipelineStageType.STAGE_5_INTEGRATION_VERIFICATION,
                PipelineStageType.STAGE_7_SECURITY_VERIFICATION,
                PipelineStageType.STAGE_8_PERFORMANCE_VERIFICATION,
                PipelineStageType.STAGE_9_CERTIFICATION_VALIDATION,
            ]
        elif has_infra:
            primary_type = PipelineChangeType.INFRASTRUCTURE
            risk_level = ChangeRiskLevel.HIGH
            affected_components = ["KubernetesCluster", "ServiceMesh", "DeploymentConfig"]
            required_stages = [
                PipelineStageType.STAGE_1_SOURCE_VALIDATION,
                PipelineStageType.STAGE_2_BUILD_VERIFICATION,
                PipelineStageType.STAGE_5_INTEGRATION_VERIFICATION,
                PipelineStageType.STAGE_7_SECURITY_VERIFICATION,
                PipelineStageType.STAGE_9_CERTIFICATION_VALIDATION,
            ]
        elif has_docs_only:
            primary_type = PipelineChangeType.DOCUMENTATION
            risk_level = ChangeRiskLevel.LOW
            affected_components = ["Documentation"]
            required_stages = [PipelineStageType.STAGE_1_SOURCE_VALIDATION]
        else:
            primary_type = PipelineChangeType.CONFIGURATION
            risk_level = ChangeRiskLevel.MEDIUM
            affected_components = ["ConfigStore"]
            required_stages = [
                PipelineStageType.STAGE_1_SOURCE_VALIDATION,
                PipelineStageType.STAGE_3_UNIT_VERIFICATION,
                PipelineStageType.STAGE_5_INTEGRATION_VERIFICATION,
                PipelineStageType.STAGE_9_CERTIFICATION_VALIDATION,
            ]

        return PipelineChangeContext(
            change_id=change_id,
            commit_sha=commit_sha,
            branch=branch,
            author=author,
            primary_change_type=primary_type,
            changed_files=changed_files,
            risk_level=risk_level,
            affected_components=affected_components,
            required_stages=required_stages,
        )
