"""
Verification Definition Manager: Specifications, requirement linking, invariants, and authoring.
"""
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from ..interfaces import VerificationDefinitionManagerInterface
from ...crosscutting.observability import ComponentObservability
from ...domain.models import VerificationDefinition

class VerificationDefinitionManager(VerificationDefinitionManagerInterface):
    """Manages formal verification specifications and invariant validation."""
    
    def __init__(self):
        self._definitions: Dict[str, Dict[str, Any]] = {}
        self._domain_defs: Dict[str, VerificationDefinition] = {}
        self.observability = ComponentObservability("VerificationDefinitionManager")
        self._seed_default_definitions()

    def _seed_default_definitions(self):
        d1 = VerificationDefinition(
            definition_id="def_ocr_accuracy_01",
            name="Production OCR Accuracy & CER Invariant Test",
            description="Verifies CER <= 0.02 and WER <= 0.05 across standard golden invoice datasets.",
            required_invariants=["accuracy > 0.95"],
            owner="lead_qa_architect"
        )
        self._domain_defs[d1.definition_id] = d1
        self._definitions[d1.definition_id] = {
            "spec_id": d1.definition_id,
            "name": d1.name,
            "invariants": d1.required_invariants,
            "parameters": {},
            "created_at": d1.created_at
        }

    async def create_definition(self, spec_id: str, name: str, invariants: List[str], parameters: Dict[str, Any]) -> Dict[str, Any]:
        self.observability.record_operation(1.2)
        spec = {
            "spec_id": spec_id,
            "name": name,
            "invariants": invariants,
            "parameters": parameters,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        self._definitions[spec_id] = spec
        return spec

    async def validate_definition(self, spec_id: str) -> Dict[str, Any]:
        self.observability.record_operation(0.9)
        if spec_id not in self._definitions:
            return {"valid": False, "error": "Spec not found"}
        spec = self._definitions[spec_id]
        has_invariants = len(spec.get("invariants", [])) > 0
        return {"valid": has_invariants, "spec_id": spec_id, "issues": [] if has_invariants else ["No invariants defined"]}

    async def get_definition(self, spec_id: str) -> Optional[Dict[str, Any]]:
        self.observability.record_operation(0.6)
        return self._definitions.get(spec_id)

    def list_definitions(self, domain: Optional[str] = None) -> List[VerificationDefinition]:
        self.observability.record_operation(1.0)
        return list(self._domain_defs.values())
