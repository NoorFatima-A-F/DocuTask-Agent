"""
Readiness Quality Score Engine (Part 13).
Computes weighted composite quality scorecards across the 6 core categories:
1. Contract correctness: 25%
2. State model quality: 20%
3. Dependency modeling: 20%
4. Failure handling: 15%
5. Security: 10%
6. Observability: 10%
"""
from typing import Dict, Any
from app.platform_verification.readiness_contract.domain.models import (
    ReadinessContractReport,
    StateMachineReport,
    DependencyPolicyReport,
    StartupValidationReport,
    FailureTransitionReport,
    OrchestrationReport,
    ReadinessScorecard,
    ReadinessTier,
)
from app.platform_verification.readiness_contract.domain.interfaces import (
    IReadinessScoreEngine,
)


class ReadinessScoreEngine(IReadinessScoreEngine):
    """
    Evaluates enterprise readiness contract components against quality standards.
    """

    def compute_scorecard(
        self,
        contract_report: ReadinessContractReport,
        state_report: StateMachineReport,
        policy_report: DependencyPolicyReport,
        startup_report: StartupValidationReport,
        failure_report: FailureTransitionReport,
        orchestration_report: OrchestrationReport,
        security_passed: bool = True,
        observability_passed: bool = True,
    ) -> ReadinessScorecard:
        # 1. Contract Correctness (25%)
        contract_score = 0.0
        if contract_report.contract_schema_valid:
            contract_score += 50.0
        if len(contract_report.checks) >= 5 and contract_report.passed:
            contract_score += 50.0

        # 2. State Model Quality (20%)
        state_score = 0.0
        if state_report.total_states == 6 and state_report.transition_matrix_valid:
            state_score += 50.0
        if state_report.all_states_deterministic and state_report.passed:
            state_score += 50.0

        # 3. Dependency Modeling (20%)
        dep_score = 0.0
        if len(policy_report.critical_dependencies) >= 3 and len(policy_report.degraded_dependencies) >= 1:
            dep_score += 50.0
        if policy_report.traffic_actions_mapped and policy_report.passed:
            dep_score += 50.0

        # 4. Failure Handling (15%)
        failure_score = 0.0
        if failure_report.passed_transitions == failure_report.total_transitions_tested:
            failure_score += 50.0
        if failure_report.db_failure_to_not_ready_passed and failure_report.recovery_to_ready_passed:
            failure_score += 50.0

        # 5. Security (10%)
        sec_score = 100.0 if security_passed else 0.0

        # 6. Observability (10%)
        obs_score = 100.0 if observability_passed else 0.0

        # Weighted composite score
        overall = (
            (contract_score * 0.25)
            + (state_score * 0.20)
            + (dep_score * 0.20)
            + (failure_score * 0.15)
            + (sec_score * 0.10)
            + (obs_score * 0.10)
        )
        overall = round(overall, 2)

        if overall >= 95.0:
            tier = ReadinessTier.ENTERPRISE_READY
            verdict = "CERTIFIED"
            passed = True
        elif overall >= 90.0:
            tier = ReadinessTier.PRODUCTION_READY
            verdict = "CERTIFIED"
            passed = True
        elif overall >= 80.0:
            tier = ReadinessTier.NEEDS_IMPROVEMENT
            verdict = "REJECTED"
            passed = False
        else:
            tier = ReadinessTier.FAILED
            verdict = "REJECTED"
            passed = False

        return ReadinessScorecard(
            contract_correctness_score=round(contract_score, 2),
            state_model_quality_score=round(state_score, 2),
            dependency_modeling_score=round(dep_score, 2),
            failure_handling_score=round(failure_score, 2),
            security_score=round(sec_score, 2),
            observability_score=round(obs_score, 2),
            overall_readiness_score=overall,
            certification_tier=tier,
            certification_verdict=verdict,
            traffic_admission_safe=passed,
            passed=passed,
            details={
                "weights": {
                    "contract_correctness": 0.25,
                    "state_model_quality": 0.20,
                    "dependency_modeling": 0.20,
                    "failure_handling": 0.15,
                    "security": 0.10,
                    "observability": 0.10,
                },
                "minimum_required_for_enterprise": 95.0,
            },
        )
