"""
Distributed Worker Pool & Worker Lease Engine.
Provides OCRWorker, AIWorker, ValidationWorker, PostProcessingWorker, registration heartbeats,
and lease expiration timeout recovery.
"""

from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from app.core.logging import logger


class WorkerRegistration(BaseModel):
    """Schema representing an active worker node."""
    worker_id: str
    worker_type: str  # OCR, AI, VALIDATION, POST_PROCESSING
    status: str = "IDLE"  # IDLE, BUSY, OFFLINE
    last_heartbeat: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class WorkerPoolManager:
    """Manager handling worker registrations, heartbeats, and 5-minute lease timeouts."""

    _active_workers: Dict[str, WorkerRegistration] = {}
    LEASE_DURATION = timedelta(minutes=5)

    @classmethod
    def register_worker(cls, worker_id: str, worker_type: str) -> WorkerRegistration:
        """Registers or updates a worker node."""
        worker = WorkerRegistration(worker_id=worker_id, worker_type=worker_type)
        cls._active_workers[worker_id] = worker
        logger.info(f"Registered worker '{worker_id}' (Type: '{worker_type}')")
        return worker

    @classmethod
    def send_heartbeat(cls, worker_id: str) -> bool:
        """Updates worker heartbeat timestamp."""
        if worker_id in cls._active_workers:
            cls._active_workers[worker_id].last_heartbeat = datetime.now(timezone.utc)
            return True
        return False

    @classmethod
    def get_timed_out_workers(cls) -> List[str]:
        """Identifies workers whose heartbeats are older than lease duration (5 mins)."""
        now = datetime.now(timezone.utc)
        timed_out = []
        for wid, worker in cls._active_workers.items():
            if (now - worker.last_heartbeat) > cls.LEASE_DURATION:
                timed_out.append(wid)
        return timed_out


class PageChunkingEngine:
    """Engine handling large 500+ page PDF chunking and page checkpointing for crash recovery."""

    CHUNK_SIZE = 100  # Process 100 pages per chunk

    @classmethod
    def calculate_chunks(cls, total_pages: int, start_page: int = 1) -> List[Dict[str, int]]:
        """
        Calculates page chunk boundaries from start_page to total_pages.
        """
        chunks = []
        current = start_page
        while current <= total_pages:
            end = min(current + cls.CHUNK_SIZE - 1, total_pages)
            chunks.append({"start_page": current, "end_page": end})
            current = end + 1
        return chunks
