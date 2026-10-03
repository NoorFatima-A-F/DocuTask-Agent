"""
Living Leaderboard Tracker (Phase 90C)
=====================================
Maintains historical and competitive leaderboard positioning for scientific papers.
"""

from __future__ import annotations
from typing import Dict, List, Optional

from research_validation.observatory.observatory_models import LeaderboardEntry


class LivingLeaderboardTracker:
    """
    Ranks evaluated models against external baselines and records progression.
    """

    def __init__(self):
        self.leaderboards: Dict[str, List[LeaderboardEntry]] = {}

    def record_standing(
        self,
        benchmark_id: str,
        model_name: str,
        model_version: str,
        score: float,
        is_measured_locally: bool = True,
        submission_date_utc: str = "",
    ) -> List[LeaderboardEntry]:
        entries = self.leaderboards.setdefault(benchmark_id, [])
        new_entry = LeaderboardEntry(
            rank=0,
            model_name=model_name,
            model_version=model_version,
            score=score,
            is_measured_locally=is_measured_locally,
            status_label="VERIFIED_LOCAL" if is_measured_locally else "REPORTED_LITERATURE",
            submission_date_utc=submission_date_utc,
        )
        entries.append(new_entry)
        
        # Sort descending by score and update ranks
        entries.sort(key=lambda e: e.score, reverse=True)
        ranked = [
            LeaderboardEntry(
                rank=idx + 1,
                model_name=e.model_name,
                model_version=e.model_version,
                score=e.score,
                is_measured_locally=e.is_measured_locally,
                status_label=e.status_label,
                submission_date_utc=e.submission_date_utc,
            )
            for idx, e in enumerate(entries)
        ]
        self.leaderboards[benchmark_id] = ranked
        return ranked

    def get_rank(self, benchmark_id: str, model_name: str) -> Optional[int]:
        for e in self.leaderboards.get(benchmark_id, []):
            if e.model_name == model_name:
                return e.rank
        return None
