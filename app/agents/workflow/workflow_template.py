"""
Workflow Templates.
Standardized blueprints for constructing recurring enterprise workflow graphs.
"""

from typing import Dict, List
from uuid import uuid4
from app.agents.workflow.workflow_definition import WorkflowDefinition
from app.agents.workflow.workflow_edge import WorkflowEdge
from app.agents.workflow.workflow_graph import WorkflowGraph
from app.agents.workflow.workflow_node import WorkflowNode, WorkflowNodeType
from app.agents.workflow.workflow_version import WorkflowVersion


class WorkflowTemplate:
    """Pre-configured templates for common document processing and human approval pipelines."""

    @staticmethod
    def create_document_extraction_template(name: str = "DocumentExtractionWorkflow") -> WorkflowDefinition:
        graph = WorkflowGraph()
        n1 = WorkflowNode(node_id="parse", name="Parse Document", handler="parse_pdf")
        n2 = WorkflowNode(node_id="extract", name="Extract Key Data", handler="extract_tables")
        n3 = WorkflowNode(node_id="validate", name="Validate Fields", handler="validate_schema")

        graph.add_node(n1)
        graph.add_node(n2)
        graph.add_node(n3)

        graph.add_edge(WorkflowEdge(edge_id="e1", source_node_id="parse", target_node_id="extract"))
        graph.add_edge(WorkflowEdge(edge_id="e2", source_node_id="extract", target_node_id="validate"))

        return WorkflowDefinition(
            definition_id=uuid4(),
            name=name,
            description="Extracts data from financial PDFs.",
            version=WorkflowVersion(major=1, minor=0, patch=0),
            graph=graph
        )

    @staticmethod
    def create_approval_pipeline_template(name: str = "HumanApprovalWorkflow") -> WorkflowDefinition:
        graph = WorkflowGraph()
        n1 = WorkflowNode(node_id="classify", name="Classify Document", handler="classify_doc")
        n2 = WorkflowNode(
            node_id="approval",
            name="Compliance Review",
            node_type=WorkflowNodeType.HUMAN_APPROVAL,
            handler="request_approval"
        )
        n3 = WorkflowNode(node_id="archive", name="Archive Record", handler="archive_record")

        graph.add_node(n1)
        graph.add_node(n2)
        graph.add_node(n3)

        graph.add_edge(WorkflowEdge(edge_id="e1", source_node_id="classify", target_node_id="approval"))
        graph.add_edge(WorkflowEdge(edge_id="e2", source_node_id="approval", target_node_id="archive"))

        return WorkflowDefinition(
            definition_id=uuid4(),
            name=name,
            description="Workflow gated by human compliance sign-off.",
            version=WorkflowVersion(major=1, minor=0, patch=0),
            graph=graph
        )


DocumentExtractionWorkflowTemplate = WorkflowTemplate
HumanApprovalWorkflowTemplate = WorkflowTemplate


