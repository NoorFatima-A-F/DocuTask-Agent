"""
Task Dependency Resolver Engine.
Resolves explicit and implicit prerequisites among planned tasks.
"""

from typing import List
from app.agents.planning.dependencies import Dependency, DependencyType
from app.agents.planning.tasks import PlanningTask


class DependencyResolver:
    """Infers and constructs explicit Dependency relationships from tasks."""

    def resolve_dependencies(self, tasks: List[PlanningTask]) -> List[Dependency]:
        dependencies: List[Dependency] = []
        for task in tasks:
            for dep_id in task.dependencies:
                dependencies.append(
                    Dependency(
                        source_id=dep_id,
                        target_id=task.task_id,
                        dependency_type=DependencyType.HARD
                    )
                )
        return dependencies
