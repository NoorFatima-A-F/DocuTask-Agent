from app.core.security import sanitize_log_input
"""
Priority Message Broker Subsystem.
Implements HIGH, MEDIUM, and LOW priority queues with starvation prevention.
"""

import asyncio
from typing import Any, Dict, List, Optional
from app.core.logging import logger


class PriorityMessageBroker:
    """Message broker supporting priority queues with anti-starvation mechanics."""

    def __init__(self):
        self.high_queue: asyncio.Queue = asyncio.Queue()
        self.medium_queue: asyncio.Queue = asyncio.Queue()
        self.low_queue: asyncio.Queue = asyncio.Queue()
        self._starvation_counter = 0

    async def enqueue(self, payload: Dict[str, Any], priority: str = "MEDIUM") -> bool:
        """
        Enqueues payload to appropriate priority queue in <100ms.
        """
        prio = priority.upper().strip()
        if prio == "HIGH":
            await self.high_queue.put(payload)
        elif prio == "LOW":
            await self.low_queue.put(payload)
        else:
            await self.medium_queue.put(payload)

        logger.info(f"Enqueued job '{sanitize_log_input(payload.get('job_id'))}' with priority '{sanitize_log_input(prio)}'")
        return True

    async def dequeue(self) -> Optional[Dict[str, Any]]:
        """
        Dequeues next job with anti-starvation mechanics (serving LOW queue after every 10 HIGH/MEDIUM requests).
        """
        self._starvation_counter += 1

        # Anti-starvation check
        if self._starvation_counter >= 10 and not self.low_queue.empty():
            self._starvation_counter = 0
            return await self.low_queue.get()

        if not self.high_queue.empty():
            return await self.high_queue.get()
        if not self.medium_queue.empty():
            return await self.medium_queue.get()
        if not self.low_queue.empty():
            self._starvation_counter = 0
            return await self.low_queue.get()

        return None

    def get_metrics(self) -> Dict[str, int]:
        """Returns current queue depths."""
        return {
            "high_queue_depth": self.high_queue.qsize(),
            "medium_queue_depth": self.medium_queue.qsize(),
            "low_queue_depth": self.low_queue.qsize(),
            "total_waiting_jobs": self.high_queue.qsize() + self.medium_queue.qsize() + self.low_queue.qsize()
        }


# Global broker singleton instance
job_broker = PriorityMessageBroker()
