"""
Unit and Integration Tests for Document Ingestion & Storage Subsystem.
"""

import shutil
import tempfile
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.exceptions import ValidationAppException, ResourceNotFoundException
from app.repositories.document_repository import DocumentRepository
from app.repositories.user_repository import UserRepository
from app.services.document_service import DocumentService
from app.storage.local import LocalStorageProvider


@pytest.fixture
def temp_storage_dir():
    """Temporary storage location fixture."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.mark.asyncio
async def test_document_validation_rules(temp_storage_dir: str):
    """Verifies all DocumentService upload validation security rules."""
    storage = LocalStorageProvider(base_directory=temp_storage_dir)
    service = DocumentService(document_repo=None, storage_provider=storage)

    # 1. Empty file
    with pytest.raises(ValidationAppException) as exc:
        service.validate_file(b"", "test.pdf", "application/pdf")
    assert "cannot be empty" in str(exc.value)

    # 2. Oversized file
    huge_content = b"X" * ((settings.MAX_UPLOAD_SIZE_MB + 1) * 1024 * 1024)
    with pytest.raises(ValidationAppException) as exc:
        service.validate_file(huge_content, "test.pdf", "application/pdf")
    assert "exceeds maximum allowed limit" in str(exc.value)

    # 3. Dangerous extension
    with pytest.raises(ValidationAppException) as exc:
        service.validate_file(b"payload", "malicious.exe", "application/octet-stream")
    assert "Forbidden executable" in str(exc.value)

    # 4. Double extension attack
    with pytest.raises(ValidationAppException) as exc:
        service.validate_file(b"payload", "contract.exe.pdf", "application/pdf")
    assert "Malicious file naming structure" in str(exc.value)

    # 5. Path traversal filename
    with pytest.raises(ValidationAppException) as exc:
        service.validate_file(b"content", "../../etc/passwd.pdf", "application/pdf")
    assert "Invalid filename character" in str(exc.value)

    # 6. Unsupported MIME type
    with pytest.raises(ValidationAppException) as exc:
        service.validate_file(b"content", "file.pdf", "application/x-executable")
    assert "MIME type" in str(exc.value)


@pytest.mark.asyncio
async def test_document_service_upload_and_deduplication(db_session: AsyncSession, temp_storage_dir: str):
    """Tests document ingestion, storage, and SHA-256 deduplication."""
    user_repo = UserRepository(db_session)
    doc_repo = DocumentRepository(db_session)
    storage = LocalStorageProvider(base_directory=temp_storage_dir)
    service = DocumentService(document_repo=doc_repo, storage_provider=storage)

    user = await user_repo.create({
        "email": "doc_owner@example.com",
        "username": "docowner",
        "hashed_password": "hashed_pass"
    })

    file_content = b"Sample Invoice Data for SHA256 Deduplication Test"
    filename = "invoice_2026.pdf"
    mime_type = "application/pdf"

    # Initial Upload
    res1 = await service.upload_document(file_content, filename, mime_type, user)
    assert res1.is_duplicate is False
    assert res1.document.original_filename == filename
    assert res1.document.file_size == len(file_content)

    # Duplicate Upload Attempt
    res2 = await service.upload_document(file_content, filename, mime_type, user)
    assert res2.is_duplicate is True
    assert res2.document.id == res1.document.id


@pytest.mark.asyncio
async def test_document_service_ownership_isolation(db_session: AsyncSession, temp_storage_dir: str):
    """Tests that user access controls isolate documents between different users."""
    user_repo = UserRepository(db_session)
    doc_repo = DocumentRepository(db_session)
    storage = LocalStorageProvider(base_directory=temp_storage_dir)
    service = DocumentService(document_repo=doc_repo, storage_provider=storage)

    user1 = await user_repo.create({"email": "user1@example.com", "username": "user1", "hashed_password": "p"})
    user2 = await user_repo.create({"email": "user2@example.com", "username": "user2", "hashed_password": "p"})

    upload_res = await service.upload_document(b"User 1 Confidential PDF", "confidential.pdf", "application/pdf", user1)
    doc_id = upload_res.document.id

    # User 1 can access
    doc_user1 = await service.get_document_by_id(doc_id, user1)
    assert doc_user1.id == doc_id

    # User 2 cannot access (raises ResourceNotFoundException for privacy)
    with pytest.raises(ResourceNotFoundException):
        await service.get_document_by_id(doc_id, user2)

    # User 2 cannot delete User 1's document
    with pytest.raises(ResourceNotFoundException):
        await service.delete_document(doc_id, user2)


@pytest.mark.asyncio
async def test_document_api_full_workflow(client: AsyncClient):
    """Verifies complete document API HTTP endpoint workflow."""

    # 1. Register & Login User
    reg = await client.post("/api/v1/auth/register", json={
        "email": "doc_api_user@example.com",
        "username": "docapiuser",
        "password": "Password123!"
    })
    assert reg.status_code == 201

    login = await client.post("/api/v1/auth/login", json={
        "username_or_email": "docapiuser",
        "password": "Password123!"
    })
    token = login.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Upload Document
    file_bytes = b"Hello, AI Document Processing Platform API!"
    files = {"file": ("test_resume.pdf", file_bytes, "application/pdf")}

    upload_res = await client.post("/api/v1/documents/upload", files=files, headers=headers)
    assert upload_res.status_code == 201
    
    body = upload_res.json()
    assert body["success"] is True
    doc_data = body["data"]["document"]
    doc_id = doc_data["id"]
    assert doc_data["original_filename"] == "test_resume.pdf"

    # 3. GET /documents (List)
    list_res = await client.get("/api/v1/documents", headers=headers)
    assert list_res.status_code == 200
    list_body = list_res.json()["data"]
    assert list_body["total"] == 1
    assert list_body["items"][0]["id"] == doc_id

    # 4. GET /documents/search
    search_res = await client.get("/api/v1/documents/search?q=resume", headers=headers)
    assert search_res.status_code == 200
    assert search_res.json()["data"]["total"] == 1

    # 5. GET /documents/{id}
    get_res = await client.get(f"/api/v1/documents/{doc_id}", headers=headers)
    assert get_res.status_code == 200
    assert get_res.json()["data"]["id"] == doc_id

    # 6. DELETE /documents/{id}
    del_res = await client.delete(f"/api/v1/documents/{doc_id}", headers=headers)
    assert del_res.status_code == 200
    assert del_res.json()["success"] is True

    # 7. Confirm deletion
    get_after_del = await client.get(f"/api/v1/documents/{doc_id}", headers=headers)
    assert get_after_del.status_code == 404
