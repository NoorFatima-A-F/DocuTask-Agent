"""
Test Reliability, Order Independence and Flakiness Analyzer.
"""
from typing import Dict, List, Any
from app.platform_verification.test_architecture_verification.domain.models import (
    FlakyTestDetectionReport,
    FlakyTestResult,
    FlakinessClass,
)
from app.platform_verification.test_architecture_verification.domain.interfaces import IReliabilityAnalyzer


class ReliabilityAnalyzer(IReliabilityAnalyzer):
    """Analyzes test run histories to detect flakiness and verify execution order independence."""

    def analyze_reliability_and_flakiness(self, execution_history: List[Dict[str, Any]]) -> FlakyTestDetectionReport:
        reliable = 0
        flaky = 0
        unstable = 0
        results: List[FlakyTestResult] = []
        order_independent = True

        for item in execution_history:
            name = item.get("test_name", "test_unnamed")
            runs = item.get("runs", 100)
            fails = item.get("failures", 0)
            order_dep = item.get("order_dependent", False)

            if order_dep:
                order_independent = False

            fail_rate = (fails / max(runs, 1)) * 100.0
            if fail_rate < 1.0:
                cls = FlakinessClass.RELIABLE
                reliable += 1
            elif fail_rate <= 5.0:
                cls = FlakinessClass.FLAKY
                flaky += 1
            else:
                cls = FlakinessClass.UNSTABLE
                unstable += 1

            results.append(
                FlakyTestResult(
                    test_name=name,
                    runs=runs,
                    failures=fails,
                    failure_rate_pct=round(fail_rate, 2),
                    classification=cls,
                )
            )

        status = "PASS" if unstable == 0 and order_independent else "FAIL"

        return FlakyTestDetectionReport(
            status=status,
            total_evaluated_tests=len(execution_history),
            reliable_tests=reliable,
            flaky_tests=flaky,
            unstable_tests=unstable,
            flaky_test_details=results,
            order_independence_verified=order_independent,
        )
