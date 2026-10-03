"""
AI Decision Evidence Collector capturing model parameters, prompts, context, and explainability records.
"""
from __future__ import annotations
from typing import Any, Dict
from app.platform_verification.evidence_engine.domain.models import (
    AiDecisionEvidence,
    EvidenceArtifact,
    EvidenceCategory,
)
from app.platform_verification.evidence_engine.core.collector import EvidenceCollector


class AiDecisionEvidenceCollector:
    """Captures and sanitizes AI decision artifacts, strictly excluding private chain-of-thought."""

    def __init__(self, collector: EvidenceCollector) -> None:
        self.collector = collector

    def capture_ai_decision(self, execution_id: str, ai_evidence: AiDecisionEvidence) -> EvidenceArtifact:
        # Sanitize permitted reasoning to ensure no raw chain-of-thought is leaked
        sanitized_reasoning = dict(ai_evidence.permitted_reasoning)
        if "chain_of_thought" in sanitized_reasoning:
            del sanitized_reasoning["chain_of_thought"]
        if "private_cot" in sanitized_reasoning:
            del sanitized_reasoning["private_cot"]

        payload = {
            "model_info": ai_evidence.model_info,
            "prompt_info": ai_evidence.prompt_info,
            "context_info": ai_evidence.context_info,
            "tool_calls": ai_evidence.tool_calls,
            "permitted_reasoning": sanitized_reasoning,
        }

        return self.collector.collect(
            execution_id=execution_id,
            category=EvidenceCategory.EVALUATION_EVIDENCE,
            data=payload,
            metadata={"type": "ai_decision_provenance", "model": ai_evidence.model_info.get("model", "unknown")},
        )
