"""
Phase 3O: Infrastructure Certification Artifact & Evidence Exporter.
"""

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from ..domain.models import (
    CertificationDecision,
    ManifestEntry,
    MaturityAssessment,
    NormalizedEvidenceItem,
    QualityRegressionReport,
    QualityScorecard,
    RawEvidenceBundle,
    RiskAssessmentReport,
    VerificationManifest,
)


class InfrastructureCertificationExporter:
    """
    Exports structured certification artifacts with cryptographic SHA-256 validation
    conforming to the Section 3O.13 storage layout.
    """

    def __init__(self, base_dir: Optional[Union[str, Path]] = None):
        self.set_base_dir(base_dir or "infrastructure_certification")

    def set_base_dir(self, base_dir: Union[str, Path]) -> None:
        self.base_dir = Path(base_dir)
        self.evidence_raw_dir = self.base_dir / "evidence" / "raw_results"
        self.evidence_norm_dir = self.base_dir / "evidence" / "normalized_results"
        self.scoring_dir = self.base_dir / "scoring"
        self.reports_dir = self.base_dir / "reports"
        self.history_dir = self.base_dir / "history"

        for d in [self.evidence_raw_dir, self.evidence_norm_dir, self.scoring_dir, self.reports_dir, self.history_dir]:
            d.mkdir(parents=True, exist_ok=True)

    def _compute_sha256(self, file_path: Path) -> str:
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

    def export_all(
        self,
        raw_bundles: List[RawEvidenceBundle],
        normalized_items: List[NormalizedEvidenceItem],
        scorecard: QualityScorecard,
        risk_report: RiskAssessmentReport,
        decision: CertificationDecision,
        maturity: MaturityAssessment,
        regression: QualityRegressionReport,
        markdown_content: str,
        export_dir: Optional[Union[str, Path]] = None,
    ) -> VerificationManifest:
        if export_dir is not None:
            self.set_base_dir(export_dir)

        # 1. Export Raw Bundles
        for idx, bundle in enumerate(raw_bundles):
            clean_name = bundle.source_phase.lower().replace("/", "_").replace("\\", "_")
            file_path = self.evidence_raw_dir / f"raw_{clean_name}_{idx + 1}.json"
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(bundle.model_dump(), f, indent=2, default=str)

        # 2. Export Normalized Evidence
        norm_path = self.evidence_norm_dir / "normalized_evidence.json"
        with open(norm_path, "w", encoding="utf-8") as f:
            json.dump([item.model_dump() for item in normalized_items], f, indent=2, default=str)

        # 3. Export Scoring
        score_path = self.scoring_dir / "quality_score.json"
        with open(score_path, "w", encoding="utf-8") as f:
            json.dump(scorecard.model_dump(), f, indent=2, default=str)

        maturity_path = self.scoring_dir / "maturity_assessment.json"
        with open(maturity_path, "w", encoding="utf-8") as f:
            json.dump(maturity.model_dump(), f, indent=2, default=str)

        # 4. Export Reports
        cert_report_path = self.reports_dir / "certification_report.json"
        with open(cert_report_path, "w", encoding="utf-8") as f:
            json.dump(decision.model_dump(), f, indent=2, default=str)

        risk_report_path = self.reports_dir / "risk_assessment.json"
        with open(risk_report_path, "w", encoding="utf-8") as f:
            json.dump(risk_report.model_dump(), f, indent=2, default=str)

        regr_report_path = self.reports_dir / "regression_report.json"
        with open(regr_report_path, "w", encoding="utf-8") as f:
            json.dump(regression.model_dump(), f, indent=2, default=str)

        md_report_path = self.reports_dir / "readiness_report.md"
        with open(md_report_path, "w", encoding="utf-8") as f:
            f.write(markdown_content)

        # Also write top-level copy of Infrastructure_Readiness_Report.md for convenience
        with open(self.base_dir / "Infrastructure_Readiness_Report.md", "w", encoding="utf-8") as f:
            f.write(markdown_content)

        # 5. Export History
        history_path = self.history_dir / "previous_scores.json"
        with open(history_path, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "version": "3.17.0",
                    "overall_score": scorecard.overall_score,
                    "certification": decision.certification.value,
                    "categories": {k: v.score for k, v in scorecard.categories.items()},
                    "recorded_at": datetime.now(timezone.utc).isoformat(),
                },
                f,
                indent=2,
                default=str,
            )

        # 6. Build Manifest of All Generated Files
        entries: List[ManifestEntry] = []
        for root, _, files in os.walk(self.base_dir):
            for file_name in files:
                if file_name in ["metadata.json", "manifest.json"]:
                    continue
                full_p = Path(root) / file_name
                rel_p = str(full_p.relative_to(self.base_dir)).replace("\\", "/")
                sha = self._compute_sha256(full_p)
                entries.append(
                    ManifestEntry(
                        filename=rel_p,
                        report_title=full_p.stem.replace("_", " ").title(),
                        sha256=sha,
                        size_bytes=full_p.stat().st_size,
                    )
                )

        manifest = VerificationManifest(
            project="DocuTask-Agent",
            framework="Enterprise Infrastructure Quality & Certification Framework",
            version="3.17.0",
            commit="HEAD",
            environment="Enterprise Production Readiness Lab",
            timestamp=datetime.now(timezone.utc).isoformat(),
            overall_score=scorecard.overall_score,
            certification=decision.certification.value,
            deployment_approved=decision.deployment_approved,
            files=sorted(entries, key=lambda x: x.filename),
        )

        manifest_data = manifest.model_dump()
        for mf_name in ["metadata.json", "manifest.json"]:
            with open(self.base_dir / mf_name, "w", encoding="utf-8") as f:
                json.dump(manifest_data, f, indent=2, default=str)

        return manifest
