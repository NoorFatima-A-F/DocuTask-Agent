"""
Certification Dashboard Engine generating real-time governance overviews.
"""
from __future__ import annotations
from datetime import datetime, timezone, timedelta
from typing import List, Optional
from app.platform_verification.certification_engine.domain.interfaces import (
    ICertificationDashboardEngine,
    ICertificationEngine,
)
from app.platform_verification.certification_engine.domain.models import (
    CertificationDashboardView,
    CertificationRecord,
    CertificationStatus,
    QualityGateDecision,
)


class EnterpriseCertificationDashboardEngine(ICertificationDashboardEngine):
    """Compiles certification metrics, active gates, risk states, and history for dashboards."""

    def __init__(
        self,
        cert_engine: ICertificationEngine,
        recent_decisions: Optional[List[QualityGateDecision]] = None,
    ):
        self.cert_engine = cert_engine
        self.recent_decisions = recent_decisions or []

    def build_dashboard_view(self) -> CertificationDashboardView:
        all_certs = getattr(self.cert_engine, "list_certifications", lambda: [])()
        active_certs = [c for c in all_certs if c.status == CertificationStatus.ACTIVE]
        
        # Expiring soon (within 14 days)
        now_dt = datetime.now(timezone.utc)
        threshold_dt = now_dt + timedelta(days=14)
        expiring_soon = [
            c for c in active_certs if now_dt <= datetime.fromisoformat(c.expires_at) <= threshold_dt
        ]

        # Gate summary counts
        gate_summary = {"passed": 0, "failed": 0, "waived": 0}
        risk_summary = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}

        for dec in self.recent_decisions:
            for g in dec.gate_results:
                if g.passed:
                    gate_summary["passed"] += 1
                else:
                    gate_summary["failed"] += 1
            risk_lvl = dec.risk_assessment.risk_level.value
            risk_summary[risk_lvl] = risk_summary.get(risk_lvl, 0) + 1

        return CertificationDashboardView(
            active_certifications_count=len(active_certs),
            system_certifications=active_certs,
            gate_summary=gate_summary,
            risk_summary=risk_summary,
            pending_approvals_count=sum(1 for d in self.recent_decisions if d.requires_human_approval),
            active_exceptions_count=0,
            expiring_soon_count=len(expiring_soon),
            recent_decisions=self.recent_decisions[:10],
        )
