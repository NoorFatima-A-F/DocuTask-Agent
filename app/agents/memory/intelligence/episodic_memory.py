"""Tier 3: Episodic Memory (Execution History & Experiences).

Stores records of past runs, failures, reflection cycles, and successful recovery
trajectories, allowing agents to learn from historical outcomes.
"""

from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from app.agents.memory.intelligence.retrieval_scorer import RetrievalScorer


@dataclass
class EpisodeRecord:
    """Historical record of an agent's execution episode."""

    episode_id: str = field(default_factory=lambda: f"ep_{uuid.uuid4().hex[:10]}")
    goal_description: str = ""
    intent: str = ""
    task_name: str = ""
    agent_id: str = ""
    tools_used: List[str] = field(default_factory=list)
    outcome: str = "SUCCESS"  # "SUCCESS", "FAILURE", "RECOVERED"
    error_summary: Optional[str] = None
    reflection_notes: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    importance: float = 0.5
    created_at: float = field(default_factory=time.time)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_searchable_text(self) -> str:
        parts = [self.goal_description, self.intent, self.task_name, self.agent_id, self.outcome]
        if self.error_summary:
            parts.append(self.error_summary)
        if self.reflection_notes:
            parts.append(self.reflection_notes)
        parts.extend(self.tags)
        return " ".join(parts)


class EpisodicMemory:
    """Stores and retrieves historical execution episodes."""

    def __init__(self, scorer: Optional[RetrievalScorer] = None) -> None:
        self.scorer = scorer or RetrievalScorer()
        self._episodes: Dict[str, EpisodeRecord] = {}

    def record_episode(self, episode: EpisodeRecord) -> str:
        self._episodes[episode.episode_id] = episode
        return episode.episode_id

    def get_episode(self, episode_id: str) -> Optional[EpisodeRecord]:
        return self._episodes.get(episode_id)

    def retrieve_relevant_episodes(
        self,
        query: str,
        task_tags: Optional[List[str]] = None,
        top_k: int = 5,
        min_score: float = 0.20,
    ) -> List[tuple[EpisodeRecord, float]]:
        """Retrieve most relevant historical episodes ranked by the multi-factor scoring formula."""
        tags = task_tags or []
        now = time.time()
        scored: List[tuple[EpisodeRecord, float]] = []

        for ep in self._episodes.values():
            text = ep.to_searchable_text()
            score = self.scorer.calculate_score(
                query=query,
                memory_content=text,
                importance=ep.importance,
                timestamp=ep.created_at,
                memory_tags=ep.tags,
                current_task_tags=tags,
                current_time=now,
            )
            if score >= min_score:
                scored.append((ep, score))

        scored.sort(key=lambda item: item[1], reverse=True)
        return scored[:top_k]

    def count(self) -> int:
        return len(self._episodes)
