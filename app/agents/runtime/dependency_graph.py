"""
Subsystem Dependency Graph Engine.
Implements dual-algorithm topological resolution (Kahn's algorithm and DFS cycle path tracing)
with DAG validation, missing dependency detection, and graph visualization export (DOT, ASCII, JSON).
"""

from collections import defaultdict, deque
import json
from typing import Any, Dict, List, Optional, Set, Tuple
from app.agents.runtime.exceptions import CyclicDependencyError


class CircularDependencyError(CyclicDependencyError):
    """Raised when a directed dependency cycle is detected, detailing the cycle chain."""

    def __init__(self, message: str, cycle_path: Optional[List[str]] = None):
        super().__init__(message)
        self.cycle_path = cycle_path or []


class DependencyGraph:
    """Production-grade DAG dependency engine with DFS cycle tracing and graph visualization."""

    def __init__(self) -> None:
        # _adj: u -> set of v where u is a prerequisite of v (u must run before v)
        self._adj: Dict[str, Set[str]] = defaultdict(set)
        # _rev: v -> set of u where v depends on u
        self._rev: Dict[str, Set[str]] = defaultdict(set)
        self._nodes: Set[str] = set()

    def add_node(self, name: str) -> None:
        """Enrolls a subsystem node into the graph."""
        self._nodes.add(name)

    def add_dependency(self, module: str, depends_on: str) -> None:
        """Declares that 'module' requires 'depends_on' prior to initialization."""
        self._nodes.add(module)
        self._nodes.add(depends_on)
        self._adj[depends_on].add(module)
        self._rev[module].add(depends_on)

    def find_cycle(self) -> Optional[List[str]]:
        """
        Executes Depth-First Search (DFS) with 3-color vertex tracking (white, gray, black)
        to identify and return the exact circular dependency cycle path.
        Returns None if acyclic.
        """
        WHITE, GRAY, BLACK = 0, 1, 2
        color = {node: WHITE for node in self._nodes}
        parent: Dict[str, Optional[str]] = {node: None for node in self._nodes}

        for start_node in sorted(self._nodes):
            if color[start_node] == WHITE:
                stack = [(start_node, iter(sorted(self._adj[start_node])))]
                color[start_node] = GRAY

                while stack:
                    curr, neighbors = stack[-1]
                    try:
                        nxt = next(neighbors)
                        if color[nxt] == GRAY:
                            # Cycle detected: backtrack from curr to nxt
                            cycle = [nxt]
                            p = curr
                            while p != nxt and p is not None:
                                cycle.append(p)
                                p = parent[p]
                            cycle.append(nxt)
                            cycle.reverse()
                            return cycle
                        elif color[nxt] == WHITE:
                            color[nxt] = GRAY
                            parent[nxt] = curr
                            stack.append((nxt, iter(sorted(self._adj[nxt]))))
                    except StopIteration:
                        color[curr] = BLACK
                        stack.pop()

        return None

    def has_cycles(self) -> bool:
        """Returns True if any cyclic loop exists in the graph."""
        return self.find_cycle() is not None

    def get_resolution_order(self) -> List[str]:
        """
        Computes deterministic topological ordering of subsystem initialization using Kahn's algorithm.
        Raises CircularDependencyError with exact cycle path if cyclic.
        """
        cycle = self.find_cycle()
        if cycle:
            cycle_str = " -> ".join(cycle)
            raise CircularDependencyError(
                f"Circular dependency detected in platform subsystems: {cycle_str}",
                cycle_path=cycle,
            )

        in_degree: Dict[str, int] = {node: len(self._rev[node]) for node in self._nodes}
        queue = deque(sorted([node for node, deg in in_degree.items() if deg == 0]))
        order: List[str] = []

        while queue:
            node = queue.popleft()
            order.append(node)
            for neighbor in sorted(self._adj[node]):
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        if len(order) != len(self._nodes):
            cycle = self.find_cycle() or ["unknown_cycle"]
            raise CircularDependencyError(
                f"Unresolved circular dependency detected: {' -> '.join(cycle)}",
                cycle_path=cycle,
            )

        return order

    def to_dot(self) -> str:
        """Exports graph in Graphviz DOT format."""
        lines = ["digraph SubsystemDependencies {", '  rankdir="LR";', '  node [shape="box", fontname="Helvetica"];']
        for u in sorted(self._nodes):
            lines.append(f'  "{u}";')
        for u in sorted(self._adj):
            for v in sorted(self._adj[u]):
                lines.append(f'  "{u}" -> "{v}";')
        lines.append("}")
        return "\n".join(lines)

    def to_ascii(self) -> str:
        """Exports textual ASCII representation of dependency relationships."""
        lines = ["Subsystem Dependency Graph:"]
        for node in sorted(self._nodes):
            deps = sorted(self._rev.get(node, set()))
            dep_str = ", ".join(deps) if deps else "None (Root)"
            lines.append(f"  * {node} [depends on: {dep_str}]")
        return "\n".join(lines)

    def to_json(self) -> str:
        """Exports JSON representation of nodes and directed edges."""
        edges = []
        for u, neighbors in self._adj.items():
            for v in neighbors:
                edges.append({"source": u, "target": v})
        data = {
            "nodes": sorted(list(self._nodes)),
            "edges": edges,
        }
        return json.dumps(data, indent=2)
