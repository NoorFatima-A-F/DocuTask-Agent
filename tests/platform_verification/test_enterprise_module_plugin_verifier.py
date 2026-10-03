"""
Unit and Integration tests for Module Boundary & Plugin Architecture Verification (PART 2D).
"""
import pytest
from app.platform_verification.module_boundary import (
    EnterpriseModuleBoundaryRuntime,
    ModularityCertificationBand,
    ModuleDependencyEdge,
    PluginInterface,
)


@pytest.fixture
def runtime():
    return EnterpriseModuleBoundaryRuntime()


def test_boundary_validator_detects_forbidden_plugin_to_database_dependency(runtime):
    """Test detecting forbidden dependency from plugin directly into core database."""
    deps = [
        ModuleDependencyEdge(
            source_module="plugins",
            target_module="database",
        ),
        ModuleDependencyEdge(
            source_module="knowledge",
            target_module="agents",
        ),
    ]

    violations = runtime.boundary_validator.validate_dependencies(deps)
    assert len(violations) >= 2
    assert any("forbidden from depending on 'database'" in v.message for v in violations)
    assert any("forbidden from depending on 'agents'" in v.message for v in violations)


def test_plugin_verifier_enforces_lifecycle_contract(runtime):
    """Test verifying full plugin interface lifecycle contracts."""
    # 1. Compliant Plugin
    class CompliantOcrPlugin(PluginInterface):
        def initialize(self, config): return True
        def execute(self, context): return {"extracted": True}
        def health(self): return {"status": "OK"}
        def shutdown(self): return True

    report = runtime.plugin_verifier.verify_plugin_contract(CompliantOcrPlugin, {"name": "TesseractOCR", "type": "OCR_PROVIDER"})
    assert report.passed is True
    assert report.satisfies_plugin_interface is True

    # 2. Non-compliant incomplete plugin
    class IncompletePlugin:
        def execute(self, context): return {}

    bad_report = runtime.plugin_verifier.verify_plugin_contract(IncompletePlugin, {"name": "BrokenPlugin"})
    assert bad_report.passed is False
    assert len(bad_report.errors) >= 3


def test_failure_isolation_containment(runtime):
    """Test that a crashing plugin is safely caught and contained by host sandbox."""
    class FaultyPlugin(PluginInterface):
        def initialize(self, config): return True
        def execute(self, context):
            raise RuntimeError("Upstream OCR engine segfaulted!")
        def health(self): return {"status": "ERROR"}
        def shutdown(self): return True

    faulty = FaultyPlugin()
    isolated, msg = runtime.plugin_verifier.test_failure_isolation(faulty, {})
    assert isolated is True
    assert "Exception successfully isolated" in msg


def test_version_compatibility_checker(runtime):
    """Test semver compatibility validation between core platform and plugin requirements."""
    assert runtime.compatibility_validator.check_compatibility(core_version="2.4.0", plugin_req_core_version=">=2.0.0") is True
    assert runtime.compatibility_validator.check_compatibility(core_version="1.9.0", plugin_req_core_version=">=2.0.0") is False


def test_modularity_metrics_and_evidence_generation(runtime):
    """Test calculating module independence metrics and compiling sealed evidence package."""
    pkg = runtime.run_full_scan()
    assert pkg.scan_id.startswith("MOD-SCAN-")
    assert pkg.registered_modules_count >= 5
    assert pkg.registered_plugins_count >= 1
    assert pkg.total_modularity_score >= 85.0
    assert pkg.certification_band in (
        ModularityCertificationBand.ENTERPRISE_PLATFORM_MODULAR,
        ModularityCertificationBand.PRODUCTION_MODULAR,
    )
    assert len(pkg.evidence_sha256) == 64
