"""LLM provider dependency. Tests override ``get_llm_provider`` with a fake."""

from fastapi import Request

from app.ai.base import LLMProvider
from app.ai.providers.gemini import GeminiProvider


def get_llm_provider(request: Request) -> LLMProvider:
    """The configured Gemini provider, reusing the app-lifespan HTTP client when present."""
    return GeminiProvider(client=getattr(request.app.state, "http_client", None))
