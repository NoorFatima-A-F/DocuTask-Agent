"""Enterprise Goal Parser.

Transforms natural language instructions or structured payloads into a
rich GoalSpecification with parsed requirements, priority, risk, and criteria.
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from app.agents.intelligence.goal.constraint_extractor import (
    ConstraintExtractor,
    ExtractedConstraints,
)
from app.agents.intelligence.goal.goal_specification import (
    GoalPriority,
    GoalSpecification,
    GoalStatus,
    RiskLevel,
)
from app.agents.intelligence.goal.intent_classifier import (
    IntentClassifier,
    IntentResult,
    IntentType,
)


class GoalParser:
    """Parses raw text goals into validated, executable GoalSpecifications."""

    def __init__(
        self,
        classifier: Optional[IntentClassifier] = None,
        extractor: Optional[ConstraintExtractor] = None,
    ) -> None:
        self.classifier = classifier or IntentClassifier()
        self.extractor = extractor or ConstraintExtractor()

    def parse(
        self,
        objective: str,
        context: Optional[Dict[str, Any]] = None,
        goal_id: Optional[str] = None,
    ) -> GoalSpecification:
        """Parse raw objective text and optional context into GoalSpecification."""
        ctx = context or {}
        intent_res: IntentResult = self.classifier.classify(objective, ctx)
        constraints: ExtractedConstraints = self.extractor.extract(objective, ctx)

        priority = self._determine_priority(objective, ctx)
        risk_level = self._assess_risk(intent_res.primary_intent, constraints)

        spec = GoalSpecification(
            objective=objective.strip(),
            goal_id=goal_id or GoalSpecification(objective="").goal_id,
            intent=intent_res.primary_intent.value,
            domain=intent_res.domain,
            priority=priority,
            risk_level=risk_level,
            status=GoalStatus.READY,
            input_requirements=self._infer_inputs(intent_res.primary_intent, ctx),
            expected_output=self._infer_outputs(intent_res.primary_intent, constraints),
            constraints=constraints.to_dict(),
            confidence_score=intent_res.confidence,
            sla_seconds=constraints.max_latency_seconds,
            metadata={
                "matched_keywords": intent_res.matched_keywords,
                "secondary_intents": [i.value for i in intent_res.secondary_intents],
                "context_provided": bool(ctx),
            },
        )

        # Generate measurable success criteria
        self._attach_default_criteria(spec, constraints)

        return spec

    def _determine_priority(self, text: str, context: Dict[str, Any]) -> GoalPriority:
        if "priority" in context:
            p = str(context["priority"]).upper()
            if p in GoalPriority.__members__:
                return GoalPriority(p)

        upper = text.upper()
        if any(w in upper for w in ["URGENT", "CRITICAL", "IMMEDIATE", "SEV-1", "P0", "BLOCKING"]):
            return GoalPriority.CRITICAL
        elif any(w in upper for w in ["HIGH", "ASAP", "EXPEDITE", "PRIORITY"]):
            return GoalPriority.HIGH
        elif any(w in upper for w in ["LOW", "BACKGROUND", "NIGHTLY", "WHENEVER"]):
            return GoalPriority.LOW
        return GoalPriority.MEDIUM

    def _assess_risk(self, intent: IntentType, constraints: ExtractedConstraints) -> RiskLevel:
        if "SOX" in constraints.compliance_frameworks or "HIPAA" in constraints.compliance_frameworks:
            return RiskLevel.CRITICAL
        if intent in (IntentType.FRAUD_DETECTION, IntentType.COMPLIANCE_AUDIT):
            return RiskLevel.HIGH
        if constraints.require_human_review:
            return RiskLevel.MEDIUM
        return RiskLevel.LOW

    def _infer_inputs(self, intent: IntentType, context: Dict[str, Any]) -> Dict[str, Any]:
        inputs: Dict[str, Any] = {
            "document_path": context.get("document_path", "required"),
            "document_bytes": context.get("document_bytes", None),
        }
        if intent in (IntentType.INVOICE_PROCESSING, IntentType.RECONCILIATION):
            inputs["expected_currency"] = context.get("currency", "USD")
        return inputs

    def _infer_outputs(self, intent: IntentType, constraints: ExtractedConstraints) -> Dict[str, Any]:
        outputs = {
            "format": constraints.output_format,
            "target_schema": f"Schema_{intent.value}",
        }
        if intent == IntentType.INVOICE_PROCESSING:
            outputs["fields"] = ["vendor_name", "invoice_number", "date", "line_items", "total_amount", "tax_amount"]
        elif intent == IntentType.FRAUD_DETECTION:
            outputs["fields"] = ["fraud_probability", "risk_factors", "anomaly_indicators"]
        return outputs

    def _attach_default_criteria(self, spec: GoalSpecification, constraints: ExtractedConstraints) -> None:
        spec.add_criterion(
            metric="accuracy",
            target=constraints.min_accuracy,
            op=">=",
            weight=1.5,
            mandatory=True,
        )
        spec.add_criterion(
            metric="schema_validation",
            target=1.0,
            op="==",
            weight=1.0,
            mandatory=True,
        )
        if constraints.max_latency_seconds:
            spec.add_criterion(
                metric="execution_latency_seconds",
                target=constraints.max_latency_seconds,
                op="<=",
                weight=0.8,
                mandatory=False,
            )
