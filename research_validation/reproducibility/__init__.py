"""Reproducibility & cross-platform verification module."""

from research_validation.reproducibility.reproduce_all import (
    MasterReproducibilityOrchestrator, MasterReproducibilityReport,
    ReproducibilityVerdict, StageResult
)
from research_validation.reproducibility.cross_platform_runner import (
    CrossPlatformRunner, CrossPlatformDivergenceReport, PlatformExecutionRecord, PlatformTarget
)
from research_validation.reproducibility.cross_architecture_runner import (
    CrossArchitectureRunner, CrossArchitectureReport, ArchExecutionRecord, ArchitectureTarget
)
from research_validation.reproducibility.environment_diff import (
    EnvironmentDiffEngine, EnvironmentDiffReport, PackageVersionDelta
)
from research_validation.reproducibility.binary_reproducibility import (
    BinaryReproducibilityAnalyzer, BinaryReproducibilityReport, BinaryArtifactDigest
)
from research_validation.reproducibility.execution_diff import (
    ExecutionDiffComparator, ExecutionTraceDiffReport, ExecutionStepDelta
)
