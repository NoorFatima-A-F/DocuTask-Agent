"""Prompt Metadata Extraction & Inference Engine (Phase 8D).

Analyzes raw prompt template text and automatically infers variables, estimated tokens,
and required capabilities.
"""

from __future__ import annotations

import re
from typing import List
from app.prompts.metadata.schemas import (
    ComprehensivePromptMetadata,
    PromptBusinessMetadata,
    PromptGovernanceMetadata,
    PromptTechnicalMetadata,
)


class PromptMetadataExtractor:
    """Extracts technical and governance properties from prompt template strings."""

    @staticmethod
    def extract_variables(template_text: str) -> List[str]:
        """Find all {{ var_name }} placeholders."""
        found = re.findall(r"\{\{\s*([a-zA-Z0-9_]+)\s*\}\}", template_text)
        return sorted(list(set(found)))

    @staticmethod
    def estimate_token_count(text: str) -> int:
        """Heuristic token estimation (approx 4 chars per token)."""
        if not text:
            return 0
        return max(1, len(text) // 4)

    @classmethod
    def infer_metadata(
        cls,
        prompt_id: str,
        template_text: str,
        owner_email: str = "ai-core@enterprise.com",
    ) -> ComprehensivePromptMetadata:
        """Infer technical and governance metadata for a prompt."""
        token_count = cls.estimate_token_count(template_text)
        requires_json = "json" in template_text.lower() or "schema" in template_text.lower()

        return ComprehensivePromptMetadata(
            prompt_id=prompt_id,
            technical=PromptTechnicalMetadata(
                estimated_tokens=token_count,
                requires_json_mode=requires_json,
            ),
            business=PromptBusinessMetadata(
                business_owner_email=owner_email,
            ),
            governance=PromptGovernanceMetadata(),
        )
