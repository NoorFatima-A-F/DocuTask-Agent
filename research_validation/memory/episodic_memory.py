"""
Scientific Episodic Memory (Phase 84C)
=====================================
Captures time-ordered sequential research episodes and interaction context.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List

from research_validation.provenance.hashing import hash_canonical_json


@dataclass(frozen=True)
class ResearchEpisode:
    """A bounded chronological episode of scientific inquiry."""
    episode_id: str
    cycle_number: int
    intent: str
    actions_taken: List[str]
    observations: Dict[str, Any]
    outcome_summary: str
    start_time_utc: str
    end_time_utc: str
    episode_digest_sha256: str = field(default="")


class EpisodicMemoryStore:
    """Maintains sequential history of research cycles and ephemeral episodes."""

    def __init__(self, max_episodes: int = 1000):
        self.max_episodes = max_episodes
        self.episodes: List[ResearchEpisode] = []

    def record_episode(
        self,
        cycle_number: int,
        intent: str,
        actions_taken: List[str],
        observations: Dict[str, Any],
        outcome_summary: str,
        start_time_utc: str,
        end_time_utc: str,
    ) -> ResearchEpisode:
        episode_id = f"ep_{cycle_number}_{len(self.episodes)}"
        payload = {
            "episode_id": episode_id,
            "cycle_number": cycle_number,
            "intent": intent,
            "actions_taken": actions_taken,
            "observations": observations,
            "outcome_summary": outcome_summary,
        }
        digest = hash_canonical_json(payload)

        ep = ResearchEpisode(
            episode_id=episode_id,
            cycle_number=cycle_number,
            intent=intent,
            actions_taken=actions_taken,
            observations=observations,
            outcome_summary=outcome_summary,
            start_time_utc=start_time_utc,
            end_time_utc=end_time_utc,
            episode_digest_sha256=digest,
        )

        self.episodes.append(ep)
        if len(self.episodes) > self.max_episodes:
            self.episodes.pop(0)
        return ep

    def get_recent_episodes(self, limit: int = 10) -> List[ResearchEpisode]:
        return self.episodes[-limit:]
