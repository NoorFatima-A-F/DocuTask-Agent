"""Prompt Template Rendering Engine (Phase 8D).

Supports variable interpolation, defaults, conditionals, component composition, and template inheritance.
"""

from __future__ import annotations

import json
import re
from typing import Any, Dict, List, Optional
from app.prompts.templates.variables import PromptVariableDefinition


class PromptTemplateRenderer:
    """Renders parametric prompt templates with dynamic variables, conditionals, and components."""

    @staticmethod
    def render(
        template: str,
        variables: Optional[Dict[str, Any]] = None,
        definitions: Optional[List[PromptVariableDefinition]] = None,
        partials: Optional[Dict[str, str]] = None,
    ) -> str:
        """Render prompt template text with provided variable inputs and partials."""
        vars_dict = dict(variables or {})
        partials_dict = partials or {}

        # 1. Apply variable definitions validation and defaults
        if definitions:
            for defn in definitions:
                val = vars_dict.get(defn.name)
                vars_dict[defn.name] = defn.validate_value(val)

        result = template

        # 2. Render partial includes: {{> partial_name }}
        def include_partial(match: re.Match) -> str:
            partial_name = match.group(1).strip()
            return partials_dict.get(partial_name, f"<!-- missing partial: {partial_name} -->")

        result = re.sub(r"\{\{>\s*([a-zA-Z0-9_\-\.]+)\s*\}\}", include_partial, result)

        # 3. Render conditionals: {% if var %}...{% endif %} or {{#if var}}...{{/if}}
        # Syntax A: {% if var %}...{% endif %}
        def process_conditional_jinja(match: re.Match) -> str:
            var_name = match.group(1).strip()
            content = match.group(2)
            val = vars_dict.get(var_name)
            if val and (not isinstance(val, (list, dict, str)) or len(val) > 0) and val is not False:
                return content
            return ""

        result = re.sub(
            r"\{%\s*if\s+([a-zA-Z0-9_]+)\s*%\}(.*?)\{%\s*endif\s*%\}",
            process_conditional_jinja,
            result,
            flags=re.DOTALL,
        )

        # Syntax B: {{#if var}}...{{/if}}
        def process_conditional_mustache(match: re.Match) -> str:
            var_name = match.group(1).strip()
            content = match.group(2)
            val = vars_dict.get(var_name)
            if val and (not isinstance(val, (list, dict, str)) or len(val) > 0) and val is not False:
                return content
            return ""

        result = re.sub(
            r"\{\{#if\s+([a-zA-Z0-9_]+)\s*\}\}(.*?)\{\{/if\}\}",
            process_conditional_mustache,
            result,
            flags=re.DOTALL,
        )

        # 4. Substitute standard variables: {{ var_name }}
        def substitute_var(match: re.Match) -> str:
            var_name = match.group(1).strip()
            if var_name in vars_dict:
                val = vars_dict[var_name]
                if isinstance(val, (dict, list)):
                    return json.dumps(val, indent=2)
                return str(val)
            return match.group(0)  # Leave untouched if not supplied

        result = re.sub(r"\{\{\s*([a-zA-Z0-9_]+)\s*\}\}", substitute_var, result)

        return result
