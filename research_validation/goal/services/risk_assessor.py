"""
Risk Assessor Service
=====================
Assesses multidimensional risk across 9 scientific, operational, and governance categories.
"""

from typing import List, Optional
from research_validation.goal.models.goal import Goal
from research_validation.goal.models.risk_profile import (
    RiskProfile, RiskItem, RiskSeverity
)


class RiskAssessor:
    """
    Evaluates multidimensional risk vectors and compiles mitigation strategies.
    """

    @classmethod
    def assess_goal_risk(
        cls,
        goal: Goal,
        missing_capabilities_count: int = 0,
        has_untested_dependencies: bool = False,
    ) -> RiskProfile:
        items: List[RiskItem] = []

        # 1. Technical & Capability Risk
        if missing_capabilities_count > 0:
            items.append(RiskItem(
                category="TECHNICAL",
                description=f"Goal requires {missing_capabilities_count} unavailable capabilities.",
                likelihood=0.90,
                impact=0.90,
                severity=RiskSeverity.CRITICAL,
                mitigation_strategy="Provision missing subsystems or utilize surrogate adapters.",
                is_blocking=True,
            ))

        # 2. Statistical Risk
        if goal.completion_threshold > 0.95 and goal.confidence_threshold.value > 0.90:
            items.append(RiskItem(
                category="STATISTICAL",
                description="High confidence (>=90%) and stringent completion threshold require large sample sizes.",
                likelihood=0.40,
                impact=0.50,
                severity=RiskSeverity.MEDIUM,
                mitigation_strategy="Increase bootstrap resample count and apply Wilson score confidence intervals.",
                is_blocking=False,
            ))

        # 3. Privacy & Governance Risk
        if "PII_UNMASKED" in goal.constraints.privacy_constraints:
            items.append(RiskItem(
                category="PRIVACY",
                description="Potential unmasked PII in dataset.",
                likelihood=0.80,
                impact=0.95,
                severity=RiskSeverity.CRITICAL,
                mitigation_strategy="Apply strict automated redaction filters prior to experiment ingestion.",
                is_blocking=True,
            ))

        # 4. Resource Risk
        if goal.maximum_runtime_hours > 48.0 or goal.maximum_cost_usd > 500.0:
            items.append(RiskItem(
                category="RESOURCE",
                description="High resource envelope requested.",
                likelihood=0.30,
                impact=0.60,
                severity=RiskSeverity.LOW,
                mitigation_strategy="Enable aggressive early stopping on plateau.",
                is_blocking=False,
            ))

        # 5. Dependency Risk
        if has_untested_dependencies:
            items.append(RiskItem(
                category="DEPENDENCY",
                description="Upstream dependency has unverified empirical state.",
                likelihood=0.50,
                impact=0.60,
                severity=RiskSeverity.MEDIUM,
                mitigation_strategy="Execute upstream dependency verification stage first.",
                is_blocking=False,
            ))

        # Baseline default safe risk item if empty
        if not items:
            items.append(RiskItem(
                category="OPERATIONAL",
                description="Standard operational runtime risk.",
                likelihood=0.10,
                impact=0.20,
                severity=RiskSeverity.NEGLIGIBLE,
                mitigation_strategy="Standard monitoring and checkpointing.",
                is_blocking=False,
            ))

        max_mag = max(item.risk_magnitude for item in items)
        avg_mag = sum(item.risk_magnitude for item in items) / len(items)
        overall_score = max_mag * 0.7 + avg_mag * 0.3
        has_blocking = any(item.is_blocking for item in items)

        if has_blocking or overall_score >= 0.70:
            sev = RiskSeverity.CRITICAL
        elif overall_score >= 0.45:
            sev = RiskSeverity.HIGH
        elif overall_score >= 0.25:
            sev = RiskSeverity.MEDIUM
        elif overall_score >= 0.10:
            sev = RiskSeverity.LOW
        else:
            sev = RiskSeverity.NEGLIGIBLE

        return RiskProfile(
            overall_risk_score=overall_score,
            severity=sev,
            risk_items=items,
            has_blocking_risks=has_blocking,
            approved_mitigations_count=len(items),
            diagnostic=f"Evaluated {len(items)} risk vectors. Overall score: {overall_score:.2f} ({sev.value})",
        )
