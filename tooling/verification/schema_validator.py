"""
Verification Schema & Contract Validator.
"""
from typing import Dict, Any
import json
from pydantic import ValidationError
from app.platform_verification.domain.models import VerificationDefinition

def validate_definition_schema(json_str: str) -> Dict[str, Any]:
    try:
        data = json.loads(json_str)
        definition = VerificationDefinition(**data)
        return {"valid": True, "definition_id": definition.definition_id}
    except (json.JSONDecodeError, ValidationError) as e:
        return {"valid": False, "error": str(e)}

if __name__ == "__main__":
    sample = '''{"name": "Valid Test", "description": "Desc", "target_domain": "ENTERPRISE"}'''
    print("Schema Check:", validate_definition_schema(sample))
