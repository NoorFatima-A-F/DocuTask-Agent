"""AI Health Quality Scorer & Certification Engine (Part 3H.3.8.15).

Calculates weighted multi-category scores across AI provider reliability dimensions.
Weights:
- Availability detection: 20%
- Authentication verification: 15%
- Latency monitoring: 15%
- Failure handling: 20%
- Response quality validation: 15%
- Security: 15%
"""

from __future__ import annotations


from app.platform_verification.ai_provider_health.domain.interfaces import (
    IAIHealthScorer,
)
from app.platform_verification.ai_provider_health.domain.models import (
    AIAuthReport,
    AIConnectivityReport,
    AIDegradedModeReport,
    AIFailureClassificationReport,
    AIFailureSimulationReport,
    AIFailoverReport,
    AIHealthQualityScorecard,
    AILatencyReport,
    AIMonitoringReport,
    AIProviderHealthReport,
    AIQualityCertificationTier,
    AIQuotaReport,
    AIResponseIntegrityReport,
    AISecurityReport,
    AITimeoutReport,
)


class AIHealthScorer(IAIHealthScorer):
    """Computes weighted multi-factor AI reliability scores and issues production certifications."""

    WEIGHT_AVAILABILITY = 0.20
    WEIGHT_AUTHENTICATION = 0.15
    WEIGHT_LATENCY = 0.15
    WEIGHT_FAILURE_HANDLING = 0.20
    WEIGHT_RESPONSE_QUALITY = 0.15
    WEIGHT_SECURITY = 0.15

    TARGET_THRESHOLD = 95.0

    def compute_scorecard(
        self,
        health_report: AIProviderHealthReport,
        auth_report: AIAuthReport,
        connectivity_report: AIConnectivityReport,
        latency_report: AILatencyReport,
        quota_report: AIQuotaReport,
        integrity_report: AIResponseIntegrityReport,
        timeout_report: AITimeoutReport,
        failure_report: AIFailureClassificationReport,
        degraded_report: AIDegradedModeReport,
        failover_report: AIFailoverReport,
        monitoring_report: AIMonitoringReport,
        security_report: AISecurityReport,
        simulation_report: AIFailureSimulationReport,
    ) -> AIHealthQualityScorecard:
        # 1. Availability Detection (20%)
        # Evaluates provider health report and connectivity report
        avail_sub1 = 100.0 if health_report.passed else 50.0
        avail_sub2 = min(100.0, connectivity_report.avg_connection_success_rate_pct) if connectivity_report.passed else 60.0
        avail_score = round(0.5 * avail_sub1 + 0.5 * avail_sub2, 2)

        # 2. Authentication Verification (15%)
        auth_score = 100.0 if auth_report.passed else 50.0

        # 3. Latency Monitoring (15%)
        latency_score = 100.0 if latency_report.passed else 60.0

        # 4. Failure Handling (20%)
        # Evaluates failure taxonomy, timeout safety, degraded mode, failover, and chaos simulations
        fail_sub1 = 100.0 if failure_report.passed else 60.0
        fail_sub2 = 100.0 if timeout_report.passed else 60.0
        fail_sub3 = 100.0 if degraded_report.passed else 60.0
        fail_sub4 = 100.0 if failover_report.passed else 60.0
        fail_sub5 = 100.0 if simulation_report.passed else 60.0
        failure_handling_score = round(
            0.20 * fail_sub1 + 0.20 * fail_sub2 + 0.20 * fail_sub3 + 0.20 * fail_sub4 + 0.20 * fail_sub5,
            2,
        )

        # 5. Response Quality Validation (15%)
        # Evaluates schema integrity and quota stability
        qual_sub1 = min(100.0, integrity_report.schema_compliance_rate_pct) if integrity_report.passed else 60.0
        qual_sub2 = 100.0 if quota_report.passed else 60.0
        response_quality_score = round(0.70 * qual_sub1 + 0.30 * qual_sub2, 2)

        # 6. Security (15%)
        security_score = 100.0 if (security_report.passed and not security_report.sensitive_data_exposed) else 40.0

        # Composite Weighted Score
        overall_score = round(
            (avail_score * self.WEIGHT_AVAILABILITY)
            + (auth_score * self.WEIGHT_AUTHENTICATION)
            + (latency_score * self.WEIGHT_LATENCY)
            + (failure_handling_score * self.WEIGHT_FAILURE_HANDLING)
            + (response_quality_score * self.WEIGHT_RESPONSE_QUALITY)
            + (security_score * self.WEIGHT_SECURITY),
            2,
        )

        # Tier Decision
        if overall_score >= 95.0:
            tier = AIQualityCertificationTier.AI_RELIABILITY_CERTIFIED
            verdict = "CERTIFIED"
            passed = True
        elif overall_score >= 90.0:
            tier = AIQualityCertificationTier.PRODUCTION_AI_READY
            verdict = "CONDITIONAL_APPROVAL"
            passed = True
        elif overall_score >= 80.0:
            tier = AIQualityCertificationTier.IMPROVEMENT_REQUIRED
            verdict = "REJECTED_REMEDIATION_REQUIRED"
            passed = False
        else:
            tier = AIQualityCertificationTier.FAILED
            verdict = "REJECTED"
            passed = False

        return AIHealthQualityScorecard(
            availability_score=avail_score,
            authentication_score=auth_score,
            latency_score=latency_score,
            failure_handling_score=failure_handling_score,
            response_quality_score=response_quality_score,
            security_score=security_score,
            overall_score=overall_score,
            certification_tier=tier,
            certification_verdict=verdict,
            passed=passed,
            details={
                "target_threshold_pct": self.TARGET_THRESHOLD,
                "category_weights": {
                    "availability_detection": self.WEIGHT_AVAILABILITY,
                    "authentication_verification": self.WEIGHT_AUTHENTICATION,
                    "latency_monitoring": self.WEIGHT_LATENCY,
                    "failure_handling": self.WEIGHT_FAILURE_HANDLING,
                    "response_quality_validation": self.WEIGHT_RESPONSE_QUALITY,
                    "security": self.WEIGHT_SECURITY,
                },
            },
        )
