"""
Semantic Reasoner for Autonomous Agent Operating System.
Fuses cognitive deductive memory, structured LLM reasoning, and contextual evidence
to resolve complex goals, deduce corrective actions, and resolve execution anomalies.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from app.agents.intelligence.reasoning.llm_reasoning_client import LLMReasoningClient
from app.agents.intelligence.reasoning.reasoning_memory import PremiseType, ReasoningMemory

logger = logging.getLogger(__name__)


class SemanticAnalysisResult(BaseModel):
    """Structured result of semantic goal or anomaly analysis."""

    primary_intent: str = Field(default="general_processing")
    document_type: str = Field(default="generic")
    confidence: float = Field(default=0.9, ge=0.0, le=1.0)
    key_entities: List[str] = Field(default_factory=list)
    constraints: Dict[str, Any] = Field(default_factory=dict)
    recommended_strategy: str = Field(default="standard")
    rationale: str = Field(default="")
    suggested_actions: List[str] = Field(default_factory=list)


class AnomalyAnalysisResult(BaseModel):
    """Structured diagnosis of execution errors or quality drops."""

    root_cause: str = Field(default="unknown")
    severity: str = Field(default="medium")
    is_recoverable: bool = Field(default=True)
    suggested_fix: str = Field(default="retry")
    mutation_recommended: bool = Field(default=False)
    new_nodes_to_insert: List[str] = Field(default_factory=list)
    rationale: str = Field(default="")


class SemanticReasoner:
    """Core semantic intelligence engine powering the autonomous runtime loop."""

    def __init__(self, llm_client: Optional[LLMReasoningClient] = None) -> None:
        self.llm_client = llm_client or LLMReasoningClient()

    async def reason_about_goal(
        self,
        goal_text: str,
        memory: Optional[ReasoningMemory] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> SemanticAnalysisResult:
        """Analyzes a high-level user goal using multi-premise reasoning."""
        mem = memory or ReasoningMemory()

        # 1. Establish ground truth premises
        mem.add_premise(
            statement=f"User goal: {goal_text}",
            premise_type=PremiseType.GOAL_OBJECTIVE,
            source="user_input",
            confidence=1.0,
        )

        if context:
            for k, v in context.items():
                mem.add_premise(
                    statement=f"Context factor {k}: {v}",
                    premise_type=PremiseType.SCHEMA_CONSTRAINT,
                    source="runtime_context",
                    confidence=0.95,
                )

        # 2. Formulate hypothesis via structured LLM prompt
        ctx_data = context or {}
        prompt = f"""Analyze the following agent goal and deduce execution requirements:
Goal: {goal_text}
Runtime Context: {ctx_data}
Identify the primary intent, document type, required key entities, strict constraints, recommended strategy, and rationale."""

        result = await self.llm_client.generate_structured(
            prompt=prompt,
            schema_model=SemanticAnalysisResult,
            system_instruction="You are an expert cognitive planner in an autonomous agent operating system.",
        )

        # 3. Update memory ledger
        hypo = mem.create_hypothesis(
            description=f"Goal classification: {result.primary_intent} on {result.document_type}",
            initial_confidence=result.confidence,
        )
        mem.validate_hypothesis(hypo.hypothesis_id, final_confidence=result.confidence)

        logger.info("Semantic reasoning concluded for goal: %s (intent=%s)", goal_text[:50], result.primary_intent)
        return result

    async def evaluate_anomaly(
        self,
        task_id: str,
        error_message: str,
        partial_output: Optional[Dict[str, Any]] = None,
        memory: Optional[ReasoningMemory] = None,
    ) -> AnomalyAnalysisResult:
        """Diagnoses execution anomalies and recommends dynamic graph mutations."""
        mem = memory or ReasoningMemory()

        mem.add_premise(
            statement=f"Task {task_id} failed with error: {error_message}",
            premise_type=PremiseType.INTERMEDIATE_DEDUCTION,
            source="execution_engine",
            confidence=1.0,
        )

        out_data = partial_output or {}
        prompt = f"""A task execution failed in the agent DAG. Analyze the root cause and prescribe recovery actions:
Task ID: {task_id}
Error: {error_message}
Partial Output: {out_data}

Determine if the error is recoverable, whether dynamic DAG mutation is required, and suggest specific repair nodes."""

        result = await self.llm_client.generate_structured(
            prompt=prompt,
            schema_model=AnomalyAnalysisResult,
            system_instruction="You are an SRE and autonomous recovery expert diagnosing pipeline failures.",
        )

        logger.warning(
            "Anomaly evaluated for task %s: root_cause=%s, recoverable=%s, mutation=%s",
            task_id,
            result.root_cause,
            result.is_recoverable,
            result.mutation_recommended,
        )
        return result
