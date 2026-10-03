"""
Weighted SOLID Scoring & Certification Engine.
"""
from __future__ import annotations
from typing import Dict, List
from app.platform_verification.solid_verification.domain.interfaces import ISolidScoringEngine
from app.platform_verification.solid_verification.domain.models import (
    PrincipleScore,
    SolidCertificationBand,
    SolidPrinciple,
    SolidQualityScorecard,
    SolidViolation,
    SolidViolationSeverity,
)


class EnterpriseSolidScoringEngine(ISolidScoringEngine):
    """Calculates weighted scores: SRP (25%), OCP (20%), LSP (20%), ISP (15%), DIP (20%)."""

    def calculate_scorecard(
        self,
        violations: List[SolidViolation],
        total_classes: int,
    ) -> SolidQualityScorecard:
        weights = {
            SolidPrinciple.SRP: 0.25,
            SolidPrinciple.OCP: 0.20,
            SolidPrinciple.LSP: 0.20,
            SolidPrinciple.ISP: 0.15,
            SolidPrinciple.DIP: 0.20,
        }

        # Count violations per principle
        v_counts: Dict[SolidPrinciple, int] = {p: 0 for p in SolidPrinciple}
        crit_counts: Dict[SolidPrinciple, int] = {p: 0 for p in SolidPrinciple}
        high_counts: Dict[SolidPrinciple, int] = {p: 0 for p in SolidPrinciple}

        for v in violations:
            v_counts[v.principle] = v_counts.get(v.principle, 0) + 1
            if v.severity == SolidViolationSeverity.CRITICAL:
                crit_counts[v.principle] = crit_counts.get(v.principle, 0) + 1
            elif v.severity == SolidViolationSeverity.HIGH:
                high_counts[v.principle] = high_counts.get(v.principle, 0) + 1

        principle_scores: List[PrincipleScore] = []
        for p, weight in weights.items():
            crit = crit_counts[p]
            high = high_counts[p]
            other = v_counts[p] - crit - high

            deduction = min(100.0, (crit * 35.0) + (high * 15.0) + (other * 5.0))
            raw = max(0.0, 100.0 - deduction)
            w_score = raw * weight
            principle_scores.append(
                PrincipleScore(
                    principle=p,
                    weight=weight,
                    raw_score=raw,
                    weighted_score=w_score,
                    violations_count=v_counts[p],
                )
            )

        total_score = round(sum(ps.weighted_score for ps in principle_scores), 2)
        total_crit = sum(crit_counts.values())

        if total_score >= 95.0 and total_crit == 0:
            band = SolidCertificationBand.ENTERPRISE_DESIGN_QUALITY
            is_certified = True
        elif total_score >= 90.0 and total_crit == 0:
            band = SolidCertificationBand.PRODUCTION_QUALITY
            is_certified = True
        elif total_score >= 80.0 and total_crit == 0:
            band = SolidCertificationBand.ACCEPTABLE
            is_certified = True
        elif total_score >= 70.0:
            band = SolidCertificationBand.TECHNICAL_DEBT_WARNING
            is_certified = False
        else:
            band = SolidCertificationBand.FAILED
            is_certified = False

        return SolidQualityScorecard(
            total_score=total_score,
            certification_band=band,
            principle_scores=principle_scores,
            total_violations_count=len(violations),
            critical_violations_count=total_crit,
            is_design_certified=is_certified,
        )
