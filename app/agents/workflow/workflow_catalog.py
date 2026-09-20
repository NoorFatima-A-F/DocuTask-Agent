"""
Workflow Catalog.
Provides discovery across pre-registered workflow templates and domain pipelines.
"""

from typing import Dict, List, Optional
from app.agents.workflow.workflow_definition import WorkflowDefinition
from app.agents.workflow.workflow_template import WorkflowTemplate


class WorkflowCatalog:
    """Catalog storing well-known enterprise workflow definitions."""

    def __init__(self):
        self._definitions: Dict[str, WorkflowDefinition] = {}
        # Pre-seed standard catalog templates
        doc_template = WorkflowTemplate.create_document_extraction_template()
        appr_template = WorkflowTemplate.create_approval_pipeline_template()
        self._definitions[doc_template.name] = doc_template
        self._definitions[appr_template.name] = appr_template

    def get_template(self, name: str) -> Optional[WorkflowDefinition]:
        return self._definitions.get(name)

    def list_templates(self) -> List[WorkflowDefinition]:
        return list(self._definitions.values())
