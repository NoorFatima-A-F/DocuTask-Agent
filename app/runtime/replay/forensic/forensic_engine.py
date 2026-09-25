"""
Forensic Engine for Phase 13.4 (AESMR-EAIP).
Master coordinator for mission forensic investigation, root cause discovery, and anomaly backtracking.
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class ForensicInvestigationReport(BaseModel):
    mission_id: str
    investigation_id: str
    target_event_id: Optional[str] = None
    findings_count: int = 0
    root_cause_summary: Optional[Dict[str, Any]] = None
    anomalies_detected: List[Dict[str, Any]] = Field(default_factory=list)
    causal_chain: List[Dict[str, Any]] = Field(default_factory=list)
    confidence_decay_points: List[Dict[str, Any]] = Field(default_factory=list)
    recommendations: List[str] = Field(default_factory=list)


class ForensicEngine:
    """
    Coordinates forensic investigation into mission executions.
    """

    @classmethod
    def investigate_mission(
        cls,
        mission_id: str,
        events: List[Dict[str, Any]],
        target_event_id: Optional[str] = None,
    ) -> ForensicInvestigationReport:
        import uuid

        report = ForensicInvestigationReport(
            mission_id=mission_id,
            investigation_id=f"inv_{uuid.uuid4().hex[:10]}",
            target_event_id=target_event_id,
        )

        prev_conf = 1.0
        for idx, ev in enumerate(events):
            evt_type = ev.get("event_type", "")
            payload = ev.get("payload", {})

            # Detect failures/anomalies
            if "fail" in evt_type or "error" in evt_type or payload.get("status") == "FAILED":
                report.anomalies_detected.append({
                    "event_id": ev.get("event_id"),
                    "index": idx,
                    "type": "EXECUTION_FAILURE",
                    "details": payload,
                    "timestamp": ev.get("timestamp"),
                })
                if not report.root_cause_summary:
                    report.root_cause_summary = {
                        "primary_fault_event_id": ev.get("event_id"),
                        "category": payload.get("error_category", "WORKER_ERROR"),
                        "message": payload.get("error_message", "Task execution failure"),
                    }

            # Detect confidence drops
            conf = payload.get("overall_score") or payload.get("confidence")
            if conf is not None and conf < prev_conf - 0.05:
                report.confidence_decay_points.append({
                    "event_id": ev.get("event_id"),
                    "score_before": prev_conf,
                    "score_after": conf,
                    "delta": round(conf - prev_conf, 4),
                    "reason": payload.get("reason", "Feature degradation"),
                })
            if conf is not None:
                prev_conf = conf

            # Trace causal links
            if ev.get("causation_id") or ev.get("correlation_id"):
                report.causal_chain.append({
                    "event_id": ev.get("event_id"),
                    "parent_id": ev.get("causation_id"),
                    "type": evt_type,
                })

        report.findings_count = len(report.anomalies_detected) + len(report.confidence_decay_points)
        if not report.anomalies_detected:
            report.recommendations.append("Mission executed within nominal parameters; no invariant violations found.")
        else:
            report.recommendations.append("Inspect primary fault event and verify worker isolation boundary.")

        return report
