"""Readiness reflects whether the extraction path can actually run; liveness stays 200."""

from __future__ import annotations

import pytest
from httpx import AsyncClient

from app.ai.providers.gemini import GeminiProvider
from app.core.config import settings
from app.dependencies.llm import get_llm_provider
from app.dependencies.ocr import get_ocr_provider
from app.main import app
from tests.fakes.ocr import FakeOCRProvider


class MissingOCR(FakeOCRProvider):
    def is_available(self) -> bool:
        return False


async def test_liveness_always_ok(client: AsyncClient) -> None:
    app.dependency_overrides[get_ocr_provider] = lambda: MissingOCR()
    assert (await client.get("/healthz")).status_code == 200


async def test_ready_when_ocr_present_in_dev(client: AsyncClient) -> None:
    app.dependency_overrides[get_ocr_provider] = lambda: FakeOCRProvider()
    app.dependency_overrides[get_llm_provider] = lambda: GeminiProvider(api_key="")
    res = await client.get("/readyz")
    assert res.status_code == 200 and res.json()["status"] == "ready"


async def test_not_ready_without_tesseract(client: AsyncClient) -> None:
    app.dependency_overrides[get_ocr_provider] = lambda: MissingOCR()
    res = await client.get("/readyz")
    assert res.status_code == 503
    assert any(r.startswith("OCR_ENGINE_UNAVAILABLE") for r in res.json()["reasons"])


async def test_not_ready_without_llm_key_in_production(client: AsyncClient, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(settings, "ENVIRONMENT", "production")
    app.dependency_overrides[get_ocr_provider] = lambda: FakeOCRProvider()
    app.dependency_overrides[get_llm_provider] = lambda: GeminiProvider(api_key="")
    res = await client.get("/readyz")
    assert res.status_code == 503
    assert any(r.startswith("LLM_NOT_CONFIGURED") for r in res.json()["reasons"])
