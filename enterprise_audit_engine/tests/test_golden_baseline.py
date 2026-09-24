"""Tests for Golden Baseline Manager & Invariant Verification."""

import pytest
from enterprise_audit_engine.baseline.baseline_manager import GoldenBaselineManager
from enterprise_audit_engine.baseline.baseline_manifest import GoldenBaselineManifest


@pytest.fixture
def baseline_setup(tmp_path):
    base_dir = tmp_path / "baselines"
    engine_mock = tmp_path / "mock_engine"
    engine_mock.mkdir(parents=True)
    (engine_mock / "__init__.py").write_text("# mock", encoding="utf-8")
    (engine_mock / "policy.py").write_text("POL = 1", encoding="utf-8")

    mgr = GoldenBaselineManager(base_dir)
    return mgr, engine_mock, base_dir


def test_create_and_load_golden_baseline(baseline_setup):
    mgr, engine_mock, base_dir = baseline_setup
    manifest = mgr.create_baseline("1.0.0", engine_mock)

    assert isinstance(manifest, GoldenBaselineManifest)
    assert manifest.baseline_version == "1.0.0"
    assert len(manifest.file_hashes) >= 2
    assert len(manifest.policies) > 0

    loaded = mgr.load_baseline("1.0.0")
    assert loaded is not None
    assert loaded.baseline_version == "1.0.0"
    assert loaded.engine_source_hash == manifest.engine_source_hash


def test_compare_identical_engine(baseline_setup):
    mgr, engine_mock, base_dir = baseline_setup
    mgr.create_baseline("1.0.0", engine_mock)

    res = mgr.compare_against_baseline("1.0.0", engine_mock)
    assert res["matched"] is True
    assert res["status"] == "BASELINE_VERIFIED"
    assert res["modified_files_count"] == 0
    assert res["removed_files_count"] == 0


def test_compare_detects_tampered_file(baseline_setup):
    mgr, engine_mock, base_dir = baseline_setup
    mgr.create_baseline("1.0.0", engine_mock)

    # Tamper with policy.py
    (engine_mock / "policy.py").write_text("POL = 99999", encoding="utf-8")

    res = mgr.compare_against_baseline("1.0.0", engine_mock)
    assert res["matched"] is False
    assert res["status"] == "BASELINE_DISCREPANCIES_FOUND"
    assert res["modified_files_count"] == 1
    assert "policy.py" in res["modified_files"]


def test_compare_detects_removed_file(baseline_setup):
    mgr, engine_mock, base_dir = baseline_setup
    mgr.create_baseline("1.0.0", engine_mock)

    (engine_mock / "policy.py").unlink()

    res = mgr.compare_against_baseline("1.0.0", engine_mock)
    assert res["matched"] is False
    assert res["removed_files_count"] == 1
    assert "policy.py" in res["removed_files"]


def test_compare_detects_added_file(baseline_setup):
    mgr, engine_mock, base_dir = baseline_setup
    mgr.create_baseline("1.0.0", engine_mock)

    (engine_mock / "backdoor.py").write_text("evil()", encoding="utf-8")

    res = mgr.compare_against_baseline("1.0.0", engine_mock)
    assert res["added_files_count"] == 1
    assert "backdoor.py" in res["added_files"]


def test_missing_baseline_handling(baseline_setup):
    mgr, engine_mock, base_dir = baseline_setup
    res = mgr.compare_against_baseline("9.9.9", engine_mock)
    assert res["matched"] is False
    assert "not found" in res["error"]
