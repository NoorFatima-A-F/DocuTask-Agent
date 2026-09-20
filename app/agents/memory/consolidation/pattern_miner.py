"""
Pattern Miner for Memory Consolidation Intelligence.
Discovers recurring failure modes, vendor layout heuristics, and extraction corrections
across historical execution episodes.
"""

from __future__ import annotations

import logging
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from app.agents.memory.intelligence.episodic_memory import EpisodeRecord

logger = logging.getLogger(__name__)


@dataclass
class MinedPattern:
    """A recurring correlation or failure heuristic extracted across multiple episodes."""

    pattern_id: str
    pattern_type: str  # "FAILURE_CORRELATION", "VENDOR_HEURISTIC", "TOOL_INEFFICIENCY"
    description: str
    frequency: int
    confidence: float
    supporting_episode_ids: List[str] = field(default_factory=list)
    attributes: Dict[str, Any] = field(default_factory=dict)


class PatternMiner:
    """Mines latent behavioral patterns and systemic errors from episodic execution logs."""

    def __init__(self, min_support: int = 2) -> None:
        self.min_support = min_support

    def mine_patterns(self, episodes: List[EpisodeRecord]) -> List[MinedPattern]:
        """Analyzes a collection of episodes and returns verified recurring patterns."""
        patterns: List[MinedPattern] = []

        patterns.extend(self._mine_tool_failures(episodes))
        patterns.extend(self._mine_vendor_heuristics(episodes))
        patterns.extend(self._mine_reflection_corrections(episodes))

        logger.info("PatternMiner: Mined %d distinct patterns from %d episodes", len(patterns), len(episodes))
        return patterns

    def _mine_tool_failures(self, episodes: List[EpisodeRecord]) -> List[MinedPattern]:
        """Identifies tools that consistently fail on specific intents or tasks."""
        tool_failures: Dict[str, List[str]] = defaultdict(list)

        for ep in episodes:
            if ep.outcome == "FAILURE" or ep.error_summary:
                for tool in ep.tools_used:
                    key = f"{tool}:{ep.task_name or ep.intent}"
                    tool_failures[key].append(ep.episode_id)

        patterns = []
        for key, ep_ids in tool_failures.items():
            if len(ep_ids) >= self.min_support:
                tool, task = key.split(":", 1)
                patterns.append(
                    MinedPattern(
                        pattern_id=f"pat_tool_fail_{tool}_{len(patterns)}",
                        pattern_type="TOOL_INEFFICIENCY",
                        description=f"Tool '{tool}' frequently encounters errors on task/intent '{task}'",
                        frequency=len(ep_ids),
                        confidence=min(0.95, 0.5 + (0.1 * len(ep_ids))),
                        supporting_episode_ids=ep_ids,
                        attributes={"tool": tool, "task": task},
                    )
                )
        return patterns

    def _mine_vendor_heuristics(self, episodes: List[EpisodeRecord]) -> List[MinedPattern]:
        """Mines vendor-specific quirks recorded in metadata or reflection notes."""
        vendor_quirks: Dict[str, List[str]] = defaultdict(list)

        for ep in episodes:
            vendor = ep.metadata.get("vendor_name")
            if vendor and ep.reflection_notes:
                vendor_quirks[vendor].append(ep.episode_id)

        patterns = []
        for vendor, ep_ids in vendor_quirks.items():
            if len(ep_ids) >= self.min_support:
                patterns.append(
                    MinedPattern(
                        pattern_id=f"pat_vendor_{vendor}_{len(patterns)}",
                        pattern_type="VENDOR_HEURISTIC",
                        description=f"Vendor '{vendor}' has recurring layout anomalies requiring custom extraction heuristic",
                        frequency=len(ep_ids),
                        confidence=min(0.98, 0.6 + (0.08 * len(ep_ids))),
                        supporting_episode_ids=ep_ids,
                        attributes={"vendor": vendor},
                    )
                )
        return patterns

    def _mine_reflection_corrections(self, episodes: List[EpisodeRecord]) -> List[MinedPattern]:
        """Identifies recurring self-corrections or recovery steps across runs."""
        recovery_actions: Dict[str, List[str]] = defaultdict(list)

        for ep in episodes:
            if ep.outcome == "RECOVERED" and ep.reflection_notes:
                recovery_actions[ep.reflection_notes].append(ep.episode_id)

        patterns = []
        for notes, ep_ids in recovery_actions.items():
            if len(ep_ids) >= self.min_support:
                patterns.append(
                    MinedPattern(
                        pattern_id=f"pat_recovery_{len(patterns)}",
                        pattern_type="FAILURE_CORRELATION",
                        description=f"Recurring recovery trajectory observed: {notes[:80]}",
                        frequency=len(ep_ids),
                        confidence=min(0.95, 0.55 + (0.1 * len(ep_ids))),
                        supporting_episode_ids=ep_ids,
                        attributes={"notes": notes},
                    )
                )
        return patterns
