"""
Unit and Integration tests for Clean Architecture & Dependency Validation (PART 2B).
"""
import pytest
from app.platform_verification.clean_architecture import (
    ArchitectureExceptionWaiver,
    ArchitectureLayer,
    CleanArchDependencyEdge,
    CleanArchSeverity,
    EnterpriseCleanArchitectureRuntime,
    ImportType,
)


@pytest.fixture
def runtime():
    return EnterpriseCleanArchitectureRuntime()


def test_clean_arch_rule_engine_detects_forbidden_outward_dependency(runtime):
    """Test that domain importing infrastructure or web frameworks is caught as CRITICAL violation."""
    edges = [
        CleanArchDependencyEdge(
            source_module="app.domain.document_entity",
            source_layer=ArchitectureLayer.DOMAIN,
            target_module="app.infrastructure.database",
            target_layer=ArchitectureLayer.INFRASTRUCTURE,
            import_type=ImportType.FROM_IMPORT,
            line_number=12,
        ),
        CleanArchDependencyEdge(
            source_module="app.domain.services",
            source_layer=ArchitectureLayer.DOMAIN,
            target_module="fastapi",
            target_layer=ArchitectureLayer.API,
            import_type=ImportType.DIRECT_IMPORT,
            line_number=3,
        ),
    ]

    violations = runtime.rule_engine.evaluate_dependencies(edges=edges)
    assert len(violations) >= 2
    assert all(v.severity == CleanArchSeverity.CRITICAL for v in violations)
    assert any("forbidden from depending on outer layer" in v.message for v in violations)
    assert any("forbidden from importing external library 'fastapi'" in v.message for v in violations)


def test_clean_arch_allowed_inward_dependencies(runtime):
    """Test that API -> Application -> Domain inward dependencies are completely allowed."""
    edges = [
        CleanArchDependencyEdge(
            source_module="app.api.v1.endpoints",
            source_layer=ArchitectureLayer.API,
            target_module="app.application.process_document_usecase",
            target_layer=ArchitectureLayer.APPLICATION,
            import_type=ImportType.FROM_IMPORT,
            line_number=5,
        ),
        CleanArchDependencyEdge(
            source_module="app.application.process_document_usecase",
            source_layer=ArchitectureLayer.APPLICATION,
            target_module="app.domain.document_entity",
            target_layer=ArchitectureLayer.DOMAIN,
            import_type=ImportType.FROM_IMPORT,
            line_number=8,
        ),
    ]

    violations = runtime.rule_engine.evaluate_dependencies(edges=edges)
    assert len(violations) == 0


def test_exception_waiver_bypass(runtime):
    """Test that an active approved exception waiver waives a violation."""
    edge = CleanArchDependencyEdge(
        source_module="app.domain.legacy_migration_helper",
        source_layer=ArchitectureLayer.DOMAIN,
        target_module="app.infrastructure.db",
        target_layer=ArchitectureLayer.INFRASTRUCTURE,
        import_type=ImportType.FROM_IMPORT,
        line_number=1,
    )

    waiver = ArchitectureExceptionWaiver(
        waiver_id="WAIVER-LEGACY-001",
        rule_id="RULE_DOMAIN_ISOLATION",
        source_file="legacy_migration_helper",
        target_module="app.infrastructure.db",
        justification="Temporary migration utility pending refactor",
        approved_by="PrincipalArchitect",
    )

    violations = runtime.rule_engine.evaluate_dependencies(edges=[edge], waivers=[waiver])
    assert len(violations) == 0
    assert edge.is_waived is True


def test_metrics_calculator_instability_and_distance(runtime):
    """Test calculating Ca, Ce, Instability I = Ce / (Ca + Ce), and Distance D = |A + I - 1|."""
    edges = [
        CleanArchDependencyEdge(
            source_module="app.api.endpoints",
            source_layer=ArchitectureLayer.API,
            target_module="app.domain.model",
            target_layer=ArchitectureLayer.DOMAIN,
            import_type=ImportType.FROM_IMPORT,
            line_number=1,
        ),
        CleanArchDependencyEdge(
            source_module="app.application.service",
            source_layer=ArchitectureLayer.APPLICATION,
            target_module="app.domain.model",
            target_layer=ArchitectureLayer.DOMAIN,
            import_type=ImportType.FROM_IMPORT,
            line_number=1,
        ),
    ]

    metrics = runtime.metrics_calculator.calculate_module_metrics(edges)
    domain_m = metrics.get("app.domain.model")
    assert domain_m is not None
    assert domain_m.afferent_coupling_ca >= 2
    assert domain_m.efferent_coupling_ce == 0
    assert domain_m.instability_i == 0.0  # Completely stable


def test_full_clean_architecture_validation_run(runtime):
    """Test running full Clean Architecture validation scan on shared_kernel."""
    import os
    target_dir = os.path.join(runtime.base_repo_dir, "app", "shared_kernel")
    if os.path.exists(target_dir):
        pkg = runtime.run_full_validation(target_dir=target_dir)
        assert pkg.scan_id.startswith("CLEAN-ARCH-")
        assert len(pkg.evidence_sha256) == 64
