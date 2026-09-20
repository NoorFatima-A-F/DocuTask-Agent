"""
Subsystem Dependency Manager.
Coordinates subsystem registrations, prerequisite validation, topological startup ordering,
and visual graph exports.
"""

from typing import Dict, List, Optional, Set
from app.agents.runtime.dependency_graph import CircularDependencyError, DependencyGraph
from app.agents.runtime.exceptions import ModuleLoadError


class DependencyManager:
    """Manages subsystem dependency registration and computes deterministic startup pipelines."""

    def __init__(self) -> None:
        self._graph = DependencyGraph()
        self._declared_subsystems: Set[str] = set()
        self._dependencies: Dict[str, Set[str]] = {}

    def register_subsystem(self, name: str, depends_on: Optional[List[str]] = None) -> None:
        """Registers a subsystem and its prerequisite dependencies."""
        deps = set(depends_on or [])
        self._declared_subsystems.add(name)
        self._dependencies[name] = deps
        self._graph.add_node(name)
        for dep in deps:
            self._graph.add_dependency(module=name, depends_on=dep)

    def validate_dependencies(self) -> None:
        """Verifies that all referenced dependencies are registered."""
        for module, deps in self._dependencies.items():
            for dep in deps:
                if dep not in self._declared_subsystems:
                    raise ModuleLoadError(
                        f"Subsystem '{module}' declares dependency on unregistered subsystem '{dep}'."
                    )

    def compute_initialization_order(self) -> List[str]:
        """
        Validates missing dependencies and computes topological startup ordering.
        Raises ModuleLoadError on missing dependency and CircularDependencyError on cycle.
        """
        self.validate_dependencies()
        return self._graph.get_resolution_order()

    def get_dependencies_for(self, module: str) -> Set[str]:
        """Returns the set of prerequisites for a given module."""
        return set(self._dependencies.get(module, set()))

    def export_graph_dot(self) -> str:
        """Returns Graphviz DOT representation of dependencies."""
        return self._graph.to_dot()

    def export_graph_ascii(self) -> str:
        """Returns ASCII overview of subsystem dependencies."""
        return self._graph.to_ascii()

    def export_graph_json(self) -> str:
        """Returns JSON schema representation of the dependency DAG."""
        return self._graph.to_json()
