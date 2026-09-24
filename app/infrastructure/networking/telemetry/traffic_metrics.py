"""Network Telemetry, Flow Metrics, and Latency Tracking."""

from dataclasses import dataclass
from typing import List
import threading


@dataclass
class NetworkMetricSummary:
    """Aggregated network telemetry metrics."""
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    total_bytes_sent: int = 0
    total_bytes_received: int = 0
    policy_denials: int = 0
    tls_handshake_failures: int = 0
    retries_count: int = 0
    avg_latency_ms: float = 0.0
    p95_latency_ms: float = 0.0
    p99_latency_ms: float = 0.0


class NetworkTelemetryCollector:
    """Collects real-time network layer metrics across services and regions."""

    def __init__(self) -> None:
        self._latencies: List[float] = []
        self._total_requests = 0
        self._successful_requests = 0
        self._failed_requests = 0
        self._bytes_sent = 0
        self._bytes_recv = 0
        self._policy_denials = 0
        self._tls_failures = 0
        self._retries = 0
        self._lock = threading.RLock()

    def record_request(
        self,
        duration_ms: float,
        success: bool = True,
        bytes_sent: int = 0,
        bytes_recv: int = 0,
        is_retry: bool = False,
    ) -> None:
        """Record a completed network request."""
        with self._lock:
            self._total_requests += 1
            if success:
                self._successful_requests += 1
            else:
                self._failed_requests += 1

            self._bytes_sent += bytes_sent
            self._bytes_recv += bytes_recv
            if is_retry:
                self._retries += 1

            self._latencies.append(duration_ms)
            if len(self._latencies) > 10000:
                self._latencies.pop(0)

    def record_policy_denial(self) -> None:
        """Increment policy denial counter."""
        with self._lock:
            self._policy_denials += 1

    def record_tls_failure(self) -> None:
        """Increment TLS handshake failure counter."""
        with self._lock:
            self._tls_failures += 1

    def get_summary(self) -> NetworkMetricSummary:
        """Calculate and return network metric summary."""
        with self._lock:
            total = self._total_requests
            if not self._latencies:
                return NetworkMetricSummary(
                    total_requests=total,
                    successful_requests=self._successful_requests,
                    failed_requests=self._failed_requests,
                    total_bytes_sent=self._bytes_sent,
                    total_bytes_received=self._bytes_recv,
                    policy_denials=self._policy_denials,
                    tls_handshake_failures=self._tls_failures,
                    retries_count=self._retries,
                )

            sorted_lat = sorted(self._latencies)
            avg = sum(sorted_lat) / len(sorted_lat)
            p95_idx = int(len(sorted_lat) * 0.95)
            p99_idx = int(len(sorted_lat) * 0.99)

            return NetworkMetricSummary(
                total_requests=total,
                successful_requests=self._successful_requests,
                failed_requests=self._failed_requests,
                total_bytes_sent=self._bytes_sent,
                total_bytes_received=self._bytes_recv,
                policy_denials=self._policy_denials,
                tls_handshake_failures=self._tls_failures,
                retries_count=self._retries,
                avg_latency_ms=avg,
                p95_latency_ms=sorted_lat[min(p95_idx, len(sorted_lat) - 1)],
                p99_latency_ms=sorted_lat[min(p99_idx, len(sorted_lat) - 1)],
            )
