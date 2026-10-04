"""
evals/runners/fuzz_ocr_resilience.py
Synthetic Adversarial Fuzzer: Tests Pydantic V2 schema resilience against noisy OCR text.
"""

from __future__ import annotations
import json
import os
import random
import sys
from pathlib import Path
from typing import Any, Dict, List

# Ensure repo root is in sys.path for standalone invocations
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from pydantic import ValidationError
from app.schemas.document import DocumentExtractionSchema

# Dynamic path resolution
EVALS_DIR = Path(__file__).resolve().parent.parent
DEFAULT_GOLD_DATASET = EVALS_DIR / "datasets" / "invoices_gold.json"


class SyntheticOCRFuzzer:
    """Injects real-world optical character recognition noise into structured payloads."""

    OCR_COMMON_MISTAKES: Dict[str, str] = {
        "O": "0",
        "0": "O",
        "I": "1",
        "1": "I",
        "l": "1",
        "S": "5",
        "5": "S",
        "B": "8",
        "8": "B",
    }

    def __init__(self, corruption_rate: float = 0.08):
        self.corruption_rate = corruption_rate

    def corrupt_string(self, text: str) -> str:
        """Randomly swaps visually similar characters based on common OCR drift."""
        chars = list(text)
        for i, char in enumerate(chars):
            if random.random() < self.corruption_rate and char in self.OCR_COMMON_MISTAKES:
                chars[i] = self.OCR_COMMON_MISTAKES[char]
        return "".join(chars)

    def run_fuzzing_drill(self, gold_dataset_path: Path = DEFAULT_GOLD_DATASET) -> Dict[str, Any]:
        """Executes synthetic adversarial OCR corruption and tests Pydantic schema validation."""
        if not gold_dataset_path.exists():
            fallback_path = Path("evals/datasets/invoices_gold.json")
            if fallback_path.exists():
                gold_dataset_path = fallback_path
            else:
                return {
                    "total_fuzzed_samples": 0,
                    "resilience_score": 0.0,
                    "status": "SKIPPED",
                    "reason": "Gold dataset not found",
                }

        with open(gold_dataset_path, "r", encoding="utf-8") as f:
            samples: List[Dict[str, Any]] = json.load(f)

        total_samples = len(samples)
        recovered_schemas = 0

        for sample in samples:
            raw_payload = sample.get("expected_schema", {}).copy()

            # Inject OCR corruption into text fields
            if "vendor_name" in raw_payload:
                raw_payload["vendor_name"] = self.corrupt_string(raw_payload["vendor_name"])
            if "invoice_number" in raw_payload:
                raw_payload["invoice_number"] = self.corrupt_string(raw_payload["invoice_number"])

            # Test schema validation and autonomous healing
            try:
                DocumentExtractionSchema.model_validate(raw_payload)
                recovered_schemas += 1
            except ValidationError:
                # Attempt simulated autonomous repair trigger
                cleaned_payload = {
                    k: DocumentExtractionSchema.clean_ocr_text(v)
                    for k, v in raw_payload.items()
                }
                try:
                    DocumentExtractionSchema.model_validate(cleaned_payload)
                    recovered_schemas += 1
                except ValidationError:
                    pass

        resilience_score = round(recovered_schemas / total_samples, 4) if total_samples > 0 else 1.0

        return {
            "total_fuzzed_samples": total_samples,
            "recovered_schemas": recovered_schemas,
            "resilience_score": resilience_score,
            "corruption_rate": self.corruption_rate,
            "status": "PASSED" if resilience_score >= 0.80 else "FAILED",
        }


if __name__ == "__main__":
    fuzzer = SyntheticOCRFuzzer(corruption_rate=0.08)
    results = fuzzer.run_fuzzing_drill()
    print(json.dumps(results, indent=2))
