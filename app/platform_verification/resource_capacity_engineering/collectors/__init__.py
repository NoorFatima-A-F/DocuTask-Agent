"""
Collectors package for Phase 3J.4 Resource Utilization & Capacity Engineering.
"""

from typing import List
from ..domain.interfaces import IResourceCollector
from .cpu_collector import CPUCollector
from .database_collector import DatabaseCollector
from .disk_collector import DiskCollector
from .memory_collector import MemoryCollector
from .network_collector import NetworkCollector
from .queue_collector import QueueCollector


def get_all_collectors() -> List[IResourceCollector]:
    return [
        CPUCollector(),
        MemoryCollector(),
        DiskCollector(),
        NetworkCollector(),
        DatabaseCollector(),
        QueueCollector(),
    ]


__all__ = [
    "CPUCollector",
    "MemoryCollector",
    "DiskCollector",
    "NetworkCollector",
    "DatabaseCollector",
    "QueueCollector",
    "get_all_collectors",
]
