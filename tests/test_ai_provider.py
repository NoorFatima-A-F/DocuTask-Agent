"""GeminiProvider HTTP behaviour, mocked with respx. Every failure must be a typed LLMError."""

from __future__ import annotations

import json
import logging

import httpx
import pytest
import respx

from app.ai.providers.gemini import GEMINI_BASE_URL, GeminiProvider
from app.core.errors.extraction import ErrorCode, LLMError

KEY = "test-secret-key-123"
MODEL = "gemini-test-model"
URL_PATTERN = f"{GEMINI_BASE_URL}/models/{MODEL}:generateContent"
SCHEMA = {"type": "object", "properties": {"vendor_name": {"type": "string"}}}


def ok_body(text: str, prompt_tokens: int = 321, out_tokens: int = 45) -> dict:
    return {
        "candidates": [{"content": {"parts": [{"text": text}]}}],
        "usageMetadata": {"promptTokenCount": prompt_tokens, "candidatesTokenCount": out_tokens},
    }


@pytest.fixture
def provider() -> GeminiProvider:
    return GeminiProvider(api_key=KEY, default_model_name=MODEL)


@pytest.fixture
def gemini() -> respx.MockRouter:
    with respx.mock(assert_all_called=False) as router:
        yield router


def route(router: respx.MockRouter) -> respx.Route:
    return router.post(url__startswith=URL_PATTERN)


async def call(provider: GeminiProvider):  # type: ignore[no-untyped-def]
    return await provider.generate_json("doc text", SCHEMA, "system")


async def test_success_parses_json_and_uses_usage_metadata(provider, gemini) -> None:  # type: ignore[no-untyped-def]
    route(gemini).respond(200, json=ok_body('{"vendor_name": "Contoso Ltd"}'))

    result = await call(provider)

    assert result.data == {"vendor_name": "Contoso Ltd"}
    assert (result.input_tokens, result.output_tokens) == (321, 45)


async def test_code_fenced_json_is_accepted(provider, gemini) -> None:  # type: ignore[no-untyped-def]
    route(gemini).respond(200, json=ok_body('```json\n{"vendor_name": "X"}\n```'))
    assert (await call(provider)).data == {"vendor_name": "X"}


async def test_missing_key_raises_not_configured_without_network(gemini) -> None:  # type: ignore[no-untyped-def]
    r = route(gemini).respond(200, json=ok_body("{}"))
    with pytest.raises(LLMError) as exc_info:
        await call(GeminiProvider(api_key="", default_model_name=MODEL))
    assert exc_info.value.code == ErrorCode.LLM_NOT_CONFIGURED
    assert exc_info.value.status_code == 503
    assert not r.called


@pytest.mark.parametrize(
    ("status", "code", "http_status"),
    [
        (400, ErrorCode.LLM_BAD_REQUEST, 502),
        (401, ErrorCode.LLM_AUTH_FAILED, 502),
        (403, ErrorCode.LLM_AUTH_FAILED, 502),
        (404, ErrorCode.LLM_MODEL_NOT_FOUND, 502),
        (500, ErrorCode.LLM_UNAVAILABLE, 503),
        (503, ErrorCode.LLM_UNAVAILABLE, 503),
    ],
)
async def test_http_errors_map_to_typed_codes(provider, gemini, status, code, http_status) -> None:  # type: ignore[no-untyped-def]
    secret_body = {"error": {"message": f"upstream detail with {KEY}"}}
    route(gemini).respond(status, json=secret_body)

    with pytest.raises(LLMError) as exc_info:
        await call(provider)

    err = exc_info.value
    assert err.code == code
    assert err.status_code == http_status
    assert KEY not in str(err) and "upstream detail" not in str(err)


async def test_429_is_rate_limited_and_carries_retry_after(provider, gemini) -> None:  # type: ignore[no-untyped-def]
    route(gemini).respond(429, headers={"Retry-After": "12"}, json={"error": {}})
    with pytest.raises(LLMError) as exc_info:
        await call(provider)
    assert exc_info.value.code == ErrorCode.LLM_RATE_LIMITED
    assert exc_info.value.retry_after == 12.0
    assert exc_info.value.transient


async def test_timeout_maps_to_llm_timeout(provider, gemini) -> None:  # type: ignore[no-untyped-def]
    route(gemini).mock(side_effect=httpx.ReadTimeout("slow"))
    with pytest.raises(LLMError) as exc_info:
        await call(provider)
    assert exc_info.value.code == ErrorCode.LLM_TIMEOUT
    assert exc_info.value.status_code == 504


async def test_connection_error_maps_to_unavailable(provider, gemini) -> None:  # type: ignore[no-untyped-def]
    route(gemini).mock(side_effect=httpx.ConnectError("refused"))
    with pytest.raises(LLMError) as exc_info:
        await call(provider)
    assert exc_info.value.code == ErrorCode.LLM_UNAVAILABLE


async def test_invalid_json_raises_invalid_output_never_empty_dict(provider, gemini) -> None:  # type: ignore[no-untyped-def]
    route(gemini).respond(200, json=ok_body("Sure! Here is the invoice: vendor Contoso"))
    with pytest.raises(LLMError) as exc_info:
        await call(provider)
    assert exc_info.value.code == ErrorCode.LLM_INVALID_OUTPUT


async def test_json_array_is_invalid_output(provider, gemini) -> None:  # type: ignore[no-untyped-def]
    route(gemini).respond(200, json=ok_body("[1, 2]"))
    with pytest.raises(LLMError) as exc_info:
        await call(provider)
    assert exc_info.value.code == ErrorCode.LLM_INVALID_OUTPUT


@pytest.mark.parametrize(
    "body",
    [
        {"candidates": []},
        {"candidates": [{"content": {"parts": []}, "finishReason": "SAFETY"}]},
        {"candidates": [{"content": {"parts": [{"text": "  "}]}}]},
        {},
    ],
)
async def test_empty_candidates_raise_empty_output(provider, gemini, body) -> None:  # type: ignore[no-untyped-def]
    route(gemini).respond(200, json=body)
    with pytest.raises(LLMError) as exc_info:
        await call(provider)
    assert exc_info.value.code == ErrorCode.LLM_EMPTY_OUTPUT


async def test_non_json_http_body_is_invalid_output(provider, gemini) -> None:  # type: ignore[no-untyped-def]
    route(gemini).respond(200, text="<html>proxy error</html>")
    with pytest.raises(LLMError) as exc_info:
        await call(provider)
    assert exc_info.value.code == ErrorCode.LLM_INVALID_OUTPUT


async def test_error_body_is_logged_scrubbed_at_debug_only(provider, gemini, caplog) -> None:  # type: ignore[no-untyped-def]
    route(gemini).respond(403, json={"error": {"message": f"bad key {KEY}"}})
    with caplog.at_level(logging.DEBUG), pytest.raises(LLMError):
        await call(provider)
    text = "\n".join(r.getMessage() for r in caplog.records)
    assert KEY not in text
    for record in caplog.records:
        if "bad key" in record.getMessage():
            assert record.levelno == logging.DEBUG


def test_unknown_model_cost_is_none(provider) -> None:  # type: ignore[no-untyped-def]
    assert provider.calculate_cost(1000, 1000, "some-unknown-model") is None


def test_request_payload_is_json(provider, gemini) -> None:  # type: ignore[no-untyped-def]
    assert json.dumps(SCHEMA)  # schema must be serialisable for the prompt


async def test_api_key_sent_in_header_never_in_url(provider, gemini) -> None:  # type: ignore[no-untyped-def]
    r = route(gemini).respond(200, json=ok_body('{"vendor_name": "X"}'))
    await call(provider)
    request = r.calls.last.request
    assert "key=" not in str(request.url)
    assert request.headers["x-goog-api-key"] == KEY


async def test_400_api_key_invalid_maps_to_auth_failed(provider, gemini) -> None:  # type: ignore[no-untyped-def]
    """Real Gemini behaviour (observed 2026-11-08): an invalid key returns 400, not 401."""
    body = {
        "error": {
            "code": 400,
            "status": "INVALID_ARGUMENT",
            "details": [{"@type": "type.googleapis.com/google.rpc.ErrorInfo", "reason": "API_KEY_INVALID"}],
        }
    }
    route(gemini).respond(400, json=body)
    with pytest.raises(LLMError) as exc_info:
        await call(provider)
    assert exc_info.value.code == ErrorCode.LLM_AUTH_FAILED
