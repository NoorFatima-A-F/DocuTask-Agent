"""
LLM Semantic Critic for Multi-Critic Reflection System.
Evaluates semantic plausibility, detects hallucinations, and checks contextual coherence.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from app.agents.intelligence.reasoning.llm_reasoning_client import LLMReasoningClient
from app.agents.reflection.critics.rule_critic import CritiqueFeedback

logger = logging.getLogger(__name__)


class LLMCritiqueSchema(BaseModel):
    """Structured LLM critique evaluation format."""

    plausibility_score: float = Field(default=0.9, ge=0.0, le=1.0)
    passed: bool = Field(default=True)
    detected_hallucinations: List[str] = Field(default_factory=list)
    semantic_inconsistencies: List[str] = Field(default_factory=list)
    recommended_repairs: List[str] = Field(default_factory=list)
    critique_notes: str = Field(default="")


class LLMCritic:
    """Semantic critic utilizing LLM reasoning for deep content critique."""

    def __init__(self, llm_client: Optional[LLMReasoningClient] = None) -> None:
        self.llm_client = llm_client or LLMReasoningClient()

    async def evaluate(
        self,
        extracted_data: Dict[str, Any],
        raw_text_context: Optional[str] = None,
        goal_description: str = "",
    ) -> CritiqueFeedback:
        """Runs semantic evaluation of extraction against the source context and goal."""
        prompt = f"""Review the extracted document payload for semantic correctness, plausible values, and hallucinations:
Goal: {goal_description}
Extracted Data: {extracted_data}
Context Snippet: {raw_text_context or 'N/A'}

Provide plausibility score, detect hallucinations or contradictions, and list recommended repair actions."""

        critique = await self.llm_client.generate_structured(
            prompt=prompt,
            schema_model=LLMCritiqueSchema,
            system_instruction="You are an expert QA auditor reviewing automated AI document extractions.",
        )

        all_issues = list(critique.detected_hallucinations) + list(critique.semantic_inconsistencies)
        return CritiqueFeedback(
            critic_name="LLMCritic",
            score=round(critique.plausibility_score, 4),
            passed=critique.passed and critique.plausibility_score >= 0.85,
            issues=all_issues,
            suggestions=critique.recommended_repairs,
        )
