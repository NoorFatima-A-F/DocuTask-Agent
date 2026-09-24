"""
Document Management Service Business Logic Layer.
Handles upload validation, magic byte signature checks, SHA256 deduplication,
transactional storage rollback safety, and retrieval authorization.
"""

import hashlib
import math
import os
from pathlib import Path
import re
from typing import Optional
from uuid import UUID

from app.core.config import settings
from app.core.security import sanitize_log_input
from app.core.exceptions import (
    AccessDeniedException,
    ResourceNotFoundException,
    ValidationAppException,
)
from app.core.logging import logger
from app.models.user import User
from app.repositories.document_repository import DocumentRepository
from app.schemas.document import (
    DeleteResponse,
    DocumentListResponse,
    DocumentResponse,
    UploadResponse,
)
from app.storage.base import StorageProvider


class DocumentService:
    """Service providing document ingestion, validation, storage, and lifecycle management."""

    # Disallowed dangerous extensions for executable attack prevention
    DANGEROUS_EXTENSIONS = {
        ".exe", ".bat", ".cmd", ".sh", ".bash", ".php", ".js", ".vbs", ".ps1", ".jar", ".py"
    }

    # File magic byte header signatures for file content validation
    FILE_SIGNATURES = {
        ".pdf": [b"%PDF-"],
        ".png": [b"\x89PNG\r\n\x1a\n"],
        ".jpg": [b"\xff\xd8\xff"],
        ".jpeg": [b"\xff\xd8\xff"],
        ".tiff": [b"II*\x00", b"MM\x00*"],
        ".tif": [b"II*\x00", b"MM\x00*"],
    }

    def __init__(
        self,
        document_repo: DocumentRepository,
        storage_provider: StorageProvider
    ):
        self.doc_repo = document_repo
        self.storage = storage_provider

    def validate_file(self, content: bytes, original_filename: str, mime_type: str) -> None:
        """
        Validates uploaded file parameters against security rules and magic byte signatures.
        
        :raises ValidationAppException: If file fails validation criteria
        """
        # 1. Empty file check
        if not content or len(content) == 0:
            logger.warning(f"Upload validation failure: File '{original_filename}' is empty")
            raise ValidationAppException("Uploaded file cannot be empty")

        # 2. File size limit check
        max_bytes = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024
        if len(content) > max_bytes:
            logger.warning(
                f"Upload validation failure: File '{original_filename}' size ({len(content)} bytes) exceeds limit ({settings.MAX_UPLOAD_SIZE_MB}MB)"
            )
            raise ValidationAppException(
                f"File size exceeds maximum allowed limit of {settings.MAX_UPLOAD_SIZE_MB} MB"
            )

        # 3. Filename sanitization & length check
        if not original_filename or len(original_filename) > settings.MAX_FILENAME_LENGTH:
            raise ValidationAppException(
                f"Filename must be non-empty and less than {settings.MAX_FILENAME_LENGTH} characters"
            )

        # 4. Path traversal attempt check
        if ".." in original_filename or "/" in original_filename or "\\" in original_filename:
            logger.error(f"Path traversal attempt in filename: '{original_filename}'")
            raise ValidationAppException("Invalid filename character sequence detected")

        # 5. Extension check & dangerous extension rejection
        path_obj = Path(original_filename)
        ext = path_obj.suffix.lower()

        if not ext:
            raise ValidationAppException("Uploaded file missing file extension")

        if ext in self.DANGEROUS_EXTENSIONS:
            logger.error(f"Executable file upload rejected: '{original_filename}'")
            raise ValidationAppException(f"Forbidden executable file extension '{ext}'")

        if ext not in [e.lower() for e in settings.ALLOWED_EXTENSIONS]:
            logger.warning(f"Unsupported extension rejected: '{ext}' for file '{original_filename}'")
            raise ValidationAppException(
                f"File extension '{ext}' is not supported. Allowed extensions: {', '.join(settings.ALLOWED_EXTENSIONS)}"
            )

        # 6. Double extension check (e.g., document.pdf.exe)
        suffixes = path_obj.suffixes
        if len(suffixes) > 1:
            for s in suffixes[:-1]:
                if s.lower() in self.DANGEROUS_EXTENSIONS:
                    logger.error(f"Double extension attack detected: '{original_filename}'")
                    raise ValidationAppException("Malicious file naming structure detected")

        # 7. MIME type check
        clean_mime = mime_type.lower().split(";")[0].strip() if mime_type else ""
        allowed_mimes = [m.lower() for m in settings.ALLOWED_MIME_TYPES]
        if clean_mime not in allowed_mimes:
            logger.warning(f"Unsupported MIME type rejected: '{clean_mime}' for file '{original_filename}'")
            raise ValidationAppException(
                f"File MIME type '{clean_mime}' is not supported."
            )

        # 8. Magic Bytes / File Header Signature Verification
        if ext in self.FILE_SIGNATURES:
            expected_sigs = self.FILE_SIGNATURES[ext]
            if not any(content.startswith(sig) for sig in expected_sigs):
                logger.error(f"Magic bytes signature mismatch for file '{original_filename}': Extension='{ext}'")
                raise ValidationAppException(
                    f"File content magic byte header does not match declared extension '{ext}'."
                )

    def calculate_sha256(self, content: bytes) -> str:
        """Calculates SHA-256 hash of binary content."""
        return hashlib.sha256(content).hexdigest()

    async def upload_document(
        self,
        content: bytes,
        original_filename: str,
        mime_type: str,
        owner: User
    ) -> UploadResponse:
        """
        Ingests file, performs security validation, checks SHA256 duplicate detection,
        stores file safely, and records metadata in database with transactional rollback safety.
        """
        logger.info(f"Document upload initiated by user '{owner.username}': File='{original_filename}'")

        # Validate file parameters & magic bytes
        self.validate_file(content, original_filename, mime_type)

        # Compute SHA256 Hash
        sha256_h = self.calculate_sha256(content)

        # Duplicate Detection
        existing_doc = await self.doc_repo.get_by_hash(sha256_h, owner_id=owner.id)
        if existing_doc:
            logger.info(f"Duplicate document detected for user '{owner.id}': Hash={sha256_h[:10]}...")
            doc_resp = DocumentResponse.model_validate(existing_doc)
            return UploadResponse(
                document=doc_resp,
                is_duplicate=True,
                message="Duplicate document detected. Returned existing document record."
            )

        # Store binary file on storage provider
        ext = Path(original_filename).suffix.lower()
        stored_filename, rel_path, abs_path = await self.storage.save(
            content=content,
            original_filename=original_filename
        )

        # Record metadata in DB with transactional rollback protection
        try:
            doc_data = {
                "owner_id": owner.id,
                "original_filename": original_filename,
                "stored_filename": stored_filename,
                "relative_path": rel_path,
                "absolute_path": abs_path,
                "file_extension": ext,
                "mime_type": mime_type.lower().split(";")[0].strip(),
                "file_size": len(content),
                "sha256_hash": sha256_h,
                "upload_status": "QUEUED"
            }

            new_doc = await self.doc_repo.create(doc_data)
        except Exception as exc:
            # Database creation failure: Delete stored file from disk to prevent orphaned files!
            logger.error(f"Database commit failed after file save. Rolling back file storage for '{stored_filename}': {str(exc)}")
            await self.storage.delete(rel_path)
            raise exc

        logger.info(f"Document successfully created: ID={new_doc.id}, File='{stored_filename}'")

        doc_resp = DocumentResponse.model_validate(new_doc)
        return UploadResponse(
            document=doc_resp,
            is_duplicate=False,
            message="Document uploaded successfully."
        )

    async def get_document_by_id(self, doc_id: UUID, owner: User) -> DocumentResponse:
        """Retrieves document details with authorization check."""
        doc = await self.doc_repo.get_by_id(doc_id)
        if not doc:
            raise ResourceNotFoundException("Document not found")

        # Owner isolation check
        if doc.owner_id != owner.id and not owner.is_superuser:
            logger.warning(f"Unauthorized document access attempt: User '{sanitize_log_input(owner.id)}' on Document '{sanitize_log_input(doc_id)}'")
            raise ResourceNotFoundException("Document not found")

        return DocumentResponse.model_validate(doc)

    async def list_documents(
        self,
        owner: User,
        page: int = 1,
        page_size: int = 20,
        search_query: Optional[str] = None
    ) -> DocumentListResponse:
        """Returns paginated list of user documents."""
        page = max(1, page)
        page_size = max(1, min(100, page_size))

        docs, total = await self.doc_repo.paginate(
            owner_id=owner.id,
            page=page,
            page_size=page_size,
            search_query=search_query
        )

        pages = math.ceil(total / page_size) if total > 0 else 0
        items = [DocumentResponse.model_validate(d) for d in docs]

        logger.info(f"Listed documents for user '{owner.username}': Page={page}/{pages}, Total={total}")

        return DocumentListResponse(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            pages=pages
        )

    async def search_documents(
        self,
        owner: User,
        query: str,
        page: int = 1,
        page_size: int = 20
    ) -> DocumentListResponse:
        """Searches documents by query string."""
        return await self.list_documents(owner=owner, page=page, page_size=page_size, search_query=query)

    async def delete_document(self, doc_id: UUID, owner: User) -> DeleteResponse:
        """Deletes document file from storage provider and metadata from database."""
        doc = await self.doc_repo.get_by_id(doc_id)
        if not doc:
            raise ResourceNotFoundException("Document not found")

        if doc.owner_id != owner.id and not owner.is_superuser:
            logger.warning(f"Unauthorized document deletion attempt: User '{sanitize_log_input(owner.id)}' on Document '{sanitize_log_input(doc_id)}'")
            raise ResourceNotFoundException("Document not found")

        # Delete physical file from storage provider
        await self.storage.delete(doc.relative_path)

        # Delete database record
        await self.doc_repo.delete(doc)

        logger.info(f"Document successfully deleted: ID={sanitize_log_input(doc_id)} by user '{sanitize_log_input(owner.username)}'")
        return DeleteResponse(
            id=doc_id,
            message="Document deleted successfully"
        )
