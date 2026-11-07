"""Google Gemini provider (REST ``generateContent``).

Fail-closed: a missing key, any non-200 response, a timeout, or unparseable output raises
a typed :class:`LLMError`. Upstream response bodies and the API key never appear in
exception messages; a truncated body is logged at DEBUG only.
"""

from __future__ import annotations

import json
import re
from typing import Any

import httpx

from app.ai.base import LLMProvider, LLMResult
from app.core.config import settings
from app.core.errors.extraction import ErrorCode, LLMError
from app.core.logging import logger

GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta"
_DEBUG_BODY_LIMIT = 300


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

    PRICING_PER_1K = {
        "gemini-1.5-pro": {"input": 0.00125, "output": 0.005},
        "gemini-1.5-flash": {"input": 0.000075, "output": 0.0003},
    }

    def __init__(
        self,
        api_key: str | None = None,
        default_model_name: str = "gemini-1.5-flash",
        timeout: float = 45.0,
    ):
        self.api_key = api_key if api_key is not None else settings.GEMINI_API_KEY
        self._default_model = default_model_name
        self._timeout = timeout

    @property
    def provider_name(self) -> str:
        return "gemini"

    @property
    def default_model(self) -> str:
        return self._default_model

    def calculate_cost(self, input_tokens: int, output_tokens: int, model: str = "") -> float | None:
        rates = self.PRICING_PER_1K.get(model or self._default_model)
        if rates is None:
            return None
        return round((input_tokens / 1000.0) * rates["input"] + (output_tokens / 1000.0) * rates["output"], 6)

    async def generate_json(
        self, prompt: str, json_schema: dict[str, Any], system_instruction: str = "", model: str = ""
    ) -> LLMResult:
        if not self.api_key:
            raise LLMError(ErrorCode.LLM_NOT_CONFIGURED)

        target_model = model or self._default_model
        instruction = (
            f"{system_instruction}\n\n"
            "Respond ONLY with a JSON object matching this JSON schema:\n"
            f"{json.dumps(json_schema)}"
        )
        payload = {
            "contents": [{"parts": [{"text": f"{instruction}\n\n{prompt}"}]}],
            "generationConfig": {"responseMimeType": "application/json"},
        }
        url = f"{GEMINI_BASE_URL}/models/{target_model}:generateContent"
        # The key goes in a header, never the URL: URLs end up in httpx/proxy access logs.
        headers = {"x-goog-api-key": self.api_key}

        try:
            async with httpx.AsyncClient(timeout=self._timeout) as client:
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
        parts = (candidates[0].get("content") or {}).get("parts") or [] if candidates else []
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
