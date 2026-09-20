"""
Phase 3H.5.6: Evidence Exporter for Failure Learning & Recovery Optimization
"""
import os
import json
import hashlib
from datetime import datetime, timezone
from typing import List, Dict, Any
from ..domain.models import (
    FailureEventReport,
    RootCauseReport,
    PatternAnalysisReport,
    KnowledgeBaseReport,
    RecoveryOptimizationReport,
    PolicyImprovementReport,
    FailurePreventionReport,
    SimulationReport,
    FailureLearningScorecard,
)


class FailureLearningExporter:
    def export_evidence_manifests(
        self,
        output_dir: str,
        event_report: FailureEventReport,
        rca_report: RootCauseReport,
        pattern_report: PatternAnalysisReport,
        kb_report: KnowledgeBaseReport,
        optimization_report: RecoveryOptimizationReport,
        policy_report: PolicyImprovementReport,
        prevention_report: FailurePreventionReport,
        simulation_report: SimulationReport,
        scorecard: FailureLearningScorecard,
    ) -> List[str]:
        os.makedirs(output_dir, exist_ok=True)
        exported_files: List[str] = []

        manifest_map: Dict[str, Any] = {
            "failure_events_report.json": event_report.model_dump(),
            "root_cause_report.json": rca_report.model_dump(),
            "pattern_analysis_report.json": pattern_report.model_dump(),
            "knowledge_base_report.json": kb_report.model_dump(),
            "recovery_optimization_report.json": optimization_report.model_dump(),
            "policy_improvement_report.json": policy_report.model_dump(),
            "prevention_report.json": prevention_report.model_dump(),
            "simulation_report.json": simulation_report.model_dump(),
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
            "phase": "3H.5.6",
            "component": "failure_learning_rca_optimization",
            "timestamp": now_iso,
            "environment": "production_verification",
            "composite_score": scorecard.composite_score,
            "tier": scorecard.tier.value,
            "certified_enterprise_ready": scorecard.certified_enterprise_ready,
            "manifest_hashes": file_hashes,
        }

        meta_filepath = os.path.join(output_dir, "metadata.json")
        with open(meta_filepath, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2)
        exported_files.append(meta_filepath)

        return exported_files
