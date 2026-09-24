"""Tests for Workflow Composer, DSL Parser, and Compiler."""

from app.platform.capability.capability_registry import CapabilityRegistry
from app.platform.dsl.dsl_parser import DSLCompiler, DSLParser
from app.platform.workflow.workflow_engine import (
    WorkflowDefinition,
    WorkflowEdge,
    WorkflowEngine,
    WorkflowNode,
)


def test_workflow_dsl_parsing_and_compilation():
    dsl_data = {
        "mission_id": "wf-invoice-audit",
        "title": "Automated Invoice Audit",
        "steps": ["perception.ocr", "extraction.invoice", "validation.reconciliation"],
    }
    spec = DSLParser.parse_dict(dsl_data)
    assert spec.mission_id == "wf-invoice-audit"
    assert len(spec.steps) == 3

    wf = DSLCompiler.compile_to_workflow_definition(spec)
    assert len(wf.nodes) == 3
    assert len(wf.edges) == 2


def test_workflow_engine_execution():
    reg = CapabilityRegistry()
    reg.register_capability("step1", "general", "Step 1")
    reg.register_capability("step2", "general", "Step 2")

    wf = WorkflowDefinition(
        workflow_id="test-wf",
        name="Test Workflow",
        description="Test description",
        nodes={
            "n1": WorkflowNode("n1", "step1", "Node 1"),
            "n2": WorkflowNode("n2", "step2", "Node 2"),
        },
        edges=[WorkflowEdge("e1", "n1", "n2")],
    )

    engine = WorkflowEngine(registry=reg)
    res = engine.execute_workflow(wf, {"input": "data"})
    assert res["status"] == "COMPLETED"
    assert res["total_steps"] == 2
