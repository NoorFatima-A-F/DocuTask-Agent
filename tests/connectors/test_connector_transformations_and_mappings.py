"""
Tests for TransformationEngine and SchemaMapper.
"""

import pytest
from app.connectors.mappings.schema_mapper import FieldMappingRule, SchemaMapper, SchemaMappingPlan
from app.connectors.transformations.engine import TransformationEngine


def test_transformation_engine_formats():
    engine = TransformationEngine()

    data = {"customer": "Acme Corp", "invoice_id": 1001, "amount": 450.50}

    # JSON roundtrip
    json_str = engine.dict_to_json(data)
    dict_from_json = engine.json_to_dict(json_str)
    assert dict_from_json["customer"] == "Acme Corp"
    assert dict_from_json["amount"] == 450.50

    # XML serialization and parsing
    xml_str = engine.dict_to_xml(data, root_tag="invoice")
    dict_from_xml = engine.xml_to_dict(xml_str)
    assert "invoice" in dict_from_xml

    # CSV serialization and parsing
    records = [
        {"id": "1", "name": "Alice", "role": "Admin"},
        {"id": "2", "name": "Bob", "role": "User"},
    ]
    csv_str = engine.records_to_csv(records)
    parsed_records = engine.csv_to_records(csv_str)
    assert len(parsed_records) == 2
    assert parsed_records[0]["name"] == "Alice"

    # Base64
    raw_bytes = b"Hello Enterprise Connector Fabric"
    b64 = engine.bytes_to_base64(raw_bytes)
    assert engine.base64_to_bytes(b64) == raw_bytes


def test_schema_mapper_declarative_rules():
    mapper = SchemaMapper()

    plan = SchemaMappingPlan(
        id="plan_lead_sync",
        rules=[
            # Direct nested path with transformation
            FieldMappingRule(
                target_field="customer.first_name",
                source_path="raw_contact.given_name",
                transform_fn_name="strip",
            ),
            FieldMappingRule(
                target_field="customer.last_name",
                source_path="raw_contact.family_name",
                transform_fn_name="uppercase",
            ),
            # Computed template
            FieldMappingRule(
                target_field="customer.full_name",
                computed_template="{raw_first} {raw_last}",
            ),
            # Default fallback
            FieldMappingRule(
                target_field="billing.currency",
                source_path="currency_code",
                default_value="USD",
            ),
            # Lookup table
            FieldMappingRule(
                target_field="status_code",
                source_path="lead_state",
                lookup_table={"NEW": "OPEN", "IN_PROGRESS": "ACTIVE", "WON": "CLOSED_WON"},
            ),
        ],
    )

    source_payload = {
        "raw_contact": {
            "given_name": "  Jordan  ",
            "family_name": "Belfort",
        },
        "raw_first": "Jordan",
        "raw_last": "Belfort",
        "lead_state": "WON",
    }

    mapped = mapper.map_schema(source_payload, plan)

    assert mapped["customer"]["first_name"] == "Jordan"
    assert mapped["customer"]["last_name"] == "BELFORT"
    assert mapped["customer"]["full_name"] == "Jordan Belfort"
    assert mapped["billing"]["currency"] == "USD"
    assert mapped["status_code"] == "CLOSED_WON"
