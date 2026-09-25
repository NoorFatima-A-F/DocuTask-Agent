"""
LLM Provider Registry Module.
Registers and maintains available LLM provider concrete implementations.
"""

from typing import Dict, Type
from app.ai.base import LLMProvider
from app.ai.exceptions import AIProviderException
from app.ai.providers.gemini import GeminiProvider


class LLMRegistry:
    """Registry maintaining available LLM providers."""

    _providers: Dict[str, Type[LLMProvider]] = {
        "gemini": GeminiProvider
    }

    @classmethod
    def register_provider(cls, name: str, provider_class: Type[LLMProvider]) -> None:
        """Registers a new LLMProvider implementation."""
        cls._providers[name.lower().strip()] = provider_class

    @classmethod
    def get_provider_class(cls, name: str) -> Type[LLMProvider]:
        """Retrieves provider class by name."""
        key = name.lower().strip()
        if key not in cls._providers:
            raise AIProviderException(f"Unsupported LLM provider '{name}'. Registered: {list(cls._providers.keys())}")
        return cls._providers[key]

    @classmethod
    def list_providers(cls) -> list[str]:
        """Lists all registered provider names."""
        return list(cls._providers.keys())
