"""
Test Suite: Critical Path Method (CPM) & Execution DAG Analysis
Validates CPM forward/backward passes, slack calculation, critical path identification, and flamegraph extraction.
"""
import pytest
from app.runtime.dag_visualizer.critical_path_analyzer import CriticalPathAnalyzer
from app.runtime.dag_visualizer.dag_runtime_extractor import DAGRuntimeExtractor
from app.runtime.dag_visualizer.flamegraph_generator import FlameGraphGenerator


def test_critical_path_calculation():
    # Simple diamond DAG: A -> B (50ms) -> D (20ms), A -> C (10ms) -> D (20ms), A duration: 30ms
    nodes = [
        {"id": "A", "label": "Start", "duration_ms": 30.0},
        {"id": "B", "label": "Heavy Task", "duration_ms": 50.0},
        {"id": "C", "label": "Light Task", "duration_ms": 10.0},
        {"id": "D", "label": "End Task", "duration_ms": 20.0},
    ]
    edges = [
        {"source": "A", "target": "B"},
        {"source": "A", "target": "C"},
        {"source": "B", "target": "D"},
        {"source": "C", "target": "D"},
    ]

    analysis = CriticalPathAnalyzer.analyze_dag(nodes, edges)

    assert analysis["total_project_duration_ms"] == 100.0  # 30 + 50 + 20
    assert "A" in analysis["critical_path_node_ids"]
    assert "B" in analysis["critical_path_node_ids"]
    assert "D" in analysis["critical_path_node_ids"]
    assert "C" not in analysis["critical_path_node_ids"]

    # Check slack for C in node_analysis
    c_node = next(n for n in analysis["node_analysis"] if n["node_id"] == "C")
    assert c_node["slack_ms"] == 40.0  # Path B is 50ms, Path C is 10ms -> slack = 40ms
    assert c_node["is_critical"] is False


def test_dag_runtime_extractor_canonical_dag():
    dag = DAGRuntimeExtractor.get_canonical_active_dag("mission_live_001")
    assert dag.mission_id == "mission_live_001"
    assert len(dag.nodes) >= 5
    assert len(dag.edges) >= 4
    assert len(dag.critical_path_node_ids) >= 1
    assert dag.total_estimated_duration_ms > 0.0


def test_flamegraph_generator_mission_tree():
    flamegraph = FlameGraphGenerator.generate_mission_flamegraph("mission_live_001")
    assert flamegraph["total_duration_ms"] > 0.0
    root = flamegraph["root_span"]
    assert root["name"] == "DocuTask End-to-End Pipeline Execution"
    assert len(root["children"]) >= 4
    assert any(s["name"] == "APDLE Planner Multi-Objective Optimization" for s in root["children"])
