"""
Performance Evidence Storage and Indexing Engine.
"""
import json
from dataclasses import asdict
from typing import Dict, List, Any, Optional
from app.platform_verification.performance_chaos_verification.domain.models import (
    PerformanceBaselineReport,
    LoadTestReport,
    StressTestReport,
    SpikeTestReport,
    EnduranceTestReport,
    HorizontalScalingReport,
    BottleneckAnalysisReport,
    ChaosExperimentResult,
    ResourceAnalysisReport,
    PerformanceSloReport,
    PerformanceMetadata,
)
from app.platform_verification.performance_chaos_verification.domain.interfaces import (
    IPerformanceEvidenceStore,
)


class PerformanceEvidenceStore(IPerformanceEvidenceStore):
    """Persists and manages all 10 required JSON performance artifacts in memory / CAS."""

    def __init__(self):
        self._store: Dict[str, str] = {}

    def persist_all_reports(
        self,
        baseline: PerformanceBaselineReport,
        load_reports: List[LoadTestReport],
        stress_report: StressTestReport,
        spike_report: SpikeTestReport,
        endurance_report: EnduranceTestReport,
        scaling_report: HorizontalScalingReport,
        bottleneck_report: BottleneckAnalysisReport,
        chaos_reports: List[ChaosExperimentResult],
        resource_report: ResourceAnalysisReport,
        slo_report: PerformanceSloReport,
        metadata: PerformanceMetadata,
    ) -> Dict[str, str]:
        self._store["baseline_report.json"] = json.dumps(asdict(baseline), indent=2)
        self._store["load_report.json"] = json.dumps([asdict(r) for r in load_reports], indent=2)
        self._store["stress_report.json"] = json.dumps(asdict(stress_report), indent=2)
        self._store["spike_report.json"] = json.dumps(asdict(spike_report), indent=2)
        self._store["endurance_report.json"] = json.dumps(asdict(endurance_report), indent=2)
        self._store["scaling_report.json"] = json.dumps(asdict(scaling_report), indent=2)
        self._store["bottleneck_report.json"] = json.dumps(asdict(bottleneck_report), indent=2)
        self._store["chaos_report.json"] = json.dumps([asdict(c) for c in chaos_reports], indent=2)
        self._store["resource_report.json"] = json.dumps(asdict(resource_report), indent=2)
        self._store["slo_report.json"] = json.dumps(asdict(slo_report), indent=2)
        self._store["metadata.json"] = json.dumps(asdict(metadata), indent=2)
        return self._store

    def get_artifact(self, filename: str) -> Optional[str]:
        return self._store.get(filename)
