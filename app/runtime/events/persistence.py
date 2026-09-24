# Event Store and Persistence
from __future__ import annotations
import asyncio
from collections import defaultdict
from typing import Dict, List, Optional
from app.runtime.events.base import RuntimeEvent

class EventStore:
    def __init__(self):
        self._events: List[RuntimeEvent] = []
        self._by_id: Dict[str, RuntimeEvent] = {}
        self._by_mission: Dict[str, List[RuntimeEvent]] = defaultdict(list)
        self._by_agent: Dict[str, List[RuntimeEvent]] = defaultdict(list)
        self._by_trace: Dict[str, List[RuntimeEvent]] = defaultdict(list)
        self._lock = asyncio.Lock()

    async def append(self, event: RuntimeEvent):
        async with self._lock:
            self._events.append(event)
            self._by_id[event.event_id] = event
            if event.mission_id:
                self._by_mission[event.mission_id].append(event)
            if event.agent_id:
                self._by_agent[event.agent_id].append(event)
            if event.trace_id:
                self._by_trace[event.trace_id].append(event)

    async def append_batch(self, events: List[RuntimeEvent]):
        async with self._lock:
            for event in events:
                self._events.append(event)
                self._by_id[event.event_id] = event
                if event.mission_id:
                    self._by_mission[event.mission_id].append(event)
                if event.agent_id:
                    self._by_agent[event.agent_id].append(event)
                if event.trace_id:
                    self._by_trace[event.trace_id].append(event)

    async def get_by_id(self, event_id: str):
        async with self._lock:
            return self._by_id.get(event_id)

    async def query(self, mission_id: Optional[str] = None, agent_id: Optional[str] = None, event_types: Optional[List[str]] = None, since_sequence: Optional[int] = None, limit: int = 500, reverse: bool = False):
        async with self._lock:
            if mission_id:
                candidates = self._by_mission.get(mission_id, [])
            elif agent_id:
                candidates = self._by_agent.get(agent_id, [])
            else:
                candidates = self._events
            results: List[RuntimeEvent] = []
            type_set = set(event_types) if event_types else None
            for ev in candidates:
                if since_sequence is not None and ev.sequence_number <= since_sequence:
                    continue
                if type_set and ev.event_type not in type_set:
                    continue
                if agent_id and ev.agent_id != agent_id:
                    continue
                results.append(ev)
            if reverse:
                results.reverse()
            return results[:limit]

    async def total_count(self):
        async with self._lock:
            return len(self._events)
