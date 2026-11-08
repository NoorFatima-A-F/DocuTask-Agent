"""Google Gemini provider (REST ``generateContent`` with structured JSON output).

Fail-closed: a missing key, any non-200 response, a timeout, or unparseable output raises
a typed :class:`LLMError`. Upstream response bodies and the API key never appear in
exception messages; a truncated, scrubbed body is logged at DEBUG only. The key is sent
in the ``x-goog-api-key`` header, never in the URL.
"""

from __future__ import annotations

import json
import re
from datetime import UTC, date, datetime
from typing import Any

import httpx

from app.ai.base import LLMProvider, LLMResult
from app.core.config import GEMINI_PRICING_USD_PER_1M, settings
from app.core.errors.extraction import ErrorCode, LLMError
from app.core.logging import logger

GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta"
_DEBUG_BODY_LIMIT = 300


def default_timeout() -> httpx.Timeout:
    """Explicit connect/read timeouts for Gemini calls."""
    return httpx.Timeout(
        connect=settings.GEMINI_CONNECT_TIMEOUT_SECONDS,
        read=settings.GEMINI_READ_TIMEOUT_SECONDS,
        write=10.0,
        pool=5.0,
    )


def _parse_retry_after(value: str | None) -> float | None:
    if not value:
        return None
    try:
        return max(0.0, float(value))
    except ValueError:
        return None


def _scrub(text: str, secret: str | None) -> str:
    text = text[:_DEBUG_BODY_LIMIT]
    if secret:
        text = text.replace(secret, "***")
    return re.sub(r"key=[^&\s\"']+", "key=***", text)


class GeminiProvider(LLMProvider):
    """Concrete LLMProvider for Google Gemini models."""

    def __init__(
        self,
        api_key: str | None = None,
        default_model_name: str | None = None,
        client: httpx.AsyncClient | None = None,
        pricing: dict[str, list[tuple[date, float, float]]] | None = None,
    ):
        self.api_key = api_key if api_key is not None else settings.gemini_api_key
        self._default_model = default_model_name or settings.GEMINI_MODEL
        self._client = client
        self._pricing = GEMINI_PRICING_USD_PER_1M if pricing is None else pricing

    @property
    def provider_name(self) -> str:
        return "gemini"

    @property
    def default_model(self) -> str:
        return self._default_model

    def calculate_cost(
        self, input_tokens: int, output_tokens: int, model: str = "", on: date | None = None
    ) -> float | None:
        """USD cost from the pricing table; ``None`` for models without a listed price."""
        periods = self._pricing.get(model or self._default_model)
        if not periods:
            return None
        day = on or datetime.now(UTC).date()
        applicable = [p for p in periods if p[0] <= day]
        if not applicable:
            return None
        _, in_rate, out_rate = applicable[-1]
        return round(input_tokens / 1e6 * in_rate + output_tokens / 1e6 * out_rate, 6)

    async def generate_json(
        self, prompt: str, json_schema: dict[str, Any], system_instruction: str = "", model: str = ""
    ) -> LLMResult:
        if not self.api_key:
            raise LLMError(ErrorCode.LLM_NOT_CONFIGURED)

        target_model = model or self._default_model
        payload: dict[str, Any] = {
            "contents": [{"role": "user", "parts": [{"text": prompt}]}],
            "generationConfig": {
                "responseMimeType": "application/json",
                "responseSchema": to_gemini_schema(json_schema),
            },
        }
        if system_instruction:
            payload["systemInstruction"] = {"parts": [{"text": system_instruction}]}
        url = f"{GEMINI_BASE_URL}/models/{target_model}:generateContent"
        headers = {"x-goog-api-key": self.api_key}

        try:
            if self._client is not None:
                response = await self._client.post(url, json=payload, headers=headers)
            else:
                async with httpx.AsyncClient(timeout=default_timeout()) as client:
                    response = await client.post(url, json=payload, headers=headers)
        except httpx.TimeoutException as exc:
            raise LLMError(ErrorCode.LLM_TIMEOUT) from exc
        except httpx.HTTPError as exc:
            logger.warning("Gemini transport error: %s", type(exc).__name__)
            raise LLMError(ErrorCode.LLM_UNAVAILABLE) from exc

        if response.status_code != 200:
            raise self._error_for_status(response)

        return self._parse_success(response)

    def _error_for_status(self, response: httpx.Response) -> LLMError:
        status = response.status_code
        logger.debug("Gemini HTTP %s body: %s", status, _scrub(response.text, self.api_key))
        if status in (401, 403) or (status == 400 and _is_invalid_key_error(response)):
            # Gemini reports an invalid API key as HTTP 400 with reason API_KEY_INVALID.
            code = ErrorCode.LLM_AUTH_FAILED
        elif status == 404:
            code = ErrorCode.LLM_MODEL_NOT_FOUND
        elif status == 429:
            return LLMError(
                ErrorCode.LLM_RATE_LIMITED, retry_after=_parse_retry_after(response.headers.get("retry-after"))
            )
        elif status >= 500:
            code = ErrorCode.LLM_UNAVAILABLE
        else:
            code = ErrorCode.LLM_BAD_REQUEST
        logger.warning("Gemini request failed: HTTP %s -> %s", status, code.value)
        return LLMError(code)

    def _parse_success(self, response: httpx.Response) -> LLMResult:
        try:
            data = response.json()
        except ValueError as exc:
            raise LLMError(ErrorCode.LLM_INVALID_OUTPUT) from exc

        candidates = data.get("candidates") or []
        parts = ((candidates[0].get("content") or {}).get("parts") or []) if candidates else []
        raw_text = "".join(p.get("text", "") for p in parts if isinstance(p, dict)).strip()
        if not raw_text:
            raise LLMError(ErrorCode.LLM_EMPTY_OUTPUT)

        try:
            parsed = json.loads(_strip_code_fence(raw_text))
        except json.JSONDecodeError as exc:
            logger.debug("Gemini returned non-JSON text: %s", _scrub(raw_text, self.api_key))
            raise LLMError(ErrorCode.LLM_INVALID_OUTPUT) from exc
        if not isinstance(parsed, dict):
            raise LLMError(ErrorCode.LLM_INVALID_OUTPUT, "The LLM returned JSON that is not an object.")

        usage = data.get("usageMetadata") or {}
        return LLMResult(
            data=parsed,
            raw_text=raw_text,
            input_tokens=int(usage.get("promptTokenCount") or 0),
            output_tokens=int(usage.get("candidatesTokenCount") or 0),
        )


def _is_invalid_key_error(response: httpx.Response) -> bool:
    try:
        details = (response.json().get("error") or {}).get("details") or []
    except (ValueError, AttributeError):
        return False
    return any(isinstance(d, dict) and d.get("reason") == "API_KEY_INVALID" for d in details)


def _strip_code_fence(text: str) -> str:
    match = re.fullmatch(r"```(?:json)?\s*(.*?)\s*```", text, re.DOTALL)
    return match.group(1) if match else text


# --------------------------------------------------------------------------- responseSchema

#: Keywords of the OpenAPI-subset ``Schema`` object accepted by Gemini's ``responseSchema``.
_GEMINI_SCHEMA_KEYS = frozenset(
    {"type", "format", "description", "nullable", "enum", "items", "properties", "required", "minItems", "maxItems"}
)
#: JSON Schema keywords with no meaning for Gemini; dropped.
_IGNORED_KEYS = frozenset({"title", "default", "examples", "additionalProperties", "$defs"})


def to_gemini_schema(schema: dict[str, Any]) -> dict[str, Any]:
    """Convert a Pydantic JSON Schema into Gemini's ``responseSchema`` dialect.

    * ``$ref`` -> inlined from ``$defs``
    * ``anyOf: [X, {type: null}]`` -> ``X`` with ``nullable: true``
    * types upper-cased (``STRING``, ``OBJECT``, ...)
    * free-form objects (no ``properties``) cannot be expressed; such a property is omitted
      from its parent and Pydantic applies the field default.

    Raises ``ValueError`` for constructs Gemini cannot express (non-nullable unions, unknown
    keywords, arrays of free-form objects), so schema changes fail in unit tests, not at runtime.
    """
    defs: dict[str, Any] = schema.get("$defs", {})

    def resolve(node: dict[str, Any]) -> dict[str, Any]:
        while "$ref" in node:
            name = node["$ref"].rsplit("/", 1)[-1]
            node = {**defs[name], **{k: v for k, v in node.items() if k != "$ref"}}
        return node

    def convert(node: dict[str, Any]) -> dict[str, Any] | None:
        node = resolve(node)
        nullable = False
        if "anyOf" in node:
            variants = [resolve(v) for v in node["anyOf"]]
            non_null = [v for v in variants if v.get("type") != "null"]
            if len(non_null) != 1:
                raise ValueError(f"Unsupported union for Gemini responseSchema: {node['anyOf']}")
            nullable = len(non_null) < len(variants)
            node = {**non_null[0], **{k: v for k, v in node.items() if k != "anyOf"}}

        if node.get("type") == "object" and not node.get("properties"):
            return None

        out: dict[str, Any] = {}
        for key, value in node.items():
            if key in _IGNORED_KEYS:
                continue
            if key not in _GEMINI_SCHEMA_KEYS:
                raise ValueError(f"Unsupported JSON Schema keyword for Gemini: {key}")
            if key == "type":
                out["type"] = str(value).upper()
            elif key == "properties":
                props = {name: convert(sub) for name, sub in value.items()}
                out["properties"] = {name: sub for name, sub in props.items() if sub is not None}
            elif key == "items":
                items = convert(value)
                if items is None:
                    raise ValueError("Arrays of free-form objects are not supported by Gemini responseSchema")
                out["items"] = items
            else:
                out[key] = value
        if "required" in out and "properties" in out:
            out["required"] = [r for r in out["required"] if r in out["properties"]]
        if nullable:
            out["nullable"] = True
        return out

    converted = convert(schema)
    if converted is None:
        raise ValueError("Top-level schema must be an object with properties")
    return converted
