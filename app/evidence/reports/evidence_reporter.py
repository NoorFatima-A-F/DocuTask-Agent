"""
Evidence Reporter for Enterprise AAOS.
Generates automated evidence matrices, evidence graphs, indices,
and master forensic reports linking claims directly to verified evidence.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

from app.evidence.registry.evidence_models import EvidenceItem, VerificationStatus
from app.evidence.registry.evidence_registry import EvidenceRegistry
from app.evidence.traceability.traceability_engine import EvidenceTraceabilityEngine

logger = logging.getLogger(__name__)


class EvidenceReporter:
    """Generates human and machine-readable evidence documentation."""

    def __init__(self, registry: EvidenceRegistry, traceability: EvidenceTraceabilityEngine) -> None:
        self.registry = registry
        self.traceability = traceability

    def generate_evidence_matrix_md(self) -> str:
        """Generates evidence_matrix.md mapping every evidence item to its type and metrics."""
        items = self.registry.list_all()
        lines = [
            "# Master Evidence Matrix",
            f"**Total Verified Evidence Items**: `{len(items)}`",
            "",
            "| Evidence ID | Title | Type | Source | Verification | Reproducibility | Hash (SHA-256) |",
            "| :--- | :--- | :---: | :--- | :---: | :---: | :--- |",
        ]
        for it in items:
            h_short = it.item_hash[:12] + "..."
            lines.append(
                f"| `{it.evidence_id}` | {it.title} | `{it.evidence_type.value}` | `{it.source}` | `{it.verification_status.value}` | `{it.reproducibility}` | `{h_short}` |"
            )
        return "\n".join(lines)

    def generate_traceability_matrix_md(self) -> str:
        """Generates markdown traceability report linking claims to evidence."""
        claims = self.traceability.list_all_claims()
        lines = [
            "# Claim-to-Evidence Traceability Matrix",
            f"**Total Claims Tracked**: `{len(claims)}` | **Fully Verified Claims**: `{sum(1 for c in claims if c.is_verified)}`",
            "",
            "| Claim ID | Subsystem | Narrative Claim | Status | Supporting Evidence IDs | Source & Test Files |",
            "| :--- | :--- | :--- | :---: | :--- | :--- |",
        ]
        for c in claims:
            status = "VERIFIED" if c.is_verified else "UNVERIFIED"
            evi_links = ", ".join(f"`{eid}`" for eid in c.supporting_evidence_ids)
            src_links = ", ".join(f"`{sf}`" for sf in c.source_files + c.test_files)
            lines.append(
                f"| `{c.claim_id}` | **{c.subsystem}** | {c.claim_text} | `{status}` | {evi_links} | {src_links} |"
            )
        return "\n".join(lines)

    def export_all_reports(self, output_dir: Path) -> None:
        """Exports all evidence reports to disk."""
        output_dir.mkdir(parents=True, exist_ok=True)

        matrix_md = self.generate_evidence_matrix_md()
        with open(output_dir / "evidence_matrix.md", "w", encoding="utf-8") as f:
            f.write(matrix_md)

        trace_md = self.generate_traceability_matrix_md()
        with open(output_dir / "claim_traceability_matrix.md", "w", encoding="utf-8") as f:
            f.write(trace_md)

        logger.info("Exported evidence reports to %s", output_dir)
