from typing import Dict, Any
from ..domain.environments_domain import EnvironmentAggregate, EnvironmentReady
from app.shared_kernel import Result, Ok, Err, get_event_bus

class EnvironmentService:
    def __init__(self, repo):
        self.repo = repo

    async def register_and_validate(self, env_id: str, name: str, tier: str, profile: Dict[str, Any]) -> Result[EnvironmentAggregate, str]:
        agg = EnvironmentAggregate(id=env_id, name=name, tier=tier, is_ready=True, profile=profile)
        self.repo.save(agg)
        await get_event_bus().publish(EnvironmentReady(env_id=env_id, tier=tier))
        return Ok(agg)
