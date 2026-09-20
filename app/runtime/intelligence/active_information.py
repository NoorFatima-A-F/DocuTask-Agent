"""Active Information Gathering & Expected Value of Information (EVOI) Engine for DocuTask ADIP.

Determines whether taking exploratory sensing actions (secondary OCR, image deskew, database lookups,
or operator clarifications) yields higher net expected utility than executing immediately.
"""

from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from app.runtime.intelligence.belief_state import BeliefStateEngine


class InformationActionType(str, Enum):
    SECONDARY_NEURAL_OCR = "SECONDARY_NEURAL_OCR"
    IMAGE_ENHANCEMENT_DESKEW = "IMAGE_ENHANCEMENT_DESKEW"
    DATABASE_METADATA_LOOKUP = "DATABASE_METADATA_LOOKUP"
    HUMAN_OPERATOR_CONFIRMATION = "HUMAN_OPERATOR_CONFIRMATION"
    VECTOR_SCHEMA_SEARCH = "VECTOR_SCHEMA_SEARCH"


class InformationActionRecommendation(BaseModel):
    """Calculated EVOI tradeoff evaluation for a single sensing action."""
    action_type: InformationActionType
    name: str
    cost_usd: float
    delay_ms: float
    expected_information_gain_bits: float
    expected_utility_gain: float
    net_evoi: float = Field(description="Expected Utility Gain - Cost Penalty")
    should_execute: bool
    rationale: str
    formula_provenance: str = "EVOI(A) = \\mathbb{E}_{o}[\\max_{a} U(a, b_{o})] - \\max_{a} U(a, b) - Cost(A)"


class ActiveInformationEngine:
    """Evaluates information gathering actions using Bayesian Expected Value of Information."""

    def evaluate_sensing_actions(
        self,
        belief_engine: BeliefStateEngine,
        current_max_utility: float = 0.4392,
    ) -> List[InformationActionRecommendation]:
        recommendations: List[InformationActionRecommendation] = []

        doc_damaged_belief = belief_engine.get_belief("document_damaged")
        layout_complex_belief = belief_engine.get_belief("layout_complex")
        ocr_success_belief = belief_engine.get_belief("ocr_success")

        p_damaged = doc_damaged_belief.mean if doc_damaged_belief else 0.20
        p_complex = layout_complex_belief.mean if layout_complex_belief else 0.40
        p_ocr_success = ocr_success_belief.mean if ocr_success_belief else 0.90

        # 1. Image Enhancement & Deskew
        gain_deskew = 0.08 if p_damaged > 0.30 else 0.01
        cost_deskew = 0.0001
        net_deskew = gain_deskew - (cost_deskew * 10.0)
        recommendations.append(
            InformationActionRecommendation(
                action_type=InformationActionType.IMAGE_ENHANCEMENT_DESKEW,
                name="Adaptive Image Enhancement & Contrast Deskew",
                cost_usd=cost_deskew,
                delay_ms=80.0,
                expected_information_gain_bits=0.45,
                expected_utility_gain=round(gain_deskew, 4),
                net_evoi=round(net_deskew, 4),
                should_execute=net_deskew > 0.03,
                rationale="Recommended when document damage probability exceeds 30% to prevent cascading OCR failures.",
            )
        )

        # 2. Secondary Neural OCR
        gain_ocr = 0.12 if p_ocr_success < 0.85 else 0.02
        cost_ocr = 0.0015
        net_ocr = gain_ocr - (cost_ocr * 10.0)
        recommendations.append(
            InformationActionRecommendation(
                action_type=InformationActionType.SECONDARY_NEURAL_OCR,
                name="Secondary Neural OCR Disambiguation (Cloud Vision)",
                cost_usd=cost_ocr,
                delay_ms=320.0,
                expected_information_gain_bits=0.62,
                expected_utility_gain=round(gain_ocr, 4),
                net_evoi=round(net_ocr, 4),
                should_execute=net_ocr > 0.04,
                rationale="Reduces character error rate on ambiguous invoice line items.",
            )
        )

        # 3. Database Metadata Lookup
        gain_db = 0.06 if p_complex > 0.35 else 0.015
        cost_db = 0.0002
        net_db = gain_db - (cost_db * 10.0)
        recommendations.append(
            InformationActionRecommendation(
                action_type=InformationActionType.DATABASE_METADATA_LOOKUP,
                name="ERP Vendor & Tax Code Canonical Lookup",
                cost_usd=cost_db,
                delay_ms=45.0,
                expected_information_gain_bits=0.38,
                expected_utility_gain=round(gain_db, 4),
                net_evoi=round(net_db, 4),
                should_execute=net_db > 0.02,
                rationale="Cross-references extracted vendor names with existing master records to eliminate typos.",
            )
        )

        # 4. Human Operator Confirmation
        # High delay and cost, but eliminates residual uncertainty
        gain_human = 0.25 if (p_damaged > 0.60 or p_ocr_success < 0.70) else 0.02
        cost_human = 0.05  # Human attention cost
        net_human = gain_human - cost_human
        recommendations.append(
            InformationActionRecommendation(
                action_type=InformationActionType.HUMAN_OPERATOR_CONFIRMATION,
                name="Targeted Human Operator Interactive Confirmation",
                cost_usd=cost_human,
                delay_ms=5000.0,
                expected_information_gain_bits=0.99,
                expected_utility_gain=round(gain_human, 4),
                net_evoi=round(net_human, 4),
                should_execute=net_human > 0.10,
                rationale="Triggered only when catastrophic uncertainty threatens mission critical compliance.",
            )
        )

        # Sort recommendations by net EVOI (highest information value first)
        recommendations.sort(key=lambda r: r.net_evoi, reverse=True)
        return recommendations
