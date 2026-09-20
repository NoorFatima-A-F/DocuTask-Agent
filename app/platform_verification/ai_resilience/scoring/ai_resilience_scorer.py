"""AI Resilience Quality Scorer (3H.3.10.15).

Calculates a 6-dimension weighted quality score:
1. Failure Detection (Weight 20%)
2. Recovery Capability (Weight 25%)
3. Data Preservation (Weight 20%)
4. Fallback Handling (Weight 15%)
5. Circuit Breaker Quality (Weight 10%)
6. Observability & Telemetry (Weight 10%)
"""

from ..domain.models import (
    AIResilienceScorecard,
    AIResilienceTier,
    OutageSimulationReport,
    LatencyChaosReport,
    MalformedResponseReport,
    AuthFailureReport,
    QuotaExhaustionReport,
    NetworkFailureReport,
    QualityDegradationReport,
    FallbackVerificationReport,
    TaskPreservationReport,
    CircuitBreakerReport,
    RecoveryMetricsReport,
)
from ..domain.interfaces import IAIResilienceScorer


class AIResilienceScorer(IAIResilienceScorer):
    """Calculates weighted resilience quality scorecard."""

    def calculate_scorecard(
        self,
        outage_report: OutageSimulationReport,
        latency_report: LatencyChaosReport,
        malformed_report: MalformedResponseReport,
        auth_report: AuthFailureReport,
        quota_report: QuotaExhaustionReport,
        network_report: NetworkFailureReport,
        quality_report: QualityDegradationReport,
        fallback_report: FallbackVerificationReport,
        preservation_report: TaskPreservationReport,
        circuit_breaker_report: CircuitBreakerReport,
        recovery_metrics: RecoveryMetricsReport,
    ) -> AIResilienceScorecard:
        # 1. Failure Detection Score (20%)
        # Based on detection seconds <= 2.0s, schema failures caught 100%, auth failures caught
        det_score = 100.0
        if outage_report.detection_seconds > 2.0:
            det_score -= 10.0
        if malformed_report.uncaught_exceptions > 0:
            det_score -= 20.0
        if not auth_report.operator_alert_triggered:
            det_score -= 15.0

        # 2. Recovery Capability Score (25%)
        # Based on successful recoveries, retry success, and repair rates
        rec_score = 100.0
        if recovery_metrics.successful_recoveries < recovery_metrics.total_documents_processed:
            deficit = recovery_metrics.total_documents_processed - recovery_metrics.successful_recoveries
            rec_score -= min(50.0, deficit * 2.0)
        if not quota_report.exponential_backoff_applied:
            rec_score -= 20.0

        # 3. Data Preservation Score (20%)
        # Based on zero lost tasks, zero duplicate executions, idempotency verified
        pres_score = 100.0
        if preservation_report.lost_documents_count > 0:
            pres_score -= 50.0
        if preservation_report.duplicate_tasks_created > 0:
            pres_score -= 20.0
        if quality_report.bad_data_escaped_to_db > 0:
            pres_score -= 30.0

        # 4. Fallback Handling Score (15%)
        # Based on successful failovers and average failover latency < 200ms
        fall_score = 100.0
        if fallback_report.successful_failovers < fallback_report.total_failover_tests:
            fall_score -= 30.0
        if fallback_report.average_failover_latency_ms > 200.0:
            fall_score -= 15.0

        # 5. Circuit Breaker Quality Score (10%)
        # Based on threshold tripping, blocking cascading calls, and safe half-open canary recovery
        cb_score = 100.0
        if circuit_breaker_report.cascading_calls_blocked < 10:
            cb_score -= 20.0
        if not circuit_breaker_report.cost_explosion_prevented:
            cb_score -= 30.0

        # 6. Observability Score (10%)
        # Based on alerts triggered and audit events logged
        obs_score = 100.0
        if recovery_metrics.alerts_triggered_count == 0:
            obs_score -= 25.0
        if not fallback_report.audit_event_logged:
            obs_score -= 20.0

        # Clamp individual scores to [0.0, 100.0]
        det_score = max(0.0, min(100.0, det_score))
        rec_score = max(0.0, min(100.0, rec_score))
        pres_score = max(0.0, min(100.0, pres_score))
        fall_score = max(0.0, min(100.0, fall_score))
        cb_score = max(0.0, min(100.0, cb_score))
        obs_score = max(0.0, min(100.0, obs_score))

        # Weighted calculation
        overall = (
            det_score * 0.20
            + rec_score * 0.25
            + pres_score * 0.20
            + fall_score * 0.15
            + cb_score * 0.10
            + obs_score * 0.10
        )
        overall = round(overall, 2)

        if overall >= 95.0:
            tier = AIResilienceTier.ENTERPRISE_AI_RESILIENT
            verdict = "CERTIFIED"
            passed = True
        elif overall >= 90.0:
            tier = AIResilienceTier.PRODUCTION_AI_READY
            verdict = "PROVISIONALLY_CERTIFIED"
            passed = True
        elif overall >= 80.0:
            tier = AIResilienceTier.IMPROVEMENT_REQUIRED
            verdict = "ACTION_REQUIRED"
            passed = False
        else:
            tier = AIResilienceTier.FAILED
            verdict = "FAILED"
            passed = False

        return AIResilienceScorecard(
            failure_detection_score=det_score,
            recovery_capability_score=rec_score,
            data_preservation_score=pres_score,
            fallback_handling_score=fall_score,
            circuit_breaker_score=cb_score,
            observability_score=obs_score,
            overall_score=overall,
            certification_tier=tier,
            certification_verdict=verdict,
            passed=passed,
        )
