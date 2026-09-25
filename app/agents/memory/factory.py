"""
Memory Subsystem Injectable Factory.
Instantiates and wires MemoryManager, BaseMemoryProvider, MemoryMetricsCollector, and memory sub-tiers.
"""

from typing import Optional
from app.agents.memory.manager import MemoryManager
from app.agents.memory.metrics import MemoryMetricsCollector
from app.agents.memory.providers import BaseMemoryProvider, InMemoryProvider


class MemoryFactory:
    """Factory container wiring memory subsystem components."""

    @staticmethod
    def create_memory_subsystem(provider: Optional[BaseMemoryProvider] = None):
        """Creates and wires MemoryManager and MemoryMetricsCollector."""
        p = provider or InMemoryProvider()
        manager = MemoryManager(provider=p)
        metrics = MemoryMetricsCollector()
        return manager, metrics
