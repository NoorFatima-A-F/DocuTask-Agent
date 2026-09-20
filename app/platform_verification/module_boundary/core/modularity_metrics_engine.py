"""
Modularity & Independence Quality Metrics Engine.
"""
from __future__ import annotations
from typing import Dict, List
from app.platform_verification.module_boundary.domain.interfaces import IModularityMetricsEngine
from app.platform_verification.module_boundary.domain.models import (
    ModuleDependencyEdge,
    ModuleManifest,
    ModuleQualityMetrics,
)


class EnterpriseModularityMetricsEngine(IModularityMetricsEngine):
    """Calculates Coupling, Cohesion, Independence, and Extension scores per module."""

    def calculate_metrics(
        self,
        modules: List[ModuleManifest],
        dependencies: List[ModuleDependencyEdge],
    ) -> Dict[str, ModuleQualityMetrics]:
        results: Dict[str, ModuleQualityMetrics] = {}

        for mod in modules:
            # Count outgoing and incoming edges for this module
            outgoing = sum(1 for d in dependencies if d.source_module == mod.module_name)
            incoming = sum(1 for d in dependencies if d.target_module == mod.module_name)

            # Coupling score (0..100, lower is better decoupled)
            coupling_score = min(100.0, outgoing * 12.0)

            # Cohesion score (based on owned responsibilities vs allowed deps)
            cohesion_score = max(50.0, min(100.0, 95.0 - (len(mod.forbidden_dependencies) * 2.0)))

            # Independence score (how easily can module run standalone)
            independence_score = max(0.0, 100.0 - (outgoing * 10.0))

            # Extension score
            extension_score = 96.0 if mod.isolation_enabled else 70.0

            composite = round(
                (cohesion_score * 0.35)
                + (independence_score * 0.35)
                + (extension_score * 0.20)
                + ((100.0 - coupling_score) * 0.10),
                2,
            )

            risk = "LOW" if composite >= 85.0 else ("MEDIUM" if composite >= 70.0 else "HIGH")

            results[mod.module_name] = ModuleQualityMetrics(
                module_name=mod.module_name,
                coupling_score=coupling_score,
                cohesion_score=cohesion_score,
                independence_score=independence_score,
                extension_score=extension_score,
                composite_modularity_index=composite,
                risk_level=risk,
            )

        return results
