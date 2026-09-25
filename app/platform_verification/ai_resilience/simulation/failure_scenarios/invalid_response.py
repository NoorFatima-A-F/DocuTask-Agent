"""Scenario: Invalid / Malformed AI Response (Broken JSON, missing keys, plain text)."""

from typing import Dict, Any


class InvalidResponseScenario:
    """Simulates malformed and schema-violating AI responses."""

    @staticmethod
    def execute(request_payload: Dict[str, Any], corruption_type: str = "SYNTAX_ERROR") -> Dict[str, Any]:
        doc_id = request_payload.get("document_id", "DOC-UNKNOWN")

        if corruption_type == "SYNTAX_ERROR":
            raw_output = '{"invoice_id": "INV-1099", "total_amount": '  # Truncated JSON
            return {
                "success": True,
                "status_code": 200,
                "raw_text": raw_output,
                "is_valid_json": False,
                "corruption_type": "SYNTAX_ERROR",
                "document_id": doc_id,
            }
        elif corruption_type == "MISSING_REQUIRED_FIELDS":
            raw_output = '{"vendor_name": "Acme Corp"}'  # Missing invoice_id, total_amount, currency
            return {
                "success": True,
                "status_code": 200,
                "raw_text": raw_output,
                "is_valid_json": True,
                "parsed_data": {"vendor_name": "Acme Corp"},
                "corruption_type": "MISSING_REQUIRED_FIELDS",
                "document_id": doc_id,
            }
        else:
            raw_output = "I have processed your invoice and the amount is one thousand dollars."
            return {
                "success": True,
                "status_code": 200,
                "raw_text": raw_output,
                "is_valid_json": False,
                "corruption_type": "UNSTRUCTURED_PLAIN_TEXT",
                "document_id": doc_id,
            }
