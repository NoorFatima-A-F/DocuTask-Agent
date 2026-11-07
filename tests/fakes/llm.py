"""Scripted LLM provider for tests. Lives in tests/ only; never imported by app/."""

from __future__ import annotations

import json
from collections import deque
from typing import Any

from app.ai.base import LLMProvider, LLMResult


class FakeLLMProvider(LLMProvider):
    """Returns scripted responses (dicts / raw strings) or raises scripted exceptions, in order.

    The last script entry is repeated once the queue is exhausted.
    """

    def __init__(self, *script: dict[str, Any] | str | BaseException, model: str = "fake-model"):
        if not script:
            raise ValueError("FakeLLMProvider needs at least one scripted response")
        self._script: deque[dict[str, Any] | str | BaseException] = deque(script)
        self._model = model
        self.calls: list[dict[str, Any]] = []

    @property
    def provider_name(self) -> str:
        return "fake"

    @property
    def default_model(self) -> str:
        return self._model

    def _next(self) -> dict[str, Any] | str | BaseException:
        return self._script.popleft() if len(self._script) > 1 else self._script[0]

    async def generate_json(
        self, prompt: str, json_schema: dict[str, Any], system_instruction: str = "", model: str = ""
    ) -> LLMResult:
        self.calls.append({"prompt": prompt, "system_instruction": system_instruction, "model": model})
        item = self._next()
        if isinstance(item, BaseException):
            raise item
        if isinstance(item, str):
            raw = item
            data = json.loads(item)
        else:
            raw = json.dumps(item)
            data = item
        return LLMResult(data=data, raw_text=raw, input_tokens=100, output_tokens=50)

    def calculate_cost(self, input_tokens: int, output_tokens: int, model: str = "") -> float | None:
        return None
