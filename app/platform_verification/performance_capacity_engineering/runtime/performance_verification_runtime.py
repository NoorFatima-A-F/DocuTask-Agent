"""
Phase 3J.1: Performance Verification Runtime Orchestrator
Coordinates all 10 verifiers, computes 6-category certification scoring, and exports evidence manifests.
"""
from typing import Dict, Any
from app.platform_verification.performance_capacity_engineering.verifiers import (
    PerformanceArchitectureVerifier,
    BaselinePerformanceVerifier,
    WorkloadModelingVerifier,
    ControlledLoadTestVerifier,
    CapacityModelingVerifier,
    BottleneckAnalysisVerifier,
    PerformanceRegressionVerifier,
    AIPipelinePerformanceVerifier,
    DatabasePerformanceVerifier,
    QueuePerformanceVerifier,
)
from app.platform_verification.performance_capacity_engineering.scoring import (
    PerformanceCertificationScorer,
)
from app.platform_verification.performance_capacity_engineering.exporter import (
    PerformanceVerificationExporter,
)


class PerformanceVerificationRuntime:
    def __init__(self, output_dir: str = "performance_verification"):
        self.output_dir = output_dir
        self.architecture_verifier = PerformanceArchitectureVerifier()
        self.baseline_verifier = BaselinePerformanceVerifier()
        self.workload_verifier = WorkloadModelingVerifier()
        self.load_test_verifier = ControlledLoadTestVerifier()
        self.capacity_verifier = CapacityModelingVerifier()
        self.bottleneck_verifier = BottleneckAnalysisVerifier()
        self.regression_verifier = PerformanceRegressionVerifier()
        self.ai_pipeline_verifier = AIPipelinePerformanceVerifier()
        self.database_verifier = DatabasePerformanceVerifier()
        self.queue_verifier = QueuePerformanceVerifier()
        self.scorer = PerformanceCertificationScorer()
        self.exporter = PerformanceVerificationExporter(output_dir=output_dir)

    def execute_all_verifications(self) -> Dict[str, Any]:
        """Runs all 10 performance and capacity verifiers."""
        return {
            "performance_architecture": self.architecture_verifier.verify(),
            "baseline_performance": self.baseline_verifier.verify(),
            "workload_modeling": self.workload_verifier.verify(),
            "controlled_load_test": self.load_test_verifier.verify(),
            "capacity_modeling": self.capacity_verifier.verify(),
            "bottleneck_analysis": self.bottleneck_verifier.verify(),
            "performance_regression": self.regression_verifier.verify(),
            "ai_pipeline_performance": self.ai_pipeline_verifier.verify(),
            "database_performance": self.database_verifier.verify(),
            "queue_performance": self.queue_verifier.verify(),
        }

    def run_pipeline(self) -> Dict[str, Any]:
        """Executes full verification, scoring, and artifact export pipeline."""
        verification_results = self.execute_all_verifications()
        certification_report = self.scorer.compute_certification(verification_results)
        exported_files = self.exporter.export(verification_results, certification_report)

        return {
            "verification_results": verification_results,
            "certification_report": certification_report,
            "exported_files": exported_files,
            "success": certification_report.certification_granted,
        }
