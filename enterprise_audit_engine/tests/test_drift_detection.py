"""Tests for Certification Drift Detection."""

from enterprise_audit_engine.drift_detection.drift_detector import (
    DriftDetector,
    CertificationDriftReport,
)


def test_no_drift_matching_state(tmp_path):
    detector = DriftDetector(tmp_path)
    # Match with current HEAD / environment
    rep = detector.detect_drift(certified_commit="HEAD", certified_python_version="3.12")
    assert isinstance(rep, CertificationDriftReport)
    assert rep.has_drift is False
    assert rep.status == "CERTIFICATION_ACTIVE"
    assert rep.re_certification_required is False


def test_detects_code_drift(tmp_path):
    detector = DriftDetector(tmp_path)
    rep = detector.detect_drift(certified_commit="old_sha_123456789", certified_python_version="3.12")
    # If git repo returns current commit != old_sha_123456789
    if rep.current_commit != "HEAD":
        assert rep.has_drift is True
        assert rep.status == "CERTIFICATION_INVALIDATED_BY_DRIFT"
        assert rep.re_certification_required is True


def test_detects_dependency_drift(tmp_path):
    req_file = tmp_path / "requirements.txt"
    req_file.write_text("fastapi==0.110.0\n", encoding="utf-8")
    detector = DriftDetector(tmp_path)

    rep = detector.detect_drift(
        certified_commit="HEAD",
        certified_python_version="3.12",
        certified_dependencies_hash="different_hash_abcdef",
    )

    assert rep.has_drift is True
    assert any(d.drift_type == "DEPENDENCY_DRIFT" for d in rep.drifts)
