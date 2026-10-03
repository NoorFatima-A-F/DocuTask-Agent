"""
Unit tests for AIValidator JSON schema validation.
"""

import pytest
from app.ai.exceptions import AIValidationException
from app.ai.validator import AIValidator


def test_schema_validation_success():
    """Verifies successful JSON schema validation and confidence calculation."""
    valid_data = {
        "invoice_number": "INV-1001",
        "vendor_name": "Acme Corp",
        "total_amount": 500.0,
        "currency": "USD",
        "line_items": []
    }

    validated_dict, confidence = AIValidator.validate(valid_data, "invoice")
    assert validated_dict["invoice_number"] == "INV-1001"
    assert validated_dict["total_amount"] == 500.0
    assert 0.5 <= confidence <= 1.0


def test_schema_validation_failure():
    """Verifies exception handling for invalid field types."""
    invalid_data = {
        "total_amount": "invalid_number_string_here"
    }

    with pytest.raises(AIValidationException) as exc_info:
        AIValidator.validate(invalid_data, "invoice")

    assert "schema validation" in str(exc_info.value).lower()
