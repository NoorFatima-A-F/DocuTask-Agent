"""
Weighted Distributed System Quality Scoring and Certification Engine.
"""
from app.platform_verification.service_communication.domain.models import (
    DependencyAnalysisReport,
    CommunicationContractReport,
    TimeoutValidationReport,
    RetryBehaviorReport,
    CircuitBreakerReport,
    NetworkFailureReport,
    DistributedConsistencyReport,
    TraceabilityReport,
    DistributedSystemCertificationReport,
    DistributedCertificationTier,
)
from app.platform_verification.service_communication.domain.interfaces import IDistributedSystemScoringEngine


class DistributedSystemScoringEngine(IDistributedSystemScoringEngine):
    """Calculates weighted composite scorecard across 6 distributed system pillars."""

    # Weights: Reliability (25%), Failure Handling (20%), Consistency (20%), Scalability (15%), Observability (10%), Security (10%)
    WEIGHT_RELIABILITY = 0.25
    WEIGHT_FAILURE = 0.20
    WEIGHT_CONSISTENCY = 0.20
    WEIGHT_SCALABILITY = 0.15
    WEIGHT_OBSERVABILITY = 0.10
    WEIGHT_SECURITY = 0.10

    def calculate_scorecard(
        self,
        dep_rep: DependencyAnalysisReport,
        contract_rep: CommunicationContractReport,
        timeout_rep: TimeoutValidationReport,
        retry_rep: RetryBehaviorReport,
        cb_rep: CircuitBreakerReport,
        net_rep: NetworkFailureReport,
        cons_rep: DistributedConsistencyReport,
        trace_rep: TraceabilityReport,
    ) -> DistributedSystemCertificationReport:
        rel_s = (dep_rep.dependency_complexity_score * 0.5) + (100.0 if contract_rep.status == "PASS" else 60.0) * 0.5
        fail_s = (100.0 if cb_rep.status == "PASS" and retry_rep.status == "PASS" and timeout_rep.status == "PASS" else 70.0)
        cons_s = 100.0 if cons_rep.status == "PASS" else 50.0
        scale_s = 100.0 if net_rep.status == "PASS" else 70.0
        obs_s = trace_rep.reconstructability_score
        sec_s = 100.0 if contract_rep.schema_validation_passed else 75.0

        composite = (
            (rel_s * self.WEIGHT_RELIABILITY)
            + (fail_s * self.WEIGHT_FAILURE)
            + (cons_s * self.WEIGHT_CONSISTENCY)
            + (scale_s * self.WEIGHT_SCALABILITY)
            + (obs_s * self.WEIGHT_OBSERVABILITY)
            + (sec_s * self.WEIGHT_SECURITY)
        )
        composite = round(composite, 2)

        if composite >= 95.0 and cons_rep.status == "PASS" and cb_rep.status == "PASS":
            tier = DistributedCertificationTier.ENTERPRISE_DISTRIBUTED_SYSTEM_READY
        elif composite >= 90.0:
            tier = DistributedCertificationTier.PRODUCTION_READY
        elif composite >= 80.0:
            tier = DistributedCertificationTier.IMPROVEMENT_REQUIRED
        else:
            tier = DistributedCertificationTier.FAILED

        return DistributedSystemCertificationReport(
            communication_reliability_score=round(rel_s, 2),
            failure_handling_score=round(fail_s, 2),
            consistency_score=round(cons_s, 2),
            scalability_score=round(scale_s, 2),
            observability_score=round(obs_s, 2),
            security_score=round(sec_s, 2),
            composite_score=composite,
            tier=tier,
        )
