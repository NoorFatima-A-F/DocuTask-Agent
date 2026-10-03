import os

from tooling.governance.naming_standards_validator import validate_naming
from tooling.governance.dependency_auditor import audit_dependencies
from tooling.governance.change_classifier import ChangeClassifier, ChangeType
from tooling.governance.tech_debt_tracker import TechnicalDebtTracker
from tooling.governance.ai_agent_guardrails import AiAgentGuardrails
from tooling.governance.repository_health_monitor import RepositoryHealthMonitor

class TestRepositoryGovernanceAndEvolution:
    def test_naming_standards_validator(self):
        root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
        violations = validate_naming(root)
        assert len(violations) == 0

    def test_dependency_auditor(self):
        root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
        proj_path = os.path.join(root, "pyproject.toml")
        violations = audit_dependencies(proj_path)
        assert len(violations) == 0

    def test_change_classifier(self):
        res_a = ChangeClassifier.classify_paths(["docs/readme.md", "tests/test_foo.py"])
        assert res_a.change_type == ChangeType.TYPE_A_PATCH
        assert res_a.requires_adr is False

        res_b = ChangeClassifier.classify_paths(["app/contexts/metrics/service.py"])
        assert res_b.change_type == ChangeType.TYPE_B_FEATURE
        assert "metrics" in res_b.affected_components

        res_c = ChangeClassifier.classify_paths(["app/shared_kernel/domain.py", "k8s/deployment.yaml"])
        assert res_c.change_type == ChangeType.TYPE_C_ARCHITECTURAL
        assert res_c.requires_adr is True
        assert res_c.requires_architecture_review is True

    def test_tech_debt_tracker(self):
        root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
        items = TechnicalDebtTracker.scan_codebase(root)
        assert isinstance(items, list)

    def test_ai_agent_guardrails(self):
        root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
        res = AiAgentGuardrails.run_all_guardrails(root)
        assert res.passed is True
        assert res.compliance_score >= 0.90

    def test_repository_health_monitor(self):
        report = RepositoryHealthMonitor.evaluate_health()
        assert report.overall_health_score >= 90.0
        assert report.grade == "A"
        assert report.category_scores["architecture_invariants"] == 1.0
