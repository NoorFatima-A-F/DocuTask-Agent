"""Liveness and readiness probes.

* ``/healthz`` (liveness) is always 200 while the process serves requests.
* ``/readyz`` (readiness) is 503 with reasons when the extraction path cannot work:
  the tesseract binary is missing, or no LLM API key is configured outside
  development/test.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.ai.base import LLMProvider
from app.core.config import settings
from app.dependencies.llm import get_llm_provider
from app.dependencies.ocr import get_ocr_provider
from app.ocr.base import OCRProvider

router = APIRouter(tags=["Health"])

DEV_ENVIRONMENTS = {"development", "dev", "local", "test", "testing"}


class HealthResponse(BaseModel):
    status: str
    version: str = settings.APP_VERSION


class ReadinessResponse(HealthResponse):
    reasons: list[str] = []


@router.get("/healthz", response_model=HealthResponse)
def liveness_probe() -> HealthResponse:
    """Liveness: the process is up."""
    return HealthResponse(status="alive")


@router.get("/readyz", response_model=ReadinessResponse, responses={503: {"model": ReadinessResponse}})
def readiness_probe(
    ocr: OCRProvider = Depends(get_ocr_provider),
    llm: LLMProvider = Depends(get_llm_provider),
) -> JSONResponse:
    """Readiness: OCR engine present and (outside dev/test) an LLM key configured."""
    reasons: list[str] = []
    if not ocr.is_available():
        reasons.append("OCR_ENGINE_UNAVAILABLE: tesseract binary not found")
    if settings.ENVIRONMENT.lower() not in DEV_ENVIRONMENTS and not getattr(llm, "api_key", None):
        reasons.append("LLM_NOT_CONFIGURED: no Gemini API key set")
    body = ReadinessResponse(status="not_ready" if reasons else "ready", reasons=reasons)
    return JSONResponse(status_code=503 if reasons else 200, content=body.model_dump())
