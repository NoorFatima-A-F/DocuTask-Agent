"""Review queue API: routing to NEEDS_REVIEW, approve/reject with audit trail, RBAC, result semantics."""

from __future__ import annotations

import uuid
from typing import Any

from httpx import AsyncClient
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.llm import get_llm_provider
from app.dependencies.ocr import get_ocr_pipeline
from app.main import app
from app.models.review_event import ReviewEvent
from app.models.user import User
from app.ocr.pipeline import OCRPipeline
from tests.fakes.data import CONTOSO_INVOICE_JSON, CONTOSO_INVOICE_TEXT, png_bytes
from tests.fakes.llm import FakeLLMProvider
from tests.fakes.ocr import FakeOCRProvider

HALLUCINATED = {**CONTOSO_INVOICE_JSON, "vendor_name": "Northwind Traders"}


async def _user(client: AsyncClient, db: AsyncSession, name: str, role: str = "user") -> dict[str, str]:
    reg = await client.post(
        "/api/v1/auth/register", json={"email": f"{name}@example.com", "username": name, "password": "Password123!"}
    )
    assert reg.status_code == 201, reg.text
    if role != "user":
        await db.execute(update(User).where(User.username == name).values(role=role))
        await db.flush()
    login = await client.post("/api/v1/auth/login", json={"username_or_email": name, "password": "Password123!"})
    return {"Authorization": f"Bearer {login.json()['data']['access_token']}"}


async def _extract(client: AsyncClient, headers: dict[str, str], llm_output: dict[str, Any]) -> tuple[str, dict]:
    app.dependency_overrides[get_llm_provider] = lambda: FakeLLMProvider(llm_output)
    app.dependency_overrides[get_ocr_pipeline] = lambda: OCRPipeline(
        ocr_provider=FakeOCRProvider(text=CONTOSO_INVOICE_TEXT)
    )
    up = await client.post(
        "/api/v1/documents/upload", files={"file": ("inv.png", png_bytes(), "image/png")}, headers=headers
    )
    doc_id = up.json()["data"]["document"]["id"]
    ext = await client.post(f"/api/v1/ai/extract/{doc_id}", json={"document_type": "invoice"}, headers=headers)
    assert ext.status_code == 200, ext.text
    return doc_id, ext.json()["data"]


async def test_low_confidence_goes_to_queue_and_result_is_not_final(
    client: AsyncClient, db_session: AsyncSession
) -> None:
    owner = await _user(client, db_session, "owner1")
    reviewer = await _user(client, db_session, "rev1", role="reviewer")
    doc_id, data = await _extract(client, owner, HALLUCINATED)

    assert data["result"]["status"] == "NEEDS_REVIEW"
    assert data["result"]["final_json"] is None
    assert data["result"]["confidence_details"]["fields"]["vendor_name"]["grounded"] is False

    queue = await client.get("/api/v1/reviews?status=pending", headers=reviewer)
    assert queue.status_code == 200
    items = queue.json()["data"]["items"]
    assert [i["document_id"] for i in items] == [doc_id]

    detail = await client.get(f"/api/v1/reviews/{items[0]['extraction_id']}", headers=reviewer)
    body = detail.json()["data"]
    assert "Contoso Ltd" in body["ocr_text"]
    assert body["confidence_details"]["required_ungrounded"] == ["vendor_name"]
    download = await client.get(body["document_download_url"], headers=reviewer)
    assert download.status_code == 200 and download.content == png_bytes()


async def test_approve_with_corrections_writes_audit_and_final_json(
    client: AsyncClient, db_session: AsyncSession
) -> None:
    owner = await _user(client, db_session, "owner2")
    reviewer = await _user(client, db_session, "rev2", role="reviewer")
    doc_id, data = await _extract(client, owner, HALLUCINATED)
    ext_id = data["id"]

    res = await client.post(
        f"/api/v1/reviews/{ext_id}/approve", json={"corrections": {"vendor_name": "Contoso Ltd"}}, headers=reviewer
    )
    assert res.status_code == 200, res.text
    assert res.json()["data"]["status"] == "COMPLETED"

    events = (
        (await db_session.execute(select(ReviewEvent).where(ReviewEvent.extraction_id == uuid.UUID(ext_id))))
        .scalars()
        .all()
    )
    assert len(events) == 1 and events[0].action == "APPROVED"
    assert '"Northwind Traders"' in (events[0].original_json or "")
    assert '"Contoso Ltd"' in (events[0].corrected_json or "")

    result = (await client.get(f"/api/v1/ai/result/{doc_id}", headers=owner)).json()["data"]["result"]
    assert result["status"] == "COMPLETED"
    assert result["final_json"]["vendor_name"] == "Contoso Ltd"
    assert result["structured_json"]["vendor_name"] == "Northwind Traders"  # original preserved

    again = await client.post(f"/api/v1/reviews/{ext_id}/approve", json={}, headers=reviewer)
    assert again.status_code == 409


async def test_corrections_are_schema_validated(client: AsyncClient, db_session: AsyncSession) -> None:
    owner = await _user(client, db_session, "owner3")
    reviewer = await _user(client, db_session, "rev3", role="reviewer")
    _, data = await _extract(client, owner, HALLUCINATED)
    res = await client.post(
        f"/api/v1/reviews/{data['id']}/approve", json={"corrections": {"total_amount": "lots"}}, headers=reviewer
    )
    assert res.status_code == 422


async def test_reject_marks_failed_with_reason(client: AsyncClient, db_session: AsyncSession) -> None:
    owner = await _user(client, db_session, "owner4")
    reviewer = await _user(client, db_session, "rev4", role="reviewer")
    doc_id, data = await _extract(client, owner, HALLUCINATED)

    res = await client.post(f"/api/v1/reviews/{data['id']}/reject", json={"reason": "wrong vendor"}, headers=reviewer)
    assert res.status_code == 200
    body = res.json()["data"]
    assert (body["status"], body["error_code"]) == ("FAILED", "REJECTED_BY_REVIEWER")
    assert body["events"][0]["reason"] == "wrong vendor"
    result = (await client.get(f"/api/v1/ai/result/{doc_id}", headers=owner)).json()["data"]["result"]
    assert result["final_json"] is None


async def test_high_confidence_is_final_without_review(client: AsyncClient, db_session: AsyncSession) -> None:
    owner = await _user(client, db_session, "owner5")
    reviewer = await _user(client, db_session, "rev5", role="reviewer")
    _, data = await _extract(client, owner, CONTOSO_INVOICE_JSON)
    assert data["result"]["status"] == "COMPLETED"
    assert data["result"]["final_json"]["total_amount"] == 42.10
    queue = await client.get("/api/v1/reviews", headers=reviewer)
    assert queue.json()["data"]["total"] == 0


async def test_non_reviewer_forbidden_and_unauthenticated_rejected(
    client: AsyncClient, db_session: AsyncSession
) -> None:
    owner = await _user(client, db_session, "owner6")
    _, data = await _extract(client, owner, HALLUCINATED)
    for method, path in [
        ("GET", "/api/v1/reviews"),
        ("GET", f"/api/v1/reviews/{data['id']}"),
        ("GET", f"/api/v1/reviews/{data['id']}/document"),
        ("POST", f"/api/v1/reviews/{data['id']}/approve"),
        ("POST", f"/api/v1/reviews/{data['id']}/reject"),
    ]:
        kwargs: dict[str, Any] = {"json": {"reason": "nope"}} if method == "POST" else {}
        assert (await client.request(method, path, headers=owner, **kwargs)).status_code == 403, path
        assert (await client.request(method, path, **kwargs)).status_code == 401, path


async def test_admin_inherits_reviewer(client: AsyncClient, db_session: AsyncSession) -> None:
    admin = await _user(client, db_session, "admin1", role="admin")
    assert (await client.get("/api/v1/reviews", headers=admin)).status_code == 200


async def test_other_users_result_is_404(client: AsyncClient, db_session: AsyncSession) -> None:
    owner = await _user(client, db_session, "owner7")
    stranger = await _user(client, db_session, "stranger")
    doc_id, _ = await _extract(client, owner, CONTOSO_INVOICE_JSON)
    assert (await client.get(f"/api/v1/ai/result/{doc_id}", headers=stranger)).status_code == 404


async def test_unknown_extraction_is_404_for_reviewer(client: AsyncClient, db_session: AsyncSession) -> None:
    reviewer = await _user(client, db_session, "rev8", role="reviewer")
    res = await client.get("/api/v1/reviews/00000000-0000-0000-0000-000000000001", headers=reviewer)
    assert res.status_code == 404
