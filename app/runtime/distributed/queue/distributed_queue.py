"""
Phase 13.18: Distributed Queue & Dead-Letter Queue (DLQ)
Provider-agnostic queue abstraction with multi-priority channels and dead-letter handling.
"""

from __future__ import annotations
from typing import Dict, List, Optional, Any
from app.runtime.distributed.models.schemas import ScheduledJob, JobPriority, JobState


class DistributedQueueChannel:
    """A prioritized queue channel with aging and Dead-Letter Queue support."""

    def __init__(self, name: str, max_size: int = 10000):
        self.name = name
        self.max_size = max_size
        self._queues: Dict[JobPriority, List[ScheduledJob]] = {
            JobPriority.CRITICAL: [],
            JobPriority.HIGH: [],
            JobPriority.NORMAL: [],
            JobPriority.BATCH: [],
        }
        self._dead_letter_queue: List[ScheduledJob] = []

    def enqueue(self, job: ScheduledJob) -> bool:
        total = sum(len(q) for q in self._queues.values())
        if total >= self.max_size:
            return False
        job.state = JobState.QUEUED
        self._queues[job.priority].append(job)
        return True

    def dequeue(self) -> Optional[ScheduledJob]:
        """Dequeues according to strict priority order: CRITICAL > HIGH > NORMAL > BATCH."""
        for prio in (JobPriority.CRITICAL, JobPriority.HIGH, JobPriority.NORMAL, JobPriority.BATCH):
            if self._queues[prio]:
                job = self._queues[prio].pop(0)
                job.state = JobState.SCHEDULED
                return job
        return None

    def send_to_dlq(self, job: ScheduledJob, reason: str):
        job.state = JobState.FAILED
        job.error_message = reason
        self._dead_letter_queue.append(job)

    def get_metrics(self) -> Dict[str, Any]:
        return {
            "channel_name": self.name,
            "critical_depth": len(self._queues[JobPriority.CRITICAL]),
            "high_depth": len(self._queues[JobPriority.HIGH]),
            "normal_depth": len(self._queues[JobPriority.NORMAL]),
            "batch_depth": len(self._queues[JobPriority.BATCH]),
            "total_depth": sum(len(q) for q in self._queues.values()),
            "dlq_depth": len(self._dead_letter_queue),
        }

    def list_dlq(self, limit: int = 50) -> List[ScheduledJob]:
        return self._dead_letter_queue[-limit:]


class QueueManager:
    """Multi-channel queue manager coordinating task ingestion across the fabric."""

    def __init__(self):
        self.channels: Dict[str, DistributedQueueChannel] = {
            "agent_tasks": DistributedQueueChannel("agent_tasks"),
            "system_jobs": DistributedQueueChannel("system_jobs"),
            "eval_workloads": DistributedQueueChannel("eval_workloads"),
        }

    def get_channel(self, channel_name: str = "agent_tasks") -> DistributedQueueChannel:
        if channel_name not in self.channels:
            self.channels[channel_name] = DistributedQueueChannel(channel_name)
        return self.channels[channel_name]

    def get_all_metrics(self) -> List[Dict[str, Any]]:
        return [c.get_metrics() for c in self.channels.values()]
