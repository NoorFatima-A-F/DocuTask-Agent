"""
Phase 3O: Human-Readable Infrastructure Readiness Markdown Generator.
"""

from datetime import datetime, timezone

from ..domain.models import (
    CertificationDecision,
    MaturityAssessment,
    QualityRegressionReport,
    QualityScorecard,
    RiskAssessmentReport,
)


class ReadinessMarkdownGenerator:
    """
    Generates an executive-level, human-readable Infrastructure_Readiness_Report.md.
    """

    def generate_report(
        self,
        decision: CertificationDecision,
        scorecard: QualityScorecard,
        risk_report: RiskAssessmentReport,
        maturity: MaturityAssessment,
        regression: QualityRegressionReport,
    ) -> str:
        status_badge = "APPROVED" if decision.deployment_approved else "BLOCKED"
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

        lines = [
            f"# DocuTask Agent — Enterprise Infrastructure Readiness & Certification Report",
            f"",
            f"**Report Generated:** `{timestamp}`  ",
            f"**Platform Version:** `3.17.0`  ",
            f"**Certification Status:** `{decision.certification.value.upper()}`  ",
            f"**Production Deployment Gate:** **`{status_badge}`**  ",
            f"",
            f"---",
            f"",
            f"## 1. Executive Summary",
            f"",
            f"DocuTask Agent has completed the **Enterprise Infrastructure Quality Scoring & Certification Program (Phase 3O)**.",
            f"The platform achieved an overall infrastructure quality score of **`{scorecard.overall_score:.2f}%`** across 6 core SRE engineering pillars.",
            f"",
            f"- **Overall Quality Score:** `{scorecard.overall_score:.2f} / 100.0`",
            f"- **Certification Level:** `{decision.certification.value}`",
            f"- **Operational Maturity:** `{maturity.maturity_level.value}`",
            f"- **Production Deployment Status:** `{'PASSED - Approved for Enterprise Production' if decision.deployment_approved else 'FAILED - Deployment Blocked'}`",
            f"",
            f"---",
            f"",
            f"## 2. Infrastructure Quality Breakdown (6 Engineering Pillars)",
            f"",
            f"| Engineering Pillar | Weight | Verified Score | Contribution | Status |",
            f"| :--- | :---: | :---: | :---: | :---: |",
        ]

        for cat_name, cat in scorecard.categories.items():
            lines.append(
                f"| **{cat_name}** | {int(cat.weight * 100)}% | **{cat.score:.2f}%** | {cat.contribution:.2f}% | {cat.status.value} |"
            )

        lines.extend([
            f"",
            f"---",
            f"",
            f"## 3. Operational Maturity Assessment",
            f"",
            f"**Evaluated Maturity:** `{maturity.maturity_level.value}` (Maturity Index: `{maturity.maturity_score:.1f}%`)",
            f"",
            f"### Verified Enterprise Capabilities",
        ])

        for cap in maturity.capabilities_achieved:
            lines.append(f"- [x] {cap}")

        lines.extend([
            f"",
            f"### Next-Level Roadmap Requirements",
        ])
        for req in maturity.next_level_requirements:
            lines.append(f"- [ ] {req}")

        lines.extend([
            f"",
            f"---",
            f"",
            f"## 4. Risk Analysis & Failure Conditions",
            f"",
            f"- **Highest Detected Risk:** `{risk_report.highest_risk.value}`",
            f"- **Critical Risks:** `{risk_report.critical_risks_count}`",
            f"- **High Risks:** `{risk_report.high_risks_count}`",
            f"- **Medium / Low Risks:** `{risk_report.medium_risks_count + risk_report.low_risks_count}`",
            f"- **Production Blockers:** `{'YES - IMMEDIATE REMEDIATION REQUIRED' if risk_report.production_blocker_present else 'NONE - Zero Blocking Vulnerabilities'}`",
            f"",
        ])

        if risk_report.risks:
            lines.append(f"### Active Risk Findings")
            for r in risk_report.risks:
                lines.append(f"- **[{r.risk_level.value}] {r.title}**: {r.reason}")
                lines.append(f"  - *Impact:* {r.impact}")
                lines.append(f"  - *Remediation:* {r.remediation}")
        else:
            lines.append(f"*(No active high or critical risks identified across the verification suite.)*")

        lines.extend([
            f"",
            f"---",
            f"",
            f"## 5. Quality Regression Analysis",
            f"",
            f"- **Previous Baseline Version:** `{regression.previous_version}` (`{regression.previous_overall_score:.2f}%`)",
            f"- **Current Build Version:** `{regression.current_version}` (`{regression.current_overall_score:.2f}%`)",
            f"- **Score Delta:** `{'+' if regression.score_delta >= 0 else ''}{regression.score_delta:.2f}%`",
            f"- **Regression Alert:** `{'REGRESSION DETECTED' if regression.regression_detected else 'CLEAN - No Quality Degradation'}`",
            f"",
            f"---",
            f"",
            f"## 6. Recommendations & SRE Action Plan",
            f"",
        ])

        for rec in decision.recommendations:
            lines.append(f"1. {rec}")

        lines.extend([
            f"",
            f"---",
            f"*Certified by DocuTask Agent Automated Enterprise Infrastructure Certification Authority (Phase 3O)*",
        ])

        return "\n".join(lines)
