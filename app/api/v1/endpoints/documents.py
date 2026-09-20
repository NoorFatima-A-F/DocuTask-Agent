"""
Document Ingestion & Management API Endpoints Router.
Receives file upload requests, validates headers/tokens, delegates to DocumentService, and returns APIResponse envelopes.
"""

from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, File, Query, UploadFile, status

from app.dependencies.auth import get_current_active_user
from app.dependencies.db import get_document_service
from app.models.user import User
from app.schemas.document import (
    DeleteResponse,
    DocumentListResponse,
    DocumentResponse,
    UploadResponse,
)
from app.schemas.response import APIResponse
from app.services.document_service import DocumentService

router = APIRouter(prefix="/documents", tags=["Document Management"])


@router.post(
    "/upload",
    response_model=APIResponse[UploadResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Upload new document",
    description="Validates, ingests, and stores document binary file with SHA256 duplicate detection."
)
async def upload_document(
    file: UploadFile = File(..., description="Binary document file to upload"),
    current_user: User = Depends(get_current_active_user),
    doc_service: DocumentService = Depends(get_document_service)
) -> APIResponse[UploadResponse]:
    """Handles document upload request."""
    content = await file.read()
    original_filename = file.filename or "file.bin"
    content_type = file.content_type or "application/octet-stream"

    upload_result = await doc_service.upload_document(
        content=content,
        original_filename=original_filename,
        mime_type=content_type,
        owner=current_user
    )

    return APIResponse.success_response(
        data=upload_result,
        message=upload_result.message
    )


@router.get(
    "",
    response_model=APIResponse[DocumentListResponse],
    status_code=status.HTTP_200_OK,
    summary="List user documents",
    description="Returns paginated list of documents owned by authenticated user."
)
async def list_documents(
    page: int = Query(1, ge=1, description="Page index"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    q: Optional[str] = Query(None, description="Optional search query filter"),
    current_user: User = Depends(get_current_active_user),
    doc_service: DocumentService = Depends(get_document_service)
) -> APIResponse[DocumentListResponse]:
    """Retrieves paginated documents."""
    result = await doc_service.list_documents(
        owner=current_user,
        page=page,
        page_size=page_size,
        search_query=q
    )

    return APIResponse.success_response(
        data=result,
        message="Documents listed successfully"
    )


@router.get(
    "/search",
    response_model=APIResponse[DocumentListResponse],
    status_code=status.HTTP_200_OK,
    summary="Search user documents",
    description="Searches user documents by filename or file extension."
)
async def search_documents(
    q: str = Query(..., min_length=1, description="Search query string"),
    page: int = Query(1, ge=1, description="Page index"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    current_user: User = Depends(get_current_active_user),
    doc_service: DocumentService = Depends(get_document_service)
) -> APIResponse[DocumentListResponse]:
    """Executes document search."""
    result = await doc_service.search_documents(
        owner=current_user,
        query=q,
        page=page,
        page_size=page_size
    )

    return APIResponse.success_response(
        data=result,
        message="Search results retrieved successfully"
    )


@router.get(
    "/{id}",
    response_model=APIResponse[DocumentResponse],
    status_code=status.HTTP_200_OK,
    summary="Get document details",
    description="Retrieves metadata details for specific document by UUID."
)
async def get_document(
    id: UUID,
    current_user: User = Depends(get_current_active_user),
    doc_service: DocumentService = Depends(get_document_service)
) -> APIResponse[DocumentResponse]:
    """Retrieves single document metadata."""
    doc_response = await doc_service.get_document_by_id(doc_id=id, owner=current_user)

    return APIResponse.success_response(
        data=doc_response,
        message="Document details retrieved successfully"
    )


@router.delete(
    "/{id}",
    response_model=APIResponse[DeleteResponse],
    status_code=status.HTTP_200_OK,
    summary="Delete document",
    description="Deletes document physical file from storage and record from database."
)
async def delete_document(
    id: UUID,
    current_user: User = Depends(get_current_active_user),
    doc_service: DocumentService = Depends(get_document_service)
) -> APIResponse[DeleteResponse]:
    """Handles document deletion."""
    delete_result = await doc_service.delete_document(doc_id=id, owner=current_user)

    return APIResponse.success_response(
        data=delete_result,
        message=delete_result.message
    )
