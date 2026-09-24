"""
Cross-Agent Experience Memory
Shared enterprise experience pool for instant retrieval and reuse of past execution successes.
"""
from typing import Dict, List
from ..models.schemas import ExperienceMemoryEntry

class CrossAgentExperienceMemory:
    def __init__(self):
        self._entries: Dict[str, ExperienceMemoryEntry] = {}

    def store_experience(
        self,
        tenant_id: str,
        task_fingerprint: str,
        agent_id: str,
        input_pattern: str,
        successful_trace: List[str],
        metrics: Dict[str, float],
        reusable_knowledge: str
    ) -> ExperienceMemoryEntry:
        entry = ExperienceMemoryEntry(
            tenant_id=tenant_id,
            task_fingerprint=task_fingerprint,
            agent_id=agent_id,
            input_pattern=input_pattern,
            successful_execution_trace=successful_trace,
            performance_metrics=metrics,
            reusable_knowledge=reusable_knowledge
        )
        self._entries[entry.id] = entry
        return entry

    def query_experience(self, tenant_id: str, task_fingerprint: str) -> List[ExperienceMemoryEntry]:
        results = [
            e for e in self._entries.values()
            if e.tenant_id == tenant_id and (task_fingerprint.lower() in e.task_fingerprint.lower() or task_fingerprint.lower() in e.input_pattern.lower())
        ]
        for r in results:
            r.reuse_count += 1
        return results

    def list_all_experiences(self, tenant_id: str) -> List[ExperienceMemoryEntry]:
        return [e for e in self._entries.values() if e.tenant_id == tenant_id]
