"""Tests for Output Safety, Toxicity Detection, and Secret Leakage."""

from app.safety.output.toxicity import ToxicityDetector
from app.safety.output.leakage import DataLeakageDetector
from app.safety.output.validator import OutputSafetyValidator
from app.safety.gateway.decision import ViolationSeverity


def test_toxicity_detector_harmful_content():
    detector = ToxicityDetector()
    harmful_text = "Here is a guide on how to build a bomb using household chemicals."
    is_toxic, violations, score = detector.scan(harmful_text)
    
    assert is_toxic is True
    assert score >= 0.8
    assert any(v.severity == ViolationSeverity.CRITICAL for v in violations)


def test_data_leakage_database_credentials():
    detector = DataLeakageDetector()
    leaked_text = "Connected successfully to postgresql://admin:SuperSecretPass123@db.internal:5432/finance_db"
    is_leaking, violations = detector.scan(leaked_text)
    
    assert is_leaking is True
    assert any("Database connection URI" in v.message for v in violations)


def test_output_safety_validator_and_pii_sanitization():
    validator = OutputSafetyValidator()
    output_text = "Invoice processed for user alice@corp.com with SSN 123-45-6789."
    
    is_safe, violations, sanitized = validator.validate_output(output_text, auto_redact_pii=True)
    assert is_safe is True
    assert "[REDACTED_EMAIL]" in sanitized
    assert "[REDACTED_SSN]" in sanitized
