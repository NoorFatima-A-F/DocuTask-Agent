"""
Health Score Engine for Health Check Architecture Verification (Part 3H.1).
"""
from app.platform_verification.health_architecture.domain.models import (
    HealthStateModelReport,
    HealthContractReport,
    DependencyGraphReport,
    FailurePolicyReport,
    SecurityAuditReport,
    AutomationIntegrationReport,
    HealthScorecard,
    HealthArchitectureTier,
)
from app.platform_verification.health_architecture.domain.interfaces import IHealthScoreEngine


class HealthScoreEngine(IHealthScoreEngine):
    """
    Computes a weighted 6-category architectural health scorecard and determines
    certification tier and automated CI/CD deployment approval.
    """

    def calculate_scorecard(
        self,
        model: HealthStateModelReport,
        contract: HealthContractReport,
        deps: DependencyGraphReport,
        policy: FailurePolicyReport,
        sec: SecurityAuditReport,
        auto: AutomationIntegrationReport,
    ) -> HealthScorecard:
        # 1. Health Model Score (20%)
        # State machine valid (50pts) + 4 layers evaluated (25pts) + transition coverage (25pts)
        model_score = 0.0
        if model.state_machine_valid:
            model_score += 50.0
        if len(model.layers_evaluated) >= 4:
            model_score += 25.0
        model_score += min(25.0, (model.transition_coverage_pct / 100.0) * 25.0)

        # 2. Contract Implementation Score (20%)
        contract_score = 0.0
        if contract.liveness_contract_valid and contract.liveness_isolated_from_dependencies:
            contract_score += 35.0
        if contract.readiness_contract_valid and contract.readiness_enforces_critical_deps:
            contract_score += 35.0
        if contract.full_health_contract_valid:
            contract_score += 30.0

        # 3. Dependency Modeling Score (20%)
        deps_score = 0.0
        if deps.total_services_mapped >= 3:
            deps_score += 30.0
        if deps.critical_dependencies_count >= 5 and deps.important_dependencies_count >= 4:
            deps_score += 40.0
        if deps.passed:
            deps_score += 30.0

        # 4. Failure Classification Score (15%)
        policy_score = 0.0
        if policy.detection_mechanisms_verified:
            policy_score += 25.0
        if policy.classification_rules_enforced:
            policy_score += 25.0
        if policy.response_actions_automated:
            policy_score += 25.0
        if policy.recovery_strategies_documented:
            policy_score += 25.0

        # 5. Security Design Score (10%)
        sec_score = 0.0
        if sec.public_endpoint_leak_free:
            sec_score += 35.0
        if sec.internal_endpoint_leak_free:
            sec_score += 35.0
        if sec.admin_diagnostic_auth_enforced:
            sec_score += 30.0
        if sec.credentials_leaked_count > 0 or sec.urls_leaked_count > 0:
            sec_score = 0.0

        # 6. Automation Readiness Score (15%)
        auto_score = 0.0
        if auto.docker_healthcheck_compatible:
            auto_score += 20.0
        if auto.kubernetes_liveness_compatible and auto.kubernetes_readiness_compatible:
            auto_score += 30.0
        if auto.kubernetes_startup_compatible:
            auto_score += 25.0
        if auto.cicd_predeployment_gating_supported:
            auto_score += 25.0

        # Weighted composite calculation
        overall = (
            (model_score * 0.20)
            + (contract_score * 0.20)
            + (deps_score * 0.20)
            + (policy_score * 0.15)
            + (sec_score * 0.10)
            + (auto_score * 0.15)
        )
        overall = round(overall, 2)

        # Classification Tier
        if overall >= 95.0:
            tier = HealthArchitectureTier.ENTERPRISE_READY
            verdict = "CERTIFIED"
            approved = True
            passed = True
        elif overall >= 90.0:
            tier = HealthArchitectureTier.PRODUCTION_READY
            verdict = "CERTIFIED"
            approved = True
            passed = True
        elif overall >= 80.0:
            tier = HealthArchitectureTier.NEEDS_IMPROVEMENT
            verdict = "REJECTED"
            approved = False
            passed = False
        else:
            tier = HealthArchitectureTier.FAILED
            verdict = "REJECTED"
            approved = False
            passed = False

        return HealthScorecard(
            health_model_score=round(model_score, 2),
            contract_implementation_score=round(contract_score, 2),
            dependency_modeling_score=round(deps_score, 2),
            failure_classification_score=round(policy_score, 2),
            security_design_score=round(sec_score, 2),
            automation_readiness_score=round(auto_score, 2),
            overall_health_score=overall,
            certification_tier=tier,
            certification_verdict=verdict,
            ci_cd_deployment_approved=approved,
            passed=passed,
            details={
                "weights": {
                    "health_model": 0.20,
                    "contracts": 0.20,
                    "dependencies": 0.20,
                    "failure_policies": 0.15,
                    "security_design": 0.10,
                    "automation": 0.15,
                },
                "minimum_required_for_enterprise": 95.0,
            },
        )
