"""
14. Collective Memory Engine Subsystem
"""
from typing import Dict, List, Optional
from app.platform_workforce.models.schemas import CollectiveMemoryRecord

class CollectiveMemoryEngine:
    def __init__(self):
        self._memories: Dict[str, Dict[str, CollectiveMemoryRecord]] = {}
        self._seed_default_memories()

    def _seed_default_memories(self):
        tenant = "default-tenant"
        mems = [
            CollectiveMemoryRecord(
                id="cmem-eng-01",
                scope="DEPARTMENT",
                scope_id="ENGINEERING",
                title="Distributed Semaphore Limits on Worker Queues",
                content="Always cap concurrent Celery ingestion tasks to 64 per shard to prevent Redis saturation.",
                tags=["redis", "concurrency", "distributed"],
                author_employee_id="emp-eng-vp",
                trust_weight=0.99
            ),
            CollectiveMemoryRecord(
                id="cmem-exec-01",
                scope="EXECUTIVE",
                scope_id="EXECUTIVE",
                title="Strict Zero-Fabrication Sentinel Standard",
                content="Any confidence score below 0.85 must trigger human-in-the-loop review or multi-agent debate.",
                tags=["governance", "sentinel", "zero-fabrication"],
                author_employee_id="emp-ceo-01",
                trust_weight=1.0
            )
        ]
        self._memories[tenant] = {m.id: m for m in mems}

    def get_memories(self, tenant_id: str = "default-tenant", scope: Optional[str] = None) -> List[CollectiveMemoryRecord]:
        mems = list(self._memories.get(tenant_id, {}).values())
        if scope:
            mems = [m for m in mems if m.scope == scope]
        return mems

    def store_memory(self, title: str, content: str, author_id: str, scope: str = "DEPARTMENT", scope_id: str = "ENGINEERING", tags: Optional[List[str]] = None, tenant_id: str = "default-tenant") -> CollectiveMemoryRecord:
        rec = CollectiveMemoryRecord(
            tenant_id=tenant_id,
            scope=scope,
            scope_id=scope_id,
            title=title,
            content=content,
            tags=tags or [],
            author_employee_id=author_id
        )
        if tenant_id not in self._memories:
            self._memories[tenant_id] = {}
        self._memories[tenant_id][rec.id] = rec
        return rec

collective_memory_engine = CollectiveMemoryEngine()
