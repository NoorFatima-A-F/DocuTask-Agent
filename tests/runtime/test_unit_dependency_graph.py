"""
Unit Tests for Subsystem Dependency Graph Engine.
Tests Kahn's algorithm, DFS cycle path detection, complex graph resolutions, and DOT/ASCII/JSON exports.
"""

import pytest
from app.agents.runtime.dependency_graph import CircularDependencyError, DependencyGraph
from app.agents.runtime.dependency_manager import DependencyManager
from app.agents.runtime.exceptions import ModuleLoadError


def test_dependency_ordering_linear():
    graph = DependencyGraph()
    graph.add_dependency("B", "A")
    graph.add_dependency("C", "B")
    order = graph.get_resolution_order()
    assert order == ["A", "B", "C"]


def test_dependency_ordering_diamond():
    graph = DependencyGraph()
    graph.add_dependency("B", "A")
    graph.add_dependency("C", "A")
    graph.add_dependency("D", "B")
    graph.add_dependency("D", "C")
    order = graph.get_resolution_order()
    assert order[0] == "A"
    assert order[-1] == "D"
    assert set(order[1:3]) == {"B", "C"}


def test_cycle_detection_simple():
    graph = DependencyGraph()
    graph.add_dependency("A", "B")
    graph.add_dependency("B", "A")
    assert graph.has_cycles()
    cycle = graph.find_cycle()
    assert cycle is not None
    assert set(cycle) == {"A", "B"}
    with pytest.raises(CircularDependencyError) as exc_info:
        graph.get_resolution_order()
    assert len(exc_info.value.cycle_path) > 0


def test_cycle_detection_three_nodes():
    graph = DependencyGraph()
    graph.add_dependency("B", "A")
    graph.add_dependency("C", "B")
    graph.add_dependency("A", "C")
    assert graph.has_cycles()
    with pytest.raises(CircularDependencyError) as exc_info:
        graph.get_resolution_order()
    assert "A" in exc_info.value.cycle_path
    assert "B" in exc_info.value.cycle_path
    assert "C" in exc_info.value.cycle_path


def test_missing_dependency():
    mgr = DependencyManager()
    mgr.register_subsystem("PlanningModule", depends_on=["NonExistentMemory"])
    with pytest.raises(ModuleLoadError, match="unregistered subsystem"):
        mgr.compute_initialization_order()


def test_complex_graph_resolution():
    graph = DependencyGraph()
    # 9 Platform Subsystems
    graph.add_dependency("DecisionModule", "MemoryModule")
    graph.add_dependency("PlanningModule", "MemoryModule")
    graph.add_dependency("PlanningModule", "DecisionModule")
    graph.add_dependency("PlanningModule", "ToolModule")
    graph.add_dependency("ExecutionModule", "ToolModule")
    graph.add_dependency("ExecutionModule", "MemoryModule")
    graph.add_dependency("RecoveryModule", "ExecutionModule")
    graph.add_dependency("ReflectionModule", "ExecutionModule")
    graph.add_dependency("ReflectionModule", "MemoryModule")
    graph.add_dependency("CoordinationModule", "ExecutionModule")
    graph.add_dependency("CoordinationModule", "PlanningModule")
    graph.add_dependency("WorkflowModule", "CoordinationModule")
    graph.add_dependency("WorkflowModule", "PlanningModule")
    graph.add_dependency("WorkflowModule", "ExecutionModule")

    assert not graph.has_cycles()
    order = graph.get_resolution_order()
    assert len(order) == 9
    assert order.index("MemoryModule") < order.index("DecisionModule")
    assert order.index("DecisionModule") < order.index("PlanningModule")
    assert order.index("ExecutionModule") < order.index("RecoveryModule")
    assert order.index("CoordinationModule") < order.index("WorkflowModule")


def test_graph_export_formats():
    graph = DependencyGraph()
    graph.add_dependency("Execution", "Tool")
    dot = graph.to_dot()
    assert "digraph SubsystemDependencies" in dot
    assert '"Tool" -> "Execution";' in dot

    ascii_rep = graph.to_ascii()
    assert "Execution [depends on: Tool]" in ascii_rep

    json_rep = graph.to_json()
    assert '"source": "Tool"' in json_rep
    assert '"target": "Execution"' in json_rep


def test_self_referential_cycle():
    graph = DependencyGraph()
    graph.add_dependency("Loop", "Loop")
    assert graph.has_cycles()
    with pytest.raises(CircularDependencyError):
        graph.get_resolution_order()


def test_disconnected_subgraphs():
    graph = DependencyGraph()
    graph.add_dependency("B1", "A1")
    graph.add_dependency("B2", "A2")
    order = graph.get_resolution_order()
    assert len(order) == 4
    assert order.index("A1") < order.index("B1")
    assert order.index("A2") < order.index("B2")


def test_dependency_manager_export():
    mgr = DependencyManager()
    mgr.register_subsystem("A")
    mgr.register_subsystem("B", ["A"])
    dot = mgr.export_graph_dot()
    assert "digraph" in dot
    ascii_out = mgr.export_graph_ascii()
    assert "B" in ascii_out
    json_out = mgr.export_graph_json()
    assert "nodes" in json_out
