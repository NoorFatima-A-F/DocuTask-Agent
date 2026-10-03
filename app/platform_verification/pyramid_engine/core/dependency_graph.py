"""
Strict Progressive Dependency Graph and Gatekeeper for Verification Pyramid.
"""
from __future__ import annotations
from typing import Dict, List
from app.platform_verification.pyramid_engine.domain.models import (
    VerificationLevel,
    LevelExecutionSummary,
    PyramidExecutionStatus,
)
from app.platform_verification.pyramid_engine.domain.interfaces import IDependencyGate

# Explicit ordered hierarchy: L1 -> L2 -> L3 -> L4 -> L5 -> L6 -> L7
LEVEL_HIERARCHY: List[VerificationLevel] = [
    VerificationLevel.L1_UNIT,
    VerificationLevel.L2_COMPONENT,
    VerificationLevel.L3_INTEGRATION,
    VerificationLevel.L4_SYSTEM,
    VerificationLevel.L5_PRODUCTION,
    VerificationLevel.L6_ADVERSARIAL,
    VerificationLevel.L7_ENTERPRISE_CERTIFICATION,
]


class DependencyGate(IDependencyGate):
    """Enforces strict prerequisite dependency rules across the verification pyramid."""

    def can_execute_level(
        self, target_level: VerificationLevel, completed_levels: Dict[VerificationLevel, LevelExecutionSummary]
    ) -> bool:
        if target_level not in LEVEL_HIERARCHY:
            return True

        target_idx = LEVEL_HIERARCHY.index(target_level)
        # All preceding levels in the hierarchy must have PASSED
        for i in range(target_idx):
            req_level = LEVEL_HIERARCHY[i]
            if req_level not in completed_levels:
                return False
            summary = completed_levels[req_level]
            if summary.status != PyramidExecutionStatus.PASSED:
                return False

        return True

    def get_prerequisites(self, target_level: VerificationLevel) -> List[VerificationLevel]:
        if target_level not in LEVEL_HIERARCHY:
            return []
        target_idx = LEVEL_HIERARCHY.index(target_level)
        return LEVEL_HIERARCHY[:target_idx]
