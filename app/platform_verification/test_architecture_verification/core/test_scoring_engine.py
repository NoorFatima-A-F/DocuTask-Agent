"""
Weighted Test Quality Scoring and Certification Engine.
"""
from app.platform_verification.test_architecture_verification.domain.models import (
    TestPyramidReport,
    UnitTestQualityReport,
    CoverageQualityReport,
    AiEvaluationTestReport,
    FlakyTestDetectionReport,
    EnvironmentReproducibilityReport,
    TestQualityScorecard,
    TestCertificationTier,
)
from app.platform_verification.test_architecture_verification.domain.interfaces import ITestScoringEngine


class TestScoringEngine(ITestScoringEngine):
    """Calculates weighted composite score across all 6 test architecture pillars."""
    __test__ = False

    # Weights: Coverage (25%), Reliability (20%), Organization/Pyramid (15%), AI Eval (15%), Reproducibility (15%), Execution/Performance (10%)
    WEIGHT_COVERAGE = 0.25
    WEIGHT_RELIABILITY = 0.20
    WEIGHT_PYRAMID = 0.15
    WEIGHT_AI_EVAL = 0.15
    WEIGHT_REPRODUCIBILITY = 0.15
    WEIGHT_PERFORMANCE = 0.10

    def calculate_scorecard(
        self,
        pyramid: TestPyramidReport,
        unit_quality: UnitTestQualityReport,
        coverage: CoverageQualityReport,
        ai_eval: AiEvaluationTestReport,
        reliability: FlakyTestDetectionReport,
        env: EnvironmentReproducibilityReport,
    ) -> TestQualityScorecard:
        cov_s = (coverage.line_coverage_pct * 0.4) + (coverage.branch_coverage_pct * 0.3) + (coverage.mutation_score_pct * 0.3)
        rel_s = 100.0 - (reliability.flaky_tests * 5.0) - (reliability.unstable_tests * 25.0)
        rel_s = max(0.0, min(100.0, rel_s))

        pyr_s = pyramid.pyramid_health_score
        ai_s = 100.0 if ai_eval.status == "PASS" else 60.0
        repro_s = env.reproducibility_score
        perf_s = unit_quality.isolation_score

        composite = (
            (cov_s * self.WEIGHT_COVERAGE)
            + (rel_s * self.WEIGHT_RELIABILITY)
            + (pyr_s * self.WEIGHT_PYRAMID)
            + (ai_s * self.WEIGHT_AI_EVAL)
            + (repro_s * self.WEIGHT_REPRODUCIBILITY)
            + (perf_s * self.WEIGHT_PERFORMANCE)
        )
        composite = round(composite, 2)

        if composite >= 92.0 and reliability.unstable_tests == 0 and ai_eval.status == "PASS":
            tier = TestCertificationTier.ENTERPRISE_TEST_READY
        elif composite >= 85.0:
            tier = TestCertificationTier.PRODUCTION_READY
        elif composite >= 75.0:
            tier = TestCertificationTier.NEEDS_IMPROVEMENT
        else:
            tier = TestCertificationTier.FAILED

        return TestQualityScorecard(
            coverage_quality_score=round(cov_s, 2),
            reliability_score=round(rel_s, 2),
            organization_pyramid_score=round(pyr_s, 2),
            ai_evaluation_score=round(ai_s, 2),
            reproducibility_score=round(repro_s, 2),
            performance_score=round(perf_s, 2),
            composite_score=composite,
            tier=tier,
        )
