"""
Unit and Integration Test Suite for Repository Topology, Metadata, and Architecture Governance.
"""
import pytest
import json
from pathlib import Path
from datetime import datetime, timezone

from tooling.governance.repository_validator import RepositoryTopologyValidator
from app.shared_kernel import (
    Ok, Err,
    VerificationRunId, DatasetId, EvidenceId, CertificateId,
    DeterministicTimeProvider,
    CorrelationContext, get_current_correlation, set_current_correlation,
    PlatformVerificationError, InvariantViolationError
)
from app.infrastructure.storage.cas_store import ContentAddressableStore
from app.infrastructure.telemetry.otel_adapter import TelemetryAdapter
from app.interfaces import run_verification_cli, PlatformVerificationApiRouter


def test_repository_topology_validation():
    repo_root = Path(__file__).resolve().parent.parent.parent
    validator = RepositoryTopologyValidator(repo_root)
    success, errors, warnings = validator.run_all()
    assert success is True, f"Topology validation errors: {errors}"
    assert len(errors) == 0


def test_repository_metadata_file():
    repo_root = Path(__file__).resolve().parent.parent.parent
    meta_path = repo_root / "repo_metadata.json"
    assert meta_path.exists()
    data = json.loads(meta_path.read_text(encoding="utf-8"))
    assert data["platform_name"] == "DocuTask Agent Enterprise Verification Platform"
    assert len(data["bounded_contexts"]) >= 4
    assert len(data["topology_roots"]) >= 10


def test_shared_kernel_result_monad():
    # Test Ok
    ok_res = Ok("verification_passed")
    assert ok_res.is_ok is True
    assert ok_res.is_err is False
    assert ok_res.unwrap() == "verification_passed"
    assert ok_res.map(lambda s: len(s)).unwrap() == len("verification_passed")

    # Test Err
    err_res = Err("failed_gate")
    assert err_res.is_ok is False
    assert err_res.is_err is True
    assert err_res.unwrap_or("fallback") == "fallback"
    with pytest.raises(ValueError):
        err_res.unwrap()


def test_shared_kernel_typed_ids():
    run_id = VerificationRunId.generate()
    assert str(run_id).startswith("vrun_")
    
    ds_id = DatasetId.generate()
    assert str(ds_id).startswith("ds_")

    ev_id = EvidenceId.generate()
    assert str(ev_id).startswith("ev_")

    cert_id = CertificateId.generate()
    assert str(cert_id).startswith("cert_")


def test_shared_kernel_deterministic_time():
    fixed = datetime(2026, 9, 14, 12, 0, 0, tzinfo=timezone.utc)
    provider = DeterministicTimeProvider(fixed)
    assert provider.now() == fixed
    provider.advance_seconds(60.0)
    assert provider.now().minute == 1


def test_shared_kernel_correlation_context():
    ctx = CorrelationContext(tenant_id="tenant-acme", originator="ci_runner")
    set_current_correlation(ctx)
    try:
        active = get_current_correlation()
        assert active.tenant_id == "tenant-acme"
        assert active.originator == "ci_runner"
        assert active.correlation_id.startswith("corr_")
    finally:
        # cleanup
        pass


def test_shared_kernel_error_hierarchy():
    err = InvariantViolationError("Accuracy dropped below 0.95", details={"actual": 0.92})
    assert isinstance(err, PlatformVerificationError)
    assert err.error_code == "ERR_INVARIANT_VIOLATION"
    assert err.details["actual"] == 0.92


def test_infrastructure_cas_storage_adapter():
    cas = ContentAddressableStore()
    payload = b"Verification evidence log bytes"
    h = cas.put(payload)
    assert len(h) == 64
    assert cas.exists(h) is True
    assert cas.get(h) == payload


def test_infrastructure_telemetry_adapter():
    otel = TelemetryAdapter(service_name="verification-runner")
    otel.record_counter("verification_runs_total", 1.0)
    otel.record_gauge("system_memory_mb", 4096.0)
    metrics = otel.get_metrics()
    assert metrics["verification_runs_total"] == 1.0
    assert metrics["system_memory_mb"] == 4096.0


def test_interfaces_cli_and_api():
    cli_res = run_verification_cli("def_ocr_01", "staging")
    assert cli_res["status"] == "CLI_DISPATCHED"
    assert cli_res["definition_id"] == "def_ocr_01"

    router = PlatformVerificationApiRouter()
    status = router.get_status()
    assert status["status"] == "HEALTHY"
