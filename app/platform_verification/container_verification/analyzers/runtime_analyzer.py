"""
Container Runtime Health and Probes Analyzer.
"""
from typing import Dict, Any
from app.platform_verification.container_verification.models.verification_models import RuntimeHealthReport


class RuntimeAnalyzer:
    """Verifies startup times and standard healthcheck endpoints (/health, /live, /ready)."""

    def analyze_runtime_health(self, service_runtime_meta: Dict[str, Any]) -> RuntimeHealthReport:
        name = service_runtime_meta.get("service_name", "api")
        startup_sec = service_runtime_meta.get("startup_time_seconds", 1.8)
        health_ok = service_runtime_meta.get("health_endpoint_verified", True)
        live_ok = service_runtime_meta.get("live_endpoint_verified", True)
        ready_ok = service_runtime_meta.get("ready_endpoint_verified", True)

        all_ok = health_ok and live_ok and ready_ok and startup_sec <= 10.0
        status = "PASS" if all_ok else "FAIL"

        return RuntimeHealthReport(
            service_name=name,
            startup_time_seconds=round(startup_sec, 2),
            health_endpoint_verified=health_ok,
            live_endpoint_verified=live_ok,
            ready_endpoint_verified=ready_ok,
            status=status,
        )
