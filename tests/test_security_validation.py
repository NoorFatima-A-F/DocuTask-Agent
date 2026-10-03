"""
Unit and integration tests for Phase V9 — Enterprise AI Security Validation & Adversarial Assurance Program (EA-SVAAP).
"""

import os
import json

from app.security_validation import (
    SecurityStatus,
    SeverityLevel,
    SecurityPillar,
    AttackCategory,
    AttackPayload,
    SecurityFinding,
    SecurityTestRunner,
    OWASPASVSScanner,
    VulnerabilityScanner,
    OWASPLLMVerifier,
    GuardrailEvaluator,
    AdversarialAttackEngine,
    MITREATLASVerifier,
    APISecurityVerifier,
    RBACAccessVerifier,
    DataProtectionVerifier,
    AgentBoundaryVerifier,
    TenantIsolationVerifier,
    ComplianceMapper,
    SecurityDashboardVerifier,
    SecurityScorer,
    SecurityReportGenerator,
)


def test_domain_models():
    payload = AttackPayload(
        payload_id="INJ-001",
        category=AttackCategory.DIRECT_PROMPT_INJECTION,
        raw_payload="Ignore rules",
        target_component="guardrail",
        expected_action="BLOCK",
        severity=SeverityLevel.CRITICAL,
    )
    d = payload.to_dict()
    assert d["payload_id"] == "INJ-001"
    assert d["category"] == "DIRECT_PROMPT_INJECTION"
    assert d["severity"] == "CRITICAL"

    finding = SecurityFinding(
        finding_id="FIND-101",
        title="Sample Finding",
        pillar=SecurityPillar.AI_SECURITY_LLM,
        severity=SeverityLevel.INFORMATIONAL,
        status=SecurityStatus.PASSED,
        description="Clean",
        remediation_recommendation="None",
    )
    fd = finding.to_dict()
    assert fd["finding_id"] == "FIND-101"
    assert fd["status"] == "PASSED"


def test_framework_test_runner():
    runner = SecurityTestRunner()
    res = runner.verify()
    assert res.score == 100.0
    assert res.status == SecurityStatus.PASSED
    assert len(res.assertions) == 4
    assert all(a.passed for a in res.assertions)


def test_asvs_scanner():
    scanner = OWASPASVSScanner()
    res = scanner.verify()
    assert res.score == 100.0
    assert res.status == SecurityStatus.PASSED
    assert len(res.assertions) == 4


def test_vulnerability_scanner():
    scanner = VulnerabilityScanner()
    res = scanner.verify()
    assert res.score == 100.0
    assert res.status == SecurityStatus.PASSED
    assert len(res.assertions) == 4


def test_owasp_llm_verifier():
    verifier = OWASPLLMVerifier()
    res = verifier.verify()
    assert res.score == 100.0
    assert res.status == SecurityStatus.PASSED
    assert len(res.assertions) == 4


def test_guardrail_evaluator():
    evaluator = GuardrailEvaluator()
    res = evaluator.verify()
    assert res.score == 100.0
    assert res.status == SecurityStatus.PASSED
    assert len(res.assertions) == 4


def test_adversarial_attack_engine():
    engine = AdversarialAttackEngine()
    res = engine.verify()
    assert res.score == 100.0
    assert res.status == SecurityStatus.PASSED
    assert len(res.assertions) == 4


def test_mitre_atlas_verifier():
    verifier = MITREATLASVerifier()
    res = verifier.verify()
    assert res.score == 100.0
    assert res.status == SecurityStatus.PASSED
    assert len(res.assertions) == 4


def test_api_security_verifier():
    verifier = APISecurityVerifier()
    res = verifier.verify()
    assert res.score == 100.0
    assert res.status == SecurityStatus.PASSED
    assert len(res.assertions) == 4


def test_rbac_access_verifier():
    verifier = RBACAccessVerifier()
    res = verifier.verify()
    assert res.score == 100.0
    assert res.status == SecurityStatus.PASSED
    assert len(res.assertions) == 4


def test_data_protection_verifier():
    verifier = DataProtectionVerifier()
    res = verifier.verify()
    assert res.score == 100.0
    assert res.status == SecurityStatus.PASSED
    assert len(res.assertions) == 4


def test_agent_boundary_verifier():
    verifier = AgentBoundaryVerifier()
    res = verifier.verify()
    assert res.score == 100.0
    assert res.status == SecurityStatus.PASSED
    assert len(res.assertions) == 4


def test_tenant_isolation_verifier():
    verifier = TenantIsolationVerifier()
    res = verifier.verify()
    assert res.score == 100.0
    assert res.status == SecurityStatus.PASSED
    assert len(res.assertions) == 4


def test_compliance_mapper():
    mapper = ComplianceMapper()
    res = mapper.verify()
    assert res.score == 100.0
    assert res.status == SecurityStatus.PASSED
    assert len(res.assertions) == 4


def test_security_dashboard_verifier():
    dashboard = SecurityDashboardVerifier()
    res = dashboard.verify()
    assert res.score == 100.0
    assert res.status == SecurityStatus.PASSED
    assert len(res.assertions) == 4


def test_security_scorer():
    scorer = SecurityScorer()
    scorecard = scorer.run_all()
    assert scorecard.composite_score == 100.0
    assert scorecard.grade == "A+"
    assert scorecard.production_ready is True
    assert scorecard.critical_vulnerabilities == 0
    assert scorecard.high_vulnerabilities == 0
    assert scorecard.total_assertions == 56
    assert scorecard.passed_assertions == 56
    assert len(scorecard.pillars) == 14
    assert len(scorecard.weighted_scores) == 6


def test_security_report_generator(tmp_path):
    scorer = SecurityScorer()
    scorecard = scorer.run_all()

    exporter = SecurityReportGenerator(
        output_dir=str(tmp_path / "evidence"),
        report_path=str(tmp_path / "report.md"),
    )
    summary = exporter.export_all(scorecard)

    assert os.path.exists(summary["output_dir"])
    assert os.path.exists(summary["manifest_file"])
    assert os.path.exists(summary["report_path"])

    with open(summary["manifest_file"], "r", encoding="utf-8") as f:
        manifest = json.load(f)
    assert len(manifest["checksums"]) == 15  # 14 pillars + 1 summary
    assert "Phase V9" in manifest["verification_program"]
    assert manifest["composite_score"] == 100.0
