"""
Task Complexity and Capability Requirement Analyzer.
"""

from typing import List
from pydantic import BaseModel, Field
from app.agents.planning.tasks import PlanningTask


class TaskAnalysisResult(BaseModel):
    """Analysis result of an individual planning task."""
    task_id: str
    required_capabilities: List[str] = Field(default_factory=list)
    estimated_complexity: float = Field(default=0.5, ge=0.0, le=1.0)
    is_parallelizable: bool = Field(default=True)
    model_config = {"frozen": True}


class TaskAnalyzer:
    """Analyzes planning tasks to infer capability requirements and execution parameters."""

    def analyze_task(self, task: PlanningTask) -> TaskAnalysisResult:
        caps = [task.capability_requirement] if task.capability_requirement else ["DEFAULT"]
        return TaskAnalysisResult(
            task_id=task.task_id,
            required_capabilities=caps,
            estimated_complexity=0.3 if task.estimated_duration_seconds < 10 else 0.8,
            is_parallelizable=len(task.dependencies) == 0
        )
