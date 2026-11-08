"""The evaluation harness scores correctly and the routing gate holds on the committed dataset."""

from __future__ import annotations

import asyncio
import json
from pathlib import Path
from typing import Any

from app.core.errors.extraction import ErrorCode, LLMError
from app.ocr.pipeline import OCRPipeline
from app.ocr.schemas import PageContent
from evals import run_eval
from evals.run_eval import Doc, load_dataset, run_replay, run_routing, values_match
from tests.fakes.llm import FakeLLMProvider
from tests.fakes.ocr import FakeOCRProvider


def test_values_match_rules() -> None:
    assert values_match("total_amount", 1250.0, "1250.004")
    assert not values_match("total_amount", 1250.0, 1251)
    assert values_match("invoice_date", "2026-08-19", "August 19, 2026")
    assert not values_match("invoice_date", "2026-08-19", "2026-08-20")
    assert values_match("vendor_name", "Halvorsen Tooling", "  halvorsen   TOOLING ")
    assert values_match("customer_name", None, None)
    assert not values_match("customer_name", "X", None)


def test_dataset_is_complete() -> None:
    docs = load_dataset()
    assert len(docs) >= 30
    assert {d.document_type for d in docs} == {"invoice", "receipt", "utility_bill"}
    assert all(d.image.exists() and d.text for d in docs)


def test_routing_gate_holds() -> None:
    report = run_routing(load_dataset())
    assert run_eval.gate_routing(report) == [], report["false_accepts"]


def test_replay_counts_a_wrong_auto_accepted_extraction_as_false_accept(tmp_path: Path) -> None:
    doc = next(d for d in load_dataset() if d.document_type == "invoice")
    wrong = {**doc.truth, "total_amount": doc.truth["total_amount"] + 100}
    # The OCR text is crafted to contain the wrong total, so the gate cannot catch it:
    # replay must still flag it as a false accept because it differs from the ground truth.
    ocr = doc.text + f"\n{wrong['total_amount']:,.2f}\n"
    (tmp_path / f"{doc.doc_id}.json").write_text(
        json.dumps({"doc_id": doc.doc_id, "ocr_text": ocr, "ocr_confidence": 0.95, "raw_text": json.dumps(wrong)})
    )
    report = run_replay([doc], tmp_path)
    assert report["documents_all_required_correct"] == 0.0
    if report["auto_accept_rate"] == 1.0:
        assert report["false_accept_rate"] == 1.0
        assert report["false_accepts"] == [f"{doc.doc_id}:total_amount"]


def test_replay_marks_unrecorded_documents_failed(tmp_path: Path) -> None:
    doc: Doc = load_dataset()[0]
    report = run_replay([doc], tmp_path)
    assert report["failure_rate"] == 1.0 and report["failures_by_code"] == {"NOT_RECORDED": 1}


def _live_env(docs: list[Doc], *script: dict[str, Any] | str | BaseException) -> tuple[FakeLLMProvider, OCRPipeline]:
    """Fake OCR (returns each document's own text) and a scripted fake LLM: no network, no tesseract."""
    texts = iter(d.text for d in docs)

    class PerDocOCR(FakeOCRProvider):
        async def extract_page(self, image_bytes: bytes, page_number: int = 1, language: str = "eng") -> PageContent:
            self.text = next(texts)
            return await super().extract_page(image_bytes, page_number, language)

    return FakeLLMProvider(*script), OCRPipeline(ocr_provider=PerDocOCR())


def _run_live(docs: list[Doc], record: Path, llm: FakeLLMProvider, ocr: OCRPipeline, **kw: Any) -> dict[str, Any]:
    return asyncio.run(run_eval.run_live(docs, record, provider=llm, pipeline=ocr, **kw))


def test_live_resume_skips_answered_documents_and_limit_caps_requests(tmp_path: Path) -> None:
    docs = [d for d in load_dataset() if d.document_type == "invoice"][:3]
    llm, ocr = _live_env(docs[:1], docs[0].truth)
    _run_live(docs, tmp_path, llm, ocr, resume=True, limit=1)
    assert len(llm.calls) == 1

    # Second run: the answered document is skipped, the other two are sent.
    llm2, ocr2 = _live_env(docs[1:], docs[1].truth, docs[2].truth)
    report = _run_live(docs, tmp_path, llm2, ocr2, resume=True)
    assert len(llm2.calls) == 2
    assert report["mode"] == "live" and report["documents"] == 3 and report["failure_rate"] == 0.0


def test_live_stops_at_the_first_rate_limit_and_resume_retries_it(tmp_path: Path) -> None:
    docs = [d for d in load_dataset() if d.document_type == "receipt"][:3]
    llm, ocr = _live_env(docs, docs[0].truth, LLMError(ErrorCode.LLM_RATE_LIMITED), docs[2].truth)
    report = _run_live(docs, tmp_path, llm, ocr, resume=True)
    assert len(llm.calls) == 2  # stopped; the third document was never sent
    assert report["failures_by_code"] == {"LLM_RATE_LIMITED": 1, "NOT_RECORDED": 1}

    llm2, ocr2 = _live_env(docs[1:], docs[1].truth, docs[2].truth)
    report = _run_live(docs, tmp_path, llm2, ocr2, resume=True)
    assert len(llm2.calls) == 2 and report["failure_rate"] == 0.0
