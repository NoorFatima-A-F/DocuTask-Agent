"""Scenario: AI Quality & Hallucination Degradation (Low confidence, invalid math, hallucination)."""

from typing import Dict, Any


class QualityDegradationScenario:
    """Simulates semantic and extraction quality failures where HTTP is 200 but content is untrustworthy."""

    @staticmethod
    def execute(request_payload: Dict[str, Any], quality_fault: str = "LOW_CONFIDENCE") -> Dict[str, Any]:
        doc_id = request_payload.get("document_id", "DOC-UNKNOWN")

        if quality_fault == "LOW_CONFIDENCE":
            return {
                "success": True,
                "status_code": 200,
                "confidence_score": 0.42,  # Threshold is >= 0.85
                "data": {
                    "invoice_id": "INV-UNKNOWN",
                    "total_amount": 0.0,
                    "vendor_name": "Uncertain Vendor",
                },
                "is_hallucinated": False,
                "document_id": doc_id,
            }
        elif quality_fault == "HALLUCINATED_FIELDS":
            return {
                "success": True,
                "status_code": 200,
                "confidence_score": 0.95,
                "data": {
                    "invoice_id": "INV-9999",
                    "total_amount": 999999.99,  # Impossible hallucinated amount
                    "vendor_name": "Martian SpaceX Mining Corp",  # Hallucinated vendor
                },
                "is_hallucinated": True,
                "document_id": doc_id,
            }
        else:
            return {
                "success": True,
                "status_code": 200,
                "confidence_score": 0.70,
                "data": {
                    "subtotal": 100.0,
                    "tax": 10.0,
                    "total_amount": 500.0,  # Inconsistent math: 100 + 10 != 500
                },
                "math_inconsistent": True,
                "document_id": doc_id,
            }
