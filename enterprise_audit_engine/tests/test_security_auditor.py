"""Tests for Engine Defensive Security Validator."""

from enterprise_audit_engine.certification.security_auditor import EngineSecurityValidator


def test_engine_security_validator_clean(tmp_path):
    # Create safe engine files
    (tmp_path / "safe.py").write_text("import json\nimport os\n\ndef run():\n    return json.loads('{}')\n", encoding="utf-8")

    result = EngineSecurityValidator.audit_engine_security(tmp_path)
    assert result["is_secure"] is True
    assert result["vulnerabilities_found_count"] == 0
    assert result["security_posture"] == "HARDENED_ENTERPRISE_STANDARD"


def test_engine_security_validator_detects_unsafe(tmp_path):
    # Create unsafe files
    (tmp_path / "unsafe_pickle.py").write_text("import pickle\npickle.loads(b'data')\n", encoding="utf-8")
    (tmp_path / "unsafe_shell.py").write_text("import subprocess\nsubprocess.run('ls', shell=True)\n", encoding="utf-8")

    result = EngineSecurityValidator.audit_engine_security(tmp_path)
    assert result["is_secure"] is False
    assert result["vulnerabilities_found_count"] == 2
    vuln_types = [v["vulnerability"] for v in result["vulnerabilities"]]
    assert "UNSAFE_DESERIALIZATION_PICKLE" in vuln_types
    assert "UNSAFE_SHELL_EXECUTION" in vuln_types
