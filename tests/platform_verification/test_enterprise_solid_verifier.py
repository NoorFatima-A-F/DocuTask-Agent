"""
Unit and Integration tests for SOLID Principle Automated Verification System (PART 2C).
"""
import pytest
from app.platform_verification.solid_verification import (
    ClassDesignMetrics,
    EnterpriseSolidVerificationRuntime,
    InterfaceDesignMetrics,
    SolidCertificationBand,
    SolidPrinciple,
    SolidViolationSeverity,
)


@pytest.fixture
def runtime():
    return EnterpriseSolidVerificationRuntime()


def test_srp_evaluator_detects_god_class(runtime):
    """Test detecting Single Responsibility Principle violation (God Class mixing 5 domains)."""
    god_class = ClassDesignMetrics(
        class_name="UniversalDocumentProcessor",
        file_path="app/domain/processor.py",
        line_count=450,
        method_count=18,
        attribute_count=12,
        constructor_param_count=9,
        wmc_weighted_methods=25,
        cbo_coupling_between_objects=12,
        lcom_lack_of_cohesion=0.8,
        rfc_response_for_class=30,
        dit_depth_of_inheritance=1,
        noc_number_of_children=0,
        detected_responsibilities=["Storage", "OCR/Extraction", "Embedding", "Notification", "Persistence"],
    )

    violations = runtime.rule_evaluator.evaluate_srp({"test:processor": god_class})
    assert len(violations) >= 2
    assert any(v.severity == SolidViolationSeverity.CRITICAL for v in violations)
    assert any("God Class violation" in v.message for v in violations)
    assert any("Excessive dependencies" in v.message for v in violations)


def test_ocp_evaluator_detects_type_switching(runtime):
    """Test detecting Open/Closed Principle violation from provider conditional branching."""
    rigid_class = ClassDesignMetrics(
        class_name="RigidModelRouter",
        file_path="app/agents/router.py",
        line_count=120,
        method_count=4,
        attribute_count=2,
        constructor_param_count=2,
        wmc_weighted_methods=8,
        cbo_coupling_between_objects=3,
        lcom_lack_of_cohesion=0.1,
        rfc_response_for_class=6,
        dit_depth_of_inheritance=1,
        noc_number_of_children=0,
        has_type_switch_violation=True,
    )

    violations = runtime.rule_evaluator.evaluate_ocp({"test:router": rigid_class})
    assert len(violations) == 1
    assert violations[0].principle == SolidPrinciple.OCP
    assert "Open/Closed violation" in violations[0].message


def test_lsp_evaluator_detects_unsupported_operation_override(runtime):
    """Test detecting Liskov Substitution Principle violation when subclass throws UnsupportedOperation."""
    bad_child = ClassDesignMetrics(
        class_name="DummyOcrProvider",
        file_path="app/infrastructure/ocr/dummy.py",
        line_count=80,
        method_count=3,
        attribute_count=1,
        constructor_param_count=1,
        wmc_weighted_methods=4,
        cbo_coupling_between_objects=2,
        lcom_lack_of_cohesion=0.1,
        rfc_response_for_class=4,
        dit_depth_of_inheritance=2,
        noc_number_of_children=0,
        has_unsupported_operation_override=True,
    )

    violations = runtime.rule_evaluator.evaluate_lsp({"test:dummy": bad_child})
    assert len(violations) == 1
    assert violations[0].principle == SolidPrinciple.LSP
    assert violations[0].severity == SolidViolationSeverity.CRITICAL


def test_isp_evaluator_detects_oversized_interface(runtime):
    """Test detecting Interface Segregation Principle violation for fat interfaces."""
    fat_interface = InterfaceDesignMetrics(
        interface_name="IAIUniversalProvider",
        file_path="app/interfaces/ai.py",
        total_methods=16,
        implementations_count=2,
        avg_usage_ratio=0.25,
        is_oversized=True,
    )

    violations = runtime.rule_evaluator.evaluate_isp({"test:ai": fat_interface})
    assert len(violations) == 1
    assert violations[0].principle == SolidPrinciple.ISP
    assert "Interface Segregation violation" in violations[0].message


def test_dip_evaluator_detects_concrete_instantiation_in_domain(runtime):
    """Test detecting Dependency Inversion Principle violation for direct vendor instantiations in high-level modules."""
    coupled_class = ClassDesignMetrics(
        class_name="AgentOrchestrator",
        file_path="app/application/orchestrator.py",
        line_count=200,
        method_count=6,
        attribute_count=3,
        constructor_param_count=2,
        wmc_weighted_methods=10,
        cbo_coupling_between_objects=4,
        lcom_lack_of_cohesion=0.2,
        rfc_response_for_class=12,
        dit_depth_of_inheritance=1,
        noc_number_of_children=0,
        has_direct_instantiation_violation=True,
    )

    violations = runtime.rule_evaluator.evaluate_dip({"test:orch": coupled_class})
    assert len(violations) == 1
    assert violations[0].principle == SolidPrinciple.DIP
    assert violations[0].severity == SolidViolationSeverity.CRITICAL


def test_solid_scoring_and_evidence_generation(runtime):
    """Test calculating weighted scorecard and generating SHA-256 evidence package."""
    pkg = runtime.run_full_scan(target_dir=runtime.base_repo_dir + "/app/shared_kernel")
    assert pkg.scan_id.startswith("SOLID-SCAN-")
    assert pkg.scorecard is not None
    assert pkg.scorecard.total_score >= 80.0
    assert len(pkg.evidence_sha256) == 64
