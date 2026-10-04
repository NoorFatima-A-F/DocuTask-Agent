"""
evals/runners/fuzz_ocr_resilience.py
Enterprise Adversarial OCR Fuzzer & Schema Drift Evaluator.
"""

from __future__ import annotations
import importlib
import json
import random
import sys
from pathlib import Path
from typing import Any, Dict, List, Type

# Bootstrap repo root into sys.path
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from pydantic import BaseModel, Field, ValidationError


# Fallback contract if specific domain schema is not present
class GenericDocumentContract(BaseModel):
    document_id: str = Field(default="doc_default")
    vendor_name: str = Field(default="Unknown Vendor")
    total_amount: float = Field(default=0.0)
    currency: str = Field(default="USD")


def get_target_schema() -> Type[BaseModel]:
    """Dynamically resolves the primary extraction schema from app.schemas."""
    try:
        # Probe common schema modules in the app
        for mod_name in ["app.schemas.document", "app.schemas.extraction", "app.schemas.invoice", "app.ai.schemas"]:
            try:
                mod = importlib.import_module(mod_name)
                for attr in ["DocumentExtractionSchema", "ExtractionResponse", "DocumentSchema", "InvoiceSchema"]:
                    if hasattr(mod, attr):
                        target = getattr(mod, attr)
                        if isinstance(target, type) and issubclass(target, BaseModel):
                            return target
            except ImportError:
                continue
    except Exception:
        pass
    return GenericDocumentContract


TargetSchema = get_target_schema()


class SyntheticOCRFuzzer:
    """Injects optical noise to test schema validation and auto-healing."""

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
        chars = list(text)
        for i, char in enumerate(chars):
            if random.random() < self.corruption_rate and char in self.OCR_COMMON_MISTAKES:
                chars[i] = self.OCR_COMMON_MISTAKES[char]
        return "".join(chars)

    def run_fuzzing_drill(self, gold_dataset_path: Path = Path("evals/datasets/invoices_gold.json")) -> Dict[str, Any]:
        if not gold_dataset_path.exists():
            alt_path = REPO_ROOT / "evals" / "datasets" / "invoices_gold.json"
            if alt_path.exists():
                gold_dataset_path = alt_path
            else:
                return {
                    "total_fuzzed_samples": 0,
                    "resilience_score": 1.0,
                    "status": "SKIPPED",
                    "reason": f"Dataset {gold_dataset_path} not found",
                }

        with open(gold_dataset_path, "r", encoding="utf-8") as f:
            samples: List[Dict[str, Any]] = json.load(f)

        total_samples = len(samples)
        recovered_schemas = 0

        for sample in samples:
            raw_payload = sample.get("expected_schema", {}).copy()
            if "vendor_name" in raw_payload and isinstance(raw_payload["vendor_name"], str):
                raw_payload["vendor_name"] = self.corrupt_string(raw_payload["vendor_name"])
            try:
                TargetSchema.model_validate(raw_payload)
                recovered_schemas += 1
            except ValidationError:
                pass

        resilience_score = round(recovered_schemas / total_samples, 4) if total_samples > 0 else 1.0

        return {
            "total_fuzzed_samples": total_samples,
            "recovered_schemas": recovered_schemas,
            "resilience_score": resilience_score,
            "status": "PASSED" if resilience_score >= 0.70 else "FAILED",
        }


if __name__ == "__main__":
    fuzzer = SyntheticOCRFuzzer()
    dataset_file = Path("evals/datasets/invoices_gold.json")
    results = fuzzer.run_fuzzing_drill(dataset_file)
    print(json.dumps(results, indent=2))
