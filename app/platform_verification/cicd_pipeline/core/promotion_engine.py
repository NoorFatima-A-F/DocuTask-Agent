"""
Environment Promotion Engine enforcing verification and certification gates.
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Dict, List, Optional
import uuid
from app.platform_verification.cicd_pipeline.domain.interfaces import IPromotionEngine
from app.platform_verification.cicd_pipeline.domain.models import (
    EnvironmentPromotionRecord,
    PipelineExecutionRecord,
    PipelineExecutionStatus,
    PromotionStatus,
    TargetEnvironment,
)


class EnterpriseEnvironmentPromotionEngine(IPromotionEngine):
    """Controls progression through Dev -> Int -> Staging -> Shadow -> Prod."""

    def __init__(self):
        self._promotions: Dict[str, EnvironmentPromotionRecord] = {}

    def evaluate_and_promote(
        self,
        pipeline_record: PipelineExecutionRecord,
        target_env: TargetEnvironment,
        approved_by: str,
    ) -> EnvironmentPromotionRecord:
        promo_id = f"PROMO-{uuid.uuid4().hex[:8].upper()}"
        source_env = pipeline_record.target_environment

        # Required certification levels by environment
        env_cert_requirements = {
            TargetEnvironment.DEVELOPMENT: "LEVEL_1_DEVELOPMENT_VERIFIED",
            TargetEnvironment.INTEGRATION: "LEVEL_3_INTEGRATION_CERTIFIED",
            TargetEnvironment.STAGING: "LEVEL_4_SYSTEM_CERTIFIED",
            TargetEnvironment.PRODUCTION_SHADOW: "LEVEL_5_PRODUCTION_CERTIFIED",
            TargetEnvironment.PRODUCTION: "LEVEL_5_PRODUCTION_CERTIFIED",
        }

        req_level = env_cert_requirements.get(target_env, "LEVEL_5_PRODUCTION_CERTIFIED")
        actual_level = "LEVEL_5_PRODUCTION_CERTIFIED" if pipeline_record.certification_id else "LEVEL_0_NOT_CERTIFIED"

        if pipeline_record.status != PipelineExecutionStatus.PASSED:
            record = EnvironmentPromotionRecord(
                promotion_id=promo_id,
                pipeline_id=pipeline_record.pipeline_id,
                source_env=source_env,
                target_env=target_env,
                status=PromotionStatus.REJECTED,
                certification_level_required=req_level,
                actual_certification_level=actual_level,
                approved_by=approved_by,
                rejection_reason=f"Pipeline status is {pipeline_record.status.value}. Promotion blocked.",
            )
        elif not pipeline_record.certification_id:
            record = EnvironmentPromotionRecord(
                promotion_id=promo_id,
                pipeline_id=pipeline_record.pipeline_id,
                source_env=source_env,
                target_env=target_env,
                status=PromotionStatus.REJECTED,
                certification_level_required=req_level,
                actual_certification_level=actual_level,
                approved_by=approved_by,
                rejection_reason="Missing verified certification record.",
            )
        else:
            record = EnvironmentPromotionRecord(
                promotion_id=promo_id,
                pipeline_id=pipeline_record.pipeline_id,
                source_env=source_env,
                target_env=target_env,
                status=PromotionStatus.PROMOTED,
                certification_level_required=req_level,
                actual_certification_level=actual_level,
                approved_by=approved_by,
                promoted_at=datetime.now(timezone.utc).isoformat(),
            )

        self._promotions[promo_id] = record
        return record

    def list_promotions(self) -> List[EnvironmentPromotionRecord]:
        return list(self._promotions.values())
