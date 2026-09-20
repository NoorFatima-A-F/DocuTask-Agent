"""
Unit tests for LLM Provider abstraction and GeminiProvider implementation.
"""

import pytest
from app.ai.base import LLMProvider
from app.ai.factory import LLMFactory
from app.ai.providers.gemini import GeminiProvider
from app.ai.registry import LLMRegistry


def test_provider_registration():
    """Verifies LLMRegistry provider registration and retrieval."""
    assert "gemini" in LLMRegistry.list_providers()
    provider_cls = LLMRegistry.get_provider_class("gemini")
    assert provider_cls == GeminiProvider


def test_gemini_provider_methods():
    """Verifies GeminiProvider interface methods and pricing calculations."""
    provider = GeminiProvider(api_key="dev_placeholder_key")

    assert provider.provider_name == "gemini"
    assert provider.default_model == "gemini-1.5-flash"
    assert provider.supports_model("gemini-1.5-pro") is True
    assert provider.supports_model("gpt-4") is False
    assert provider.supports_streaming() is True

    # Token estimation check
    tokens = provider.estimate_tokens("Hello World 1234567890")
    assert tokens > 0

    # Cost calculation check
    cost = provider.calculate_cost(input_tokens=1000, output_tokens=1000, model="gemini-1.5-pro")
    assert cost == 0.00625


@pytest.mark.asyncio
async def test_gemini_dev_mode_generation():
    """Verifies dev mode simulated completions."""
    provider = GeminiProvider(api_key="dev_placeholder_key")

    health = await provider.health_check()
    assert health is True

    text = await provider.generate("Extract data", system_instruction="System prompt")
    assert isinstance(text, str)
    assert len(text) > 0

    schema = {
        "type": "object",
        "properties": {
            "vendor_name": {"type": "string"},
            "total_amount": {"type": "number"}
        }
    }
    parsed, raw, in_tok, out_tok = await provider.generate_json(
        prompt="Document text",
        json_schema=schema,
        system_instruction="System instruction"
    )

    assert isinstance(parsed, dict)
    assert "vendor_name" in parsed
    assert in_tok > 0
    assert out_tok > 0
