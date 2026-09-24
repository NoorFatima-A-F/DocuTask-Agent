"""Auditor Simulation Engine.

Orchestrates multi-perspective technical reviews simulating external auditors,
aggregating verdicts, blocking ungrounded claims, and computing consensus scores.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from pydantic import BaseModel, Field
from .personas import AuditorPersonas, PersonaReviewResult


class AuditorSimulationReport(BaseModel):
    """Consolidated report across all simulated auditor personas."""
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    target_system: str
    target_version: str
    consensus_score: float
    consensus_passed: bool
    status: str  # AUDITOR_CONSENSUS_APPROVED, AUDITOR_REVIEW_BLOCKED
    persona_reviews: Dict[str, PersonaReviewResult] = Field(default_factory=dict)
    all_blocked_claims: List[str] = Field(default_factory=list)
    all_required_actions: List[str] = Field(default_factory=list)
    total_findings_count: int = 0


class AuditorSimulator:
    """Runs simulated multi-persona audits on evidence repositories."""

    @classmethod
    def run_simulation(
        cls,
        evidence_items: List[Dict[str, Any]],
        metrics: Optional[Dict[str, Any]] = None,
        target_system: str = "DocuTask Agent",
        target_version: str = "v1.0.0",
    ) -> AuditorSimulationReport:
        metrics = metrics or {}
        
        pe_res = AuditorPersonas.review_as_principal_engineer(evidence_items, metrics)
        sec_res = AuditorPersonas.review_as_security_auditor(evidence_items, metrics)
        cto_res = AuditorPersonas.review_as_cto(evidence_items, metrics)
        dd_res = AuditorPersonas.review_as_due_diligence_team(evidence_items, metrics)

        reviews = {
            "PrincipalEngineer": pe_res,
            "SecurityAuditor": sec_res,
            "CTOReviewer": cto_res,
            "DueDiligenceTeam": dd_res,
        }

        all_blocked = set()
        all_actions = set()
        total_findings = 0
        total_scores = 0.0

        for r in reviews.values():
            all_blocked.update(r.blocked_claims)
            all_actions.update(r.required_actions)
            total_findings += len(r.findings)
            total_scores += r.review_score

        consensus_score = round(total_scores / len(reviews), 2)
        consensus_passed = all(r.passed for r in reviews.values()) and consensus_score >= 80.0

        return AuditorSimulationReport(
            target_system=target_system,
            target_version=target_version,
            consensus_score=consensus_score,
            consensus_passed=consensus_passed,
            status="AUDITOR_CONSENSUS_APPROVED" if consensus_passed else "AUDITOR_REVIEW_BLOCKED",
            persona_reviews=reviews,
            all_blocked_claims=sorted(list(all_blocked)),
            all_required_actions=sorted(list(all_actions)),
            total_findings_count=total_findings,
        )
