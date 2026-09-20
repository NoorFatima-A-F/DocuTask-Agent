"""
Quarantine Manager.
Isolates poisoned documents, faulty tools, or crashing workers from further scheduling.
"""

from typing import Set


class QuarantineManager:
    """Isolates hazardous entities to prevent repeated systemic crashes."""

    def __init__(self):
        self._quarantined_tools: Set[str] = set()
        self._quarantined_workers: Set[str] = set()

    def quarantine_tool(self, tool_name: str) -> None:
        self._quarantined_tools.add(tool_name)

    def is_tool_quarantined(self, tool_name: str) -> bool:
        return tool_name in self._quarantined_tools

    def quarantine_worker(self, worker_id: str) -> None:
        self._quarantined_workers.add(worker_id)

    def is_worker_quarantined(self, worker_id: str) -> bool:
        return worker_id in self._quarantined_workers
