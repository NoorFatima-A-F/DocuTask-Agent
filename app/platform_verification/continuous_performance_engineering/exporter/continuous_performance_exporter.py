"""
Phase 3J.12: Continuous Performance Engineering Evidence & Artifact Exporter.
"""

import hashlib
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from ..domain.models import (
    BaseVerificationReport,
    ContinuousPerformanceScorecard,
    ManifestEntry,
    VerificationManifest,
)


class ContinuousPerformanceExporter:
    """Exports signed, traceable JSON artifacts for continuous performance engineering with SHA-256 validation."""

    PHASE_FILENAME_MAP = {
        r"3j\.12\.1(?!\d)": ["architecture_report.json", "continuous_performance_architecture_report.json"],
        r"3j\.12\.2(?!\d)": ["baseline_report.json", "performance_baseline_report.json"],
        r"3j\.12\.3(?!\d)": ["benchmark_report.json", "benchmark_execution_report.json"],
        r"3j\.12\.4(?!\d)": ["regression_report.json", "performance_regression_report.json"],
        r"3j\.12\.5(?!\d)": ["impact_analysis.json", "change_impact_analysis_report.json"],
        r"3j\.12\.6(?!\d)": ["quality_gate_report.json", "performance_gate_report.json"],
        r"3j\.12\.7(?!\d)": ["environment_comparison.json", "environment_performance_comparison.json", "multi_environment_comparison_report.json"],
        r"3j\.12\.8(?!\d)": ["knowledge_repository.json", "performance_knowledge_report.json"],
        r"3j\.12\.9(?!\d)": ["trend_analysis.json", "performance_trend_report.json"],
        r"3j\.12\.10(?!\d)": ["dashboard_report.json", "performance_dashboard_report.json"],
        r"3j\.12\.11(?!\d)": ["cicd_report.json", "cicd_performance_pipeline_report.json"],
        r"3j\.12\.12(?!\d)": ["experiment_report.json", "performance_experiment_report.json"],
    }

    def __init__(self, export_dir: Optional[str] = None):
        if export_dir:
            self.export_dir = Path(export_dir)
        else:
            self.export_dir = Path("continuous_performance_verification")
        self.export_dir.mkdir(parents=True, exist_ok=True)

    def _compute_sha256(self, file_path: Path) -> str:
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

    def export_report(self, report: BaseVerificationReport) -> List[Path]:
        written_paths: List[Path] = []
        report_data = report.model_dump()
        target_filenames: List[str] = []

        for pattern, filenames in self.PHASE_FILENAME_MAP.items():
            if re.search(pattern, report.phase_id, re.IGNORECASE) or re.search(pattern, report.verifier_id, re.IGNORECASE):
                target_filenames.extend(filenames)
                break

        if not target_filenames:
            safe_name = report.verifier_id.lower().replace("verify-", "").replace("-", "_")
            target_filenames = [f"{safe_name}.json"]

        for filename in target_filenames:
            file_path = self.export_dir / filename
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(report_data, f, indent=2, default=str)
            written_paths.append(file_path)

        return written_paths

    def export_scorecard(self, scorecard: ContinuousPerformanceScorecard) -> List[Path]:
        scorecard_data = scorecard.model_dump()
        filenames = ["scorecard.json", "continuous_performance_scorecard.json"]
        paths: List[Path] = []
        for filename in filenames:
            file_path = self.export_dir / filename
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(scorecard_data, f, indent=2, default=str)
            paths.append(file_path)
        return paths

    def generate_manifest(
        self,
        scorecard: ContinuousPerformanceScorecard,
        reports: List[BaseVerificationReport],
    ) -> VerificationManifest:
        manifest_entries: List[ManifestEntry] = []

        for item in sorted(self.export_dir.iterdir()):
            if item.is_file() and item.name not in ["metadata.json", "manifest.json"]:
                sha = self._compute_sha256(item)
                size = item.stat().st_size
                manifest_entries.append(
                    ManifestEntry(
                        filename=item.name,
                        report_title=item.stem.replace("_", " ").title(),
                        sha256=sha,
                        size_bytes=size,
                    )
                )

        manifest = VerificationManifest(
            system="DocuTask Agent",
            version="3.12.0",
            commit="HEAD",
            environment="Continuous Performance Engineering Platform",
            timestamp=datetime.now(timezone.utc).isoformat(),
            overall_score=scorecard.overall_score,
            certification_tier=scorecard.certification_tier.value,
            files=manifest_entries,
        )

        manifest_data = manifest.model_dump()
        for mf in ["metadata.json", "manifest.json"]:
            mf_path = self.export_dir / mf
            with open(mf_path, "w", encoding="utf-8") as f:
                json.dump(manifest_data, f, indent=2, default=str)

        return manifest
