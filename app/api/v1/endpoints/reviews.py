"""Review queue API: list, inspect, approve (with corrections) or reject NEEDS_REVIEW extractions.

All routes require the ``reviewer`` role (admins and superusers inherit it).
"""

from __future__ import annotations

import json
import os
from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ResourceNotFoundException
from app.database.session import get_db
from app.dependencies.auth import RoleChecker
from app.models.ai_extraction import AIExtraction
from app.models.user import User
from app.schemas.response import APIResponse
from app.services.review_service import ReviewService

require_reviewer = RoleChecker(["reviewer"])

router = APIRouter(prefix="/reviews", tags=["Human Review"], dependencies=[Depends(require_reviewer)])


def get_review_service(db: AsyncSession = Depends(get_db)) -> ReviewService:
    return ReviewService(db)


class ReviewSummary(BaseModel):
    extraction_id: UUID
    document_id: UUID
    document_type: str
    status: str
    confidence: Optional[float]
    created_at: datetime


class ReviewPage(BaseModel):
    items: List[ReviewSummary]
    total: int
    page: int
    page_size: int


class ReviewEventOut(BaseModel):
    action: str
    reviewer_id: UUID
    reason: Optional[str] = None
    corrected_json: Optional[Dict[str, Any]] = None
    created_at: datetime


class ReviewDetail(ReviewSummary):
    structured_json: Optional[Dict[str, Any]]
    final_json: Optional[Dict[str, Any]]
    confidence_details: Optional[Dict[str, Any]]
    error_code: Optional[str]
    ocr_text: str
    document_filename: Optional[str]
    document_download_url: str
    events: List[ReviewEventOut]


class ApproveRequest(BaseModel):
    corrections: Optional[Dict[str, Any]] = Field(
        None, description="Field overrides, validated against the document type's schema"
    )


class RejectRequest(BaseModel):
    reason: str = Field(..., min_length=3, max_length=2000)


def _loads(value: Optional[str]) -> Optional[Dict[str, Any]]:
    return json.loads(value) if value else None


def _summary(r: AIExtraction) -> ReviewSummary:
    return ReviewSummary(
        extraction_id=r.id,
        document_id=r.document_id,
        document_type=r.document_type,
        status=r.status,
        confidence=r.confidence,
        created_at=r.created_at,
    )


async def _detail(service: ReviewService, extraction_id: UUID) -> ReviewDetail:
    data = await service.get_detail(extraction_id)
    r: AIExtraction = data["record"]
    events = await service.events_for(extraction_id)
    return ReviewDetail(
        **_summary(r).model_dump(),
        structured_json=_loads(r.structured_json),
        final_json=_loads(r.final_json),
        confidence_details=_loads(r.confidence_details),
        error_code=r.error_code,
        ocr_text=data["ocr_text"],
        document_filename=data["document"].original_filename if data["document"] else None,
        document_download_url=f"/api/v1/reviews/{r.id}/document",
        events=[
            ReviewEventOut(
                action=e.action,
                reviewer_id=e.reviewer_id,
                reason=e.reason,
                corrected_json=_loads(e.corrected_json),
                created_at=e.created_at,
            )
            for e in events
        ],
    )


@router.get("", response_model=APIResponse[ReviewPage], summary="List extractions awaiting review (oldest first)")
async def list_reviews(
    status: str = Query("pending", pattern="^pending$"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    service: ReviewService = Depends(get_review_service),
) -> APIResponse[ReviewPage]:
    items, total = await service.list_pending(page=page, page_size=page_size)
    return APIResponse.success_response(
        data=ReviewPage(items=[_summary(r) for r in items], total=total, page=page, page_size=page_size)
    )


@router.get("/{extraction_id}", response_model=APIResponse[ReviewDetail], summary="Extraction with evidence")
async def get_review(
    extraction_id: UUID, service: ReviewService = Depends(get_review_service)
) -> APIResponse[ReviewDetail]:
    return APIResponse.success_response(data=await _detail(service, extraction_id))


@router.get("/{extraction_id}/document", summary="Download the source document", response_class=FileResponse)
async def download_document(extraction_id: UUID, service: ReviewService = Depends(get_review_service)) -> FileResponse:
    path, mime, filename = await service.get_document_path(extraction_id)
    if not os.path.isfile(path):
        raise ResourceNotFoundException("Document file not found")
    return FileResponse(path, media_type=mime, filename=filename)


@router.post(
    "/{extraction_id}/approve", response_model=APIResponse[ReviewDetail], summary="Approve, optionally corrected"
)
async def approve_review(
    extraction_id: UUID,
    body: ApproveRequest = ApproveRequest(),
    reviewer: User = Depends(require_reviewer),
    service: ReviewService = Depends(get_review_service),
) -> APIResponse[ReviewDetail]:
    await service.approve(extraction_id, reviewer, body.corrections)
    return APIResponse.success_response(data=await _detail(service, extraction_id), message="Extraction approved")


@router.post("/{extraction_id}/reject", response_model=APIResponse[ReviewDetail], summary="Reject with a reason")
async def reject_review(
    extraction_id: UUID,
    body: RejectRequest,
    reviewer: User = Depends(require_reviewer),
    service: ReviewService = Depends(get_review_service),
) -> APIResponse[ReviewDetail]:
    await service.reject(extraction_id, reviewer, body.reason)
    return APIResponse.success_response(data=await _detail(service, extraction_id), message="Extraction rejected")
