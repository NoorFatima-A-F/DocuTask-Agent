"""Unified Agent Memory System.

Coordinates the 4-Tier Memory Architecture:
1. Short-Term Memory (Scratchpad / Volatile tokens)
2. Working Memory (Active Task & Plan Context)
3. Episodic Memory (Historical Runs & Past Corrections)
4. Semantic Memory (Domain Facts & Permanent Learned Rules)
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from app.agents.memory.intelligence.episodic_memory import (
    EpisodeRecord,
    EpisodicMemory,
)
from app.agents.memory.intelligence.retrieval_scorer import (
    RetrievalScorer,
    RetrievalScoringConfig,
)
from app.agents.memory.intelligence.semantic_memory import (
    SemanticFact,
    SemanticMemory,
)
from app.agents.memory.intelligence.short_term_memory import ShortTermMemory
from app.agents.memory.intelligence.working_memory import WorkingMemory

logger = logging.getLogger(__name__)


@dataclass
class MemoryContextBundle:
    """Consolidated context retrieved from all memory tiers for agent reasoning."""

    working_context: Dict[str, Any]
    relevant_episodes: List[Dict[str, Any]]
    relevant_facts: List[Dict[str, Any]]
    scratchpad_summary: List[str]


class AgentMemorySystem:
    """Unified 4-Tier Memory System for Autonomous Agent OS."""

    def __init__(self, session_id: str, config: Optional[RetrievalScoringConfig] = None) -> None:
        self.session_id = session_id
        self.scorer = RetrievalScorer(config)
        self.short_term = ShortTermMemory()
        self.working = WorkingMemory(session_id=session_id)
        self.episodic = EpisodicMemory(scorer=self.scorer)
        self.semantic = SemanticMemory(scorer=self.scorer)

    def assemble_context_bundle(
        self,
        query: str,
        task_tags: Optional[List[str]] = None,
        top_k: int = 3,
    ) -> MemoryContextBundle:
        """Query episodic and semantic memory alongside active working memory."""
        episodes = self.episodic.retrieve_relevant_episodes(query, task_tags=task_tags, top_k=top_k)
        facts = self.semantic.retrieve_relevant_facts(query, task_tags=task_tags, top_k=top_k)

        ep_list = [
            {
                "episode_id": ep.episode_id,
                "task": ep.task_name,
                "outcome": ep.outcome,
                "reflection": ep.reflection_notes,
                "score": score,
            }
            for ep, score in episodes
        ]

        fact_list = [
            {
                "subject": f.subject,
                "predicate": f.predicate,
                "value": f.fact_value,
                "score": score,
            }
            for f, score in facts
        ]

        return MemoryContextBundle(
            working_context=self.working.export_snapshot(),
            relevant_episodes=ep_list,
            relevant_facts=fact_list,
            scratchpad_summary=self.short_term.list_keys(),
        )

    def finalize_and_learn(
        self,
        goal_description: str,
        intent: str,
        outcome: str,
        reflection_notes: Optional[str] = None,
        learned_facts: Optional[List[SemanticFact]] = None,
    ) -> str:
        """Promote working memory findings to Episodic and Semantic memory tiers."""
        errors = self.working.get_errors()
        error_summary = "; ".join([e["error"] for e in errors]) if errors else None

        episode = EpisodeRecord(
            goal_description=goal_description,
            intent=intent,
            task_name=self.working.state.current_task_id,
            outcome=outcome,
            error_summary=error_summary,
            reflection_notes=reflection_notes,
            tags=[intent.lower(), outcome.lower(), "autonomous_execution"],
            importance=0.85 if outcome == "SUCCESS" else 0.95,
        )
        ep_id = self.episodic.record_episode(episode)
        logger.info("Promoted execution to EpisodicMemory: %s (%s)", ep_id, outcome)

        if learned_facts:
            for fact in learned_facts:
                fid = self.semantic.store_fact(fact)
                logger.info("Learned new Semantic Fact: %s (%s %s)", fid, fact.subject, fact.predicate)

        return ep_id
