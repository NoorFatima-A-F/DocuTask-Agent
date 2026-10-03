"""
Risk Evaluation Engine implementing Probability * Impact * Exposure scoring model.
"""
from __future__ import annotations
import uuid
from typing import Any, Dict, List, Optional
from app.platform_verification.certification_engine.domain.interfaces import IRiskEngine
from app.platform_verification.certification_engine.domain.models import (
    GateEvaluationResult,
    RiskAssessment,
    RiskLevel,
    Severity,
)


class EnterpriseRiskEngine(IRiskEngine):
    """Calculates risk scores based on severity of failed gates, exposure level, and context."""

    def assess_risk(
        self,
        system_id: str,
        failed_gates: List[GateEvaluationResult],
        metrics: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None,
    ) -> RiskAssessment:
        ctx = context or {}
        exposure = int(ctx.get("exposure_level", 4))  # 1 (isolated test) to 5 (full prod)
        
        # Calculate impact and probability based on failed gates
        if not failed_gates:
            probability = 1
            impact = 1
            identified_risks = ["No gate failures detected. Baseline operational risk."]
        else:
            has_critical = any(g.severity == Severity.CRITICAL for g in failed_gates)
            has_high = any(g.severity == Severity.HIGH for g in failed_gates)
            has_security = any(g.category.value == "SECURITY" for g in failed_gates)
            
            if has_critical or has_security:
                impact = 5
                probability = 4
            elif has_high:
                impact = 4
                probability = 3
            else:
                impact = 2
                probability = 2

            identified_risks = [
                f"Failed gate '{g.gate_name}' ({g.category.value}): {', '.join(g.failure_reasons)}"
                for g in failed_gates
            ]

        # Additional risk signals from metrics
        if metrics.get("critical_vulnerabilities", 0) > 0:
            impact = 5
            probability = 5
            identified_risks.append(f"Detected {metrics.get('critical_vulnerabilities')} critical security vulnerabilities.")

        if metrics.get("hallucination_rate", 0.0) > 0.08:
            impact = max(impact, 4)
            probability = max(probability, 4)
            identified_risks.append(f"Elevated AI hallucination rate: {metrics.get('hallucination_rate'):.2%}")

        mitigating_controls = ctx.get("mitigations", ["Automated rollback enabled", "Canary deployment 5%"])

        return RiskAssessment(
            risk_id=f"RISK-{uuid.uuid4().hex[:8].upper()}",
            system_id=system_id,
            probability=probability,
            impact=impact,
            exposure=exposure,
            identified_risks=identified_risks,
            mitigating_controls=mitigating_controls,
        )
