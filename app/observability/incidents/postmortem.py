"""Blameless Postmortem Generation and Preventative Action Tracking."""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import List

from .manager import IncidentRecord


@dataclass
class PreventativeAction:
    action_id: str
    description: str
    owner: str
    priority: str = "P1"
    status: str = "OPEN"  # OPEN, IN_PROGRESS, COMPLETED


@dataclass
class PostmortemReport:
    postmortem_id: str
    incident_id: str
    title: str
    summary: str
    impact: str
    five_whys: List[str] = field(default_factory=list)
    lessons_learned: List[str] = field(default_factory=list)
    action_items: List[PreventativeAction] = field(default_factory=list)
    timeline_markdown: str = ""
    author: str = "SRE Lead"
    created_at: float = field(default_factory=time.time)


class PostmortemGenerator:
    """Generates comprehensive blameless postmortem documents from incident records."""

    @staticmethod
    def generate(
        incident: IncidentRecord,
        summary: str,
        impact: str,
        five_whys: List[str],
        lessons_learned: List[str],
        action_items: List[PreventativeAction],
        author: str = "SRE Lead",
    ) -> PostmortemReport:
        report_id = f"pm-{incident.incident_id}"
        timeline_md = incident.timeline.to_markdown()

        return PostmortemReport(
            postmortem_id=report_id,
            incident_id=incident.incident_id,
            title=f"Postmortem: {incident.title}",
            summary=summary,
            impact=impact,
            five_whys=five_whys,
            lessons_learned=lessons_learned,
            action_items=action_items,
            timeline_markdown=timeline_md,
            author=author,
        )
