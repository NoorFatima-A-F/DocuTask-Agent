"""Tests for Independent Reality Validators (API, DB, Security)."""

from enterprise_audit_engine.external_validation.api_validator import (
    ApiRealityValidator,
    ApiRealityValidationResult,
)
from enterprise_audit_engine.external_validation.db_validator import (
    DatabaseRealityValidator,
    DatabaseRealityValidationResult,
)
from enterprise_audit_engine.external_validation.security_reality_validator import (
    SecurityRealityValidator,
    SecurityRealityValidationResult,
)


def test_api_reality_validator(tmp_path):
    validator = ApiRealityValidator(tmp_path)
    res = validator.validate_api_reality()

    assert isinstance(res, ApiRealityValidationResult)
    assert res.is_valid is True
    assert res.status == "REALITY_CONFIRMED"
    assert res.passed_checks >= 5
    assert res.failed_checks == 0
    assert len(res.contradictions) == 0


def test_database_reality_validator(tmp_path):
    validator = DatabaseRealityValidator(tmp_path)
    res = validator.validate_database_reality()

    assert isinstance(res, DatabaseRealityValidationResult)
    assert res.is_valid is True
    assert res.status == "REALITY_CONFIRMED"
    assert res.passed_checks >= 4
    assert res.failed_checks == 0
    assert len(res.contradictions) == 0


def test_security_reality_validator(tmp_path):
    validator = SecurityRealityValidator(tmp_path)
    res = validator.execute_security_probes()

    assert isinstance(res, SecurityRealityValidationResult)
    assert res.is_secure is True
    assert res.status == "ADVERSARIAL_DEFENSE_VERIFIED"
    assert res.defense_rate_percentage == 100.0
    assert res.attacks_blocked >= 5
    assert res.attacks_escaped == 0
