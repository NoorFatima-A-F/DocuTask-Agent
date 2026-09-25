from typing import List
from ..domain.plugins_domain import PluginRegistryAggregate, PluginRegistered
from app.shared_kernel import Result, Ok, Err, get_event_bus

class PluginService:
    def __init__(self, repo):
        self.repo = repo

    async def register_plugin(self, plugin_id: str, name: str, capabilities: List[str]) -> Result[PluginRegistryAggregate, str]:
        if not plugin_id or not name:
            return Err("plugin_id and name required")
        agg = PluginRegistryAggregate(id=plugin_id, name=name, capabilities=capabilities, status="ACTIVE")
        self.repo.save(agg)
        await get_event_bus().publish(PluginRegistered(plugin_id=plugin_id, name=name))
        return Ok(agg)
