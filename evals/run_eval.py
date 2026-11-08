"""Evaluate extraction and routing against the synthetic dataset.

Modes
-----
``routing`` (default, offline, used by CI)
    Measures the confidence gate, not the model. For every document it scores the
    ground-truth extraction and several corrupted versions (hallucinated value, wrong
    total, wrong date, missing required field) against the document text, and reports how
    often a corrupted extraction is auto-accepted (false-accept rate) and how often a
    correct one is accepted without review.

``live``
    Runs the real pipeline on ``document.png``: tesseract OCR -> Gemini -> validation ->
    confidence routing, and compares the output with the ground truth. Needs tesseract and
    ``GEMINI_API_KEY``. ``--record DIR`` stores the OCR text and raw model output per document.
    Free-tier keys have a small daily request quota, so a run can be split: ``--resume`` skips
    documents that already have a model output in ``DIR``, ``--limit N`` sends at most N requests,
    ``--delay S`` waits between requests, and the run stops at the first rate-limit error.
    With ``--resume`` the report covers every document recorded in ``DIR`` so far.

``replay``
    Re-scores recordings made with ``live --record`` without OCR or network calls, so changes
    to validation/confidence can be compared on identical model outputs.

Usage::

    python evals/run_eval.py --mode routing --gate
    python evals/run_eval.py --mode live --record evals/recordings/2026-11-08
    python evals/run_eval.py --mode live --record evals/recordings/2026-11-08 --resume --limit 18
    python evals/run_eval.py --mode replay --recordings evals/recordings/2026-11-08
"""

from __future__ import annotations

import argparse
import asyncio
import copy
import json
import statistics
import sys
import time
import uuid
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dateutil import parser as date_parser

from app.ai.confidence import REQUIRED_FIELDS, assess, routing_status
from app.core.errors.extraction import ExtractionStatus

DATASET = Path(__file__).resolve().parent / "dataset"
REPORTS = Path(__file__).resolve().parent / "reports"
THRESHOLD = 0.85
#: CI gate (routing mode): no corrupted extraction may be auto-accepted, and at least this
#: share of correct extractions must pass without review.
GATE_MAX_FALSE_ACCEPT = 0.0
GATE_MIN_CORRECT_ACCEPT = 0.90
#: Fields compared in live/replay mode (scalar fields of the schema; line items are excluded).
SCALAR_FIELDS = {
    "invoice": [
        "invoice_number",
        "vendor_name",
        "customer_name",
        "invoice_date",
        "due_date",
        "subtotal",
        "tax_amount",
        "total_amount",
        "currency",
    ],
    "receipt": ["store_name", "transaction_date", "subtotal", "tax", "total_amount", "payment_method"],
    "utility_bill": [
        "utility_company",
        "account_number",
        "service_address",
        "bill_date",
        "due_date",
        "amount_due",
        "consumption",
    ],
}


@dataclass
class Doc:
    doc_id: str
    document_type: str
    truth: dict[str, Any]
    text: str
    image: Path


def load_dataset() -> list[Doc]:
    docs = []
    for d in sorted(p for p in DATASET.iterdir() if p.is_dir()):
        t = json.loads((d / "truth.json").read_text(encoding="utf-8"))
        docs.append(
            Doc(
                d.name,
                t["document_type"],
                t["fields"],
                (d / "text.txt").read_text(encoding="utf-8"),
                d / "document.png",
            )
        )
    return docs


# --------------------------------------------------------------------------- field comparison


def _norm_str(v: Any) -> str:
    return " ".join(str(v).casefold().split())


def values_match(field_name: str, expected: Any, actual: Any) -> bool:
    """Numbers within 0.01, dates by calendar day, strings case/whitespace-insensitive."""
    if expected is None or actual is None:
        return expected is None and actual is None
    if isinstance(expected, (int, float)) and not isinstance(expected, bool):
        try:
            return abs(float(expected) - float(actual)) <= 0.01
        except (TypeError, ValueError):
            return False
    if field_name.endswith("_date") or field_name == "transaction_date":
        try:
            return date_parser.parse(str(actual)).date().isoformat() == str(expected)
        except (ValueError, OverflowError):
            return False
    return _norm_str(expected) == _norm_str(actual)


def wrong_required(doc_type: str, truth: dict[str, Any], output: dict[str, Any]) -> list[str]:
    return [f for f in REQUIRED_FIELDS[doc_type] if not values_match(f, truth.get(f), output.get(f))]


# --------------------------------------------------------------------------- routing mode


def corruptions(doc: Doc) -> dict[str, dict[str, Any]]:
    """Plausible model errors, each touching a required field."""
    t = doc.truth
    req = REQUIRED_FIELDS[doc.document_type]
    name_field = next(f for f in req if f.endswith("_name") or f in ("utility_company",))
    date_field = next(f for f in req if f.endswith("_date"))
    amount_field = next(f for f in req if f in ("total_amount", "amount_due"))
    out: dict[str, dict[str, Any]] = {}

    c = copy.deepcopy(t)
    c[name_field] = "Northwind Traders"
    out["hallucinated_name"] = c

    c = copy.deepcopy(t)
    c[amount_field] = round(t[amount_field] * 1.1 + 3, 2)
    out["wrong_amount"] = c

    c = copy.deepcopy(t)
    shifted = datetime.fromisoformat(t[date_field]) + (
        datetime.fromisoformat("2026-01-14") - datetime.fromisoformat("2026-01-01")
    )
    c[date_field] = shifted.date().isoformat()
    out["wrong_date"] = c

    c = copy.deepcopy(t)
    c[amount_field] = None
    out["missing_amount"] = c

    if doc.document_type == "invoice":
        c = copy.deepcopy(t)
        c["invoice_number"] = t["invoice_number"][:-1] + str((int(t["invoice_number"][-1]) + 1) % 10)
        out["off_by_one_id"] = c
    return out


@dataclass
class RoutingStats:
    correct_total: int = 0
    correct_accepted: int = 0
    corrupt_total: int = 0
    corrupt_accepted: int = 0
    by_kind: dict[str, list[int]] = field(default_factory=dict)  # kind -> [caught, total]
    misses: list[str] = field(default_factory=list)
    rejected_correct: list[dict[str, Any]] = field(default_factory=list)


def run_routing(docs: list[Doc]) -> dict[str, Any]:
    s = RoutingStats()
    for doc in docs:
        report = assess(doc.document_type, doc.truth, doc.text, 0.95, THRESHOLD)
        s.correct_total += 1
        if routing_status(report, THRESHOLD) == ExtractionStatus.COMPLETED:
            s.correct_accepted += 1
        else:
            s.rejected_correct.append(
                {
                    "doc": doc.doc_id,
                    "score": round(report.score, 3),
                    "ungrounded": report.required_ungrounded,
                    "missing": report.required_missing,
                    "failed_checks": [c.name for c in report.failed_checks],
                }
            )
        for kind, data in corruptions(doc).items():
            r = assess(doc.document_type, data, doc.text, 0.95, THRESHOLD)
            accepted = routing_status(r, THRESHOLD) == ExtractionStatus.COMPLETED
            s.corrupt_total += 1
            s.corrupt_accepted += accepted
            caught, total = s.by_kind.get(kind, [0, 0])
            s.by_kind[kind] = [caught + (not accepted), total + 1]
            if accepted:
                s.misses.append(f"{doc.doc_id}:{kind}")
    return {
        "mode": "routing",
        "documents": len(docs),
        "threshold": THRESHOLD,
        "false_accept_rate": s.corrupt_accepted / s.corrupt_total,
        "correct_auto_accept_rate": s.correct_accepted / s.correct_total,
        "corrupted_cases": s.corrupt_total,
        "catch_rate_by_corruption": {k: v[0] / v[1] for k, v in sorted(s.by_kind.items())},
        "false_accepts": s.misses,
        "correct_sent_to_review": s.rejected_correct,
    }


# --------------------------------------------------------------------------- live / replay


@dataclass
class DocResult:
    doc_id: str
    document_type: str
    status: str
    error_code: str | None = None
    field_hits: int = 0
    field_total: int = 0
    wrong_required: list[str] = field(default_factory=list)
    latency_s: float = 0.0
    cost_usd: float | None = None


def score_output(
    doc: Doc, output: dict[str, Any] | None, status: str, error_code: str | None, latency: float, cost: float | None
) -> DocResult:
    res = DocResult(doc.doc_id, doc.document_type, status, error_code, latency_s=latency, cost_usd=cost)
    if output is not None:
        for f in SCALAR_FIELDS[doc.document_type]:
            res.field_total += 1
            res.field_hits += values_match(f, doc.truth.get(f), output.get(f))
        res.wrong_required = wrong_required(doc.document_type, doc.truth, output)
    return res


def summarize(results: list[DocResult], mode: str, model: str | None) -> dict[str, Any]:
    n = len(results)
    ok = [r for r in results if r.status != "FAILED"]
    accepted = [r for r in results if r.status == "COMPLETED"]
    wrong = [r for r in ok if r.wrong_required]
    latencies = sorted(r.latency_s for r in results)
    costs = [r.cost_usd for r in results if r.cost_usd is not None]
    return {
        "mode": mode,
        "model": model,
        "documents": n,
        "failure_rate": (n - len(ok)) / n,
        "failures_by_code": _count(r.error_code or "?" for r in results if r.status == "FAILED"),
        "field_accuracy": sum(r.field_hits for r in ok) / max(1, sum(r.field_total for r in ok)),
        "documents_all_required_correct": sum(not r.wrong_required for r in ok) / max(1, len(ok)),
        "auto_accept_rate": len(accepted) / n,
        "review_rate": sum(r.status == "NEEDS_REVIEW" for r in results) / n,
        # Of the extractions with at least one wrong required field, how many were auto-accepted.
        "false_accept_rate": sum(bool(r.wrong_required) for r in accepted) / max(1, len(wrong)),
        "false_accepts": [f"{r.doc_id}:{','.join(r.wrong_required)}" for r in accepted if r.wrong_required],
        "latency_p50_s": statistics.median(latencies) if latencies else None,
        "latency_p95_s": latencies[int(0.95 * (n - 1))] if latencies else None,
        "cost_usd_total": round(sum(costs), 6) if costs else None,
        "per_document": [r.__dict__ for r in results],
    }


def _count(items: Any) -> dict[str, int]:
    out: dict[str, int] = {}
    for i in items:
        out[i] = out.get(i, 0) + 1
    return out


def _finish(
    doc: Doc, data: dict[str, Any] | None, ocr_text: str, ocr_conf: float | None
) -> tuple[dict[str, Any] | None, str]:
    from app.ai.exceptions import AIValidationException
    from app.ai.validator import AIValidator

    if data is None:
        return None, "FAILED"
    try:
        validated = AIValidator.validate(data, doc.document_type)
    except AIValidationException:
        return None, "FAILED"
    report = assess(doc.document_type, validated, ocr_text, ocr_conf, THRESHOLD)
    return validated, routing_status(report, THRESHOLD).value


def _save(record: Path, doc_id: str, rec: dict[str, Any]) -> None:
    record.mkdir(parents=True, exist_ok=True)
    (record / f"{doc_id}.json").write_text(json.dumps(rec, indent=2), encoding="utf-8")


def _has_model_output(record: Path | None, doc_id: str) -> bool:
    path = record / f"{doc_id}.json" if record else None
    return bool(path and path.exists() and "raw_text" in json.loads(path.read_text(encoding="utf-8")))


async def run_live(
    docs: list[Doc],
    record: Path | None,
    *,
    resume: bool = False,
    limit: int | None = None,
    delay: float = 0.0,
    provider: Any = None,
    pipeline: Any = None,
) -> dict[str, Any]:
    from app.ai.prompt_builder import PromptBuilder
    from app.core.errors.extraction import ErrorCode, ExtractionError

    if provider is None:
        from app.ai.providers.gemini import GeminiProvider

        provider = GeminiProvider()
    if pipeline is None:
        from app.ocr.pipeline import OCRPipeline
        from app.ocr.providers.tesseract import TesseractOCRProvider

        pipeline = OCRPipeline(ocr_provider=TesseractOCRProvider())
    if resume and record is None:
        raise ValueError("--resume needs --record")
    todo = [d for d in docs if not (resume and _has_model_output(record, d.doc_id))]
    if limit is not None:
        todo = todo[:limit]
    results = []
    for i, doc in enumerate(todo):
        if i and delay:
            await asyncio.sleep(delay)
        t0 = time.perf_counter()
        rec: dict[str, Any] = {"doc_id": doc.doc_id}
        try:
            content = await pipeline.process(
                document_id=uuid.uuid4(),
                file_content=await asyncio.to_thread(doc.image.read_bytes),
                file_extension=".png",
                mime_type="image/png",
            )
            rec["ocr_text"], rec["ocr_confidence"] = content.text, content.average_confidence
            boundary = PromptBuilder.new_boundary()
            out = await provider.generate_json(
                PromptBuilder.build_prompt(content.text, doc.document_type, boundary),
                PromptBuilder.get_json_schema(doc.document_type),
                PromptBuilder.build_system_instruction(doc.document_type, boundary),
            )
            rec["raw_text"] = out.raw_text
            cost = provider.calculate_cost(out.input_tokens, out.output_tokens)
            rec["latency_s"], rec["cost_usd"] = time.perf_counter() - t0, cost
            validated, status = _finish(doc, out.data, content.text, content.average_confidence)
            results.append(
                score_output(
                    doc, validated, status, None if validated else "INVALID_OUTPUT", time.perf_counter() - t0, cost
                )
            )
        except ExtractionError as exc:
            rec["error_code"] = exc.error_code
            results.append(score_output(doc, None, "FAILED", exc.error_code, time.perf_counter() - t0, None))
        if record:
            _save(record, doc.doc_id, rec)
        print(f"{doc.doc_id}: {results[-1].status} {results[-1].error_code or ''}", flush=True)
        if results[-1].error_code == ErrorCode.LLM_RATE_LIMITED.value:
            print("rate limited (quota): stopping; rerun later with --resume", flush=True)
            break
    if resume and record is not None:
        report = run_replay(docs, record)
        report.update(mode="live", model=provider.default_model)
        return report
    return summarize(results, "live", provider.default_model)


def run_replay(docs: list[Doc], recordings: Path) -> dict[str, Any]:
    results = []
    for doc in docs:
        path = recordings / f"{doc.doc_id}.json"
        if not path.exists():
            results.append(score_output(doc, None, "FAILED", "NOT_RECORDED", 0.0, None))
            continue
        rec = json.loads(path.read_text(encoding="utf-8"))
        if "raw_text" not in rec:
            results.append(score_output(doc, None, "FAILED", rec.get("error_code"), 0.0, None))
            continue
        latency, cost = float(rec.get("latency_s", 0.0)), rec.get("cost_usd")
        try:
            data = json.loads(rec["raw_text"])
        except json.JSONDecodeError:
            data = None
        validated, status = _finish(doc, data, rec["ocr_text"], rec.get("ocr_confidence"))
        results.append(score_output(doc, validated, status, None if validated else "INVALID_OUTPUT", latency, cost))
    return summarize(results, "replay", None)


# --------------------------------------------------------------------------- CLI


def gate_routing(report: dict[str, Any]) -> list[str]:
    problems = []
    if report["false_accept_rate"] > GATE_MAX_FALSE_ACCEPT:
        problems.append(f"false_accept_rate {report['false_accept_rate']:.3f} > {GATE_MAX_FALSE_ACCEPT}")
    if report["correct_auto_accept_rate"] < GATE_MIN_CORRECT_ACCEPT:
        problems.append(
            f"correct_auto_accept_rate {report['correct_auto_accept_rate']:.3f} < {GATE_MIN_CORRECT_ACCEPT}"
        )
    return problems


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["routing", "live", "replay"], default="routing")
    ap.add_argument("--gate", action="store_true", help="Exit 1 if the routing gate fails")
    ap.add_argument("--record", type=Path, help="live: write per-document recordings here")
    ap.add_argument("--recordings", type=Path, help="replay: read recordings from here")
    ap.add_argument("--out", type=Path, help="Write the JSON report here (default: evals/reports/<mode>-<date>.json)")
    ap.add_argument("--resume", action="store_true", help="live: skip documents already answered in --record")
    ap.add_argument("--limit", type=int, help="live: send at most this many model requests")
    ap.add_argument("--delay", type=float, default=0.0, help="live: seconds to wait between requests")
    args = ap.parse_args(argv)

    docs = load_dataset()
    runners: dict[str, Callable[[], dict[str, Any]]] = {
        "routing": lambda: run_routing(docs),
        "live": lambda: asyncio.run(
            run_live(docs, args.record, resume=args.resume, limit=args.limit, delay=args.delay)
        ),
        "replay": lambda: run_replay(docs, args.recordings),
    }
    if args.mode == "replay" and not args.recordings:
        ap.error("--recordings is required for replay")
    if args.resume and not args.record:
        ap.error("--resume needs --record")
    report = runners[args.mode]()
    report["generated_at"] = datetime.now(UTC).isoformat(timespec="seconds")

    out = args.out or REPORTS / f"{args.mode}-{datetime.now(UTC):%Y-%m-%d}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in report.items() if k not in ("per_document",)}, indent=2))
    print(f"report: {out}")

    if args.gate and args.mode == "routing":
        problems = gate_routing(report)
        for p in problems:
            print(f"GATE FAILED: {p}", file=sys.stderr)
        return 1 if problems else 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
