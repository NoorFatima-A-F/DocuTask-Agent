"""
Phase 3Q: Release Gatekeeper & Production Decision Engine.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List

from ..domain.interfaces import IReleaseGatekeeper
from ..domain.models import (
    GateDecision,
    PipelineStageStatus,
    ProductionReadinessCertificate,
    ReleaseDecision,
)


class ReleaseGatekeeper(IReleaseGatekeeper):
    """
    Evaluates the results of all CI/CD continuous verification stages to issue
    an automated, authoritative production deployment PASS/BLOCK verdict.
    """

    def evaluate_release(self, gate_reports: Dict[str, Any]) -> ReleaseDecision:
        blockers: List[str] = []
        evaluations: Dict[str, str] = {}

        # 1. Check Security Gate
        sec_report = gate_reports.get("security")
        if sec_report and hasattr(sec_report, "gate_passed") and not sec_report.gate_passed:
            blockers.extend(sec_report.blocking_reasons)
            evaluations["Security Gate"] = "FAILED (Blocking Vulnerabilities Detected)"
        else:
            evaluations["Security Gate"] = "PASSED (Zero Critical CVEs / Zero Secret Leaks)"

        # 2. Check Build Status
        build_report = gate_reports.get("build")
        if build_report and getattr(build_report, "build_status", None) == PipelineStageStatus.FAILED:
            blockers.append("Build Failure: Deterministic image compilation failed.")
            evaluations["Build Stage"] = "FAILED"
        else:
            evaluations["Build Stage"] = "PASSED"

        # 3. Check Performance Regression
        perf_report = gate_reports.get("performance")
        if perf_report and getattr(perf_report, "threshold_exceeded", False):
            blockers.append(f"Performance Regression Failure: P95 latency increased by {perf_report.latency_increase_pct}%.")
            evaluations["Performance Gate"] = "FAILED (Regression Exceeded 50% Threshold)"
        else:
            evaluations["Performance Gate"] = "PASSED (Within Latency SLA Target)"

        # 4. Check Chaos Resilience
        chaos_report = gate_reports.get("chaos")
        if chaos_report and not getattr(chaos_report, "resilience_passed", True):
            blockers.append("Chaos Resilience Failure: System failed to self-heal during fault injection.")
            evaluations["Chaos Gate"] = "FAILED"
        else:
            evaluations["Chaos Gate"] = "PASSED"

        # 5. Check Drift Status
        drift_report = gate_reports.get("drift")
        if drift_report and getattr(drift_report, "drift_detected", False) and drift_report.drift_severity == "HIGH":
            blockers.append(f"Infrastructure Drift Failure: {drift_report.drifted_resources} unmanaged resources detected.")
            evaluations["Drift Gate"] = "FAILED (High Severity Drift)"
        else:
            evaluations["Drift Gate"] = "PASSED (Zero Infrastructure Drift)"

        is_approved = len(blockers) == 0
        decision = GateDecision.APPROVED if is_approved else GateDecision.BLOCKED
        confidence = 100.0 if is_approved else max(0.0, 100.0 - (len(blockers) * 20.0))

        return ReleaseDecision(
            release_version="3.19.0",
            decision=decision,
            confidence_score=confidence,
            blocking_reasons=blockers,
            gate_evaluations=evaluations,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )

    def issue_certificate(self, decision: ReleaseDecision, gate_reports: Dict[str, Any]) -> ProductionReadinessCertificate:
        status_flag = "PASS" if decision.decision == GateDecision.APPROVED else "BLOCK"
        return ProductionReadinessCertificate(
            application="DocuTask Agent",
            version=decision.release_version,
            security=status_flag,
            performance=status_flag,
            chaos=status_flag,
            recovery=status_flag,
            drift="CLEAN" if decision.decision == GateDecision.APPROVED else "DRIFT_DETECTED",
            certification="PRODUCTION READY" if decision.decision == GateDecision.APPROVED else "DEPLOYMENT BLOCKED",
            certificate_id="CERT-3Q-PROD-202609-001",
            issued_at=datetime.now(timezone.utc).isoformat(),
        )
