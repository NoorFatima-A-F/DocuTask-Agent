"""
Role-Based Access Control (RBAC) for Verification Evidence System.
"""
from __future__ import annotations
from typing import Dict, List
from app.platform_verification.evidence_engine.domain.models import (
    EvidenceRole,
    EvidenceClassification,
)
from app.platform_verification.evidence_engine.domain.interfaces import IEvidenceAccessController

ROLE_PERMISSIONS: Dict[EvidenceRole, Dict[str, List[EvidenceClassification]]] = {
    EvidenceRole.DEVELOPER: {
        "VIEW": [EvidenceClassification.PUBLIC, EvidenceClassification.INTERNAL],
        "EXPORT": [EvidenceClassification.PUBLIC],
        "APPROVE": [],
        "ADMIN": [],
    },
    EvidenceRole.REVIEWER: {
        "VIEW": [EvidenceClassification.PUBLIC, EvidenceClassification.INTERNAL, EvidenceClassification.CONFIDENTIAL],
        "EXPORT": [EvidenceClassification.PUBLIC, EvidenceClassification.INTERNAL],
        "APPROVE": [EvidenceClassification.PUBLIC, EvidenceClassification.INTERNAL, EvidenceClassification.CONFIDENTIAL],
        "ADMIN": [],
    },
    EvidenceRole.AUDITOR: {
        "VIEW": [EvidenceClassification.PUBLIC, EvidenceClassification.INTERNAL, EvidenceClassification.CONFIDENTIAL, EvidenceClassification.RESTRICTED],
        "EXPORT": [EvidenceClassification.PUBLIC, EvidenceClassification.INTERNAL, EvidenceClassification.CONFIDENTIAL],
        "APPROVE": [EvidenceClassification.PUBLIC, EvidenceClassification.INTERNAL, EvidenceClassification.CONFIDENTIAL],
        "ADMIN": [],
    },
    EvidenceRole.ADMINISTRATOR: {
        "VIEW": [EvidenceClassification.PUBLIC, EvidenceClassification.INTERNAL, EvidenceClassification.CONFIDENTIAL, EvidenceClassification.RESTRICTED],
        "EXPORT": [EvidenceClassification.PUBLIC, EvidenceClassification.INTERNAL, EvidenceClassification.CONFIDENTIAL, EvidenceClassification.RESTRICTED],
        "APPROVE": [EvidenceClassification.PUBLIC, EvidenceClassification.INTERNAL, EvidenceClassification.CONFIDENTIAL, EvidenceClassification.RESTRICTED],
        "ADMIN": [EvidenceClassification.PUBLIC, EvidenceClassification.INTERNAL, EvidenceClassification.CONFIDENTIAL, EvidenceClassification.RESTRICTED],
    },
}


class EvidenceAccessController(IEvidenceAccessController):
    """Enforces enterprise RBAC permissions on evidence artifacts."""

    def check_permission(self, role: EvidenceRole, action: str, classification: EvidenceClassification) -> bool:
        perm_map = ROLE_PERMISSIONS.get(role, {})
        allowed_classes = perm_map.get(action.upper(), [])
        return classification in allowed_classes
