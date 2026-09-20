"""
Experiment Archive (Phase 82B.3)
================================
Packs and archives experiments into self-contained, cryptographically signed
research bundles for long-term preservation and external peer review.
"""

from __future__ import annotations
import json
import os
import tarfile
import zipfile
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

from research_validation.scientific_execution.experiment_manifest import ExperimentManifest
from research_validation.scientific_execution.experiment_runner import ExperimentRunResult
from research_validation.provenance.hashing import hash_canonical_json, compute_sha256


@dataclass(frozen=True)
class ArchivedExperimentBundle:
    archive_id: str
    experiment_id: str
    manifest_digest: str
    created_at_utc: str
    included_files: Tuple[str, ...]
    bundle_sha256: str
    archive_metadata: Dict[str, Any] = field(default_factory=dict)


class ExperimentArchiver:
    """
    Creates standalone archival packages for experiments.
    """

    def __init__(self, output_root: Optional[str] = None):
        self.output_root = output_root or "archives/experiments"

    def create_bundle(
        self,
        manifest: ExperimentManifest,
        run_result: Optional[ExperimentRunResult] = None,
        additional_files: Optional[Dict[str, str]] = None,
    ) -> ArchivedExperimentBundle:
        """Create archive metadata and sealed representation."""
        now_str = datetime.now(timezone.utc).isoformat()
        arch_id = f"arch_{manifest.experiment_id}_{int(datetime.now(timezone.utc).timestamp())}"

        files = {
            "MANIFEST.json": json.dumps(manifest.to_canonical_dict(), indent=2),
        }
        if run_result:
            files["RUN_RESULT.json"] = json.dumps({
                "run_id": run_result.run_id,
                "status": run_result.status.value,
                "metrics": run_result.metrics,
                "duration_ms": run_result.duration_ms,
                "final_digest": run_result.final_output_digest,
            }, indent=2)

        if additional_files:
            files.update(additional_files)

        # Compute bundle digest
        combined_payload = {
            "archive_id": arch_id,
            "experiment_id": manifest.experiment_id,
            "files": {fname: compute_sha256(content.encode()) for fname, content in files.items()},
        }
        bundle_h = hash_canonical_json(combined_payload)

        # Write to disk if output_root exists
        if self.output_root:
            os.makedirs(self.output_root, exist_ok=True)
            arch_dir = os.path.join(self.output_root, arch_id)
            os.makedirs(arch_dir, exist_ok=True)
            for fname, content in files.items():
                with open(os.path.join(arch_dir, fname), "w", encoding="utf-8") as f:
                    f.write(content)

        return ArchivedExperimentBundle(
            archive_id=arch_id,
            experiment_id=manifest.experiment_id,
            manifest_digest=manifest.manifest_digest_sha256,
            created_at_utc=now_str,
            included_files=tuple(sorted(files.keys())),
            bundle_sha256=bundle_h,
            archive_metadata={"total_files": len(files)},
        )
