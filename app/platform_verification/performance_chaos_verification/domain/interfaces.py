"""
Domain interfaces for Enterprise Performance, Scaling & Chaos Verification.
"""
from abc import ABC, abstractmethod
from typing import List, Dict
from app.platform_verification.performance_chaos_verification.domain.models import (
    PerformanceBaselineReport,
    LoadTestReport,
    StressTestReport,
    SpikeTestReport,
    EnduranceTestReport,
    ResourceAnalysisReport,
    BottleneckAnalysisReport,
    HorizontalScalingReport,
    DatabasePerformanceReport,
    AiPerformanceReport,
    ChaosExperimentResult,
    PerformanceSloReport,
    PerformanceCertificationScorecard,
    PerformanceMetadata,
)


class IPerformanceBaselineEngine(ABC):
    @abstractmethod
    def establish_baseline(self) -> PerformanceBaselineReport:
        pass


class ILoadStressGenerator(ABC):
    __test__ = False
    @abstractmethod
    def execute_load_tests(self) -> List[LoadTestReport]:
        pass

    @abstractmethod
    def execute_stress_test(self) -> StressTestReport:
        pass


class ISpikeEnduranceTester(ABC):
    __test__ = False
    @abstractmethod
    def execute_spike_test(self) -> SpikeTestReport:
        pass

    @abstractmethod
    def execute_endurance_test(self, duration_hours: float = 24.0) -> EnduranceTestReport:
        pass


class IResourceBottleneckAnalyzer(ABC):
    @abstractmethod
    def analyze_resources(self) -> ResourceAnalysisReport:
        pass

    @abstractmethod
    def identify_bottleneck(self, resource_report: ResourceAnalysisReport) -> BottleneckAnalysisReport:
        pass


class IHorizontalScalingVerifier(ABC):
    @abstractmethod
    def verify_horizontal_scaling(self) -> HorizontalScalingReport:
        pass


class IDatabaseAiPerformanceVerifier(ABC):
    @abstractmethod
    def verify_database_performance(self) -> DatabasePerformanceReport:
        pass

    @abstractmethod
    def verify_ai_workload_performance(self) -> AiPerformanceReport:
        pass


class IChaosExperimentEngine(ABC):
    @abstractmethod
    def run_chaos_experiments(self) -> List[ChaosExperimentResult]:
        pass


class IPerformanceSloValidator(ABC):
    @abstractmethod
    def validate_slos(
        self,
        baseline: PerformanceBaselineReport,
        load_tests: List[LoadTestReport],
        chaos_results: List[ChaosExperimentResult],
    ) -> PerformanceSloReport:
        pass


class IPerformanceCertificationEngine(ABC):
    @abstractmethod
    def compute_certification(
        self,
        baseline: PerformanceBaselineReport,
        load_tests: List[LoadTestReport],
        stress_test: StressTestReport,
        scaling: HorizontalScalingReport,
        resources: ResourceAnalysisReport,
        chaos: List[ChaosExperimentResult],
        slo_report: PerformanceSloReport,
    ) -> PerformanceCertificationScorecard:
        pass


class IPerformanceEvidenceStore(ABC):
    @abstractmethod
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
        pass
