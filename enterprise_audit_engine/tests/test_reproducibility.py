"""Tests for Deterministic Audit Reproducibility Engine."""

import asyncio
from enterprise_audit_engine.certification.reproducibility import AuditReproducibilityVerifier


def test_reproducibility_verifier(tmp_path):
    """Verifies that twin audit runs produce identical deterministic classifications."""
    # Create minimal repository structure
    repo_dir = tmp_path / "repo"
    repo_dir.mkdir()
    (repo_dir / "app").mkdir()
    (repo_dir / "app" / "main.py").write_text("# Main app\nimport os\n", encoding="utf-8")
    (repo_dir / "pyproject.toml").write_text("[project]\nname='test'\n", encoding="utf-8")

    temp_base = tmp_path / "runs"
    temp_base.mkdir()

    result = asyncio.run(AuditReproducibilityVerifier.verify_reproducibility(
        repo_root=repo_dir,
        temp_base_dir=temp_base,
    ))

    assert result["is_deterministic"] is True
    assert result["status"] == "DETERMINISTIC_REPRODUCIBLE"
    assert result["differences_count"] == 0
    assert result["run_a"]["merkle_root"] == result["run_b"]["merkle_root"]
