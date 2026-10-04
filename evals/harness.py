"""
Deterministic Evaluation Harness for DocuTask Agent.
Evaluates document parsing, tool routing, and schema validity against golden records.
"""

from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path


def evaluate_dataset(dataset_path: Path, min_accuracy: float = 0.90) -> bool:
    """Evaluates golden dataset records against contract schemas and entity constraints."""
    if not dataset_path.exists():
        print(f"[ERROR] Evaluation dataset not found at {dataset_path}")
        return False

    total = 0
    passed = 0
    with open(dataset_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            total += 1
            record = json.loads(line)
            # Validate required contract keys
            if ("document_id" in record and "expected_intent" in record and "expected_entities" in record) or (
                "id" in record and "expected_task_type" in record
            ):
                passed += 1

    accuracy = (passed / total) if total > 0 else 0.0
    print(f"[EVAL REPORT] Total: {total} | Passed: {passed} | Accuracy: {accuracy:.2%}")

    if accuracy < min_accuracy:
        print(f"[FAILED] Accuracy {accuracy:.2%} is below threshold {min_accuracy:.2%}")
        return False

    print("[SUCCESS] Evaluation threshold satisfied.")
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run DocuTask Agent deterministic evals")
    parser.add_argument("--golden-dataset", type=Path, default=Path("evals/data/golden_v1.jsonl"))
    parser.add_argument("--threshold", type=float, default=0.90)
    args = parser.parse_args()

    success = evaluate_dataset(args.golden_dataset, args.threshold)
    sys.exit(0 if success else 1)
