"""
Unit and Integration tests for Enterprise Architecture Verification Framework (PART 2A).
"""
import pytest
from app.platform_verification.architecture_verification import (
    ArchitectureCertificationBand,
    ArchitectureDependency,
    ArchitectureRule,
    CircularDependencyCycle,
    EnterpriseArchitectureVerificationRuntime,
    RuleCategory,
    RuleFailureAction,
    RuleSeverity,
)


@pytest.fixture
def runtime():
    return EnterpriseArchitectureVerificationRuntime()


def test_rule_engine_detects_layer_isolation_violations(runtime):
    """Test detecting forbidden imports between layers (e.g. domain importing infrastructure)."""
    deps = [
        ArchitectureDependency(
            source_module="app.domain.document_aggregate",
            target_module="app.infrastructure.database",
            dependency_type="from_import",
            line_number=14,
        ),
        ArchitectureDependency(
            source_module="app.domain.entities",
            target_module="sqlalchemy.orm",
            dependency_type="import",
            line_number=3,
        ),
    ]

    violations = runtime.rule_engine.evaluate_rules(
        dependencies=deps,
        file_metrics={},
        circular_cycles=[],
    )

    assert len(violations) >= 2
    assert all(v.severity == RuleSeverity.CRITICAL for v in violations)
    assert any("Layer violation" in v.message for v in violations)


def test_dependency_graph_and_cycle_detection(runtime):
    """Test directed graph construction and Tarjan cycle detection."""
    deps = [
        ArchitectureDependency("app.module_a", "app.module_b"),
        ArchitectureDependency("app.module_b", "app.module_c"),
        ArchitectureDependency("app.module_c", "app.module_a"),  # Loop: A -> B -> C -> A
    ]

    graph = runtime.graph_engine.build_graph(deps)
    cycles = runtime.graph_engine.detect_circular_dependencies(graph)

    assert len(cycles) == 1
    assert "app.module_a" in cycles[0].cycle_path
    assert "app.module_b" in cycles[0].cycle_path
    assert "app.module_c" in cycles[0].cycle_path


def test_architecture_scoring_and_certification_bands(runtime):
    """Test dimensional scoring and certification band computation."""
    # 1. Clean architecture scan
    clean_score = runtime.scoring_engine.calculate_score(
        violations=[],
        circular_cycles=[],
        total_files=50,
    )
    assert clean_score.total_score >= 95.0
    assert clean_score.certification_band == ArchitectureCertificationBand.ENTERPRISE_ARCHITECTURE_READY
    assert clean_score.is_deployable is True

    # 2. Severely degraded architecture with critical violations
    from app.platform_verification.architecture_verification.domain.models import ArchitectureViolation
    bad_violations = [
        ArchitectureViolation(
            violation_id="V1",
            rule_id="R1",
            rule_name="Domain Isolation",
            category=RuleCategory.DEPENDENCY,
            severity=RuleSeverity.CRITICAL,
            source_file="app/domain/model.py",
            line_number=10,
            message="Domain depends on DB",
        )
    ]
    bad_cycles = [CircularDependencyCycle(cycle_path=["a", "b", "a"])]

    bad_score = runtime.scoring_engine.calculate_score(
        violations=bad_violations,
        circular_cycles=bad_cycles,
        total_files=50,
    )
    assert bad_score.total_score < 80.0
    assert bad_score.is_deployable is False


def test_architecture_regression_detection(runtime):
    """Test detecting regressions between baseline and degraded scans."""
    from app.platform_verification.architecture_verification.domain.models import (
        ArchitectureEvidencePackage,
        ArchitectureViolation,
        ScanMetadata,
    )

    baseline_score = runtime.scoring_engine.calculate_score(
        violations=[],
        circular_cycles=[],
        total_files=10,
    )
    baseline_pkg = ArchitectureEvidencePackage(
        scan_id="SCAN-BASELINE",
        metadata=ScanMetadata("SCAN-BASELINE", "app", "commit1"),
        dependency_graph={},
        violations=[],
        circular_cycles=[],
        score_report=baseline_score,
    )

    degraded_score = runtime.scoring_engine.calculate_score(
        violations=[
            ArchitectureViolation("V1", "R1", "Domain Isolation", RuleCategory.DEPENDENCY, RuleSeverity.CRITICAL, "file.py", 1, "msg")
        ],
        circular_cycles=[],
        total_files=10,
    )

    degraded_pkg = ArchitectureEvidencePackage(
        scan_id="SCAN-DEGRADED",
        metadata=ScanMetadata("SCAN-DEGRADED", "app", "commit2"),
        dependency_graph={},
        violations=[ArchitectureViolation("V1", "R1", "Domain Isolation", RuleCategory.DEPENDENCY, RuleSeverity.CRITICAL, "file.py", 1, "msg")],
        circular_cycles=[],
        score_report=degraded_score,
    )

    report = runtime.regression_engine.detect_regression(
        baseline_evidence=baseline_pkg,
        current_evidence=degraded_pkg,
    )

    assert report.is_regression is True
    assert report.score_delta < 0
    assert len(report.new_violations) == 1


def test_ast_scanner_and_evidence_generation(runtime):
    """Test executing actual AST analysis against app/shared_kernel/ directory."""
    import os
    app_dir = os.path.join(runtime.base_repo_dir, "app", "shared_kernel")
    if os.path.exists(app_dir):
        deps, file_metrics, total_files, total_lines = runtime.scanner.scan_directory(app_dir)
        assert total_files > 0
        assert total_lines > 0
        assert len(deps) > 0
