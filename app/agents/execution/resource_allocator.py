"""
Resource Allocator.
"""

from app.agents.execution.resource_manager import ResourceManager
from app.agents.planning.resources import ResourceRequirement


class ResourceAllocator:
    """Allocates resources to tasks prior to dispatching."""

    def __init__(self, resource_manager: ResourceManager):
        self.manager = resource_manager

    def check_and_reserve(self, req: ResourceRequirement) -> bool:
        if req.resource_type == "MEMORY":
            return self.manager.allocate_memory(req.amount)
        return True
