"""
Structured Output Parser for LLM Semantic Reasoning Engine.
Extracts, sanitizes, repairs, and parses structured JSON/Pydantic models
from raw or malformed LLM responses.
"""

from __future__ import annotations

import json
import logging
import re
from typing import Any, Dict, Type, TypeVar
from pydantic import BaseModel, ValidationError

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)


class StructuredOutputParser:
    """Production-grade parser for extracting structured data from LLM responses."""

    JSON_BLOCK_PATTERN = re.compile(r"```(?:json)?\s*([\s\S]*?)\s*```", re.IGNORECASE)
    RAW_JSON_OBJECT_PATTERN = re.compile(r"(\{[\s\S]*\})", re.MULTILINE)
    RAW_JSON_ARRAY_PATTERN = re.compile(r"(\[[\s\S]*\])", re.MULTILINE)

    @classmethod
    def clean_json_string(cls, raw: str) -> str:
        """Strips markdown fences, comments, and trailing commas from JSON string."""
        text = raw.strip()

        # Check for code blocks
        match = cls.JSON_BLOCK_PATTERN.search(text)
        if match:
            text = match.group(1).strip()
        else:
            # Try to match largest outer JSON object or array
            obj_match = cls.RAW_JSON_OBJECT_PATTERN.search(text)
            arr_match = cls.RAW_JSON_ARRAY_PATTERN.search(text)
            if obj_match and arr_match:
                # Pick whichever starts earlier
                text = obj_match.group(1) if obj_match.start() < arr_match.start() else arr_match.group(1)
            elif obj_match:
                text = obj_match.group(1)
            elif arr_match:
                text = arr_match.group(1)

        # Fix trailing commas before closing braces/brackets
        text = re.sub(r",\s*(\}|\])", r"\1", text)
        return text

    @classmethod
    def parse_dict(cls, raw: str) -> Dict[str, Any]:
        """Parses raw text into a Python dictionary, attempting multiple repair passes."""
        cleaned = cls.clean_json_string(raw)
        try:
            parsed = json.loads(cleaned)
            if isinstance(parsed, dict):
                return parsed
            return {"data": parsed}
        except json.JSONDecodeError as ex:
            logger.debug("Initial JSON parse failed: %s. Attempting repair.", ex)

        # Repair pass 1: Replace unescaped newlines within string literals
        try:
            repaired = re.sub(r'(?<!\\)\n', r'\\n', cleaned)
            parsed = json.loads(repaired)
            if isinstance(parsed, dict):
                return parsed
        except Exception:
            pass

        # Repair pass 2: Single quotes to double quotes
        try:
            repaired = cleaned.replace("'", '"')
            repaired = re.sub(r",\s*(\}|\])", r"\1", repaired)
            parsed = json.loads(repaired)
            if isinstance(parsed, dict):
                return parsed
        except Exception:
            pass

        raise ValueError(f"Failed to parse valid JSON from LLM output: {raw[:200]}...")

    @classmethod
    def parse_model(cls, raw: str, model_cls: Type[T]) -> T:
        """Parses and validates raw text into an instance of a Pydantic model."""
        parsed_dict = cls.parse_dict(raw)
        try:
            return model_cls.model_validate(parsed_dict)
        except ValidationError as vex:
            logger.warning("Pydantic validation error for %s: %s", model_cls.__name__, vex)
            raise
