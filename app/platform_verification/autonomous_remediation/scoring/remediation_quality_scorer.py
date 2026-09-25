"""Autonomous Remediation Quality Scorer (3H.4.3.14).

Computes 6-dimension weighted self-healing score:
- Recovery Accuracy (25%)
- Safety Controls (20%)
- Validation Correctness (20%)
- Rollback Capability (15%)
- Observability (10%)
- Security (10%)

Awards Certification Tier:
- 95-100: Enterprise Self-Healing Ready
- 90-94.99: Production Ready
- 80-89.99: Improvement Required
- <80: Failed
"""

from datetime import datetime, timezone
from ..domain.models import (
    RemediationPolicyReport,
    ActionExecutionReport,
    RecoveryValidationReport,
    RollbackReport,
    SelfHealingTestReport,
    RemediationMetricsReport,
    RemediationSecurityReport,
    AutonomousRemediationScorecard,
    SelfHealingTier,
)
from ..domain.interfaces import IAutonomousRemediationScorer


class AutonomousRemediationScorer(IAutonomousRemediationScorer):
    """Calculates weighted operational self-healing scores and assigns tiers."""

    def score_remediation(
        self,
        policy_rep: RemediationPolicyReport,
        exec_rep: ActionExecutionReport,
        val_rep: RecoveryValidationReport,
        roll_rep: RollbackReport,
        scen_rep: SelfHealingTestReport,
        metrics_rep: RemediationMetricsReport,
        sec_rep: RemediationSecurityReport,
    ) -> AutonomousRemediationScorecard:
        # 1. Recovery Accuracy (Weight: 25%)
        # Based on policy coverage, scenario success rate, and automation success rate
        scen_pass_rate = (scen_rep.passed_scenarios / scen_rep.total_scenarios * 100.0) if scen_rep.total_scenarios > 0 else 100.0
        acc_score = (scen_pass_rate * 0.6) + (metrics_rep.automation_success_rate_pct * 0.4)
        acc_score = min(100.0, max(0.0, acc_score))

        # 2. Safety Controls (Weight: 20%)
        # Evaluates policy definitions, rate limits, cooldowns, and blast radius controls
        safety_score = 100.0 if policy_rep.total_policies >= 5 and policy_rep.level_3_count >= 1 else 90.0

        # 3. Validation Correctness (Weight: 20%)
        val_score = val_rep.recovery_success_rate_pct

        # 4. Rollback Capability (Weight: 15%)
        roll_score = roll_rep.rollback_success_rate_pct

        # 5. Observability (Weight: 10%)
        obs_score = 100.0 if exec_rep.total_actions_executed > 0 else 90.0

        # 6. Security (Weight: 10%)
        sec_score = 100.0 if sec_rep.secret_leaks_found == 0 and sec_rep.unauthorized_commands_blocked >= 3 else 80.0

        # Weighted calculation
        overall = (
            (acc_score * 0.25)
            + (safety_score * 0.20)
            + (val_score * 0.20)
            + (roll_score * 0.15)
            + (obs_score * 0.10)
            + (sec_score * 0.10)
        )
        overall = round(overall, 2)

        if overall >= 95.0:
            tier = SelfHealingTier.ENTERPRISE_SELF_HEALING_READY
            verdict = "CERTIFIED"
            passed = True
        elif overall >= 90.0:
            tier = SelfHealingTier.PRODUCTION_READY
            verdict = "CONDITIONALLY CERTIFIED"
            passed = True
        elif overall >= 80.0:
            tier = SelfHealingTier.IMPROVEMENT_REQUIRED
            verdict = "IMPROVEMENT REQUIRED"
            passed = False
        else:
            tier = SelfHealingTier.FAILED
            verdict = "FAILED"
            passed = False

        return AutonomousRemediationScorecard(
            recovery_accuracy_score=round(acc_score, 2),
            safety_controls_score=round(safety_score, 2),
            validation_correctness_score=round(val_score, 2),
            rollback_capability_score=round(roll_score, 2),
            observability_score=round(obs_score, 2),
            security_score=round(sec_score, 2),
            overall_score=overall,
            certification_tier=tier,
            certification_verdict=verdict,
            passed=passed,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
