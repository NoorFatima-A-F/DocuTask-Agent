"""
Experiment Scheduler V2 (Phase 82B.3)
=====================================
Asynchronous prioritized experiment queue with dependency blocking, concurrency
throttling, and stateful pause/resume mechanisms.
"""

from __future__ import annotations
import heapq
import threading
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Set, Tuple

from research_validation.scientific_execution.experiment_manifest import (
    ExperimentManifest, ExperimentStatus
)


class PriorityLevel(int, Enum):
    CRITICAL = 1
    HIGH = 2
    NORMAL = 3
    LOW = 4
    BACKGROUND = 5


@dataclass(order=True)
class ScheduledJob:
    priority: int
    scheduled_epoch: float
    job_id: str = field(compare=False)
    manifest: ExperimentManifest = field(compare=False)
    dependencies: Tuple[str, ...] = field(default=(), compare=False)
    status: ExperimentStatus = field(default=ExperimentStatus.SCHEDULED, compare=False)


class ExperimentSchedulerV2:
    """
    Thread-safe priority experiment scheduler.
    """

    def __init__(self, max_concurrency: int = 4):
        self.max_concurrency = max_concurrency
        self._lock = threading.Lock()
        self._queue: List[ScheduledJob] = []
        self._jobs: Dict[str, ScheduledJob] = {}
        self._completed_jobs: Set[str] = set()
        self._running_jobs: Set[str] = set()

    def submit_job(
        self,
        manifest: ExperimentManifest,
        priority: PriorityLevel = PriorityLevel.NORMAL,
        dependencies: Optional[List[str]] = None,
    ) -> ScheduledJob:
        """Submit an experiment to the prioritized scheduling queue."""
        with self._lock:
            job_id = f"job_{manifest.experiment_id}"
            deps = tuple(dependencies or [])
            job = ScheduledJob(
                priority=priority.value,
                scheduled_epoch=time.time(),
                job_id=job_id,
                manifest=manifest,
                dependencies=deps,
                status=ExperimentStatus.SCHEDULED,
            )
            self._jobs[job_id] = job
            heapq.heappush(self._queue, job)
            return job

    def get_next_runnable_job(self) -> Optional[ScheduledJob]:
        """Fetch next ready job whose dependencies have all completed."""
        with self._lock:
            if len(self._running_jobs) >= self.max_concurrency:
                return None

            temp_unready: List[ScheduledJob] = []
            runnable: Optional[ScheduledJob] = None

            while self._queue:
                job = heapq.heappop(self._queue)
                # Check if all dependencies are satisfied
                if all(dep in self._completed_jobs for dep in job.dependencies):
                    runnable = job
                    break
                else:
                    temp_unready.append(job)

            # Re-insert unready jobs
            for unready in temp_unready:
                heapq.heappush(self._queue, unready)

            if runnable:
                self._running_jobs.add(runnable.job_id)
                self._jobs[runnable.job_id].status = ExperimentStatus.RUNNING

            return runnable

    def mark_job_completed(self, job_id: str, is_success: bool = True) -> None:
        """Mark job finished and release concurrency slot."""
        with self._lock:
            self._running_jobs.discard(job_id)
            if is_success:
                self._completed_jobs.add(job_id)
                if job_id in self._jobs:
                    self._jobs[job_id].status = ExperimentStatus.COMPLETED
            else:
                if job_id in self._jobs:
                    self._jobs[job_id].status = ExperimentStatus.FAILED

    def get_job_status(self, job_id: str) -> Optional[ExperimentStatus]:
        with self._lock:
            job = self._jobs.get(job_id)
            return job.status if job else None

    def get_queue_depth(self) -> int:
        with self._lock:
            return len(self._queue)
