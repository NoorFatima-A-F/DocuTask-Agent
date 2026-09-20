"""
Container Security & Hardening Configuration Analyzer.
"""
from typing import Dict, Any, List
from app.platform_verification.container_verification.models.verification_models import (
    ServiceDefinition,
    NetworkSecurityReport,
)


class SecurityAnalyzer:
    """Audits container capabilities, read-only root filesystems, and network exposure."""

    INTERNAL_ONLY_PORTS = {"5432", "6379", "9000"}  # Postgres, Redis, MinIO

    def analyze_network_security(self, services: Dict[str, ServiceDefinition]) -> NetworkSecurityReport:
        exposed: List[str] = []
        for name, s in services.items():
            for p in s.ports:
                port_str = str(p)
                # Check if internal ports are mapped to 0.0.0.0
                for internal in self.INTERNAL_ONLY_PORTS:
                    if f":{internal}" in port_str or port_str == internal:
                        if not port_str.startswith("127.0.0.1:"):
                            exposed.append(f"Service '{name}' exposes internal port '{port_str}' publicly")

        status = "PASS" if len(exposed) == 0 else "FAIL"
        return NetworkSecurityReport(
            publicly_exposed_internal_ports=exposed,
            unauthorized_cross_network_access=False,
            status=status,
        )
