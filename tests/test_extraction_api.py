"""
Integration tests for AI Extraction HTTP API endpoints.
"""

import io
from PIL import Image
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_ai_extraction_api_endpoints(client: AsyncClient):
    """Verifies AI extraction HTTP API routes."""
    # 1. Register & Login User
    reg = await client.post("/api/v1/auth/register", json={
        "email": "ai_api_user@example.com",
        "username": "aiapiuser",
        "password": "Password123!"
    })
    assert reg.status_code == 201

    login = await client.post("/api/v1/auth/login", json={
        "username_or_email": "aiapiuser",
        "password": "Password123!"
    })
    token = login.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Upload Document
    img = Image.new("RGB", (100, 50), color="white")
    buf = io.BytesIO()
    img.save(buf, format="PNG")

    files = {"file": ("bill.png", buf.getvalue(), "image/png")}
    up_res = await client.post("/api/v1/documents/upload", files=files, headers=headers)
    assert up_res.status_code == 201
    doc_id = up_res.json()["data"]["document"]["id"]

    # 3. POST /api/v1/ai/extract/{document_id}
    ext_payload = {
        "document_type": "invoice",
        "force_reextract": False
    }
    ext_res = await client.post(f"/api/v1/ai/extract/{doc_id}", json=ext_payload, headers=headers)
    assert ext_res.status_code == 200
    body = ext_res.json()
    assert body["success"] is True
    assert body["data"]["metadata"]["document_id"] == doc_id
    assert body["data"]["metadata"]["document_type"] == "invoice"

    # 4. GET /api/v1/ai/result/{document_id}
    get_res = await client.get(f"/api/v1/ai/result/{doc_id}", headers=headers)
    assert get_res.status_code == 200
    assert get_res.json()["data"]["metadata"]["document_id"] == doc_id

    # 5. GET /api/v1/ai/status/{document_id}
    status_res = await client.get(f"/api/v1/ai/status/{doc_id}", headers=headers)
    assert status_res.status_code == 200
    assert status_res.json()["data"]["status"] == "EXTRACTION_COMPLETED"

    # 6. GET /api/v1/ai/history/{document_id}
    hist_res = await client.get(f"/api/v1/ai/history/{doc_id}", headers=headers)
    assert hist_res.status_code == 200
    assert len(hist_res.json()["data"]) >= 1

    # 7. DELETE /api/v1/ai/result/{document_id}
    del_res = await client.delete(f"/api/v1/ai/result/{doc_id}", headers=headers)
    assert del_res.status_code == 200
