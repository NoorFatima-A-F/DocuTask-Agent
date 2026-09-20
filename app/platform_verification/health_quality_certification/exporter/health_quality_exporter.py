"""
Phase 3H.5.11: Health Quality Evidence Exporter
"""
import os
import json
import hashlib
from typing import Dict, Any
from datetime import datetime, timezone

from ..domain.models import (
    ScoringModelDefinition,
    HealthQualityScorecard,
)


class HealthQualityExporter:
    """
    Exports standardized certification reports, category scores, SRE metrics,
    regression comparisons, deployment gates, and metadata.json with SHA-256 hashes.
    """

    def __init__(self, output_dir: str = "health_quality_certification"):
        self.output_dir = output_dir

    def _compute_sha256(self, file_path: str) -> str:
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

    def export_all(self, scorecard: HealthQualityScorecard) -> Dict[str, str]:
        os.makedirs(self.output_dir, exist_ok=True)

        scoring_def = ScoringModelDefinition()

        artifacts = {
            "scoring_model.json": scoring_def.model_dump(),
            "category_scores.json": [c.model_dump() for c in scorecard.category_scores],
            "reliability_metrics_report.json": scorecard.sre_metrics.model_dump(),
            "regression_report.json": scorecard.regression_report.model_dump(),
            "certification_report.json": scorecard.certification_report.model_dump(),
            "deployment_gate_report.json": scorecard.deployment_gate.model_dump(),
        }

        generated_files = {}
        for filename, data in artifacts.items():
            filepath = os.path.join(self.output_dir, filename)
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            generated_files[filename] = filepath

        # Calculate checksums for metadata.json
        checksums = {}
        for filename, filepath in generated_files.items():
            checksums[filename] = self._compute_sha256(filepath)

        metadata = {
            "project": "DocuTask-Agent",
            "phase": "3H.5.11 — Enterprise Health Quality Scoring & Operational Certification Framework",
            "verification_id": scorecard.verification_id,
            "environment": "production-readiness-verification",
            "version": "1.0.0",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "overall_score": scorecard.overall_score,
            "maturity_level": scorecard.maturity_level.value,
            "certification_status": scorecard.certification_status.value,
            "passed": scorecard.passed,
            "deployment_decision": scorecard.deployment_gate.decision.value,
            "file_manifest": checksums,
        }

        metadata_path = os.path.join(self.output_dir, "metadata.json")
        with open(metadata_path, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2)

        generated_files["metadata.json"] = metadata_path
        return generated_files
