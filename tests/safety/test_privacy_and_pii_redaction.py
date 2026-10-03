"""Tests for PII Detection, Masking, and Redaction/Pseudonymization."""

from app.safety.privacy.pii_detector import PIIDetector, PIIType
from app.safety.privacy.masking import DataMasker
from app.safety.privacy.redaction import DataRedactor


def test_pii_detection_types():
    detector = PIIDetector()
    sample = (
        "Customer John Doe (email: john.doe@example.com, phone: 555-123-4567, "
        "SSN: 123-45-6789, credit_card: 4111-2222-3333-4444, "
        "AWS key: AKIAIOSFODNN7EXAMPLE, API key: sk-abcdef1234567890abcdef1234567890)"
    )
    matches = detector.detect(sample)
    types_found = {m.pii_type for m in matches}
    
    assert PIIType.EMAIL in types_found
    assert PIIType.PHONE in types_found
    assert PIIType.SSN in types_found
    assert PIIType.CREDIT_CARD in types_found
    assert PIIType.AWS_KEY in types_found
    assert PIIType.API_KEY in types_found


def test_pii_masking():
    masker = DataMasker()
    text = "User SSN is 123-45-6789 and email is alice@corp.com"
    masked = masker.mask_text(text)
    
    assert "123-45-6789" not in masked
    assert "***-**-6789" in masked
    assert "alice@corp.com" not in masked
    assert "@corp.com" in masked


def test_pii_redaction_and_unredact():
    redactor = DataRedactor()
    text = "Please invoice bob@company.com with card 4111-2222-3333-4444"
    
    # 1. Static redaction
    static_res = redactor.redact(text, pseudonymize=False)
    assert "[REDACTED_EMAIL]" in static_res.redacted_text
    assert "[REDACTED_CREDIT_CARD]" in static_res.redacted_text

    # 2. Reversible pseudonymization
    pseudo_res = redactor.redact(text, pseudonymize=True)
    assert "<EMAIL_1>" in pseudo_res.redacted_text
    assert "<CREDIT_CARD_1>" in pseudo_res.redacted_text

    # Reversal
    reversed_text = redactor.unredact(pseudo_res.redacted_text, pseudo_res.token_mapping)
    assert reversed_text == text
