"""
Unit Tests for Storage Subsystem (LocalStorageProvider).
"""

import os
import shutil
import tempfile
import pytest

from app.core.exceptions import ValidationAppException
from app.storage.local import LocalStorageProvider


@pytest.fixture
def temp_storage_dir():
    """Creates temporary directory for storage tests and cleans up after."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.mark.asyncio
async def test_local_storage_provider_crud(temp_storage_dir: str):
    """Tests save, read, exists, and delete operations of LocalStorageProvider."""
    storage = LocalStorageProvider(base_directory=temp_storage_dir)

    content = b"Sample document binary content for storage provider test."
    original_filename = "test_contract.pdf"

    # 1. Save
    stored_filename, rel_path, abs_path = await storage.save(content, original_filename)
    assert stored_filename.endswith(".pdf")
    assert os.path.exists(abs_path)
    assert await storage.exists(rel_path) is True

    # 2. Read
    read_content = await storage.read(rel_path)
    assert read_content == content

    # 3. Delete
    deleted = await storage.delete(rel_path)
    assert deleted is True
    assert await storage.exists(rel_path) is False


@pytest.mark.asyncio
async def test_path_traversal_prevention(temp_storage_dir: str):
    """Verifies that LocalStorageProvider rejects directory traversal attempts."""
    storage = LocalStorageProvider(base_directory=temp_storage_dir)

    with pytest.raises(ValidationAppException):
        storage.get_absolute_path("../../etc/passwd")


def test_unique_filename_generation():
    """Verifies generated filenames are unique and retain extensions."""
    storage = LocalStorageProvider()
    fn1 = storage.generate_unique_filename("sample.pdf")
    fn2 = storage.generate_unique_filename("sample.pdf")

    assert fn1 != fn2
    assert fn1.endswith(".pdf")
    assert fn2.endswith(".pdf")
