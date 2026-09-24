"""
Production Tests for Agent Security Governance Layer and Advanced Tool Policy.
Covers RBAC Permissions, ActionPolicy, ToolAccessController, SecurityGuardian, PrivacyPolicy, CompliancePolicy, and ToolDecisionEngine.
"""

import pytest

from app.agents.security.action_policy import ActionPolicy
from app.agents.security.agent_permission import (
    AgentPermission,
    AgentRole,
    ROLE_PERMISSION_MATRIX,
)
from app.agents.security.security_guardian import SecurityGuardian
from app.agents.security.tool_access_control import ToolAccessController
from app.agents.tools.policy.compliance_policy import (
    ComplianceFramework,
    CompliancePolicy,
)
from app.agents.tools.policy.privacy_policy import PrivacyPolicy
from app.agents.tools.policy.tool_decision_engine import (
    PolicyDecision,
    ToolDecisionEngine,
)


class TestAgentPermissions:
    def test_admin_has_all_permissions(self):
        admin_perms = ROLE_PERMISSION_MATRIX[AgentRole.ADMIN]
        for perm in AgentPermission:
            assert perm in admin_perms

    def test_extractor_least_privilege(self):
        extractor_perms = ROLE_PERMISSION_MATRIX[AgentRole.EXTRACTOR]
        assert AgentPermission.EXECUTE_OCR in extractor_perms
        assert AgentPermission.EXECUTE_LLM in extractor_perms
        assert AgentPermission.DELETE_DATA not in extractor_perms
        assert AgentPermission.MUTATE_GRAPH not in extractor_perms

    def test_auditor_permissions(self):
        auditor_perms = ROLE_PERMISSION_MATRIX[AgentRole.AUDITOR]
        assert AgentPermission.READ_DOCUMENT in auditor_perms
        assert AgentPermission.EXPORT_DATA in auditor_perms
        assert AgentPermission.EXECUTE_OCR not in auditor_perms


class TestActionPolicy:
    def test_action_policy_allowed(self):
        policy = ActionPolicy()
        res = policy.is_action_allowed(
            role=AgentRole.EXTRACTOR,
            permission=AgentPermission.EXECUTE_OCR,
            target_resource="doc-1",
        )
        assert res.allowed is True

    def test_action_policy_denied_permission(self):
        policy = ActionPolicy()
        res = policy.is_action_allowed(
            role=AgentRole.VALIDATOR,
            permission=AgentPermission.DELETE_DATA,
            target_resource="doc-1",
        )
        assert res.allowed is False
        assert "lacks required permission" in res.reason

    def test_action_policy_prohibited_delete_non_admin(self):
        policy = ActionPolicy()
        res = policy.is_action_allowed(
            role=AgentRole.COORDINATOR,
            permission=AgentPermission.DELETE_DATA,
            target_resource="raw_files",
        )
        assert res.allowed is False

    def test_action_policy_extractor_graph_mutation_forbidden(self):
        policy = ActionPolicy()
        res = policy.is_action_allowed(
            role=AgentRole.EXTRACTOR,
            permission=AgentPermission.MUTATE_GRAPH,
        )
        assert res.allowed is False
        assert "lacks required permission" in res.reason or "forbidden" in res.reason.lower()


class TestToolAccessControl:
    def test_default_tool_access(self):
        tac = ToolAccessController()
        assert tac.is_tool_accessible(AgentRole.EXTRACTOR, "tesseract_ocr") is True
        assert tac.is_tool_accessible(AgentRole.VALIDATOR, "tesseract_ocr") is False
        assert tac.is_tool_accessible(AgentRole.ADMIN, "tesseract_ocr") is True

    def test_grant_and_revoke_tool_access(self):
        tac = ToolAccessController()
        assert tac.is_tool_accessible(AgentRole.VALIDATOR, "custom_ocr") is True  # unlisted tool allowed by default

        tac.grant_tool_access("custom_ocr", AgentRole.EXTRACTOR)
        # Once registered with explicit roles, VALIDATOR is no longer allowed
        assert tac.is_tool_accessible(AgentRole.EXTRACTOR, "custom_ocr") is True
        assert tac.is_tool_accessible(AgentRole.VALIDATOR, "custom_ocr") is False

        assert tac.revoke_tool_access("custom_ocr", AgentRole.EXTRACTOR) is True


class TestSecurityGuardian:
    def test_guardian_verify_action_and_audit_trail(self):
        guardian = SecurityGuardian()
        res1 = guardian.verify_action("ag_ext", AgentRole.EXTRACTOR, AgentPermission.EXECUTE_OCR)
        assert res1.allowed is True

        res2 = guardian.verify_action("ag_ext", AgentRole.EXTRACTOR, AgentPermission.DELETE_DATA)
        assert res2.allowed is False

        trail = guardian.get_audit_trail()
        assert len(trail) == 2
        assert trail[0].granted is True
        assert trail[1].granted is False

    def test_guardian_verify_tool_invocation(self):
        guardian = SecurityGuardian()
        assert guardian.verify_tool_invocation("ag_ext", AgentRole.EXTRACTOR, "tesseract_ocr") is True
        assert guardian.verify_tool_invocation("ag_val", AgentRole.VALIDATOR, "tesseract_ocr") is False


class TestPrivacyPolicy:
    def test_detect_and_mask_ssn_and_credit_card(self):
        raw = "Customer SSN: 123-45-6789 and Card: 4111 2222 3333 4444"
        assert PrivacyPolicy.contains_pii(raw) is True

        res = PrivacyPolicy.mask_pii(raw, salt="SEC")
        assert "123-45-6789" not in res.sanitized_text
        assert "4111 2222 3333 4444" not in res.sanitized_text
        assert "[SSN_SEC_1]" in res.sanitized_text
        assert "[CREDIT_CARD_SEC_2]" in res.sanitized_text
        assert "SSN" in res.detected_pii_types
        assert "CREDIT_CARD" in res.detected_pii_types

    def test_clean_text_contains_no_pii(self):
        raw = "ACME Corporation standard invoice total: $500.00"
        assert PrivacyPolicy.contains_pii(raw) is False


class TestCompliancePolicy:
    def test_hipaa_phi_external_tool_violation(self):
        policy = CompliancePolicy(active_frameworks=[ComplianceFramework.HIPAA])
        res = policy.evaluate(
            tool_name="public_ocr_api",
            document_domain="medical_records",
            payload={"patient_notes": "Patient John Doe"},
        )
        assert res.compliant is False
        assert any("HIPAA" in v for v in res.violations)

    def test_gdpr_pii_masking_requirement(self):
        policy = CompliancePolicy(active_frameworks=[ComplianceFramework.GDPR])
        res = policy.evaluate(
            tool_name="internal_extractor",
            document_domain="general",
            payload={"contact": "user@example.com"},
        )
        assert res.compliant is True


class TestToolDecisionEngine:
    def test_clean_approval(self):
        engine = ToolDecisionEngine()
        auth = engine.evaluate_tool_call(
            tool_name="pdf_plumber",
            payload={"path": "/docs/invoice.pdf"},
            document_domain="FINANCIAL",
        )
        assert auth.decision == PolicyDecision.APPROVED
        assert len(auth.violations) == 0

    def test_approval_with_pii_masking(self):
        engine = ToolDecisionEngine()
        auth = engine.evaluate_tool_call(
            tool_name="gemini_vision",
            payload={"text": "Contact patient with SSN: 999-88-7777"},
            document_domain="HEALTHCARE",
        )
        assert auth.decision == PolicyDecision.APPROVED_WITH_MASKING
        assert "999-88-7777" not in auth.effective_payload["text"]
        assert auth.masking_metadata is not None

    def test_forbidden_tool_denial(self):
        engine = ToolDecisionEngine()
        auth = engine.evaluate_tool_call(
            tool_name="os_system",
            payload={"cmd": "ls"},
        )
        assert auth.decision == PolicyDecision.DENIED
        assert any("explicitly forbidden" in v for v in auth.violations)

    def test_command_injection_denial(self):
        engine = ToolDecisionEngine()
        auth = engine.evaluate_tool_call(
            tool_name="pdf_plumber",
            payload={"filename": "doc.pdf; rm -rf /"},
        )
        assert auth.decision == PolicyDecision.DENIED
        assert any("Potential injection" in v for v in auth.violations)

    @pytest.mark.parametrize(
        "role,perm,expected_allowed",
        [
            (AgentRole.COORDINATOR, AgentPermission.MUTATE_GRAPH, True),
            (AgentRole.COORDINATOR, AgentPermission.ESCALATE_HUMAN, True),
            (AgentRole.EXTRACTOR, AgentPermission.MUTATE_GRAPH, False),
            (AgentRole.VALIDATOR, AgentPermission.DELETE_DATA, False),
            (AgentRole.VALIDATOR, AgentPermission.READ_DOCUMENT, True),
            (AgentRole.ADMIN, AgentPermission.DELETE_DATA, True),
            (AgentRole.AUDITOR, AgentPermission.READ_DOCUMENT, True),
            (AgentRole.AUDITOR, AgentPermission.DELETE_DATA, False),
        ],
    )
    def test_rbac_permission_matrix_parameterized(self, role, perm, expected_allowed):
        policy = ActionPolicy()
        res = policy.is_action_allowed(role=role, permission=perm)
        assert res.allowed is expected_allowed

    @pytest.mark.parametrize(
        "pii_text,expected_detected_type",
        [
            ("User email: john.doe@company.org in report", "EMAIL"),
            ("Direct phone line: 1-800-555-0199 ext 4", "PHONE"),
            ("Tax ID SSN: 000-12-3456 verified", "SSN"),
            ("Visa card: 4000 1234 5678 9010 on receipt", "CREDIT_CARD"),
        ],
    )
    def test_privacy_policy_pii_types_parameterized(self, pii_text, expected_detected_type):
        assert PrivacyPolicy.contains_pii(pii_text) is True
        res = PrivacyPolicy.mask_pii(pii_text)
        assert expected_detected_type in res.detected_pii_types
        assert res.sanitized_text != pii_text

    @pytest.mark.parametrize(
        "injection_payload",
        [
            {"input_path": "/var/data/file.pdf | cat /etc/passwd"},
            {"command": "echo test && rm -rf /"},
            {"cmd_sub": "file_`whoami`.pdf"},
            {"eval_sub": "file_$(whoami).pdf"},
        ],
    )
    def test_security_policy_command_injection_detection(self, injection_payload):
        engine = ToolDecisionEngine()
        auth = engine.evaluate_tool_call(tool_name="pdf_extractor", payload=injection_payload)
        assert auth.decision == PolicyDecision.DENIED
        assert any("injection" in v.lower() for v in auth.violations)

    def test_compliance_pci_dss_credit_card_masking(self):
        policy = CompliancePolicy(active_frameworks=[ComplianceFramework.PCI_DSS])
        res = policy.evaluate(
            tool_name="payment_gateway",
            document_domain="payment",
            payload={"card_info": "Card: 4532 0150 9988 1234"},
        )
        assert res.compliant is False
        assert any("PCI-DSS" in v for v in res.violations)

    def test_security_guardian_filter_audit_trail(self):
        guardian = SecurityGuardian()
        guardian.verify_action("ag_admin", AgentRole.ADMIN, AgentPermission.DELETE_DATA)
        guardian.verify_action("ag_ext", AgentRole.EXTRACTOR, AgentPermission.DELETE_DATA)
        guardian.verify_action("ag_ext", AgentRole.EXTRACTOR, AgentPermission.EXECUTE_OCR)

        trail = guardian.get_audit_trail()
        assert len(trail) == 3

        ext_trail = [e for e in trail if e.agent_id == "ag_ext"]
        assert len(ext_trail) == 2
        denied = [e for e in ext_trail if not e.granted]
        assert len(denied) == 1

    @pytest.mark.parametrize(
        "tool,role,expected_granted",
        [
            ("tesseract_ocr", AgentRole.EXTRACTOR, True),
            ("pdf_plumber", AgentRole.EXTRACTOR, True),
            ("gemini_vision", AgentRole.EXTRACTOR, True),
            ("tesseract_ocr", AgentRole.VALIDATOR, False),
            ("rule_engine", AgentRole.VALIDATOR, True),
            ("schema_validator", AgentRole.VALIDATOR, True),
            ("database_writer", AgentRole.ADMIN, True),
            ("export_csv", AgentRole.AUDITOR, True),
            ("tesseract_ocr", AgentRole.ADMIN, True),
            ("unknown_tool_xyz", AgentRole.EXTRACTOR, True),
        ],
    )
    def test_tool_access_controller_role_mappings(self, tool, role, expected_granted):
        tac = ToolAccessController()
        assert tac.is_tool_accessible(role, tool) == expected_granted

    @pytest.mark.parametrize(
        "clean_text",
        [
            "Standard invoice for widgets without any sensitive numbers",
            "Purchase Order #98124 total $1,250.00 USD",
            "Deliver goods to Warehouse 4B dock 12",
            "Contract termination date 2026-12-31",
            "Meeting agenda: quarterly financial review",
        ],
    )
    def test_privacy_policy_clean_strings(self, clean_text):
        assert PrivacyPolicy.contains_pii(clean_text) is False
        res = PrivacyPolicy.mask_pii(clean_text)
        assert res.sanitized_text == clean_text
        assert len(res.detected_pii_types) == 0

