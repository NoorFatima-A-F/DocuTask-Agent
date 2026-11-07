"""LLM provider contract.

Providers either return a real, parsed model response or raise
:class:`app.core.errors.extraction.LLMError`. They never return placeholder data.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class LLMResult:
    """A parsed structured response from an LLM provider."""

    data: dict[str, Any]
    raw_text: str
    input_tokens: int
    output_tokens: int


class LLMProvider(ABC):
    """Abstract interface for structured-extraction LLM providers."""

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Unique provider identifier, e.g. ``gemini``."""

    @property
    @abstractmethod
    def default_model(self) -> str:
        """Model used when the request does not override it."""

    @abstractmethod
    async def generate_json(
        self, prompt: str, json_schema: dict[str, Any], system_instruction: str = "", model: str = ""
    ) -> LLMResult:
        """Return a JSON object produced by the model, or raise ``LLMError``."""

    @abstractmethod
    def calculate_cost(self, input_tokens: int, output_tokens: int, model: str = "") -> float | None:
        """USD cost for the given usage, or ``None`` when pricing for the model is unknown."""
