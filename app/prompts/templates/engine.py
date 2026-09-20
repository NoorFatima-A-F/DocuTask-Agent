"""Prompt Template Engine (Phase 8D).

Composes modular prompt templates, handles inheritance, and coordinates rendering pipelines.
"""

from __future__ import annotations

import re
from typing import Any, Dict, List, Optional
from app.prompts.templates.renderer import PromptTemplateRenderer
from app.prompts.templates.variables import PromptVariableDefinition


class PromptTemplateEngine:
    """Enterprise template composition and rendering engine."""

    def __init__(self):
        self._partials: Dict[str, str] = {}

    def register_partial(self, name: str, template_content: str) -> None:
        """Register a reusable partial snippet (e.g. standard output format guidelines)."""
        self._partials[name] = template_content

    def extract_variables(self, template: str) -> List[str]:
        """Extract all unique {{ variable }} placeholders from a template string."""
        matches = re.findall(r"\{\{\s*([a-zA-Z0-9_]+)\s*\}\}", template)
        return sorted(list(set(matches)))

    def compose_templates(
        self,
        base_template: str,
        department_rules: Optional[str] = None,
        task_instructions: Optional[str] = None,
    ) -> str:
        """Compose hierarchical prompt from persona base, domain rules, and task instructions."""
        parts = [base_template.strip()]
        if department_rules:
            parts.append("\n--- Department Guidelines ---\n" + department_rules.strip())
        if task_instructions:
            parts.append("\n--- Task Instructions ---\n" + task_instructions.strip())
        return "\n\n".join(parts)

    def render(
        self,
        template: str,
        variables: Optional[Dict[str, Any]] = None,
        definitions: Optional[List[PromptVariableDefinition]] = None,
        additional_partials: Optional[Dict[str, str]] = None,
    ) -> str:
        """Render composed template with dynamic context."""
        all_partials = dict(self._partials)
        if additional_partials:
            all_partials.update(additional_partials)

        return PromptTemplateRenderer.render(
            template=template,
            variables=variables,
            definitions=definitions,
            partials=all_partials,
        )
