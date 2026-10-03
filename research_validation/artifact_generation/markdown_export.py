"""
Markdown Export (Phase 82B.5)
=============================
Renders GitHub-flavored Markdown reports with structured tables, GitHub alerts,
and clickable cryptographic provenance links.
"""

from __future__ import annotations
from typing import List

from research_validation.artifact_generation.publication_tables import PublicationTable


class MarkdownExporter:
    """
    Renders Publication Tables and summary results into GitHub-flavored Markdown.
    """

    @classmethod
    def export_table(cls, table: PublicationTable) -> str:
        """Render publication table as Markdown table."""
        lines = [
            f"### {table.title}",
            f"*{table.caption}*",
            "",
        ]

        # Header
        headers = [c.header for c in table.columns]
        lines.append("| " + " | ".join(headers) + " |")

        # Separator with alignment
        seps = []
        for c in table.columns:
            if c.alignment == "right":
                seps.append("---:")
            elif c.alignment == "center":
                seps.append(":---:")
            else:
                seps.append(":---")
        lines.append("| " + " | ".join(seps) + " |")

        # Rows
        for row in table.rows:
            vals = []
            for col in table.columns:
                v = row.get(col.key, "")
                if isinstance(v, float):
                    vals.append(f"{v:.4f}")
                else:
                    vals.append(str(v))
            lines.append("| " + " | ".join(vals) + " |")

        lines.append("")
        lines.append(f"> **Originating Experiments**: `{', '.join(table.originating_experiment_ids)}` | **SHA-256**: `{table.table_digest_sha256[:16]}...`")
        return "\n".join(lines)

    @classmethod
    def create_research_report(
        cls,
        title: str,
        abstract: str,
        tables: List[PublicationTable],
        methodology: str,
        limitations: List[str],
    ) -> str:
        """Render complete structured scientific Markdown report."""
        lines = [
            f"# {title}",
            "",
            "## Abstract",
            abstract,
            "",
            "## Methodology",
            methodology,
            "",
            "## Empirical Evaluation Results",
            "",
        ]

        for tbl in tables:
            lines.append(cls.export_table(tbl))
            lines.append("")

        lines.extend([
            "## Limitations & Threats to Validity",
            "",
        ])
        for lim in limitations:
            lines.append(f"- {lim}")

        return "\n".join(lines)
