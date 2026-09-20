"""
Timeline and Schedule Planner.
"""

from typing import List
from app.agents.planning.tasks import PlanningTask
from app.agents.planning.timelines import EstimatedTimeline


class TimelinePlanner:
    """Computes projected execution timeline and schedule estimates."""

    def plan_timeline(self, tasks: List[PlanningTask]) -> EstimatedTimeline:
        duration = sum(t.estimated_duration_seconds for t in tasks)
        node_timelines = {t.task_id: t.estimated_duration_seconds for t in tasks}
        return EstimatedTimeline(duration_seconds=duration, node_timelines=node_timelines)
