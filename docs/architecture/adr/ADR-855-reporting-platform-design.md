# ADR-855: Automated Governance Reporting & Multi-Format Exporters

## Status
Accepted

## Context
Regulators, executive committees, compliance auditors, and engineering leaders require governance summaries formatted according to their operational needs. Building one-off reporting scripts creates data drift and maintenance overhead.

## Decision
We implemented an automated reporting engine under `app/governance/analytics/reporting/`:
1. **Parameterized Report Templates**: Standardized templates for `DAILY_OPERATIONAL`, `WEEKLY_SUMMARY`, `MONTHLY_EXECUTIVE`, `COMPLIANCE_AUDIT`, and `RISK_ASSESSMENT`.
2. **Multi-Format Export Engine**: `ReportExporter` supports automated rendering to JSON, CSV, PDF formatted text, and Excel tabular (TSV) formats.
3. **Automated Synthesis**: Reports aggregate executive summaries, section findings, quantitative metrics, and actionable policy remediation steps.

## Consequences
### Positive
- Instant generation of audit-ready compliance and executive briefing packages.
- Zero manual effort for weekly and monthly governance reviews.
- Consistent metrics across all generated export formats.

### Negative / Trade-offs
- Adding complex graphical chart elements into PDF/Excel requires downstream rendering pipelines.
