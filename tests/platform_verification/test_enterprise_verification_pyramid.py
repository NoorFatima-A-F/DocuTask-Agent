"""
Comprehensive test suite for Enterprise Verification Pyramid Architecture (PART 2).
"""
from app.platform_verification.pyramid_engine import (
    VerificationLevel,
    TestClassification,
    FailureSeverity,
    PyramidExecutionStatus,
    ContinuousTrigger,
    TestDefinition,
    MaturityEngine,
    ContinuousVerificationManager,
    PyramidPlatformRuntime,
)


def test_maturity_engine_and_unverified_inventory():
    engine = MaturityEngine()
    components = engine.list_all_components()
    assert len(components) >= 6

    # Verify Level 0 inventory detection
    unverified = engine.get_unverified_components()
    assert len(unverified) >= 6

    # Update maturity for OCR
    ocr = engine.update_component_maturity("ocr_preprocessing_engine", VerificationLevel.L2_COMPONENT, is_verified=True)
    assert ocr.current_level == VerificationLevel.L2_COMPONENT
    assert ocr.is_verified is True


def test_continuous_verification_trigger_matrix():
    # Commit trigger -> only L1
    commit_levels = ContinuousVerificationManager.get_levels_for_trigger(ContinuousTrigger.COMMIT)
    assert commit_levels == [VerificationLevel.L1_UNIT]

    # PR trigger -> L1, L2, L3
    pr_levels = ContinuousVerificationManager.get_levels_for_trigger(ContinuousTrigger.PULL_REQUEST)
    assert len(pr_levels) == 3
    assert VerificationLevel.L3_INTEGRATION in pr_levels

    # Release trigger -> L1 to L7
    release_levels = ContinuousVerificationManager.get_levels_for_trigger(ContinuousTrigger.RELEASE)
    assert len(release_levels) == 7
    assert VerificationLevel.L7_ENTERPRISE_CERTIFICATION in release_levels


def test_strict_dependency_gating_blocks_higher_levels():
    runtime = PyramidPlatformRuntime()

    # Define tests where Level 2 fails
    tests = [
        TestDefinition(
            id="unit_001",
            name="Unit_OCR_Preprocessor",
            level=VerificationLevel.L1_UNIT,
            classification=TestClassification.FUNCTIONAL,
            description="Unit verification",
            target_component="ocr_preprocessing_engine",
        ),
        TestDefinition(
            id="comp_001",
            name="Component_OCR_Pipeline",
            level=VerificationLevel.L2_COMPONENT,
            classification=TestClassification.FUNCTIONAL,
            description="Component verification",
            target_component="ocr_preprocessing_engine",
        ),
        TestDefinition(
            id="integ_001",
            name="Integ_OCR_to_AI",
            level=VerificationLevel.L3_INTEGRATION,
            classification=TestClassification.FUNCTIONAL,
            description="Integration verification",
            target_component="ocr_preprocessing_engine",
        ),
    ]

    # Inject failure at Level 2
    context = {"simulated_failures": ["comp_001"]}
    report = runtime.run_pyramid_verification(
        system_version="v2.0.0",
        trigger=ContinuousTrigger.PULL_REQUEST,
        tests=tests,
        context=context,
    )

    assert report.overall_status == PyramidExecutionStatus.FAILED
    assert report.level_summaries[VerificationLevel.L1_UNIT].status == PyramidExecutionStatus.PASSED
    assert report.level_summaries[VerificationLevel.L2_COMPONENT].status == PyramidExecutionStatus.FAILED
    assert report.level_summaries[VerificationLevel.L3_INTEGRATION].status == PyramidExecutionStatus.BLOCKED
    assert any("BLOCKED" in msg for msg in report.blocking_failures)


def test_full_release_pyramid_and_certification():
    runtime = PyramidPlatformRuntime()

    # Clean release execution where all levels pass
    tests = [
        TestDefinition(id="u1", name="Unit_Logic", level=VerificationLevel.L1_UNIT, classification=TestClassification.FUNCTIONAL, description="Unit test", target_component="ocr_preprocessing_engine"),
        TestDefinition(id="c1", name="Comp_Pipeline", level=VerificationLevel.L2_COMPONENT, classification=TestClassification.FUNCTIONAL, description="Comp test", target_component="ocr_preprocessing_engine"),
        TestDefinition(id="i1", name="Integ_API", level=VerificationLevel.L3_INTEGRATION, classification=TestClassification.FUNCTIONAL, description="Integ test", target_component="ocr_preprocessing_engine"),
        TestDefinition(id="s1", name="Sys_E2E", level=VerificationLevel.L4_SYSTEM, classification=TestClassification.FUNCTIONAL, description="System test", target_component="ocr_preprocessing_engine"),
        TestDefinition(id="p1", name="Prod_Perf", level=VerificationLevel.L5_PRODUCTION, classification=TestClassification.PERFORMANCE, description="Prod test", target_component="ocr_preprocessing_engine"),
        TestDefinition(id="a1", name="Adv_Security", level=VerificationLevel.L6_ADVERSARIAL, classification=TestClassification.SECURITY, description="Adversarial test", target_component="ocr_preprocessing_engine"),
        TestDefinition(id="cert1", name="Cert_Enterprise", level=VerificationLevel.L7_ENTERPRISE_CERTIFICATION, classification=TestClassification.COMPLIANCE, description="Cert test", target_component="ocr_preprocessing_engine"),
    ]

    report = runtime.run_pyramid_verification(
        system_version="v2.5.0-gold",
        trigger=ContinuousTrigger.RELEASE,
        tests=tests,
    )

    assert report.overall_status == PyramidExecutionStatus.PASSED
    assert report.certification_achieved is True
    assert len(report.level_summaries) == 7
    for summary in report.level_summaries.values():
        assert summary.status == PyramidExecutionStatus.PASSED


def test_defect_creation_and_permanent_regression_safeguard():
    runtime = PyramidPlatformRuntime()

    # Trigger failure
    tests = [
        TestDefinition(
            id="sec_leak_001",
            name="Security_Data_Leak_Check",
            level=VerificationLevel.L6_ADVERSARIAL,
            classification=TestClassification.SECURITY,
            description="Checks data leakage under prompt injection",
            target_component="security_auth_gateway",
        )
    ]
    context = {"simulated_failures": ["sec_leak_001"]}
    report = runtime.run_pyramid_verification(
        system_version="v2.0.0-vuln",
        trigger=ContinuousTrigger.RELEASE,
        tests=tests,
        context=context,
    )

    assert len(report.defects_created) == 1
    defect = report.defects_created[0]
    assert defect.severity == FailureSeverity.CRITICAL

    # Register fixed defect as permanent regression
    reg_record = runtime.register_fixed_defect_as_regression(defect)
    assert reg_record.test_case_id == f"REG-{defect.bug_id}"

    # Replay regression suite
    reg_runs = runtime.regression_engine.run_regression_suite({"version": "v2.0.1-fixed"})
    assert len(reg_runs) == 1
    assert reg_runs[0].status == PyramidExecutionStatus.PASSED


def test_pyramid_dashboard_metrics():
    runtime = PyramidPlatformRuntime()
    dashboard = runtime.get_dashboard_summary()

    assert dashboard.total_components >= 6
    assert 0.0 <= dashboard.coverage_pct <= 100.0
    assert 0.0 <= dashboard.risk_index <= 100.0
    assert VerificationLevel.L0_NOT_TESTED.value in dashboard.maturity_distribution
