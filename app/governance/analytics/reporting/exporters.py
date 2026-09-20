"""Multi-Format Report Exporters (JSON, CSV, PDF Text, Excel Tabular)."""

import json
import csv
import io
from typing import Dict, Any, List
from .templates import GovernanceReport, ReportFormat


class ReportExporter:
    """Formats and exports GovernanceReport objects into various standardized representations."""

    @staticmethod
    def export(report: GovernanceReport, format: ReportFormat = ReportFormat.JSON) -> str:
        if format == ReportFormat.JSON:
            return report.model_dump_json(indent=2)

        elif format == ReportFormat.CSV:
            output = io.StringIO()
            writer = csv.writer(output)
            writer.writerow(["Report ID", "Tenant ID", "Report Type", "Title", "Governance Score", "Generated At"])
            writer.writerow([report.report_id, report.tenant_id, report.report_type.value, report.title, report.governance_score, report.generated_at.isoformat()])
            writer.writerow([])
            writer.writerow(["Section Title", "Summary Text", "Key Findings Count", "Recommendations Count"])
            for s in report.sections:
                writer.writerow([s.title, s.summary_text, len(s.key_findings), len(s.recommendations)])
            return output.getvalue()

        elif format == ReportFormat.PDF:
            # Formatted text representation for PDF printing
            lines = [
                f"==================================================================",
                f"            {report.title.upper()}",
                f"==================================================================",
                f"Report ID:        {report.report_id}",
                f"Tenant:           {report.tenant_id}",
                f"Type:             {report.report_type.value}",
                f"Governance Score: {report.governance_score}/100",
                f"Generated At:     {report.generated_at.isoformat()}",
                f"------------------------------------------------------------------",
                f"EXECUTIVE SUMMARY:",
                f"{report.executive_summary}",
                f"------------------------------------------------------------------",
            ]
            for s in report.sections:
                lines.append(f"\nSECTION: {s.title.upper()}")
                lines.append(f"{s.summary_text}")
                if s.key_findings:
                    lines.append("Key Findings:")
                    for k in s.key_findings:
                        lines.append(f"  - {k}")
                if s.recommendations:
                    lines.append("Recommendations:")
                    for r in s.recommendations:
                        lines.append(f"  - {r}")
            return "\n".join(lines)

        elif format == ReportFormat.EXCEL:
            # Tab-delimited TSV string format for Excel import
            lines = [f"Section\tMetric\tValue"]
            for s in report.sections:
                for k, v in s.metrics.items():
                    lines.append(f"{s.title}\t{k}\t{v}")
            return "\n".join(lines)

        return report.model_dump_json()
