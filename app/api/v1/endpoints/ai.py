"""
AI Engine & Structured Extraction API Endpoints Router.
Receives structured extraction requests, delegates to AIExtractionService, and returns APIResponse envelopes.
"""

from typing import Any, Dict, List
from uuid import UUID
from fastapi import APIRouter, Depends, status

from app.dependencies.auth import get_current_active_user
from app.dependencies.db import get_ai_extraction_service
from app.models.user import User
from app.ai.schemas import ExtractionRequest, ExtractionResponse
from app.schemas.response import APIResponse
from app.services.ai_extraction_service import AIExtractionService

router = APIRouter(prefix="/ai", tags=["AI Engine Extraction"])


@router.post(
    "/extract/{document_id}",
    response_model=APIResponse[ExtractionResponse],
    status_code=status.HTTP_200_OK,
    summary="Extract structured document data",
    description="Triggers structured information extraction using configured LLM provider and document schema."
)
@router.post(
    "/extract/{document_id}",
    response_model=APIResponse[ExtractionResponse],
    status_code=status.HTTP_200_OK,
    include_in_schema=False
)
async def extract_structured_data(
    document_id: UUID,
    request: ExtractionRequest = ExtractionRequest(),
    current_user: User = Depends(get_current_active_user),
    ai_service: AIExtractionService = Depends(get_ai_extraction_service)
) -> APIResponse[ExtractionResponse]:
    """Handles structured extraction execution."""
    result = await ai_service.extract_structured_data(
        document_id=document_id,
        owner=current_user,
        request=request
    )

    return APIResponse.success_response(
        data=result,
        message="Structured AI extraction completed successfully"
    )


@router.get(
    "/result/{document_id}",
    response_model=APIResponse[ExtractionResponse],
    status_code=status.HTTP_200_OK,
    summary="Get latest extraction result",
    description="Retrieves the most recent structured extraction result for specified document."
)
@router.get(
    "/extract/{document_id}",
    response_model=APIResponse[ExtractionResponse],
    status_code=status.HTTP_200_OK,
    include_in_schema=False
)
async def get_latest_result(
    document_id: UUID,
    current_user: User = Depends(get_current_active_user),
    ai_service: AIExtractionService = Depends(get_ai_extraction_service)
) -> APIResponse[ExtractionResponse]:
    """Retrieves latest extraction result."""
    result = await ai_service.get_latest_result(
        document_id=document_id,
        owner=current_user
    )

    return APIResponse.success_response(
        data=result,
        message="Latest extraction result retrieved successfully"
    )


@router.get(
    "/status/{document_id}",
    response_model=APIResponse[Dict[str, Any]],
    status_code=status.HTTP_200_OK,
    summary="Get AI extraction status",
    description="Retrieves AI extraction status and document type metadata."
)
@router.get(
    "/extract/status/{document_id}",
    response_model=APIResponse[Dict[str, Any]],
    status_code=status.HTTP_200_OK,
    include_in_schema=False
)
async def get_extraction_status(
    document_id: UUID,
    current_user: User = Depends(get_current_active_user),
    ai_service: AIExtractionService = Depends(get_ai_extraction_service)
) -> APIResponse[Dict[str, Any]]:
    """Retrieves extraction status."""
    status_data = await ai_service.get_extraction_status(
        document_id=document_id,
        owner=current_user
    )

    return APIResponse.success_response(
        data=status_data,
        message="AI extraction status retrieved successfully"
    )


@router.get(
    "/history/{document_id}",
    response_model=APIResponse[List[ExtractionResponse]],
    status_code=status.HTTP_200_OK,
    summary="Get extraction history",
    description="Retrieves complete historical record of all past AI extractions for document."
)
@router.get(
    "/extract/history/{document_id}",
    response_model=APIResponse[List[ExtractionResponse]],
    status_code=status.HTTP_200_OK,
    include_in_schema=False
)
async def get_extraction_history(
    document_id: UUID,
    current_user: User = Depends(get_current_active_user),
    ai_service: AIExtractionService = Depends(get_ai_extraction_service)
) -> APIResponse[List[ExtractionResponse]]:
    """Retrieves historical extractions."""
    history = await ai_service.get_extraction_history(
        document_id=document_id,
        owner=current_user
    )

    return APIResponse.success_response(
        data=history,
        message="Extraction history retrieved successfully"
    )


@router.delete(
    "/result/{document_id}",
    response_model=APIResponse[dict],
    status_code=status.HTTP_200_OK,
    summary="Delete extraction result",
    description="Deletes structured AI extraction result for specified document."
)
@router.delete(
    "/extract/{document_id}",
    response_model=APIResponse[dict],
    status_code=status.HTTP_200_OK,
    include_in_schema=False
)
async def delete_result(
    document_id: UUID,
    current_user: User = Depends(get_current_active_user),
    ai_service: AIExtractionService = Depends(get_ai_extraction_service)
) -> APIResponse[dict]:
    """Handles deletion of extraction results."""
    await ai_service.delete_result(
        document_id=document_id,
        owner=current_user
    )

    return APIResponse.success_response(
        data={},
        message="AI extraction result deleted successfully"
    )
