"""LLM provider dependency. Tests override ``get_llm_provider`` with a fake."""

from app.ai.base import LLMProvider
from app.ai.providers.gemini import GeminiProvider


def get_llm_provider() -> LLMProvider:
    """The configured production LLM provider (Gemini)."""
    return GeminiProvider()
