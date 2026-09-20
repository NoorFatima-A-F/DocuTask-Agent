"""
Goal Intelligence Interfaces Package
====================================
"""

from research_validation.goal.interfaces.clock import (
    IClock, SystemClock, FrozenClock
)
from research_validation.goal.interfaces.id_generator import (
    IIdGenerator, Uuid4IdGenerator, DeterministicIdGenerator
)
from research_validation.goal.interfaces.event_bus import (
    GoalIntelligenceDomainEvent, IEventBus, InMemoryEventBus, EventHandler
)
from research_validation.goal.interfaces.repository import (
    IGoalRepository, IMissionRepository
)
from research_validation.goal.interfaces.capability_provider import (
    DiscoveredCapability, ICapabilityProvider, DefaultSystemCapabilityProvider
)

__all__ = [
    "IClock",
    "SystemClock",
    "FrozenClock",
    "IIdGenerator",
    "Uuid4IdGenerator",
    "DeterministicIdGenerator",
    "GoalIntelligenceDomainEvent",
    "IEventBus",
    "InMemoryEventBus",
    "EventHandler",
    "IGoalRepository",
    "IMissionRepository",
    "DiscoveredCapability",
    "ICapabilityProvider",
    "DefaultSystemCapabilityProvider",
]
