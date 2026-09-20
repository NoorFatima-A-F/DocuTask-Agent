"""
Evidence Retention & Archival Manager.
"""
from datetime import datetime, timezone
from typing import List
from app.platform_verification.evidence_engine.domain.models import (
    EvidenceArtifact, EvidenceLifecycleState
)


class EvidenceRetentionManager:
    def evaluate_retention(self, artifacts: List[EvidenceArtifact]) -> List[EvidenceArtifact]:
        active = []
        for a in artifacts:
            if a.lifecycle_state != EvidenceLifecycleState.EXPIRED:
                active.append(a)
        return active


evidence_retention_manager = EvidenceRetentionManager()
RetentionPolicyManager = EvidenceRetentionManager
