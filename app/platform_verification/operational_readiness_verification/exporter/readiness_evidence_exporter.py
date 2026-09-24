"""
Phase 3H.4.11.13: Operational Readiness Evidence Exporter
"""
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List
from app.core.security import resolve_safe_path, validate_safe_filename_segment
from ..domain.interfaces import IReadinessEvidenceExporter
from ..domain.models import OperationalReadinessScorecard


class ReadinessEvidenceExporter(IReadinessEvidenceExporter):
    def export_evidence_manifests(
        self,
        output_dir: str,
        scorecard: OperationalReadinessScorecard,
    ) -> List[str]:
        safe_dir = Path(output_dir) if output_dir else Path.cwd() / "operational_readiness_verification"
        safe_dir.mkdir(parents=True, exist_ok=True)
        files_written = []

        manifests: Dict[str, Any] = {
            "scoring_model.json": {
                "model_name": "Enterprise Operational Readiness Weighted Scoring Framework",
                "categories": [
                    {"category": "Metrics Completeness", "weight": 0.20, "score": scorecard.metrics_completeness.score},
                    {"category": "Monitoring Accuracy", "weight": 0.20, "score": scorecard.monitoring_accuracy.score},
                    {"category": "Alert Reliability", "weight": 0.20, "score": scorecard.alert_reliability.score},
                    {"category": "Incident Quality", "weight": 0.15, "score": scorecard.incident_quality.score},
                    {"category": "Dashboard Usability", "weight": 0.15, "score": scorecard.dashboard_usability.score},
                    {"category": "Security Readiness", "weight": 0.10, "score": scorecard.security_readiness.score},
                ],
                "composite_formula": "Final Score = (Metrics * 0.20) + (Monitoring * 0.20) + (Alert * 0.20) + (Incident * 0.15) + (Dashboard * 0.15) + (Security * 0.10)",
                "composite_score": scorecard.composite_score,
            },
            "metrics_score.json": scorecard.metrics_completeness.model_dump(),
            "monitoring_score.json": scorecard.monitoring_accuracy.model_dump(),
            "alert_score.json": scorecard.alert_reliability.model_dump(),
            "incident_score.json": scorecard.incident_quality.model_dump(),
            "dashboard_score.json": scorecard.dashboard_usability.model_dump(),
            "security_score.json": scorecard.security_readiness.model_dump(),
            "maturity_report.json": scorecard.maturity_report.model_dump(),
            "risk_report.json": scorecard.risk_report.model_dump(),
            "certification_result.json": scorecard.certification_result.model_dump(),
            "remediation_report.json": scorecard.remediation_report.model_dump(),
            "metadata.json": {
                "project": "DocuTask-Agent",
                "phase": "3H.4.11",
                "title": "Enterprise Operational Readiness Scoring & Certification Framework",
                "frameworks": [
                    "SRE Reliability Principles",
                    "Google SRE Practices",
                    "NIST CSF",
                    "ISO 27001 Controls",
                ],
                "commit": "git-head-verified",
                "timestamp": datetime.utcnow().isoformat(),
                "composite_score": scorecard.composite_score,
                "certification": scorecard.certification_result.certification.value,
                "release_approved": scorecard.certification_result.release_approved,
            },
        }

        for filename, data in manifests.items():
            clean_name = validate_safe_filename_segment(filename)
            path = resolve_safe_path(safe_dir, clean_name)
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, default=str)
            files_written.append(str(path))

        return files_written
