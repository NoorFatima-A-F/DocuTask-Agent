"""
Human Feedback Memory for Human-In-The-Loop Collaboration.
Stores validated human corrections into long-term Semantic and Episodic memory,
ensuring the agent learns from human supervision and never repeats corrected mistakes.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, Optional

from app.agents.human.feedback_processor import HumanFeedbackDirective
from app.agents.memory.intelligence.episodic_memory import EpisodeRecord, EpisodicMemory
from app.agents.memory.intelligence.semantic_memory import SemanticFact, SemanticMemory

logger = logging.getLogger(__name__)


class HumanFeedbackMemory:
    """Propagates verified human corrections into the permanent cognitive memory tiers."""

    def __init__(
        self,
        semantic_memory: Optional[SemanticMemory] = None,
        episodic_memory: Optional[EpisodicMemory] = None,
    ) -> None:
        self.semantic_memory = semantic_memory
        self.episodic_memory = episodic_memory

    def learn_from_feedback(
        self,
        directive: HumanFeedbackDirective,
        document_id: str = "",
        document_domain: str = "FINANCIAL",
    ) -> None:
        """Embeds human correction directly into episodic and semantic stores."""
        # 1. Store in Episodic Memory
        if self.episodic_memory:
            ep = EpisodeRecord(
                goal_description=f"HITL Correction on execution {directive.execution_id}",
                intent="HUMAN_INTERVENTION",
                task_name=directive.task_id,
                agent_id=f"human:{directive.operator_id}",
                outcome="SUCCESS" if directive.should_resume_graph else "FAILURE",
                reflection_notes=directive.guidance_notes,
                importance=0.95,  # Human corrections carry maximum importance
                tags=["hitl", "human_correction", directive.action_type.value.lower()],
                metadata={
                    "document_id": document_id,
                    "effective_data": directive.effective_data,
                    "operator_id": directive.operator_id,
                },
            )
            self.episodic_memory.record_episode(ep)
            logger.info("HumanFeedbackMemory: Recorded episodic correction %s", ep.episode_id)

        # 2. Store individual field corrections in Semantic Memory
        if self.semantic_memory and directive.effective_data:
            vendor = directive.effective_data.get("vendor_name", "VendorCorrection")
            for k, v in directive.effective_data.items():
                if v is not None and k not in ("raw_text", "bounding_boxes"):
                    fact = SemanticFact(
                        subject=str(vendor),
                        predicate=f"verified_{k}",
                        fact_value=v,
                        domain=document_domain,
                        confidence=1.0,  # Human ground truth
                        importance=0.95,
                        tags=["human_verified", k, str(vendor).lower()],
                        metadata={
                            "source": "human_operator",
                            "operator_id": directive.operator_id,
                            "execution_id": directive.execution_id,
                        },
                    )
                    self.semantic_memory.store_fact(fact)
                    logger.debug("HumanFeedbackMemory: Stored ground-truth fact '%s %s'", fact.subject, fact.predicate)
