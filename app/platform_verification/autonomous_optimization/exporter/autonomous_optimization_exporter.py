"""
Phase 3H.10: Evidence Exporter for Autonomous Operational Intelligence & Self-Optimization
"""
import os
import json
import hashlib
from typing import Dict, Any
from datetime import datetime, timezone
from ..domain.models import (
    OperationalGraphReport,
    SignalCorrelationReport,
    TrendAnalysisReport,
    PredictiveReliabilityReport,
    OptimizationRecommendationsReport,
    AutonomousExecutionReport,
    ExplainabilityReport,
    LearningEffectivenessReport,
    GovernanceReport,
    CertificationReport,
)
from ..domain.interfaces import IAutonomousOptimizationExporter


class AutonomousOptimizationExporter(IAutonomousOptimizationExporter):
    """
    Exports 10 standardized JSON evidence reports plus signed metadata.json with SHA-256 digests.
    """

    def export_all_reports(
        self,
        output_dir: str,
        graph_report: OperationalGraphReport,
        correlation_report: SignalCorrelationReport,
        trend_report: TrendAnalysisReport,
        predictive_report: PredictiveReliabilityReport,
        recommendations_report: OptimizationRecommendationsReport,
        execution_report: AutonomousExecutionReport,
        explainability_report: ExplainabilityReport,
        learning_report: LearningEffectivenessReport,
        governance_report: GovernanceReport,
        certification_report: CertificationReport,
    ) -> Dict[str, Any]:
        os.makedirs(output_dir, exist_ok=True)

        report_payloads = {
            "operational_graph_report.json": graph_report.model_dump(mode="json"),
            "signal_correlation_report.json": correlation_report.model_dump(mode="json"),
            "trend_analysis_report.json": trend_report.model_dump(mode="json"),
            "predictive_reliability_report.json": predictive_report.model_dump(mode="json"),
            "optimization_recommendations.json": recommendations_report.model_dump(mode="json"),
            "autonomous_execution_report.json": execution_report.model_dump(mode="json"),
            "explainability_report.json": explainability_report.model_dump(mode="json"),
            "learning_effectiveness_report.json": learning_report.model_dump(mode="json"),
            "governance_report.json": governance_report.model_dump(mode="json"),
            "certification_report.json": certification_report.model_dump(mode="json"),
        }

        manifest: Dict[str, str] = {}
        for filename, data in report_payloads.items():
            filepath = os.path.join(output_dir, filename)
            content_str = json.dumps(data, indent=2)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content_str)
            sha256_hash = hashlib.sha256(content_str.encode("utf-8")).hexdigest()
            manifest[filename] = sha256_hash

        metadata = {
            "framework_phase": "Phase 3H.10 — Autonomous Operational Intelligence & Self-Optimization Verification Framework",
            "exported_at": datetime.now(timezone.utc).isoformat(),
            "overall_score_pct": certification_report.overall_score_pct,
            "certification_tier": certification_report.certification_tier.value,
            "certification_granted": certification_report.certification_granted,
            "total_artifacts": len(manifest),
            "manifest_sha256": manifest,
            "auditor": certification_report.auditor,
        }

        meta_path = os.path.join(output_dir, "metadata.json")
        meta_str = json.dumps(metadata, indent=2)
        with open(meta_path, "w", encoding="utf-8") as f:
            f.write(meta_str)

        return metadata
