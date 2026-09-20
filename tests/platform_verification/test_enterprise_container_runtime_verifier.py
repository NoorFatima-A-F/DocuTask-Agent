"""
Comprehensive Test Suite for Part 3A: Enterprise Container & Runtime Verification Framework.
"""
import pytest
from app.platform_verification.container_verification.cli import ContainerVerificationPlatform
from app.platform_verification.container_verification.models.verification_models import (
    ContainerCertificationTier,
    ServiceDefinition,
    ContainerArchitectureModel,
    VulnerabilitySeverity,
)


@pytest.fixture
def container_platform():
    return ContainerVerificationPlatform()


def test_dockerfile_quality_analyzer(container_platform):
    """Verifies base image pinning, non-root user enforcement, and dev dependency filtering."""
    analyzer = container_platform.dockerfile_analyzer

    good_df = """
    FROM python:3.12-slim as builder
    WORKDIR /build
    RUN pip install --no-cache-dir requests
    FROM python:3.12-slim
    USER appuser
    WORKDIR /app
    COPY . /app
    CMD ["uvicorn", "app.main:app"]
    """
    good_rep = analyzer.analyze_dockerfile_content(good_df)
    assert good_rep.status == "PASS"
    assert good_rep.base_image_pinned
    assert good_rep.runs_as_non_root
    assert good_rep.multi_stage_build

    bad_df = """
    FROM python:latest
    USER root
    RUN pip install pytest black jupyter
    """
    bad_rep = analyzer.analyze_dockerfile_content(bad_df)
    assert bad_rep.status == "FAIL"
    assert not bad_rep.base_image_pinned
    assert not bad_rep.runs_as_non_root
    assert len(bad_rep.dev_dependencies_found) == 3


def test_container_boundary_and_isolation_validator(container_platform):
    """Evaluates single-responsibility containers and detects god containers & shared mutable volumes."""
    validator = container_platform.isolation_validator

    clean_services = {
        "api": ServiceDefinition(name="api", image="api", depends_on=["db"]),
        "worker": ServiceDefinition(name="worker", image="worker", depends_on=["db"]),
        "db": ServiceDefinition(name="db", image="db", depends_on=[]),
    }
    clean_rep = validator.validate_boundaries(clean_services)
    assert clean_rep.status == "PASS"
    assert clean_rep.isolation_score >= 0.90

    leaky_services = {
        "god_api": ServiceDefinition(name="god_api", image="god", ports=["80:80", "443:443", "5432:5432", "6379:6379"], volumes=["shared_data:/data"]),
        "worker": ServiceDefinition(name="worker", image="worker", volumes=["shared_data:/data"]),
    }
    leaky_rep = validator.validate_boundaries(leaky_services)
    assert leaky_rep.status == "FAIL"
    assert len(leaky_rep.god_containers) > 0
    assert len(leaky_rep.shared_mutable_volumes) > 0


def test_vulnerability_scanner_and_security(container_platform):
    """Tests CVE vulnerability scanning and status classification."""
    scanner = container_platform.vuln_scanner

    clean_data = []
    clean_rep = scanner.scan_image(clean_data)
    assert clean_rep.status == "PASS"
    assert clean_rep.critical_vulnerabilities == 0

    crit_data = [
        {"cve_id": "CVE-2026-9999", "package_name": "openssl", "severity": "CRITICAL"},
        {"cve_id": "CVE-2026-8888", "package_name": "curl", "severity": "HIGH"},
    ]
    crit_rep = scanner.scan_image(crit_data)
    assert crit_rep.status == "FAIL"
    assert crit_rep.critical_vulnerabilities == 1
    assert crit_rep.high_vulnerabilities == 1


def test_image_efficiency_analyzer(container_platform):
    """Tests image size constraints and detection of unnecessary cache/test files."""
    analyzer = container_platform.image_analyzer

    efficient = {"image_name": "api", "uncompressed_size_mb": 350.0, "contained_files": ["app/main.py"]}
    eff_rep = analyzer.analyze_image(efficient)
    assert eff_rep.meets_efficiency_target

    bloated = {"image_name": "api", "uncompressed_size_mb": 850.0, "contained_files": [".git/objects", "tests/unit"]}
    bloat_rep = analyzer.analyze_image(bloated)
    assert not bloat_rep.meets_efficiency_target
    assert len(bloat_rep.unnecessary_files_detected) >= 2


def test_reproducibility_and_failure_experiments(container_platform):
    """Tests build digest reproducibility and container failure recovery simulation."""
    repro = container_platform.reproducibility_validator.validate_reproducibility(
        {"source_commit": "c1", "digest_build_1": "sha256:111", "digest_build_2": "sha256:111"}
    )
    assert repro.status == "PASS"
    assert repro.is_deterministic

    fail_rep = container_platform.failure_experiments.execute_failure_simulations(
        [
            {"target_service": "api", "recovered_successfully": True, "data_loss": False},
            {"target_service": "redis", "recovered_successfully": True, "data_loss": False},
        ]
    )
    assert fail_rep.status == "PASS"
    assert fail_rep.recovery_success_count == 2


def test_network_security_and_resource_limits(container_platform):
    """Verifies that internal ports (Postgres, Redis) are not publicly exposed and limits are set."""
    services = {
        "api": ServiceDefinition(name="api", image="api", ports=["8000:8000"], cpu_limit="1.0", memory_limit="1G"),
        "postgres": ServiceDefinition(name="postgres", image="pg", ports=["127.0.0.1:5432:5432"], cpu_limit="2.0", memory_limit="2G"),
    }
    net_rep = container_platform.security_analyzer.analyze_network_security(services)
    res_rep = container_platform.resource_validator.validate_resource_limits(services)
    assert net_rep.status == "PASS"
    assert res_rep.status == "PASS"

    insecure_services = {
        "postgres": ServiceDefinition(name="postgres", image="pg", ports=["0.0.0.0:5432:5432"], cpu_limit=None, memory_limit=None),
    }
    bad_net = container_platform.security_analyzer.analyze_network_security(insecure_services)
    bad_res = container_platform.resource_validator.validate_resource_limits(insecure_services)
    assert bad_net.status == "FAIL"
    assert bad_res.status == "FAIL"


def test_end_to_end_container_verification_and_evidence(container_platform, tmp_path):
    """Tests end-to-end container verification execution, scoring, and artifact export."""
    package = container_platform.run_full_verification(commit_sha="git-commit-3a-99")
    assert package.scorecard.composite_score >= 90.0
    assert package.scorecard.tier in [ContainerCertificationTier.ENTERPRISE_CONTAINER_READY, ContainerCertificationTier.PRODUCTION_READY]
    assert package.package_sha256 != ""

    # Test evidence export
    out_dir = container_platform.evidence_generator.export_results_directory(package, str(tmp_path / "evidence_out"))
    assert (tmp_path / "evidence_out" / "metadata.json").exists()
    assert (tmp_path / "evidence_out" / "architecture_report.json").exists()
    assert (tmp_path / "evidence_out" / "dockerfile_report.json").exists()
