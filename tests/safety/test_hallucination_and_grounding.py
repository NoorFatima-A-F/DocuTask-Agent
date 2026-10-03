"""Tests for Grounding Verification and Numeric Hallucination Detection."""

from app.safety.gateway.context import KnowledgeChunk, SourceTrustLevel
from app.safety.hallucination.grounding import GroundingVerifier
from app.safety.hallucination.detector import HallucinationDetector


def test_grounding_verifier_supported_and_unsupported_claims():
    verifier = GroundingVerifier()
    chunks = [
        KnowledgeChunk(
            content="Acme Corp total revenue for FY2025 was $45.2 million with a net profit margin of 18%.",
            source_name="annual_report_2025.pdf",
            trust_level=SourceTrustLevel.DOCUMENT,
        )
    ]

    # Grounded statement
    grounded_output = "Acme Corp reported $45.2 million in total revenue for FY2025."
    rep_grounded = verifier.verify_grounding(grounded_output, chunks)
    assert rep_grounded.is_grounded is True
    assert rep_grounded.grounding_score >= 0.70

    # Hallucinated statement
    hallucinated_output = "Acme Corp announced an acquisition of Quantum Robotics in Tokyo for $900 million."
    rep_hallucinated = verifier.verify_grounding(hallucinated_output, chunks)
    assert rep_hallucinated.is_grounded is False
    assert rep_hallucinated.grounding_score < 0.70


def test_hallucination_detector_numeric_inventions():
    detector = HallucinationDetector()
    chunks = [
        KnowledgeChunk(
            content="The total invoice amount is $1,250.00 payable within 30 days.",
            source_name="invoice.pdf",
        )
    ]

    # Output with fabricated currency figure $9,999.00
    output_text = "The invoice states a total balance of $9,999.00."
    is_hal, violations, report = detector.detect(output_text, chunks)
    
    assert is_hal is True
    assert any("Invented numeric figure '$9,999.00'" in v.message for v in violations)
