"""Prompt Diff Engine (Phase 8D).

Compares prompt versions structurally and semantically, identifying added/removed instructions,
variable additions/removals, constraint adjustments, and output schema differences.
"""

from __future__ import annotations

import difflib
from typing import Any, Dict, List, Set
from pydantic import BaseModel, Field
from app.prompts.registry.models import PromptVersion


class PromptDiffReport(BaseModel):
    """Structured report detailing differences between two prompt versions."""
    base_version_id: str
    target_version_id: str
    text_diff: str
    added_lines: List[str] = Field(default_factory=list)
    removed_lines: List[str] = Field(default_factory=list)
    added_variables: Set[str] = Field(default_factory=set)
    removed_variables: Set[str] = Field(default_factory=set)
    schema_changed: bool = False
    compatibility_changed: bool = False


class PromptDiffEngine:
    """Computes differences across prompt releases."""

    @staticmethod
    def compare_versions(base: PromptVersion, target: PromptVersion) -> PromptDiffReport:
        """Compare base version against target version."""
        base_lines = base.prompt_template.splitlines(keepends=True)
        target_lines = target.prompt_template.splitlines(keepends=True)

        diff = list(difflib.unified_diff(
            base_lines,
            target_lines,
            fromfile=f"version_{base.version_number}",
            tofile=f"version_{target.version_number}",
        ))
        text_diff = "".join(diff)

        added_lines = [
            line[1:].strip()
            for line in diff
            if line.startswith("+") and not line.startswith("+++")
        ]
        removed_lines = [
            line[1:].strip()
            for line in diff
            if line.startswith("-") and not line.startswith("---")
        ]

        base_vars = set(base.variables)
        target_vars = set(target.variables)

        added_vars = target_vars - base_vars
        removed_vars = base_vars - target_vars

        schema_changed = base.expected_output_schema != target.expected_output_schema
        compat_changed = set(base.model_compatibility) != set(target.model_compatibility)

        return PromptDiffReport(
            base_version_id=base.version_id,
            target_version_id=target.version_id,
            text_diff=text_diff,
            added_lines=added_lines,
            removed_lines=removed_lines,
            added_variables=added_vars,
            removed_variables=removed_vars,
            schema_changed=schema_changed,
            compatibility_changed=compat_changed,
        )
