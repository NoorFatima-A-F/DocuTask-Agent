"""
Phase 3H.5.7: Evidence Exporter for Reliability Intelligence
"""
import os
import json
import hashlib
from datetime import datetime, timezone
from typing import List, Dict, Any
from ..domain.models import (
    ReliabilityDataCollectionReport,
    ComponentReliabilityScoreReport,
    SystemReliabilityHealthReport,
    SLOComplianceReport,
    ErrorBudgetReport,
    ReliabilityRiskReport,
    ResilienceRecommendationReport,
    ChaosValidationReport,
    ReliabilityTrendReport,
    ReliabilityGovernanceReport,
    ReliabilityScorecard,
)


class ReliabilityIntelligenceExporter:
    def export_evidence_manifests(
        self,
        output_dir: str,
        data_report: ReliabilityDataCollectionReport,
        comp_report: ComponentReliabilityScoreReport,
        health_report: SystemReliabilityHealthReport,
        slo_report: SLOComplianceReport,
        budget_report: ErrorBudgetReport,
        risk_report: ReliabilityRiskReport,
        rec_report: ResilienceRecommendationReport,
        chaos_report: ChaosValidationReport,
        trend_report: ReliabilityTrendReport,
        gov_report: ReliabilityGovernanceReport,
        scorecard: ReliabilityScorecard,
    ) -> List[str]:
        os.makedirs(output_dir, exist_ok=True)
        exported_files: List[str] = []

        manifest_map: Dict[str, Any] = {
            "data_collection_report.json": data_report.model_dump(),
            "component_score_report.json": comp_report.model_dump(),
            "health_score_report.json": health_report.model_dump(),
            "slo_report.json": slo_report.model_dump(),
            "error_budget_report.json": budget_report.model_dump(),
            "risk_analysis_report.json": risk_report.model_dump(),
            "recommendation_report.json": rec_report.model_dump(),
            "chaos_validation_report.json": chaos_report.model_dump(),
            "trend_report.json": trend_report.model_dump(),
            "governance_report.json": gov_report.model_dump(),
            "certification_report.json": scorecard.model_dump(),
        }

        # Calculate integrity hashes
        file_hashes = {}
        for filename, data in manifest_map.items():
            filepath = os.path.join(output_dir, filename)
            content_str = json.dumps(data, indent=2, default=str)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content_str)
            exported_files.append(filepath)
            sha = hashlib.sha256(content_str.encode("utf-8")).hexdigest()
            file_hashes[filename] = sha

        # Metadata manifest
        now_iso = datetime.now(timezone.utc).isoformat()
        metadata = {
            "project": "DocuTask-Agent",
            "phase": "3H.5.7",
            "capability": "Reliability Intelligence",
            "environment": "production_verification",
            "timestamp": now_iso,
            "overall_health_score": health_report.overall_health_score,
            "composite_score": scorecard.composite_score,
            "tier": scorecard.tier,
            "certified_enterprise_ready": scorecard.certified_enterprise_ready,
            "manifest_hashes": file_hashes,
        }

        meta_filepath = os.path.join(output_dir, "metadata.json")
        with open(meta_filepath, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2)
        exported_files.append(meta_filepath)

        return exported_files
