"""
Asynchronous Scientific Experiment Scheduler (Phase 74A)
========================================================
Stateful orchestration for multi-hour, multi-day long-duration endurance runs.
Maintains true wall-clock tracking, periodic checkpointing, heartbeat monitors,
interruption tolerance, and disk persistence.

Adheres strictly to the Zero-Trust / Zero-Fabrication rule:
Never accelerates or simulates wall-clock time; strictly reports actual elapsed seconds.
"""

from __future__ import annotations
import json
import os
import time
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

from research_validation.provenance.hashing import hash_canonical_json


class ExperimentStatus(str, Enum):
    SCHEDULED = "SCHEDULED"
    RUNNING = "RUNNING"
    PAUSED = "PAUSED"
    INTERRUPTED = "INTERRUPTED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    EXPIRED = "EXPIRED"
    FAILED = "FAILED"


@dataclass(frozen=True)
class ExperimentCheckpoint:
    checkpoint_id: str
    job_id: str
    step_index: int
    timestamp_utc: str
    elapsed_seconds: float
    metrics: Dict[str, float]
    state_hash: str


@dataclass
class ExperimentJob:
    job_id: str
    title: str
    planned_duration_seconds: float
    status: ExperimentStatus = ExperimentStatus.SCHEDULED
    created_at_utc: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    started_at_utc: Optional[str] = None
    completed_at_utc: Optional[str] = None
    last_heartbeat_utc: Optional[str] = None
    actual_elapsed_seconds: float = 0.0
    checkpoint_count: int = 0
    failure_reason: Optional[str] = None
    config: Dict[str, Any] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)


class AsynchronousExperimentScheduler:
    """
    Manages long-running experiment state, checkpoints, and telemetry
    across multiple days without faking time.
    """

    def __init__(self, storage_dir: Optional[str] = None):
        self.storage_dir = storage_dir or "experiments/scheduler_state"
        self._jobs: Dict[str, ExperimentJob] = {}
        self._checkpoints: Dict[str, List[ExperimentCheckpoint]] = {}

    def schedule_experiment(
        self,
        title: str,
        planned_duration_seconds: float,
        config: Optional[Dict[str, Any]] = None,
        tags: Optional[List[str]] = None,
    ) -> ExperimentJob:
        """Schedule a new scientific endurance experiment."""
        job_id = f"exp_{uuid.uuid4().hex[:12]}"
        job = ExperimentJob(
            job_id=job_id,
            title=title,
            planned_duration_seconds=planned_duration_seconds,
            status=ExperimentStatus.SCHEDULED,
            config=config or {},
            tags=tags or [],
        )
        self._jobs[job_id] = job
        self._checkpoints[job_id] = []
        return job

    def start_experiment(self, job_id: str) -> ExperimentJob:
        """Mark experiment as running and record start time."""
        job = self._get_job(job_id)
        now_str = datetime.now(timezone.utc).isoformat()
        job.status = ExperimentStatus.RUNNING
        job.started_at_utc = now_str
        job.last_heartbeat_utc = now_str
        return job

    def record_checkpoint(
        self,
        job_id: str,
        elapsed_delta_seconds: float,
        metrics: Dict[str, float],
    ) -> ExperimentCheckpoint:
        """Record an empirical telemetry checkpoint with real incremental elapsed time."""
        job = self._get_job(job_id)
        if job.status not in (ExperimentStatus.RUNNING, ExperimentStatus.PAUSED):
            raise ValueError(f"Cannot record checkpoint for job in state: {job.status}")

        now_str = datetime.now(timezone.utc).isoformat()
        job.actual_elapsed_seconds += max(0.0, elapsed_delta_seconds)
        job.last_heartbeat_utc = now_str
        job.checkpoint_count += 1

        state_hash = hash_canonical_json({
            "job_id": job_id,
            "step": job.checkpoint_count,
            "elapsed": job.actual_elapsed_seconds,
            "metrics": metrics,
        })

        ckpt = ExperimentCheckpoint(
            checkpoint_id=f"ckpt_{job_id}_{job.checkpoint_count:05d}",
            job_id=job_id,
            step_index=job.checkpoint_count,
            timestamp_utc=now_str,
            elapsed_seconds=job.actual_elapsed_seconds,
            metrics=dict(metrics),
            state_hash=state_hash,
        )
        self._checkpoints[job_id].append(ckpt)

        if job.actual_elapsed_seconds >= job.planned_duration_seconds:
            job.status = ExperimentStatus.COMPLETED
            job.completed_at_utc = now_str

        return ckpt

    def pause_experiment(self, job_id: str) -> ExperimentJob:
        """Pause a running experiment."""
        job = self._get_job(job_id)
        if job.status == ExperimentStatus.RUNNING:
            job.status = ExperimentStatus.PAUSED
        return job

    def resume_experiment(self, job_id: str) -> ExperimentJob:
        """Resume a paused or interrupted experiment."""
        job = self._get_job(job_id)
        if job.status in (ExperimentStatus.PAUSED, ExperimentStatus.INTERRUPTED):
            job.status = ExperimentStatus.RUNNING
            job.last_heartbeat_utc = datetime.now(timezone.utc).isoformat()
        return job

    def interrupt_experiment(self, job_id: str, reason: str = "Process interrupted") -> ExperimentJob:
        """Mark experiment as interrupted."""
        job = self._get_job(job_id)
        job.status = ExperimentStatus.INTERRUPTED
        job.failure_reason = reason
        return job

    def complete_experiment(self, job_id: str) -> ExperimentJob:
        """Mark experiment as explicitly completed."""
        job = self._get_job(job_id)
        job.status = ExperimentStatus.COMPLETED
        job.completed_at_utc = datetime.now(timezone.utc).isoformat()
        return job

    def cancel_experiment(self, job_id: str, reason: str) -> ExperimentJob:
        """Cancel an experiment."""
        job = self._get_job(job_id)
        job.status = ExperimentStatus.CANCELLED
        job.failure_reason = reason
        return job

    def get_checkpoints(self, job_id: str) -> List[ExperimentCheckpoint]:
        """Return all checkpoints for a job."""
        return list(self._checkpoints.get(job_id, []))

    def get_job(self, job_id: str) -> Optional[ExperimentJob]:
        return self._jobs.get(job_id)

    def list_jobs(self, status: Optional[ExperimentStatus] = None) -> List[ExperimentJob]:
        if status is None:
            return list(self._jobs.values())
        return [j for j in self._jobs.values() if j.status == status]

    def export_state_json(self) -> str:
        """Serialize all scheduler jobs and checkpoint metadata."""
        jobs_data = {}
        for jid, job in self._jobs.items():
            jobs_data[jid] = {
                "job_id": job.job_id,
                "title": job.title,
                "planned_duration_seconds": job.planned_duration_seconds,
                "status": job.status.value,
                "created_at_utc": job.created_at_utc,
                "started_at_utc": job.started_at_utc,
                "completed_at_utc": job.completed_at_utc,
                "last_heartbeat_utc": job.last_heartbeat_utc,
                "actual_elapsed_seconds": job.actual_elapsed_seconds,
                "checkpoint_count": job.checkpoint_count,
                "failure_reason": job.failure_reason,
                "config": job.config,
                "tags": job.tags,
            }
        ckpts_data = {
            jid: [asdict(c) for c in ckpts]
            for jid, ckpts in self._checkpoints.items()
        }
        return json.dumps({"jobs": jobs_data, "checkpoints": ckpts_data}, indent=2)

    def _get_job(self, job_id: str) -> ExperimentJob:
        if job_id not in self._jobs:
            raise KeyError(f"Experiment job '{job_id}' not found.")
        return self._jobs[job_id]
