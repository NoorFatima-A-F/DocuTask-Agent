"""
Tests for Workflow Fluent SDK Builder.
"""

import pytest
from app.workflows.sdk.builder import WorkflowBuilder
from app.workflows.domain.models import TaskType
from app.workflows.compiler.compiler import WorkflowCompiler


def test_fluent_sdk_builder_creates_valid_workflow():
    builder = WorkflowBuilder("Invoice Verification Pipeline")
    defn = (
        builder.with_version("2.1.0")
        .with_description("Automated invoice compliance verification")
        .with_organization("org_fintech")
        .with_variable("threshold_amount", 10000)
        .task("ocr_extract", name="OCR Document Extract", task_type=TaskType.SYSTEM)
        .task("compliance_check", name="Compliance Check", task_type=TaskType.VALIDATION, dependencies=["ocr_extract"])
        .condition("check_threshold", "amount > 10000", dependencies=["compliance_check"])
        .approval("executive_signoff", role="cfo", dependencies=["check_threshold"])
        .build()
    )

    assert defn.name == "Invoice Verification Pipeline"
    assert str(defn.version) == "2.1.0"
    assert defn.organization_id == "org_fintech"
    assert len(defn.tasks) == 4

    # Compiles cleanly
    graph = WorkflowCompiler.compile(defn)
    assert len(graph.list_nodes()) == 4
    assert len(graph.list_edges()) == 3
