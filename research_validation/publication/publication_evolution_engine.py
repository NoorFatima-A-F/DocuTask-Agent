"""
Publication Evolution Engine (Phase 92C)
========================================
Dynamically updates publication reports, LaTeX tables, figures, and claims
when new empirical evidence is validated, recording full cryptographic provenance.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

from research_validation.publication.publication_diff import (
    PublicationDiffItem, PublicationEvolutionReport
)
from research_validation.provenance.hashing import hash_canonical_json


@dataclass(frozen=True)
class PublicationDraft:
    """Complete publication state with embedded cryptographic evidence bindings."""
    version: str
    title: str
    claims: Dict[str, str]
    table_data: Dict[str, Dict[str, float]]
    limitations: List[str]
    markdown_content: str
    latex_content: str
    publication_digest_sha256: str = field(default="")


class PublicationEvolutionEngine:
    """
    Automates continuous publication synchronization with underlying scientific evidence.
    """

    def __init__(self, base_version: str = "1.0.0"):
        self.current_version = base_version
        self.drafts: Dict[str, PublicationDraft] = {}

    def synthesize_draft(
        self,
        version: str,
        title: str,
        claims: Dict[str, str],
        table_data: Dict[str, Dict[str, float]],
        limitations: List[str],
        evidence_digests: Dict[str, str],
    ) -> PublicationDraft:
        """Constructs a publication draft bound to evidence digests."""
        # 1. Build Markdown Document
        md_lines = [
            f"# {title}",
            f"**Version**: {version} | **Generated**: {datetime.now(timezone.utc).isoformat()}",
            "",
            "## 1. Verified Scientific Claims",
        ]
        for c_name, c_text in claims.items():
            ev = evidence_digests.get(c_name, "NOT_TRACEABLE")
            md_lines.append(f"### Claim: {c_name}")
            md_lines.append(f"{c_text}")
            md_lines.append(f"> **Evidence Digest**: `{ev}`")
            md_lines.append("")

        md_lines.append("## 2. Empirical Results")
        md_lines.append("| Model / Metric | Baseline | Observed | Delta |")
        md_lines.append("| :--- | ---: | ---: | ---: |")
        for row_key, vals in table_data.items():
            b = vals.get("baseline", 0.0)
            o = vals.get("observed", 0.0)
            d = o - b
            md_lines.append(f"| {row_key} | {b:.4f} | {o:.4f} | {d:+.4f} |")
        md_lines.append("")

        md_lines.append("## 3. Threats to Validity & Limitations")
        for lim in limitations:
            md_lines.append(f"- {lim}")

        md_text = "\n".join(md_lines)

        # 2. Build LaTeX Code
        latex_lines = [
            f"% LaTeX Table for Publication Draft {version}",
            r"\begin{table}[htbp]",
            r"\centering",
            f"\\caption{{Empirical Evaluation Results ({version})}}",
            f"\\label{{tab:eval_{version.replace('.', '_')}}}",
            r"\begin{tabular}{lrrr}",
            r"\toprule",
            r"\textbf{Model / Metric} & \textbf{Baseline} & \textbf{Observed} & \textbf{Delta} \\",
            r"\midrule",
        ]
        for row_key, vals in table_data.items():
            b = vals.get("baseline", 0.0)
            o = vals.get("observed", 0.0)
            d = o - b
            latex_lines.append(f"{row_key} & {b:.4f} & {o:.4f} & {d:+.4f} \\\\")
        latex_lines.extend([
            r"\bottomrule",
            r"\end{tabular}",
            r"\end{table}",
        ])
        latex_text = "\n".join(latex_lines)

        payload = {
            "version": version,
            "title": title,
            "claims": claims,
            "table_data": table_data,
            "limitations": limitations,
            "evidence": evidence_digests,
        }
        digest = hash_canonical_json(payload)

        draft = PublicationDraft(
            version=version,
            title=title,
            claims=claims,
            table_data=table_data,
            limitations=limitations,
            markdown_content=md_text,
            latex_content=latex_text,
            publication_digest_sha256=digest,
        )
        self.drafts[version] = draft
        self.current_version = version
        return draft

    def evolve_publication(
        self,
        new_version: str,
        updated_claims: Dict[str, str],
        updated_metrics: Dict[str, Dict[str, float]],
        new_limitations: List[str],
        evidence_digests: Dict[str, str],
    ) -> Tuple[PublicationDraft, PublicationEvolutionReport]:
        """Evolves the publication to a new version and computes the diff."""
        prev_draft = self.drafts.get(self.current_version)
        new_draft = self.synthesize_draft(
            version=new_version,
            title="Scientific Validation & Autonomous Research Report",
            claims=updated_claims,
            table_data=updated_metrics,
            limitations=new_limitations,
            evidence_digests=evidence_digests,
        )

        changes: List[PublicationDiffItem] = []
        if prev_draft:
            for k, new_v in updated_claims.items():
                old_v = prev_draft.claims.get(k, "")
                if old_v != new_v:
                    changes.append(PublicationDiffItem(
                        section="Claims",
                        item_key=k,
                        old_value=old_v,
                        new_value=new_v,
                        change_type="ADDED" if not old_v else "UPDATED",
                        evidence_citation_sha256=evidence_digests.get(k, ""),
                    ))

        report = PublicationEvolutionReport(
            from_version=prev_draft.version if prev_draft else "0.0.0",
            to_version=new_version,
            changes=changes,
            has_significant_changes=len(changes) > 0,
        )
        return new_draft, report
