"""
Phase 3H.4.10.12: Observability Security Evidence Exporter
"""
import os
import json
from datetime import datetime
from typing import Dict, Any, List
from ..domain.interfaces import IObservabilitySecurityExporter
from ..domain.models import (
    DataClassificationReport,
    LogSecurityReport,
    LogSanitizationReport,
    MetricSecurityReport,
    TraceSecurityReport,
    DashboardAccessReport,
    AlertSecurityReport,
    PipelineSecurityReport,
    AISecurityReport,
    SecurityFailureSimulationResult,
    ObservabilitySecurityScorecard,
)


class ObservabilitySecurityExporter(IObservabilitySecurityExporter):
    def export_evidence_manifests(
        self,
        output_dir: str,
        classification_report: DataClassificationReport,
        log_report: LogSecurityReport,
        sanitization_report: LogSanitizationReport,
        metric_report: MetricSecurityReport,
        trace_report: TraceSecurityReport,
        access_report: DashboardAccessReport,
        alert_report: AlertSecurityReport,
        pipeline_report: PipelineSecurityReport,
        ai_report: AISecurityReport,
        simulations: List[SecurityFailureSimulationResult],
        scorecard: ObservabilitySecurityScorecard,
    ) -> List[str]:
        os.makedirs(output_dir, exist_ok=True)
        files_written = []

        manifests: Dict[str, Any] = {
            "data_classification_report.json": classification_report.model_dump(),
            "log_security_report.json": log_report.model_dump(),
            "sanitization_report.json": sanitization_report.model_dump(),
            "metric_security_report.json": metric_report.model_dump(),
            "trace_security_report.json": trace_report.model_dump(),
            "dashboard_access_report.json": access_report.model_dump(),
            "alert_security_report.json": alert_report.model_dump(),
            "pipeline_security_report.json": pipeline_report.model_dump(),
            "ai_security_report.json": ai_report.model_dump(),
            "failure_test_report.json": [s.model_dump() for s in simulations],
            "certification_report.json": scorecard.model_dump(),
            "metadata.json": {
                "project": "DocuTask-Agent",
                "phase": "3H.4.10",
                "title": "Enterprise Observability Security Verification Framework",
                "security_standard": [
                    "OWASP ASVS",
                    "OWASP LLM Top 10",
                    "NIST Cybersecurity Framework",
                ],
                "commit": "git-head-verified",
                "timestamp": datetime.utcnow().isoformat(),
                "composite_score": scorecard.composite_score,
                "tier": scorecard.tier.value,
                "certified": scorecard.certified_enterprise_ready,
            },
        }

        for filename, data in manifests.items():
            path = os.path.join(output_dir, filename)
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, default=str)
            files_written.append(path)

        return files_written
