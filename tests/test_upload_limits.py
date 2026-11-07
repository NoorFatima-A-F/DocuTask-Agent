"""Upload size is enforced while the body streams in, not after it is fully buffered."""

from __future__ import annotations

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from tests.fakes.data import png_bytes
from tests.test_reviews import _user

UPLOAD = f"{settings.API_V1_STR}/documents/upload"


async def test_declared_oversized_body_rejected_before_parsing(client: AsyncClient) -> None:
    res = await client.post(
        UPLOAD, content=b"x", headers={"Content-Length": str(10**12), "Content-Type": "multipart/form-data; boundary=x"}
    )
    assert res.status_code == 413


async def test_streamed_oversized_upload_is_cut_off(
    client: AsyncClient, db_session: AsyncSession, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(settings, "MAX_UPLOAD_SIZE_MB", 1)
    headers = await _user(client, db_session, "bigupload")
    big = png_bytes() + b"\0" * (2 * 1024 * 1024)
    res = await client.post(UPLOAD, files={"file": ("big.png", big, "image/png")}, headers=headers)
    assert res.status_code == 413


async def test_chunked_body_without_length_is_counted(client: AsyncClient) -> None:
    async def body():
        for _ in range(3):
            yield b"a" * (600 * 1024)

    res = await client.post(
        f"{settings.API_V1_STR}/auth/login", content=body(), headers={"Content-Type": "application/json"}
    )
    assert res.status_code == 413


async def test_normal_upload_still_works(client: AsyncClient, db_session: AsyncSession) -> None:
    headers = await _user(client, db_session, "smallupload")
    res = await client.post(UPLOAD, files={"file": ("ok.png", png_bytes(), "image/png")}, headers=headers)
    assert res.status_code == 201, res.text


async def test_storage_read_refuses_paths_outside_root(tmp_path) -> None:  # type: ignore[no-untyped-def]
    from app.core.exceptions import ValidationAppException
    from app.storage.local import LocalStorageProvider

    outside = tmp_path / "secret.txt"
    outside.write_text("top secret")
    storage = LocalStorageProvider(base_directory=str(tmp_path / "root"))
    for path in (str(outside), "../secret.txt"):
        with pytest.raises(ValidationAppException):
            await storage.read(path)
