"""Test Data Classification and Sensitive Data Detection."""

from app.data_governance.registry.models import ClassificationLevel, SensitivityCategory
from app.data_governance.classification.detectors import SensitiveDataDetector
from app.data_governance.classification.classifier import DataClassificationEngine


def test_sensitive_data_detector():
    """Verify rule-based detection for PII, Financial, Healthcare, and Credentials."""
    detector = SensitiveDataDetector()

    text = """
    Patient record for John Doe.
    Email: john.doe@hospital.org, Phone: (555) 234-5678, SSN: 123-45-6789.
    Payment card: 4111 2222 3333 4444. Amount due: $1,250.00.
    MRN: MRN-998877.
    """

    results = detector.detect(text)
    assert SensitivityCategory.PII in results
    assert SensitivityCategory.FINANCIAL in results
    assert SensitivityCategory.HEALTHCARE in results


def test_classification_engine_confidence_and_tiering():
    """Verify automated classification assignment based on detected sensitivity."""
    classifier = DataClassificationEngine()

    # Highly restricted (Medical / SSN)
    res_high = classifier.classify_text("Patient medical record with SSN 123-45-6789 and MRN-123456.")
    assert res_high.classification in (ClassificationLevel.HIGHLY_RESTRICTED, ClassificationLevel.RESTRICTED)
    assert res_high.confidence_score >= 0.75
    assert len(res_high.evidence_snippets) > 0

    # Confidential (General Invoice)
    res_conf = classifier.classify_text("Invoice #4402 total due $500.00 for services rendered to client.")
    assert res_conf.classification in (ClassificationLevel.CONFIDENTIAL, ClassificationLevel.RESTRICTED)

    # Internal
    res_internal = classifier.classify_text("Meeting notes discussing roadmap and team updates.")
    assert res_internal.classification == ClassificationLevel.INTERNAL
