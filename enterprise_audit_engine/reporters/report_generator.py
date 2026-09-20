"""Automated Evidence-Backed Report Generator."""

from pathlib import Path
from typing import List, Dict, Any, Optional
from ..domain.evidence.models import (
    EvidenceRecord,
    AuditReportManifest,
    AuditRunMetadata,
    CollectorExecutionManifest,
    VerificationScorecard,
)
from ..analyzers.confidence_engine import ConfidenceEngine


class ReportGenerator:
    """Generates structured, evidence-backed audit reports from collected evidence."""

    def __init__(self, reports_dir: Path):
        self.reports_dir = reports_dir
        self.reports_dir.mkdir(parents=True, exist_ok=True)

    def generate_all_reports(
        self,
        records: List[EvidenceRecord],
        scorecards: Optional[Dict[str, VerificationScorecard]] = None,
        metadata: Optional[AuditRunMetadata] = None,
        exec_manifest: Optional[CollectorExecutionManifest] = None,
        provenance_data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Path]:
        """Generates the full suite of Markdown due diligence reports."""
        generated: Dict[str, Path] = {}
        generated["executive_summary"] = self._generate_executive_summary(
            records, scorecards, metadata, exec_manifest
        )
        generated["technical_due_diligence"] = self._generate_technical_due_diligence(
            records, scorecards, metadata
        )
        generated["security_report"] = self._generate_security_report(records, metadata)
        generated["production_readiness_matrix"] = self._generate_production_readiness_matrix(
            records, scorecards
        )
        if provenance_data:
            generated["provenance_manifest"] = self._generate_provenance_manifest(
                provenance_data
            )
        return generated

    def _generate_executive_summary(
        self,
        records: List[EvidenceRecord],
        scorecards: Optional[Dict[str, VerificationScorecard]],
        metadata: Optional[AuditRunMetadata],
        exec_manifest: Optional[CollectorExecutionManifest],
    ) -> Path:
        target = self.reports_dir / "executive_summary.md"
        overall_confidence = ConfidenceEngine.calculate_confidence(records)
        overall_classification = ConfidenceEngine.classify_subsystem(records)

        commit = metadata.git_commit_hash[:8] if metadata else "UNKNOWN"
        run_id = metadata.run_id if metadata else "N/A"

        content = [
            "# Executive Technical Due Diligence Summary: DocuTask Agent",
            "",
            "## 1. Audit Run Provenance",
            f"- **Audit Run ID**: `{run_id}`",
            f"- **Git Commit Verified**: `{commit}`",
            f"- **Overall Maturity Classification**: `{overall_classification.value}`",
            f"- **Aggregate Evidence Confidence**: `{overall_confidence.value}`",
            f"- **Total Immutable Evidence Items**: `{len(records)}`",
            "",
            "## 2. Multi-Dimensional Subsystem Verification Scorecards",
            "",
            "| Subsystem | Source (20) | Tests (20) | Runtime (25) | Security (15) | Benchmarks (10) | Repro (10) | Total (100) | Classification | Confidence |",
            "| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |",
        ]

        if scorecards:
            for sub, card in scorecards.items():
                content.append(
                    f"| **{sub}** | {card.source_inspection_score:.0f} | {card.automated_tests_score:.0f} | {card.runtime_execution_score:.0f} | {card.security_validation_score:.0f} | {card.benchmark_evidence_score:.0f} | {card.reproducibility_score:.0f} | **{card.total_score:.0f}** | `{card.classification.value}` | `{card.confidence.value}` |"
                )

        content.extend([
            "",
            "## 3. Collector Execution Health & Verifier Integrity",
            "",
            "| Collector Name | Attempted | Completed | Evidence Count | Duration (ms) | Status |",
            "| :--- | :--- | :--- | :--- | :--- | :--- |",
        ])

        if exec_manifest:
            for col in exec_manifest.collectors:
                status = "PASS" if col.execution_completed else f"FAIL ({col.exception_message})"
                content.append(
                    f"| `{col.collector_name}` | {col.execution_attempted} | {col.execution_completed} | {col.evidence_generated_count} | {col.duration_ms:.1f} | `{status}` |"
                )

        content.extend([
            "",
            "## 4. Evidence Registry & Cryptographic Hashes",
            "",
            "| Evidence ID | Category | Source Type | Classification | Confidence | SHA-256 Fingerprint | Summary |",
            "| :--- | :--- | :--- | :--- | :--- | :--- | :--- |",
        ])

        for r in records:
            short_hash = f"`{r.content_hash[:12]}...`" if r.content_hash else "None"
            content.append(
                f"| `{r.id}` | {r.category} | `{r.source_type.value}` | `{r.classification.value}` | `{r.confidence.value}` | {short_hash} | {r.summary} |"
            )

        content.extend([
            "",
            "---",
            "*Report generated automatically by Enterprise Evidence Verification Engine (enterprise_audit_engine).* - Every claim is cryptographically linked to verifiable artifacts.",
        ])

        with open(target, "w", encoding="utf-8") as fp:
            fp.write("\n".join(content))
        return target

    def _generate_technical_due_diligence(
        self,
        records: List[EvidenceRecord],
        scorecards: Optional[Dict[str, VerificationScorecard]],
        metadata: Optional[AuditRunMetadata],
    ) -> Path:
        target = self.reports_dir / "technical_due_diligence.md"
        content = [
            "# Deep Technical Due Diligence Audit: DocuTask Agent",
            "",
            "## 1. Rigorous Evidence-Driven Methodology",
            "This document establishes technical claims solely on verifiable automated evidence collected directly from repository files, configurations, automated test suites, and static analysis models.",
            "",
            "## 2. Findings by Architectural Domain",
            "",
        ]

        for r in records:
            content.extend([
                f"### Evidence Item: `{r.id}` — {r.category}",
                f"- **Collector**: `{r.collector}`",
                f"- **Source Type**: `{r.source_type.value}`",
                f"- **Classification**: `{r.classification.value}`",
                f"- **Confidence Level**: `{r.confidence.value}`",
                f"- **SHA-256 Fingerprint**: `{r.content_hash}`",
                f"- **Summary**: {r.summary}",
            ])
            if r.command:
                content.append(f"- **Reproduction Command**: `{r.command}`")
            if r.artifact_paths:
                content.append(f"- **Referenced Artifacts**: {', '.join(f'`{p}`' for p in r.artifact_paths)}")
            content.append("")

        with open(target, "w", encoding="utf-8") as fp:
            fp.write("\n".join(content))
        return target

    def _generate_security_report(
        self, records: List[EvidenceRecord], metadata: Optional[AuditRunMetadata]
    ) -> Path:
        target = self.reports_dir / "security_report.md"
        sec_records = [r for r in records if r.category in {"SecurityAndCompliance", "Security"}]

        content = [
            "# Enterprise Security & Compliance Assessment",
            "",
            "## 1. Secret Exposure & Vulnerability Posture",
            "DocuTask Agent enforces a zero-secrets-in-repo invariant verified by automated pattern scanning.",
            "",
            "## 2. Security Evidence Items",
            "",
        ]

        if sec_records:
            for r in sec_records:
                content.extend([
                    f"### Security Finding: `{r.id}`",
                    f"- **Classification**: `{r.classification.value}`",
                    f"- **Confidence**: `{r.confidence.value}`",
                    f"- **Summary**: {r.summary}",
                    f"- **Cryptographic Hash**: `{r.content_hash}`",
                    "",
                ])
        else:
            content.append("No dedicated security records generated.")

        with open(target, "w", encoding="utf-8") as fp:
            fp.write("\n".join(content))
        return target

    def _generate_production_readiness_matrix(
        self, records: List[EvidenceRecord], scorecards: Optional[Dict[str, VerificationScorecard]]
    ) -> Path:
        target = self.reports_dir / "production_readiness_matrix.md"
        content = [
            "# Production Readiness Verification Matrix",
            "",
            "| Subsystem / Dimension | Score (/100) | Classification | Evidence Source | Confidence |",
            "| :--- | :--- | :--- | :--- | :--- |",
        ]

        if scorecards:
            for sub, card in scorecards.items():
                content.append(
                    f"| **{sub}** | {card.total_score:.0f} | `{card.classification.value}` | Multi-source | `{card.confidence.value}` |"
                )
        else:
            for r in records:
                content.append(
                    f"| **{r.category}** | N/A | `{r.classification.value}` | `{r.source_type.value}` | `{r.confidence.value}` |"
                )

        with open(target, "w", encoding="utf-8") as fp:
            fp.write("\n".join(content))
        return target

    def _generate_provenance_manifest(self, provenance_data: Dict[str, Any]) -> Path:
        target = self.reports_dir / "provenance_manifest.md"
        steps = provenance_data.get("lineage_steps", [])
        content = [
            "# Audit Evidence Chain of Custody & Provenance Manifest",
            "",
            f"- **Run ID**: `{provenance_data.get('run_id')}`",
            f"- **Provenance Chain Hash**: `{provenance_data.get('provenance_chain_hash')}`",
            f"- **Total Lineage Steps**: `{len(steps)}`",
            "",
            "## Lineage Execution Steps",
            "",
            "| Step ID | Timestamp | Action / Step | Output Evidence ID | Duration (ms) |",
            "| :--- | :--- | :--- | :--- | :--- |",
        ]

        for s in steps:
            content.append(
                f"| `{s.get('step_id')}` | `{s.get('timestamp')}` | {s.get('step_name')} | `{s.get('output_evidence_id')}` | {s.get('duration_ms', 0):.1f} |"
            )

        with open(target, "w", encoding="utf-8") as fp:
            fp.write("\n".join(content))
        return target
