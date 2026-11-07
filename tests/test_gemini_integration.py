"""Phase 2: config-driven model, key precedence, structured output schema, pricing, client reuse."""

from __future__ import annotations

import json
from datetime import date
from typing import Any

import httpx
import pytest
import respx

from app.ai.prompt_builder import PromptBuilder
from app.ai.providers.gemini import GEMINI_BASE_URL, GeminiProvider, to_gemini_schema
from app.core.config import Settings, settings

ALL_TYPES = sorted(PromptBuilder.DOCUMENT_MODEL_MAP)
GEMINI_TYPES = {"STRING", "NUMBER", "INTEGER", "BOOLEAN", "ARRAY", "OBJECT"}
ALLOWED_KEYS = {"type", "format", "description", "nullable", "enum", "items", "properties", "required"}


def _walk(node: dict[str, Any]) -> None:
    assert set(node) <= ALLOWED_KEYS, f"unsupported keys: {set(node) - ALLOWED_KEYS}"
    assert node["type"] in GEMINI_TYPES
    if node["type"] == "OBJECT":
        assert node["properties"], "Gemini rejects OBJECT without properties"
        for sub in node["properties"].values():
            _walk(sub)
        assert set(node.get("required", [])) <= set(node["properties"])
    if node["type"] == "ARRAY":
        _walk(node["items"])


def test_fourteen_document_types_registered() -> None:
    assert len(ALL_TYPES) == 14


@pytest.mark.parametrize("doc_type", ALL_TYPES)
def test_schema_converts_for_every_document_type(doc_type: str) -> None:
    converted = to_gemini_schema(PromptBuilder.get_json_schema(doc_type))
    text = json.dumps(converted)
    assert "$ref" not in text and "$defs" not in text and "anyOf" not in text
    _walk(converted)


def test_nullable_and_ref_inlining() -> None:
    inv = to_gemini_schema(PromptBuilder.get_json_schema("invoice"))
    assert inv["properties"]["vendor_name"] == {
        "type": "STRING",
        "description": "Vendor or issuing company name",
        "nullable": True,
    }
    item = inv["properties"]["line_items"]["items"]
    assert item["type"] == "OBJECT" and item["required"] == ["description"]


def test_free_form_map_is_omitted() -> None:
    generic = to_gemini_schema(PromptBuilder.get_json_schema("generic"))
    assert "metadata_fields" not in generic["properties"]
    assert generic["required"] == ["summary"]


def test_unsupported_union_raises() -> None:
    with pytest.raises(ValueError):
        to_gemini_schema({"type": "object", "properties": {"x": {"anyOf": [{"type": "string"}, {"type": "integer"}]}}})


def test_model_comes_from_settings(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(settings, "GEMINI_MODEL", "gemini-configured")
    assert GeminiProvider(api_key="k").default_model == "gemini-configured"


def test_default_model_is_current_ga() -> None:
    assert Settings.model_fields["GEMINI_MODEL"].default == "gemini-3.8-flash"


def test_no_hardcoded_model_ids_in_provider() -> None:
    from pathlib import Path

    src = (Path(__file__).resolve().parent.parent / "app/ai/providers/gemini.py").read_text("utf-8")
    assert "gemini-1." not in src and "gemini-3" not in src


@pytest.mark.parametrize(
    ("gemini", "google", "expected"),
    [("g1", "g2", "g1"), (None, "g2", "g2"), ("", "g2", "g2"), ("  ", None, None), (None, None, None)],
)
def test_key_precedence(gemini: str | None, google: str | None, expected: str | None) -> None:
    s = Settings(GEMINI_API_KEY=gemini, GOOGLE_API_KEY=google, _env_file=None)
    assert s.gemini_api_key == expected


def test_unsupported_provider_keys_removed() -> None:
    assert "ANTHROPIC_API_KEY" not in Settings.model_fields
    assert "OPENAI_API_KEY" not in Settings.model_fields


def test_pricing_table_by_date_and_unknown_model() -> None:
    p = GeminiProvider(api_key="k", default_model_name="gemini-3.8-flash")
    assert p.calculate_cost(1_000_000, 1_000_000, on=date(2026, 11, 8)) == pytest.approx(4.50)
    assert p.calculate_cost(1_000_000, 1_000_000, on=date(2027, 1, 1)) == pytest.approx(9.00)
    assert p.calculate_cost(1000, 1000, model="gemini-unknown") is None


async def test_request_uses_structured_output_and_shared_client() -> None:
    schema = PromptBuilder.get_json_schema("invoice")
    body = {
        "candidates": [{"content": {"parts": [{"text": '{"vendor_name": "Contoso Ltd"}'}]}}],
        "usageMetadata": {"promptTokenCount": 10, "candidatesTokenCount": 5},
    }
    with respx.mock() as router:
        route = router.post(f"{GEMINI_BASE_URL}/models/gemini-x:generateContent").respond(200, json=body)
        async with httpx.AsyncClient() as client:
            provider = GeminiProvider(api_key="k", default_model_name="gemini-x", client=client)
            await provider.generate_json("doc", schema, "sys")
            await provider.generate_json("doc", schema, "sys")
        sent = json.loads(route.calls.last.request.content)

    assert route.call_count == 2
    assert sent["generationConfig"]["responseMimeType"] == "application/json"
    assert sent["generationConfig"]["responseSchema"] == to_gemini_schema(schema)
    assert sent["systemInstruction"] == {"parts": [{"text": "sys"}]}
    assert "key=" not in str(route.calls.last.request.url)
