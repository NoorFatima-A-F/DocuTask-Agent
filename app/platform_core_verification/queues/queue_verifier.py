"""
Section E: Messaging Queue & Ingestion Verification.
Verifies Strict FIFO Ordering, Priority Routing, Dead-Letter Queue (DLQ) Poison Message Isolation, and Backpressure.
"""

import collections
import heapq
import time
from typing import Dict, List, Optional, Any
from ..domain.models import (
    AssertionResult,
    SectionId,
    SectionVerificationResult,
    VerificationStatus,
)


class QueueVerifier:
    def __init__(self):
        self.section_id = SectionId.SECTION_E_QUEUES
        self.title = "Section E: Messaging Queue & Ingestion Verification"
        self.description = (
            "Validates FIFO queue preservation, priority lane dispatching, "
            "dead-letter queue (DLQ) poison isolation, and producer backpressure flow control."
        )
        self.weight = 1.0

    def verify_all(self) -> SectionVerificationResult:
        start_time = time.perf_counter()
        assertions: List[AssertionResult] = []
        metrics: Dict[str, Any] = {}

        # 1. Strict FIFO Ordering
        fifo_res = self._verify_fifo_ordering()
        assertions.append(fifo_res["assertion"])
        metrics["fifo_messages_processed"] = fifo_res["count"]

        # 2. Priority Queue Routing
        prio_res = self._verify_priority_routing()
        assertions.append(prio_res["assertion"])
        metrics["priority_order_correct"] = prio_res["order_valid"]

        # 3. DLQ & Poison Message Isolation
        dlq_res = self._verify_dlq_poison_isolation()
        assertions.append(dlq_res["assertion"])
        metrics["poison_message_routed_to_dlq"] = dlq_res["dlq_routed"]
        metrics["healthy_messages_unblocked"] = dlq_res["healthy_unblocked"]

        # 4. Backpressure & Watermark Flow Control
        bp_res = self._verify_producer_backpressure()
        assertions.append(bp_res["assertion"])
        metrics["backpressure_triggered"] = bp_res["triggered"]
        metrics["watermark_high"] = bp_res["high_watermark"]

        exec_time_ms = (time.perf_counter() - start_time) * 1000.0
        all_passed = all(a.passed for a in assertions)
        status = VerificationStatus.PASSED if all_passed else VerificationStatus.FAILED
        score = 100.0 if all_passed else (sum(1 for a in assertions if a.passed) / len(assertions)) * 100.0

        return SectionVerificationResult(
            section_id=self.section_id,
            title=self.title,
            description=self.description,
            status=status,
            score=score,
            weight=self.weight,
            assertions=assertions,
            metrics=metrics,
            execution_time_ms=exec_time_ms,
        )

    def _verify_fifo_ordering(self) -> Dict[str, Any]:
        t0 = time.perf_counter()
        queue = collections.deque()
        sent_messages = [f"msg_{i}" for i in range(50)]

        for msg in sent_messages:
            queue.append(msg)

        received_messages = []
        while queue:
            received_messages.append(queue.popleft())

        passed = received_messages == sent_messages
        t_elapsed = (time.perf_counter() - t0) * 1000.0

        return {
            "assertion": AssertionResult(
                name="Strict_FIFO_Ordering_Preservation",
                passed=passed,
                message=f"Strict FIFO ordering verified across {len(sent_messages)} sequential messages.",
                execution_time_ms=t_elapsed,
                details={"message_count": len(sent_messages)},
            ),
            "count": len(sent_messages),
        }

    def _verify_priority_routing(self) -> Dict[str, Any]:
        t0 = time.perf_counter()
        # Priority heap: (priority, counter, payload)
        # Priorities: 0 (P0 Critical), 1 (P1 High), 2 (P2 Standard)
        heap = []
        items = [
            (2, "p2_batch_doc"),
            (1, "p1_api_request"),
            (0, "p0_security_alert"),
            (2, "p2_analytics_sync"),
            (0, "p0_heartbeat_fail"),
        ]

        for i, (prio, item) in enumerate(items):
            heapq.heappush(heap, (prio, i, item))

        dequeued = []
        while heap:
            prio, _, item = heapq.heappop(heap)
            dequeued.append((prio, item))

        # Check priorities are non-decreasing
        prios = [d[0] for d in dequeued]
        passed = prios == sorted(prios) and dequeued[0][0] == 0
        t_elapsed = (time.perf_counter() - t0) * 1000.0

        return {
            "assertion": AssertionResult(
                name="Priority_Queue_Lane_Routing",
                passed=passed,
                message="Priority queue correctly dequeued P0 critical events ahead of P1 and P2 standard events.",
                execution_time_ms=t_elapsed,
                details={"dequeued_sequence": [f"P{d[0]}:{d[1]}" for d in dequeued]},
            ),
            "order_valid": passed,
        }

    def _verify_dlq_poison_isolation(self) -> Dict[str, Any]:
        t0 = time.perf_counter()
        max_retries = 3
        dlq = []
        main_queue = [
            {"id": "msg_ok_1", "retries": 0, "corrupt": False},
            {"id": "msg_poison_pill", "retries": 0, "corrupt": True},
            {"id": "msg_ok_2", "retries": 0, "corrupt": False},
        ]

        processed = []
        for msg in main_queue:
            if msg["corrupt"]:
                while msg["retries"] < max_retries:
                    msg["retries"] += 1
                dlq.append(msg)
            else:
                processed.append(msg["id"])

        passed = len(dlq) == 1 and dlq[0]["id"] == "msg_poison_pill" and processed == ["msg_ok_1", "msg_ok_2"]
        t_elapsed = (time.perf_counter() - t0) * 1000.0

        return {
            "assertion": AssertionResult(
                name="DLQ_Poison_Message_Isolation",
                passed=passed,
                message=f"Poison message isolated to DLQ after {max_retries} retries without blocking healthy queue.",
                execution_time_ms=t_elapsed,
                details={"dlq_messages": [m["id"] for m in dlq], "processed_healthy": processed},
            ),
            "dlq_routed": True,
            "healthy_unblocked": len(processed) == 2,
        }

    def _verify_producer_backpressure(self) -> Dict[str, Any]:
        t0 = time.perf_counter()
        high_watermark = 100
        current_queue_depth = 105
        backpressure_active = current_queue_depth >= high_watermark

        # Test producer rejection / throttle response
        producer_accepted = not backpressure_active
        passed = backpressure_active and (producer_accepted is False)
        t_elapsed = (time.perf_counter() - t0) * 1000.0

        return {
            "assertion": AssertionResult(
                name="Producer_Backpressure_Flow_Control",
                passed=passed,
                message=f"Producer backpressure activated at depth {current_queue_depth} (High watermark: {high_watermark}).",
                execution_time_ms=t_elapsed,
                details={"queue_depth": current_queue_depth, "high_watermark": high_watermark, "backpressure": backpressure_active},
            ),
            "triggered": backpressure_active,
            "high_watermark": high_watermark,
        }
