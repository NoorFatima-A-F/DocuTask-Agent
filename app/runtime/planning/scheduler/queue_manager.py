"""
Multi-Priority Worker Task Queue Manager.

Maintains priority-ordered scheduling queues for tasks ready for worker execution.
"""

from __future__ import annotations

import heapq
from typing import List, Optional
from app.runtime.planning.graph.node import DAGNode


class PriorityQueueManager:
    """Heap-based priority queue ordered by node priority (lower int = higher urgency)."""

    def __init__(self) -> None:
        self._heap: List[tuple[int, float, DAGNode]] = []
        self._counter = 0

    def push(self, node: DAGNode) -> None:
        """Pushes node into queue prioritized by (priority, tie-breaker, node)."""
        self._counter += 1
        heapq.heappush(self._heap, (node.priority, self._counter, node))

    def pop(self) -> Optional[DAGNode]:
        """Pops highest priority node."""
        if not self._heap:
            return None
        _, _, node = heapq.heappop(self._heap)
        return node

    def peek(self) -> Optional[DAGNode]:
        if not self._heap:
            return None
        return self._heap[0][2]

    def size(self) -> int:
        return len(self._heap)

    def is_empty(self) -> bool:
        return len(self._heap) == 0

    def clear(self) -> None:
        self._heap.clear()
        self._counter = 0
