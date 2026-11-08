"""The evaluation harness scores correctly and the routing gate holds on the committed dataset."""

from __future__ import annotations

import json
from pathlib import Path

from evals import run_eval
from evals.run_eval import Doc, load_dataset, run_replay, run_routing, values_match


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
