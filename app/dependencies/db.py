"""
Database Repositories and Services Dependency Injectors.
Provides cleanly scoped instances bound to the request database session.
"""

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.repositories.refresh_token_repository import RefreshTokenRepository
from app.repositories.user_repository import UserRepository
from app.repositories.document_repository import DocumentRepository
from app.repositories.extracted_text_repository import ExtractedTextRepository
from app.repositories.ai_extraction_repository import AIExtractionRepository
from app.repositories.processing_job_repository import ProcessingJobRepository
from app.services.auth_service import AuthService
from app.services.document_service import DocumentService
from app.services.ocr_service import OCRService
from app.services.ai_extraction_service import AIExtractionService
from app.dependencies.storage import get_storage_provider
from app.dependencies.ocr import get_ocr_pipeline
from app.dependencies.workers import get_queue_provider
from app.storage.base import StorageProvider
from app.ocr.pipeline import OCRPipeline
from app.workers.base import JobQueueProvider
from app.workers.dispatcher import JobDispatcher


def get_user_repository(db: AsyncSession = Depends(get_db)) -> UserRepository:
    """Provides UserRepository instance scoped to database session."""
    return UserRepository(db)


def get_refresh_token_repository(db: AsyncSession = Depends(get_db)) -> RefreshTokenRepository:
    """Provides RefreshTokenRepository instance scoped to database session."""
    return RefreshTokenRepository(db)


def get_document_repository(db: AsyncSession = Depends(get_db)) -> DocumentRepository:
    """Provides DocumentRepository instance scoped to database session."""
    return DocumentRepository(db)


def get_extracted_text_repository(db: AsyncSession = Depends(get_db)) -> ExtractedTextRepository:
    """Provides ExtractedTextRepository instance scoped to database session."""
    return ExtractedTextRepository(db)


def get_ai_extraction_repository(db: AsyncSession = Depends(get_db)) -> AIExtractionRepository:
    """Provides AIExtractionRepository instance scoped to database session."""
    return AIExtractionRepository(db)


def get_processing_job_repository(db: AsyncSession = Depends(get_db)) -> ProcessingJobRepository:
    """Provides ProcessingJobRepository instance scoped to database session."""
    return ProcessingJobRepository(db)


def get_auth_service(
    user_repo: UserRepository = Depends(get_user_repository),
    token_repo: RefreshTokenRepository = Depends(get_refresh_token_repository)
) -> AuthService:
    """Provides AuthService instance injected with user and token repositories."""
    return AuthService(user_repo=user_repo, token_repo=token_repo)


def get_document_service(
    doc_repo: DocumentRepository = Depends(get_document_repository),
    storage: StorageProvider = Depends(get_storage_provider)
) -> DocumentService:
    """Provides DocumentService instance injected with document repository and storage provider."""
    return DocumentService(document_repo=doc_repo, storage_provider=storage)


def get_ocr_service(
    doc_repo: DocumentRepository = Depends(get_document_repository),
    text_repo: ExtractedTextRepository = Depends(get_extracted_text_repository),
    storage: StorageProvider = Depends(get_storage_provider),
    pipeline: OCRPipeline = Depends(get_ocr_pipeline)
) -> OCRService:
    """Provides OCRService instance injected with repositories, storage provider, and OCR pipeline."""
    return OCRService(
        document_repo=doc_repo,
        extracted_text_repo=text_repo,
        storage_provider=storage,
        ocr_pipeline=pipeline
    )


def get_ai_extraction_service(
    doc_repo: DocumentRepository = Depends(get_document_repository),
    ai_repo: AIExtractionRepository = Depends(get_ai_extraction_repository),
    ocr_service: OCRService = Depends(get_ocr_service)
) -> AIExtractionService:
    """Provides AIExtractionService instance injected with repositories and OCR service."""
    return AIExtractionService(
        document_repo=doc_repo,
        ai_extraction_repo=ai_repo,
        ocr_service=ocr_service
    )


def get_job_dispatcher(
    job_repo: ProcessingJobRepository = Depends(get_processing_job_repository),
    doc_repo: DocumentRepository = Depends(get_document_repository),
    queue: JobQueueProvider = Depends(get_queue_provider)
) -> JobDispatcher:
    """Provides JobDispatcher instance."""
    return JobDispatcher(
        job_repo=job_repo,
        doc_repo=doc_repo,
        queue_provider=queue
    )
