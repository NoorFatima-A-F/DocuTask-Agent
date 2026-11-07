"""Guard: app/ must not contain the fabricated-fallback code paths removed in remediation Phase 1.

If this fails, someone re-introduced a code path that returns invented data as if it
were a real extraction. Fakes belong in tests/fakes/ and are injected via dependency
overrides.
"""

from __future__ import annotations

from pathlib import Path

import pytest

APP_DIR = Path(__file__).resolve().parent.parent / "app"

FORBIDDEN = [
    "dev_placeholder_key",
    "_build_dev_mode_fallback",
    "Simulated text generation",
    "Extracted OCR text via",
    "No readable text content was found",
]

#: Scaffolding packages unreachable from app.main, scheduled for deletion in Phase 4.
#: Remove entries as they are deleted; the list must only shrink.
PENDING_DELETION: tuple[str, ...] = ()


def _app_sources() -> list[Path]:
    files = []
    for path in APP_DIR.rglob("*.py"):
        rel = path.relative_to(APP_DIR)
        if "__pycache__" in rel.parts or rel.parts[0] in PENDING_DELETION:
            continue
        files.append(path)
    return files


@pytest.mark.parametrize("needle", FORBIDDEN)
def test_no_fabricated_fallback_markers_in_app(needle: str) -> None:
    offenders = [
        str(p.relative_to(APP_DIR.parent)) for p in _app_sources() if needle in p.read_text("utf-8", errors="replace")
    ]
    assert offenders == [], f"{needle!r} found in: {offenders}"


def test_guard_scans_the_document_path() -> None:
    scanned = {p.relative_to(APP_DIR).as_posix() for p in _app_sources()}
    assert {"ai/providers/gemini.py", "ocr/providers/tesseract.py", "services/ai_extraction_service.py"} <= scanned
