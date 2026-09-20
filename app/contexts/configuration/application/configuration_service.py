from typing import Dict, Any, Optional
import hashlib
import json
from ..domain.configuration_domain import ConfigurationAggregate, ConfigurationSnapshotCreated
from app.shared_kernel import Result, Ok, get_event_bus

class ConfigurationService:
    def __init__(self, repo):
        self.repo = repo

    async def resolve_snapshot(self, config_id: str, tier: str, overrides: Optional[Dict[str, Any]] = None) -> Result[ConfigurationAggregate, str]:
        params = {"timeout_seconds": 300, "precision": "float32", "tier": tier}
        if overrides:
            params.update(overrides)
        serialized = json.dumps(params, sort_keys=True)
        h = hashlib.sha256(serialized.encode("utf-8")).hexdigest()
        agg = ConfigurationAggregate(id=config_id, tier=tier, parameters=params, snapshot_hash=h)
        self.repo.save(agg)
        await get_event_bus().publish(ConfigurationSnapshotCreated(config_id=config_id, snapshot_hash=h))
        return Ok(agg)
