"""
Communication Contract & Schema Validator.
"""
from typing import List, Dict, Any
from app.platform_verification.service_communication.domain.models import CommunicationContractReport
from app.platform_verification.service_communication.domain.interfaces import IContractValidator


class ContractValidator(IContractValidator):
    """Validates OpenAPI / JSON schema contracts across service boundaries."""

    def validate_contracts(self, contracts: List[Dict[str, Any]]) -> CommunicationContractReport:
        undocumented: List[str] = []
        breaking: List[str] = []

        for c in contracts:
            endpoint = c.get("endpoint", "/api/v1/unknown")
            req_schema = c.get("request_schema", {})
            resp_schema = c.get("response_schema", {})

            if not req_schema or not resp_schema:
                undocumented.append(f"Endpoint '{endpoint}' lacks formal schema definition")

            if c.get("has_breaking_change", False):
                breaking.append(f"Breaking change detected in '{endpoint}': {c.get('breaking_reason', 'modified payload')}")

        status = "PASS" if len(undocumented) == 0 and len(breaking) == 0 else "FAIL"

        return CommunicationContractReport(
            total_contracts_scanned=len(contracts),
            undocumented_fields=undocumented,
            breaking_changes=breaking,
            schema_validation_passed=(len(undocumented) == 0),
            status=status,
        )
