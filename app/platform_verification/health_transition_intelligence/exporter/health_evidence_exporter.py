"""
Health Evidence Exporter (Part 3H.3.3.14).
Persists structured audit artifacts to the health_verification/ directory.
"""
import os
import json
from datetime import datetime, timezone
from dataclasses import asdict
from typing import Dict, Any, List
from app.platform_verification.health_transition_intelligence.domain.models import (
    StateMachineReport,
    HealthEvent,
    DegradationReport,
    RecoveryValidationReport,
    FlappingReport,
    IncidentTimeline,
    AlertingReport,
    HealthIntelligenceScorecard,
)


class HealthEvidenceExporter:
    """
    Persists structured audit artifacts for Part 3H.3.3.
    """

    def __init__(self, output_dir: str = "health_verification"):
        self.output_dir = output_dir

    def _ensure_dir(self):
        os.makedirs(self.output_dir, exist_ok=True)

    def _write_json(self, filename: str, data: Dict[str, Any]) -> str:
        self._ensure_dir()
        file_path = os.path.join(self.output_dir, filename)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, default=str)
        return file_path

    def export_all(
        self,
        sm_report: StateMachineReport,
        events: List[HealthEvent],
        deg_report: DegradationReport,
        rec_report: RecoveryValidationReport,
        flapping_report: FlappingReport,
        timeline: IncidentTimeline,
        alert_report: AlertingReport,
        scorecard: HealthIntelligenceScorecard,
    ) -> Dict[str, str]:
        exported = {}

        # 1. state_machine_report.json
        exported["state_machine_report.json"] = self._write_json(
            "state_machine_report.json",
            asdict(sm_report),
        )

        # 2. transition_history.json
        exported["transition_history.json"] = self._write_json(
            "transition_history.json",
            {
                "total_transitions": len(events),
                "events": [asdict(e) for e in events],
            },
        )

        # 3. degradation_report.json
        exported["degradation_report.json"] = self._write_json(
            "degradation_report.json",
            asdict(deg_report),
        )

        # 4. recovery_report.json
        exported["recovery_report.json"] = self._write_json(
            "recovery_report.json",
            asdict(rec_report),
        )

        # 5. flapping_report.json
        exported["flapping_report.json"] = self._write_json(
            "flapping_report.json",
            asdict(flapping_report),
        )

        # 6. incident_timeline.json
        exported["incident_timeline.json"] = self._write_json(
            "incident_timeline.json",
            asdict(timeline),
        )

        # 7. alerting_report.json
        exported["alerting_report.json"] = self._write_json(
            "alerting_report.json",
            asdict(alert_report),
        )

        # 8. metadata.json
        exported["metadata.json"] = self._write_json(
            "metadata.json",
            {
                "phase": "3H.3.3",
                "component": "Health State Intelligence",
                "status": "PASS" if scorecard.passed else "FAIL",
                "score": scorecard.overall_score,
                "tier": scorecard.certification_tier.value,
                "verdict": scorecard.certification_verdict,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "total_artifacts": 8,
            },
        )

        return exported
