"""
Verification Maturity Model Engine managing Level 0 through Level 7 component inventories.
"""
from __future__ import annotations
from typing import Dict, List, Optional
from datetime import datetime, timezone
from app.platform_verification.pyramid_engine.domain.models import (
    VerificationLevel,
    ComponentCoverageItem,
    FailureSeverity,
)


class MaturityEngine:
    """Manages platform component inventory and tracks verification maturity levels."""

    def __init__(self) -> None:
        self._inventory: Dict[str, ComponentCoverageItem] = {}
        self._load_default_platform_components()

    def register_component(
        self, name: str, owner: str, risk_level: FailureSeverity, missing_coverage: Optional[List[str]] = None
    ) -> ComponentCoverageItem:
        item = ComponentCoverageItem(
            component_name=name,
            owner=owner,
            risk_level=risk_level,
            current_level=VerificationLevel.L0_NOT_TESTED,
            missing_coverage=missing_coverage or ["Unit Tests", "Component Tests", "Integration Tests"],
            is_verified=False,
        )
        self._inventory[name] = item
        return item

    def update_component_maturity(
        self, component_name: str, level: VerificationLevel, is_verified: bool = True
    ) -> ComponentCoverageItem:
        if component_name not in self._inventory:
            raise KeyError(f"Component '{component_name}' not found in verification inventory.")
        comp = self._inventory[component_name]
        comp.current_level = level
        comp.is_verified = is_verified
        comp.last_verified_at = datetime.now(timezone.utc).isoformat()
        return comp

    def list_all_components(self) -> List[ComponentCoverageItem]:
        return list(self._inventory.values())

    def get_unverified_components(self) -> List[ComponentCoverageItem]:
        """Returns Level 0 unverified components."""
        return [c for c in self._inventory.values() if c.current_level == VerificationLevel.L0_NOT_TESTED or not c.is_verified]

    def _load_default_platform_components(self) -> None:
        defaults = [
            ("ocr_preprocessing_engine", "ocr_team", FailureSeverity.HIGH),
            ("ai_extraction_pipeline", "ai_team", FailureSeverity.CRITICAL),
            ("agent_orchestration_core", "platform_team", FailureSeverity.CRITICAL),
            ("document_validator", "qa_team", FailureSeverity.HIGH),
            ("security_auth_gateway", "security_team", FailureSeverity.CRITICAL),
            ("evidence_cas_store", "storage_team", FailureSeverity.HIGH),
            ("metrics_evaluation_engine", "eval_team", FailureSeverity.MEDIUM),
            ("reporting_service", "reporting_team", FailureSeverity.LOW),
        ]
        for name, owner, risk in defaults:
            self.register_component(name, owner, risk)
