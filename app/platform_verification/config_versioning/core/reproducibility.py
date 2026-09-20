"""
Deterministic Reproducibility Engine.
Captures full execution snapshots and verifies exact replay fidelity.
"""
from dataclasses import dataclass
from typing import Any, Dict, Optional, Tuple
from app.platform_verification.config_versioning.domain.models import (
    ExecutionSnapshot, EnvironmentTier, ConfigurationSnapshot
)
from app.platform_verification.config_versioning.core.snapshot_manager import snapshot_manager
from app.platform_verification.config_versioning.core.fingerprint import environment_fingerprinter


@dataclass
class ReproducibilityFidelityReport:
    is_exact_match: bool
    fidelity_score: float
    matched_vectors: Dict[str, bool]
    discrepancies: Dict[str, Any]


class ReproducibilityEngine:
    def __init__(self):
        self._execution_snapshots: Dict[str, ExecutionSnapshot] = {}

    def capture_execution_snapshot(
        self,
        verification_id: str,
        code_commit_sha: str,
        configuration_snapshot_id: str,
        configuration_hash: str,
        dataset_id: str,
        dataset_version: str,
        dataset_hash: str,
        model_identifier: str,
        model_version: str,
        prompt_template_id: str,
        prompt_version: str,
        prompt_hash: str,
        dependency_lock_hash: str,
        sbom_manifest_id: str,
        environment_tier: EnvironmentTier,
        infrastructure_version: str,
        feature_flags_state: Optional[Dict[str, bool]] = None
    ) -> ExecutionSnapshot:
        fp = environment_fingerprinter.capture_fingerprint(tier=environment_tier)
        snap = ExecutionSnapshot(
            verification_id=verification_id,
            code_commit_sha=code_commit_sha,
            configuration_snapshot_id=configuration_snapshot_id,
            configuration_hash=configuration_hash,
            dataset_id=dataset_id,
            dataset_version=dataset_version,
            dataset_hash=dataset_hash,
            model_identifier=model_identifier,
            model_version=model_version,
            prompt_template_id=prompt_template_id,
            prompt_version=prompt_version,
            prompt_hash=prompt_hash,
            dependency_lock_hash=dependency_lock_hash,
            sbom_manifest_id=sbom_manifest_id,
            environment_tier=environment_tier,
            environment_fingerprint_id=fp.fingerprint_id,
            infrastructure_version=infrastructure_version,
            feature_flags_state=feature_flags_state or {}
        )
        self._execution_snapshots[verification_id] = snap
        return snap

    def get_execution_snapshot(self, verification_id: str) -> Optional[ExecutionSnapshot]:
        return self._execution_snapshots.get(verification_id)

    def verify_reproducibility_fidelity(
        self,
        baseline: ExecutionSnapshot,
        candidate: ExecutionSnapshot
    ) -> ReproducibilityFidelityReport:
        vectors = {
            "code_commit": baseline.code_commit_sha == candidate.code_commit_sha,
            "configuration": baseline.configuration_hash == candidate.configuration_hash,
            "dataset": baseline.dataset_hash == candidate.dataset_hash,
            "model": (baseline.model_identifier, baseline.model_version) == (candidate.model_identifier, candidate.model_version),
            "prompt": baseline.prompt_hash == candidate.prompt_hash,
            "dependencies": baseline.dependency_lock_hash == candidate.dependency_lock_hash,
            "environment_tier": baseline.environment_tier == candidate.environment_tier,
            "infrastructure": baseline.infrastructure_version == candidate.infrastructure_version,
        }
        passed = sum(1 for v in vectors.values() if v)
        total = len(vectors)
        score = float(passed) / float(total)
        is_exact = score == 1.0

        discrepancies = {}
        for k, v in vectors.items():
            if not v:
                discrepancies[k] = {
                    "baseline": getattr(baseline, k, None) or getattr(baseline, f"{k}_hash", None),
                    "candidate": getattr(candidate, k, None) or getattr(candidate, f"{k}_hash", None)
                }

        return ReproducibilityFidelityReport(
            is_exact_match=is_exact,
            fidelity_score=score,
            matched_vectors=vectors,
            discrepancies=discrepancies
        )


reproducibility_engine = ReproducibilityEngine()
