"""
Abstract LLM Provider Base Class.
Defines common provider contract for Gemini, OpenAI, Claude, Azure, and Local models.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Tuple


class LLMProvider(ABC):
    """Abstract interface for LLM extraction providers."""

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Returns unique identifier name of provider (e.g. 'gemini')."""
        pass

    @property
    @abstractmethod
    def default_model(self) -> str:
        """Returns default model identifier."""
        pass

    @abstractmethod
    async def generate(self, prompt: str, system_instruction: str = "", model: str = "") -> str:
        """
        Generates text completion for prompt.
        
        :param prompt: User prompt
        :param system_instruction: System prompt context
        :param model: Optional model override
        :return: Raw text completion string
        """
        pass

    @abstractmethod
    async def generate_json(
        self,
        prompt: str,
        json_schema: Dict[str, Any],
        system_instruction: str = "",
        model: str = ""
    ) -> Tuple[Dict[str, Any], str, int, int]:
        """
        Generates structured JSON response conforming to schema.
        
        :return: Tuple of (parsed_json_dict, raw_response_string, input_tokens, output_tokens)
        """
        pass

    @abstractmethod
    async def health_check(self) -> bool:
        """Checks provider operational status and API connectivity."""
        pass

    @abstractmethod
    def supports_model(self, model_name: str) -> bool:
        """Checks if specified model is supported by provider."""
        pass

    @abstractmethod
    def supports_streaming(self) -> bool:
        """Checks if provider supports token streaming responses."""
        pass

    @abstractmethod
    def estimate_tokens(self, text: str) -> int:
        """Estimates token count for input text."""
        pass

    @abstractmethod
    def calculate_cost(self, input_tokens: int, output_tokens: int, model: str = "") -> float:
        """Calculates estimated USD cost for token usage."""
        pass
