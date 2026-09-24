"""Tests for Audit Engine Self-Integrity & Environment Verification."""

import pytest
from enterprise_audit_engine.assurance.self_integrity import (
    SelfIntegrityVerifier,
    EngineIntegrityFingerprint,
)
from enterprise_audit_engine.assurance.environment import (
    CertificationExecutionEnvironment,
    EnvironmentCollector,
)
from enterprise_audit_engine.assurance.rule_validator import (
    IndependentRuleValidator,
    RuleValidationResult,
)


@pytest.fixture
def temp_repo(tmp_path):
    repo = tmp_path / "test_repo"
    repo.mkdir()
    engine_dir = repo / "enterprise_audit_engine"
    engine_dir.mkdir()
    (engine_dir / "__init__.py").write_text("# init", encoding="utf-8")
    (engine_dir / "core.py").write_text("class Core: pass", encoding="utf-8")
    return repo


def test_self_integrity_verifier_initialization(temp_repo):
    verifier = SelfIntegrityVerifier(temp_repo)
    assert verifier.repo_root == temp_repo
    assert verifier.engine_dir == temp_repo / "enterprise_audit_engine"


def test_compute_fingerprint_structure(temp_repo):
    verifier = SelfIntegrityVerifier(temp_repo)
    fp = verifier.compute_fingerprint()
    assert isinstance(fp, EngineIntegrityFingerprint)
    assert len(fp.overall_engine_hash) == 64
    assert len(fp.source_code_hash) == 64
    assert fp.total_engine_files >= 2


def test_fingerprint_deterministic_recomputation(temp_repo):
    verifier = SelfIntegrityVerifier(temp_repo)
    fp1 = verifier.compute_fingerprint()
    fp2 = verifier.compute_fingerprint()
    assert fp1.overall_engine_hash == fp2.overall_engine_hash
    assert fp1.source_code_hash == fp2.source_code_hash


def test_fingerprint_detects_source_modification(temp_repo):
    verifier = SelfIntegrityVerifier(temp_repo)
    fp_before = verifier.compute_fingerprint()

    # Modify a file
    (temp_repo / "enterprise_audit_engine" / "core.py").write_text("class ModifiedCore: pass", encoding="utf-8")
    fp_after = verifier.compute_fingerprint()

    assert fp_before.overall_engine_hash != fp_after.overall_engine_hash
    assert fp_before.source_code_hash != fp_after.source_code_hash


def test_fingerprint_detects_file_addition(temp_repo):
    verifier = SelfIntegrityVerifier(temp_repo)
    fp_before = verifier.compute_fingerprint()

    # Add new python file
    (temp_repo / "enterprise_audit_engine" / "extra.py").write_text("SECRET = 123", encoding="utf-8")
    fp_after = verifier.compute_fingerprint()

    assert fp_before.overall_engine_hash != fp_after.overall_engine_hash
    assert fp_after.total_engine_files == fp_before.total_engine_files + 1


def test_fingerprint_detects_file_deletion(temp_repo):
    (temp_repo / "enterprise_audit_engine" / "to_delete.py").write_text("pass", encoding="utf-8")
    verifier = SelfIntegrityVerifier(temp_repo)
    fp_before = verifier.compute_fingerprint()

    (temp_repo / "enterprise_audit_engine" / "to_delete.py").unlink()
    fp_after = verifier.compute_fingerprint()

    assert fp_before.overall_engine_hash != fp_after.overall_engine_hash
    assert fp_after.total_engine_files == fp_before.total_engine_files - 1


def test_environment_telemetry_collection(temp_repo):
    collector = EnvironmentCollector(temp_repo)
    env = collector.capture_environment()
    assert isinstance(env, CertificationExecutionEnvironment)
    assert env.python_version != ""
    assert env.os_platform != ""
    assert len(env.environment_hash) == 64


def test_environment_isolation_properties(temp_repo):
    collector = EnvironmentCollector(temp_repo)
    env = collector.capture_environment()
    dump = env.model_dump()
    assert "cpu_architecture" in dump
    assert "hostname" in dump
    assert "execution_timestamp" in dump


def test_independent_rule_validator_invariants():
    validator = IndependentRuleValidator()
    res = validator.validate_all_invariants()
    assert isinstance(res, RuleValidationResult)
    assert res.is_valid is True
    assert res.rules_checked_count > 0
    assert len(res.violations) == 0


def test_rule_validator_monotonicity():
    validator = IndependentRuleValidator()
    # Higher quality score should not downgrade tier
    assert validator.verify_monotonic_tier(score_low=75.0, tier_low="COMMERCIAL", score_high=95.0, tier_high="ENTERPRISE") is True
    assert validator.verify_monotonic_tier(score_low=95.0, tier_low="ENTERPRISE", score_high=60.0, tier_high="COMMERCIAL") is True


def test_rule_validator_tamper_detection():
    validator = IndependentRuleValidator()
    # Invariant failure if 0 score yields ENTERPRISE
    assert validator.verify_tier_boundary(score=0.0, assigned_tier="ENTERPRISE") is False
    assert validator.verify_tier_boundary(score=100.0, assigned_tier="ENTERPRISE") is True
