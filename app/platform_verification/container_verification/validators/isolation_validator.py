"""
Container Boundary and Runtime Isolation Validator.
"""
from typing import Dict, List
from app.platform_verification.container_verification.models.verification_models import (
    ServiceDefinition,
    ContainerBoundaryReport,
)


class IsolationValidator:
    """Evaluates single-responsibility compliance, coupling scores, and shared mutable state."""

    def validate_boundaries(self, services: Dict[str, ServiceDefinition]) -> ContainerBoundaryReport:
        total_services = len(services)
        god_containers: List[str] = []
        shared_volumes: List[str] = []
        total_dependencies = 0

        volume_owners: Dict[str, List[str]] = {}

        for name, s in services.items():
            total_dependencies += len(s.depends_on)

            # Detect God Container: e.g. service running worker + api + db
            if len(s.ports) > 2 and len(s.depends_on) == 0 and total_services > 1:
                god_containers.append(name)

            for v in s.volumes:
                vol_name = v.split(":")[0]
                if vol_name not in volume_owners:
                    volume_owners[vol_name] = []
                volume_owners[vol_name].append(name)

        for vol, owners in volume_owners.items():
            if len(owners) > 1 and not vol.startswith("/tmp"):
                shared_volumes.append(f"Volume '{vol}' shared mutably between {owners}")

        coupling = total_dependencies / max(total_services * 2, 1)
        coupling = min(1.0, coupling)
        isolation = 1.0 - (len(god_containers) * 0.3) - (len(shared_volumes) * 0.2)
        isolation = max(0.0, min(1.0, isolation))

        status = "PASS" if len(god_containers) == 0 and len(shared_volumes) == 0 else "FAIL"

        return ContainerBoundaryReport(
            containers_count=total_services,
            coupling_score=round(coupling, 2),
            isolation_score=round(isolation, 2),
            god_containers=god_containers,
            shared_mutable_volumes=shared_volumes,
            status=status,
        )
