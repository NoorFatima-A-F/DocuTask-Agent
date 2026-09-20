"""
OCR & Text Extraction API Endpoints Router.
Receives extraction requests, delegates to OCRService, and returns APIResponse envelopes.
"""

from typing import Any, Dict, List
from uuid import UUID
from fastapi import APIRouter, Depends, Query, status

from app.dependencies.auth import get_current_active_user
from app.dependencies.db import get_ocr_service
from app.models.user import User
from app.ocr.schemas import DocumentContent, PageContent
from app.schemas.response import APIResponse
from app.services.ocr_service import OCRService

router = APIRouter(prefix="/ocr", tags=["OCR & Text Extraction"])


@router.post(
    "/extract/{document_id}",
    response_model=APIResponse[DocumentContent],
    status_code=status.HTTP_200_OK,
    summary="Trigger text extraction",
    description="Runs text extraction pipeline (native digital text or OCR) for specified document."
)
@router.post(
    "/{document_id}/ocr",
    response_model=APIResponse[DocumentContent],
    status_code=status.HTTP_200_OK,
    include_in_schema=False
)
async def extract_text(
    document_id: UUID,
    force_reextract: bool = Query(False, description="Set True to bypass cache and force re-extraction"),
    language: str = Query("eng", description="OCR language code (e.g. 'eng', 'urd', 'ara')"),
    current_user: User = Depends(get_current_active_user),
    ocr_service: OCRService = Depends(get_ocr_service)
) -> APIResponse[DocumentContent]:
    """Handles text extraction execution."""
    result = await ocr_service.extract_text_for_document(
        document_id=document_id,
        owner=current_user,
        force_reextract=force_reextract,
        language=language
    )

    return APIResponse.success_response(
        data=result,
        message="Text extraction completed successfully"
    )


@router.get(
    "/text/{document_id}",
    response_model=APIResponse[DocumentContent],
    status_code=status.HTTP_200_OK,
    summary="Get extracted text",
    description="Retrieves full extracted text object for document."
)
@router.get(
    "/{document_id}/ocr",
    response_model=APIResponse[DocumentContent],
    status_code=status.HTTP_200_OK,
    include_in_schema=False
)
async def get_extracted_text(
    document_id: UUID,
    current_user: User = Depends(get_current_active_user),
    ocr_service: OCRService = Depends(get_ocr_service)
) -> APIResponse[DocumentContent]:
    """Retrieves extracted document text."""
    result = await ocr_service.get_extracted_text(
        document_id=document_id,
        owner=current_user
    )

    return APIResponse.success_response(
        data=result,
        message="Extracted text retrieved successfully"
    )


@router.get(
    "/pages/{document_id}",
    response_model=APIResponse[List[PageContent]],
    status_code=status.HTTP_200_OK,
    summary="Get page-level extracted text",
    description="Retrieves page breakdown of extracted text for document."
)
async def get_extracted_pages(
    document_id: UUID,
    current_user: User = Depends(get_current_active_user),
    ocr_service: OCRService = Depends(get_ocr_service)
) -> APIResponse[List[PageContent]]:
    """Retrieves page breakdown."""
    pages = await ocr_service.get_extracted_pages(
        document_id=document_id,
        owner=current_user
    )

    return APIResponse.success_response(
        data=pages,
        message="Extracted pages retrieved successfully"
    )


@router.get(
    "/status/{document_id}",
    response_model=APIResponse[Dict[str, Any]],
    status_code=status.HTTP_200_OK,
    summary="Get OCR extraction status",
    description="Retrieves extraction status, total pages, and average confidence score."
)
@router.get(
    "/{document_id}/ocr/status",
    response_model=APIResponse[Dict[str, Any]],
    status_code=status.HTTP_200_OK,
    include_in_schema=False
)
async def get_ocr_status(
    document_id: UUID,
    current_user: User = Depends(get_current_active_user),
    ocr_service: OCRService = Depends(get_ocr_service)
) -> APIResponse[Dict[str, Any]]:
    """Retrieves OCR extraction status."""
    status_data = await ocr_service.get_ocr_status(
        document_id=document_id,
        owner=current_user
    )

    return APIResponse.success_response(
        data=status_data,
        message="OCR status retrieved successfully"
    )
