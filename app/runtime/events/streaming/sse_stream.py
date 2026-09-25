"""
DocuTask Agent - Server-Sent Events (SSE) Event Stream Generator
Phase 13.1: Autonomous Runtime Observability & Domain Event Platform (ARODP)
"""

import asyncio
import json
from typing import AsyncGenerator
from app.runtime.events.models.event import DomainEvent
from app.runtime.events.bus.event_bus import domain_event_bus


class SSEEventStream:
    """
    Server-Sent Events (SSE) Stream Provider.
    Yields real-time events to connected HTTP clients without polling.
    """

    @staticmethod
    async def generate_stream() -> AsyncGenerator[str, None]:
        queue: asyncio.Queue[DomainEvent] = asyncio.Queue(maxsize=500)

        async def handler(event: DomainEvent) -> None:
            try:
                queue.put_nowait(event)
            except asyncio.QueueFull:
                pass

        sub_id = f"sse-client-{id(queue)}"
        domain_event_bus.subscribe(sub_id, handler)

        try:
            while True:
                event = await queue.get()
                payload_json = json.dumps(event.to_dict())
                yield f"event: {event.event_type.value}\ndata: {payload_json}\n\n"
                queue.task_done()
        except asyncio.CancelledError:
            pass
        finally:
            domain_event_bus.unsubscribe(sub_id)
