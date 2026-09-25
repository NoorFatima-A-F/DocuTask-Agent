"""
Confidence Versioning Registry for Phase 13.3 (ASCE-CGP).
Maintains version snapshots of calculated confidence reports.
"""

from typing import Dict, List, Optional
from app.runtime.confidence.models.confidence_models import MissionConfidenceReport


class ConfidenceVersioningRegistry:
    """
    Stores versioned mission confidence reports for auditability and replay.
    """

    _reports: Dict[str, List[MissionConfidenceReport]] = {}

    @classmethod
    def save_report(cls, report: MissionConfidenceReport):
        if report.mission_id not in cls._reports:
            cls._reports[report.mission_id] = []
        cls._reports[report.mission_id].append(report)

    @classmethod
    def get_latest(cls, mission_id: str) -> Optional[MissionConfidenceReport]:
        reports = cls._reports.get(mission_id, [])
        return reports[-1] if reports else None

    @classmethod
    def get_all(cls, mission_id: str) -> List[MissionConfidenceReport]:
        return cls._reports.get(mission_id, [])
