"""
Test Evidence & Certification Reporter.
Renders standardized JSON/Markdown audit evidence from verification test runs.
"""
import json
from typing import Dict, Any
from .runner import TestSuiteReport

class TestEvidenceReporter:
    """Formats verification run reports for audit and compliance certification."""
    @staticmethod
    def to_json(report: TestSuiteReport) -> str:
        data = {
            "suite_id": report.suite_id,
            "target_module": report.target_module,
            "overall_passed": report.overall_passed,
            "pass_rate": report.pass_rate,
            "total_duration_ms": report.total_duration_ms,
            "started_at": report.started_at,
            "completed_at": report.completed_at,
            "tier_results": [
                {
                    "tier": r.tier.value,
                    "passed": r.passed,
                    "passed_tests": r.passed_tests,
                    "failed_tests": r.failed_tests,
                    "duration_ms": r.duration_ms,
                    "evidence": r.evidence_payload
                }
                for r in report.tier_results
            ]
        }
        return json.dumps(data, indent=2)

    @staticmethod
    def to_markdown(report: TestSuiteReport) -> str:
        status_badge = "✅ PASSED" if report.overall_passed else "❌ FAILED"
        lines = [
            f"# Verification Platform Test Report: {report.target_module}",
            f"**Status**: {status_badge} | **Pass Rate**: {report.pass_rate * 100:.1f}% | **Duration**: {report.total_duration_ms:.2f}ms",
            "",
            "## Testing Tier Breakdown",
            "| Tier | Status | Passed | Failed | Duration (ms) |",
            "|---|---|---|---|---|"
        ]
        for r in report.tier_results:
            st = "PASS" if r.passed else "FAIL"
            lines.append(f"| `{r.tier.value}` | {st} | {r.passed_tests} | {r.failed_tests} | {r.duration_ms:.2f} |")

        return "\n".join(lines)
