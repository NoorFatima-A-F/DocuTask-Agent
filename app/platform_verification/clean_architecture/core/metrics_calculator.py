"""
Robert C. Martin Package Coupling, Instability (I), Abstractness (A), and Distance (D) Calculator.
"""
from __future__ import annotations
from typing import Dict, List, Optional, Tuple
from app.platform_verification.clean_architecture.domain.interfaces import IDependencyMetricsCalculator
from app.platform_verification.clean_architecture.domain.models import (
    CleanArchDependencyEdge,
    ModuleQualityMetrics,
)


class EnterpriseDependencyMetricsCalculator(IDependencyMetricsCalculator):
    """Calculates Ca, Ce, Instability I = Ce / (Ca + Ce), and Distance D = |A + I - 1|."""

    def calculate_module_metrics(
        self,
        edges: List[CleanArchDependencyEdge],
        module_class_counts: Optional[Dict[str, Tuple[int, int]]] = None,
    ) -> Dict[str, ModuleQualityMetrics]:
        # Track Ca (incoming) and Ce (outgoing) per module
        ca_counts: Dict[str, int] = {}
        ce_counts: Dict[str, int] = {}
        all_modules: Set[str] = set()

        for edge in edges:
            src = edge.source_module
            tgt = edge.target_module
            all_modules.add(src)

            # Record outgoing for src
            ce_counts[src] = ce_counts.get(src, 0) + 1

            # If target is an internal module, record incoming
            if tgt.startswith("app.") or tgt.startswith("domain."):
                all_modules.add(tgt)
                ca_counts[tgt] = ca_counts.get(tgt, 0) + 1

        class_counts = module_class_counts or {}
        metrics_map: Dict[str, ModuleQualityMetrics] = {}

        for mod in all_modules:
            ca = ca_counts.get(mod, 0)
            ce = ce_counts.get(mod, 0)
            abstract_cnt, total_cnt = class_counts.get(mod, (0, max(1, ca + ce)))

            m = ModuleQualityMetrics(
                module_name=mod,
                afferent_coupling_ca=ca,
                efferent_coupling_ce=ce,
                instability_i=0.0,
                abstract_classes_count=abstract_cnt,
                total_classes_count=total_cnt,
            )
            m.calculate_metrics()
            metrics_map[mod] = m

        return metrics_map
