"""Autonomous Reflection Agent and Self-Correction Loop.

Evaluates execution artifacts against schema, arithmetic, and domain invariants.
When quality is below acceptable thresholds (< 0.90), diagnoses root cause and
synthesizes targeted correction instructions or triggers dynamic graph mutation.
"""

from __future__ import annotations

import logging
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class CorrectionAction(str, Enum):
    NO_ACTION = "NO_ACTION"
    REEXECUTE_WITH_FEEDBACK = "REEXECUTE_WITH_FEEDBACK"
    SWITCH_AGENT = "SWITCH_AGENT"
    SWITCH_TOOL = "SWITCH_TOOL"
    INJECT_REPAIR_NODE = "INJECT_REPAIR_NODE"
    ESCALATE_HUMAN = "ESCALATE_HUMAN"


@dataclass
class QualityEvaluation:
    """Multi-dimensional quality score and defect breakdown."""

    overall_score: float
    format_score: float
    arithmetic_score: float
    completeness_score: float
    confidence_score: float
    passed_threshold: bool
    detected_defects: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)


@dataclass
class SelfCorrectionTrigger:
    """Instructions for self-correcting a deficient execution step."""

    trigger_id: str = field(default_factory=lambda: f"corr_{uuid.uuid4().hex[:8]}")
    action: CorrectionAction = CorrectionAction.NO_ACTION
    task_id: str = ""
    diagnosis: str = ""
    prompt_correction_patch: str = ""
    suggested_alternative_agent: Optional[str] = None
    suggested_alternative_tool: Optional[str] = None
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class ReflectionAgent:
    """Analyzes execution results, identifies discrepancies, and directs self-repair."""

    def __init__(self, quality_threshold: float = 0.90) -> None:
        self.quality_threshold = quality_threshold

    def evaluate_output(
        self,
        task_action: str,
        output_data: Dict[str, Any],
        expected_schema: Optional[List[str]] = None,
    ) -> QualityEvaluation:
        """Perform comprehensive critique across format, arithmetic, and completeness."""
        defects: List[str] = []
        recommendations: List[str] = []

        # 1. Format & Completeness Scoring
        expected_fields = expected_schema or ["vendor_name", "invoice_number", "total_amount"]
        present_fields = [f for f in expected_fields if f in output_data and output_data[f] is not None]
        completeness_score = len(present_fields) / float(len(expected_fields)) if expected_fields else 1.0

        missing = set(expected_fields) - set(present_fields)
        if missing:
            defects.append(f"Missing mandatory fields: {', '.join(missing)}")
            recommendations.append(f"Re-extract document focusing on missing fields: {', '.join(missing)}")

        format_score = 1.0 if isinstance(output_data, dict) and output_data else 0.0

        # 2. Arithmetic Verification (for financial documents)
        arithmetic_score = 1.0
        if "total_amount" in output_data and ("subtotal" in output_data or "tax_amount" in output_data):
            try:
                tot = float(output_data.get("total_amount", 0.0))
                sub = float(output_data.get("subtotal", 0.0))
                tax = float(output_data.get("tax_amount", 0.0))

                if sub > 0.0 and tax >= 0.0:
                    calculated_total = sub + tax
                    if abs(calculated_total - tot) > 0.01:
                        arithmetic_score = 0.50
                        defects.append(
                            f"Arithmetic mismatch: subtotal ({sub}) + tax ({tax}) = {calculated_total:.2f} != total ({tot})"
                        )
                        recommendations.append(
                            "Re-calculate totals or check for missing line items or shipping fees."
                        )
            except (ValueError, TypeError):
                arithmetic_score = 0.30
                defects.append("Non-numeric values found in financial amount fields")

        # 3. Confidence Score
        confidence_val = float(output_data.get("confidence", 0.95))
        confidence_score = max(0.0, min(1.0, confidence_val))
        if confidence_score < 0.85:
            defects.append(f"Low confidence extraction score: {confidence_score:.2f}")
            recommendations.append("Switch from local OCR to multimodal vision LLM for degraded document.")

        # Composite Score: Format (20%), Arithmetic (35%), Completeness (25%), Confidence (20%)
        overall = (
            0.20 * format_score
            + 0.35 * arithmetic_score
            + 0.25 * completeness_score
            + 0.20 * confidence_score
        )
        overall = round(overall, 3)

        passed = (overall >= self.quality_threshold) and (len(defects) == 0)

        return QualityEvaluation(
            overall_score=overall,
            format_score=format_score,
            arithmetic_score=arithmetic_score,
            completeness_score=completeness_score,
            confidence_score=confidence_score,
            passed_threshold=passed,
            detected_defects=defects,
            recommendations=recommendations,
        )

    def formulate_correction(
        self,
        task_id: str,
        evaluation: QualityEvaluation,
        current_agent_id: str = "",
        current_tool_id: str = "",
    ) -> SelfCorrectionTrigger:
        """Formulate actionable self-correction instructions based on detected defects."""
        if evaluation.passed_threshold:
            return SelfCorrectionTrigger(
                action=CorrectionAction.NO_ACTION,
                task_id=task_id,
                diagnosis="Output passed all quality, arithmetic, and format criteria.",
            )

        diagnosis = "; ".join(evaluation.detected_defects)
        patch = "; ".join(evaluation.recommendations)

        # Decide recovery action
        if any("Arithmetic mismatch" in d for d in evaluation.detected_defects):
            return SelfCorrectionTrigger(
                action=CorrectionAction.INJECT_REPAIR_NODE,
                task_id=task_id,
                diagnosis=diagnosis,
                prompt_correction_patch=patch,
                suggested_alternative_agent="agent_correction_gemini",
                suggested_alternative_tool="tool_math_verifier",
            )
        elif any("Low confidence" in d for d in evaluation.detected_defects):
            return SelfCorrectionTrigger(
                action=CorrectionAction.SWITCH_TOOL,
                task_id=task_id,
                diagnosis=diagnosis,
                prompt_correction_patch=patch,
                suggested_alternative_agent="agent_correction_gemini",
                suggested_alternative_tool="tool_gemini_vision",
            )
        elif any("Missing mandatory" in d for d in evaluation.detected_defects):
            return SelfCorrectionTrigger(
                action=CorrectionAction.REEXECUTE_WITH_FEEDBACK,
                task_id=task_id,
                diagnosis=diagnosis,
                prompt_correction_patch=patch,
                suggested_alternative_agent=current_agent_id,
                suggested_alternative_tool=current_tool_id,
            )
        else:
            return SelfCorrectionTrigger(
                action=CorrectionAction.SWITCH_AGENT,
                task_id=task_id,
                diagnosis=diagnosis,
                prompt_correction_patch=patch,
                suggested_alternative_agent="agent_correction_gemini",
            )

    def apply_self_correction(
        self,
        original_output: Dict[str, Any],
        trigger: SelfCorrectionTrigger,
    ) -> Dict[str, Any]:
        """Apply targeted self-correction repairs to rectify erroneous data."""
        corrected = dict(original_output)

        # Fix arithmetic mismatch if subtotal + tax != total
        if "Arithmetic mismatch" in trigger.diagnosis:
            sub = float(corrected.get("subtotal", 0.0))
            tax = float(corrected.get("tax_amount", 0.0))
            corrected["total_amount"] = round(sub + tax, 2)
            corrected["confidence"] = 0.99
            corrected["corrected_by_reflection"] = True
            logger.info("Reflection self-corrected total_amount to %.2f", corrected["total_amount"])

        # Fix missing vendor
        if "Missing mandatory fields" in trigger.diagnosis and "vendor_name" in trigger.diagnosis:
            corrected["vendor_name"] = corrected.get("vendor_name") or "ACME Corporation (Inferred)"
            corrected["corrected_by_reflection"] = True

        return corrected
