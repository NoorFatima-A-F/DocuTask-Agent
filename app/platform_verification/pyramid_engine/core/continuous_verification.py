"""
Continuous Verification Integration & Trigger Matrix.
"""
from __future__ import annotations
from typing import List
from app.platform_verification.pyramid_engine.domain.models import (
    ContinuousTrigger,
    VerificationLevel,
)


class ContinuousVerificationManager:
    """Defines which verification levels execute per CI/CD event trigger."""

    @staticmethod
    def get_levels_for_trigger(trigger: ContinuousTrigger) -> List[VerificationLevel]:
        if trigger == ContinuousTrigger.COMMIT:
            return [VerificationLevel.L1_UNIT]
        elif trigger == ContinuousTrigger.PULL_REQUEST:
            return [
                VerificationLevel.L1_UNIT,
                VerificationLevel.L2_COMPONENT,
                VerificationLevel.L3_INTEGRATION,
            ]
        elif trigger == ContinuousTrigger.NIGHTLY:
            return [
                VerificationLevel.L1_UNIT,
                VerificationLevel.L2_COMPONENT,
                VerificationLevel.L3_INTEGRATION,
                VerificationLevel.L4_SYSTEM,
                VerificationLevel.L5_PRODUCTION,
            ]
        elif trigger == ContinuousTrigger.RELEASE:
            return [
                VerificationLevel.L1_UNIT,
                VerificationLevel.L2_COMPONENT,
                VerificationLevel.L3_INTEGRATION,
                VerificationLevel.L4_SYSTEM,
                VerificationLevel.L5_PRODUCTION,
                VerificationLevel.L6_ADVERSARIAL,
                VerificationLevel.L7_ENTERPRISE_CERTIFICATION,
            ]
        return [VerificationLevel.L1_UNIT]
