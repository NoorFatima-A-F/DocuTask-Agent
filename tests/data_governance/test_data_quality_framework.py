"""Test Data Quality Framework and Multidimensional Scoring."""

from datetime import datetime, timezone
from app.data_governance.quality.scoring import DataQualityScorer


def test_data_quality_scoring():
    """Verify Completeness, Freshness, Validity, and Composite Quality Scores."""
    scorer = DataQualityScorer()

    record = {
        "invoice_number": "INV-2026-900",
        "vendor_name": "Cloud Infra LLC",
        "amount_usd": 4500.50,
        "due_date": "2026-10-01",
        "line_items": [{"item": "Server compute", "cost": 4500.50}],
    }

    required_fields = ["invoice_number", "vendor_name", "amount_usd", "due_date"]
    schema_types = {
        "invoice_number": str,
        "vendor_name": str,
        "amount_usd": float,
        "line_items": list,
    }

    report = scorer.evaluate_quality(
        asset_id="asset_inv_quality_1",
        record=record,
        required_fields=required_fields,
        record_timestamp=datetime.now(timezone.utc),
        schema_types=schema_types,
    )

    assert report.composite_score >= 0.90
    assert report.completeness_score == 1.0
    assert report.validity_score == 1.0
    assert report.is_acceptable is True
