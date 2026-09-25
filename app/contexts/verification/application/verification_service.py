from typing import Dict, Any, List
from ..domain.verification_domain import VerificationDefinition, VerificationDefinitionCreated
from app.shared_kernel import Result, Ok, Err, get_event_bus

class VerificationService:
    def __init__(self, repo):
        self.repo = repo

    async def create_definition(self, spec_id: str, name: str, invariants: List[str], parameters: Dict[str, Any]) -> Result[VerificationDefinition, str]:
        if not spec_id or not name:
            return Err("spec_id and name are required")
        defn = VerificationDefinition(id=spec_id, name=name, invariants=invariants, parameters=parameters)
        self.repo.save(defn)
        await get_event_bus().publish(VerificationDefinitionCreated(definition_id=spec_id, name=name))
        return Ok(defn)
