"""Audit Reproducibility Challenge Engine."""

import tempfile
from pathlib import Path
from typing import Dict, Any
from enterprise_audit_engine.certification.reproducibility import AuditReproducibilityVerifier


class ReproducibilityChallenge:
    """Executes multi-environment reproducibility challenges to ensure identical results across execution sandboxes."""

    @classmethod
    async def run_challenge(cls, repo_root: Path) -> Dict[str, Any]:
        with tempfile.TemporaryDirectory() as temp_dir:
            base_p = Path(temp_dir)
            result = await AuditReproducibilityVerifier.verify_reproducibility(
                repo_root=repo_root,
                temp_base_dir=base_p,
            )

        is_passed = result.get("is_deterministic", False)
        return {
            "challenge_status": "CHALLENGE_PASSED" if is_passed else "CHALLENGE_FAILED",
            "is_deterministic": is_passed,
            "merkle_root_a": result["run_a"]["merkle_root"],
            "merkle_root_b": result["run_b"]["merkle_root"],
            "total_evidence_a": result["run_a"]["total_evidence"],
            "total_evidence_b": result["run_b"]["total_evidence"],
            "discrepancies": result.get("differences", []),
        }
