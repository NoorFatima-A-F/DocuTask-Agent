"""Deterministic Audit Reproducibility Engine."""

import asyncio
import json
import shutil
import tempfile
from pathlib import Path
from typing import Dict, Any, List, Tuple
from enterprise_audit_engine.orchestration.audit_runner import AuditRunner
from enterprise_audit_engine.certification.merkle_tree import MerkleEvidenceTree


class AuditReproducibilityVerifier:
    """Verifies that executing independent audit runs on the same codebase produces deterministic proof."""

    @classmethod
    async def verify_reproducibility(cls, repo_root: Path, temp_base_dir: Path) -> Dict[str, Any]:
        dir_a = temp_base_dir / "run_a"
        dir_b = temp_base_dir / "run_b"
        dir_a.mkdir(parents=True, exist_ok=True)
        dir_b.mkdir(parents=True, exist_ok=True)

        runner_a = AuditRunner(repo_root=repo_root, output_dir=dir_a)
        runner_b = AuditRunner(repo_root=repo_root, output_dir=dir_b)

        result_a = await runner_a.run_full_audit()
        result_b = await runner_b.run_full_audit()

        records_a = runner_a.store.load_all_evidence()
        records_b = runner_b.store.load_all_evidence()

        differences: List[str] = []

        # 1. Compare counts
        if len(records_a) != len(records_b):
            differences.append(f"Evidence count mismatch: Run A ({len(records_a)}) vs Run B ({len(records_b)})")

        # 2. Compare classifications per category
        map_a = {r.category: r.classification.value for r in records_a}
        map_b = {r.category: r.classification.value for r in records_b}

        for cat, class_a in map_a.items():
            if cat not in map_b:
                differences.append(f"Category '{cat}' missing from Run B")
            elif map_b[cat] != class_a:
                differences.append(f"Classification mismatch for '{cat}': Run A={class_a} vs Run B={map_b[cat]}")

        # 3. Compare collector health statuses
        cols_a = {c["collector_name"]: c["execution_completed"] for c in result_a["collector_manifest"]["collectors"]}
        cols_b = {c["collector_name"]: c["execution_completed"] for c in result_b["collector_manifest"]["collectors"]}
        if cols_a != cols_b:
            differences.append(f"Collector execution status mismatch: Run A={cols_a} vs Run B={cols_b}")

        # 4. Compare overall classification and confidence
        if result_a["overall_classification"] != result_b["overall_classification"]:
            differences.append(f"Overall classification mismatch: Run A={result_a['overall_classification']} vs Run B={result_b['overall_classification']}")

        if result_a["overall_confidence"] != result_b["overall_confidence"]:
            differences.append(f"Overall confidence mismatch: Run A={result_a['overall_confidence']} vs Run B={result_b['overall_confidence']}")

        is_deterministic = len(differences) == 0

        # Build Merkle roots
        merkle_a = MerkleEvidenceTree(records_a).merkle_root
        merkle_b = MerkleEvidenceTree(records_b).merkle_root

        return {
            "is_deterministic": is_deterministic,
            "status": "DETERMINISTIC_REPRODUCIBLE" if is_deterministic else "NON_DETERMINISTIC_AUDIT_BEHAVIOR",
            "differences_count": len(differences),
            "differences": differences,
            "run_a": {
                "run_id": result_a["run_id"],
                "total_evidence": result_a["total_evidence"],
                "classification": result_a["overall_classification"],
                "merkle_root": merkle_a,
            },
            "run_b": {
                "run_id": result_b["run_id"],
                "total_evidence": result_b["total_evidence"],
                "classification": result_b["overall_classification"],
                "merkle_root": merkle_b,
            },
        }
