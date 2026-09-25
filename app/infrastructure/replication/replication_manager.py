"""
Replication Manager.

Manages cross-region data replication topology, evaluates replication stream lag metrics,
and enforces RPO compliance boundaries.
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Dict, List, Optional

from app.infrastructure.replication.models import (
    ReplicationLagMetric,
    ReplicationMode,
    ReplicationStream,
)

logger = logging.getLogger("infrastructure.replication.manager")


class ReplicationManager:
    """
    Coordinates multi-region replication streams and tracks lag telemetry.
    """

    def __init__(self) -> None:
        self._streams: Dict[str, ReplicationStream] = {}
        self._lag_metrics: Dict[str, ReplicationLagMetric] = {}

    def register_stream(
        self,
        stream_id: str,
        source_region: str,
        target_region: str,
        dataset_name: str,
        mode: ReplicationMode = ReplicationMode.ASYNCHRONOUS,
        max_acceptable_lag_seconds: float = 60.0,
    ) -> ReplicationStream:
        """Register a new replication stream between source and target regions."""
        stream = ReplicationStream(
            stream_id=stream_id,
            source_region=source_region,
            target_region=target_region,
            dataset_name=dataset_name,
            mode=mode,
            max_acceptable_lag_seconds=max_acceptable_lag_seconds,
        )
        self._streams[stream_id] = stream
        logger.info(f"Registered replication stream '{stream_id}' ({source_region} -> {target_region})")
        return stream

    def record_lag(
        self,
        stream_id: str,
        lag_seconds: float,
        byte_lag: int = 0,
        unapplied_mutations: int = 0,
    ) -> ReplicationLagMetric:
        """Record real-time replication lag telemetry."""
        stream = self._streams.get(stream_id)
        if not stream:
            raise KeyError(f"Replication stream '{stream_id}' not found.")

        metric = ReplicationLagMetric(
            stream_id=stream_id,
            source_region=stream.source_region,
            target_region=stream.target_region,
            lag_seconds=lag_seconds,
            byte_lag=byte_lag,
            unapplied_mutations=unapplied_mutations,
        )
        self._lag_metrics[stream_id] = metric
        stream.last_synced_at = datetime.now(timezone.utc)

        if lag_seconds > stream.max_acceptable_lag_seconds:
            logger.warning(
                f"Replication stream '{stream_id}' lag {lag_seconds:.2f}s exceeds SLA "
                f"threshold {stream.max_acceptable_lag_seconds}s"
            )

        return metric

    def get_stream(self, stream_id: str) -> Optional[ReplicationStream]:
        return self._streams.get(stream_id)

    def get_lag_metric(self, stream_id: str) -> Optional[ReplicationLagMetric]:
        return self._lag_metrics.get(stream_id)

    def is_stream_in_sla(self, stream_id: str) -> bool:
        """Check if replication stream is within tolerable lag bounds."""
        stream = self._streams.get(stream_id)
        metric = self._lag_metrics.get(stream_id)
        if not stream or not metric:
            return False
        return metric.lag_seconds <= stream.max_acceptable_lag_seconds

    def list_streams(self) -> List[ReplicationStream]:
        return list(self._streams.values())

    def get_all_lag_metrics(self) -> List[ReplicationLagMetric]:
        return list(self._lag_metrics.values())
