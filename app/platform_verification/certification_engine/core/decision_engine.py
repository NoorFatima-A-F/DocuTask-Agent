"""
Enterprise Decision Engine combining quality gates, policy evaluations, risk scoring, and exceptions.
"""
from __future__ import annotations
import uuid
from typing import Any, Dict, List, Optional
from app.platform_verification.certification_engine.domain.interfaces import (
    IDecisionEngine,
    IPolicyEngine,
    IQualityGateEngine,
    IRiskEngine,
)
from app.platform_verification.certification_engine.domain.models import (
    CertificationLevel,
    FailureAction,
    GateEvaluationResult,
    QualityGateDecision,
    ReleaseDecisionType,
    RiskLevel,
    Severity,
)


class EnterpriseDecisionEngine(IDecisionEngine):
    """Produces explainable, deterministic release and certification decisions."""

    def __init__(
        self,
        gate_engine: IQualityGateEngine,
        policy_engine: IPolicyEngine,
        risk_engine: IRiskEngine,
    ):
        self.gate_engine = gate_engine
        self.policy_engine = policy_engine
        self.risk_engine = risk_engine

    def make_release_decision(
        self,
        system_id: str,
        system_version: str,
        model_version: str,
        target_level: CertificationLevel,
        metrics: Dict[str, Any],
        gate_ids: List[str],
        policy_ids: Optional[List[str]] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> QualityGateDecision:
        ctx = context or {}
        active_exceptions = ctx.get("exceptions", [])

        # 1. Evaluate Gates
        gate_results = self.gate_engine.evaluate_gates(
            gate_ids=gate_ids,
            metrics=metrics,
            active_exceptions=active_exceptions,
        )

        failed_gates = [g for g in gate_results if not g.passed]

        # 2. Evaluate Policies
        policy_failure_reasons: List[str] = []
        if policy_ids:
            for pid in policy_ids:
                passed, reasons = self.policy_engine.evaluate_policy(pid, metrics)
                if not passed:
                    policy_failure_reasons.extend(reasons)

        # 3. Assess Risk
        risk_assessment = self.risk_engine.assess_risk(
            system_id=system_id,
            failed_gates=failed_gates,
            metrics=metrics,
            context=ctx,
        )

        # 4. Synthesize Decision & Explainable Reasoning
        explainable_reasons: List[str] = []
        decision: ReleaseDecisionType = ReleaseDecisionType.APPROVED
        requires_human_approval = False

        # Calculate weighted quality score (0..100)
        total_score = float(metrics.get("overall_score", 92.5))

        if risk_assessment.risk_level == RiskLevel.CRITICAL:
            decision = ReleaseDecisionType.REJECTED
            explainable_reasons.append(
                f"REJECTED: Critical risk level detected (Score: {risk_assessment.risk_score}). Blocking defects identified."
            )
            for g in failed_gates:
                if g.severity == Severity.CRITICAL:
                    explainable_reasons.extend(g.failure_reasons)

        elif risk_assessment.risk_level == RiskLevel.HIGH:
            decision = ReleaseDecisionType.MANUAL_REVIEW
            requires_human_approval = True
            explainable_reasons.append(
                f"MANUAL_REVIEW: High risk level ({risk_assessment.risk_score}). Executive / AI Governance approval required."
            )
            for g in failed_gates:
                explainable_reasons.extend(g.failure_reasons)

        elif risk_assessment.risk_level == RiskLevel.MEDIUM:
            decision = ReleaseDecisionType.CONDITIONAL_APPROVAL
            requires_human_approval = True
            explainable_reasons.append(
                f"CONDITIONAL_APPROVAL: Medium risk level ({risk_assessment.risk_score}). Approved with active monitoring & mitigations."
            )
            for g in failed_gates:
                explainable_reasons.extend(g.failure_reasons)

        else:  # LOW RISK
            if policy_failure_reasons:
                decision = ReleaseDecisionType.REJECTED
                explainable_reasons.append("REJECTED: Policy compliance violations detected.")
                explainable_reasons.extend(policy_failure_reasons)
            elif any(g.failure_action == FailureAction.BLOCK_RELEASE for g in failed_gates):
                decision = ReleaseDecisionType.REJECTED
                explainable_reasons.append("REJECTED: Non-waived blocking quality gate failures.")
                for g in failed_gates:
                    explainable_reasons.extend(g.failure_reasons)
            else:
                decision = ReleaseDecisionType.APPROVED
                explainable_reasons.append(
                    f"APPROVED: All quality gates and release policies passed successfully (Total Score: {total_score:.1f}/100)."
                )

        exception_ids = [e.exception_id for e in active_exceptions]

        return QualityGateDecision(
            decision_id=f"DEC-{uuid.uuid4().hex[:8].upper()}",
            system_id=system_id,
            system_version=system_version,
            model_version=model_version,
            decision=decision,
            total_score=total_score,
            gate_results=gate_results,
            risk_assessment=risk_assessment,
            explainable_reasons=explainable_reasons,
            target_certification_level=target_level,
            requires_human_approval=requires_human_approval,
            active_exceptions=exception_ids,
        )
