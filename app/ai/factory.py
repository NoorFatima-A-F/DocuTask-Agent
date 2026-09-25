"""
LLM Factory Module.
Instantiates requested LLMProvider based on configuration or runtime parameters.
"""

from typing import Optional
from app.ai.base import LLMProvider
from app.ai.registry import LLMRegistry


class LLMFactory:
    """Factory for instantiating LLM providers."""

    @staticmethod
    def get_provider(provider_name: Optional[str] = None) -> LLMProvider:
        """
        Instantiates and returns an LLMProvider instance.
        
        :param provider_name: Target provider name (default: 'gemini')
        :return: LLMProvider concrete instance
        """
        target = provider_name or "gemini"
        provider_cls = LLMRegistry.get_provider_class(target)
        return provider_cls()
