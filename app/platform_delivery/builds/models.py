"""Declarative Build Definitions and Structured Test Evidence Models."""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
import uuid


class PipelineStageType(str, Enum):
    """Supported pipeline execution stages (Req 16 & 17)."""
    LINT = "LINT"
    TYPECHECK = "TYPECHECK"
    UNIT_TEST = "UNIT_TEST"
    INTEGRATION_TEST = "INTEGRATION_TEST"
    SECURITY_SCAN = "SECURITY_SCAN"
    DEPENDENCY_AUDIT = "DEPENDENCY_AUDIT"
    SECRET_SCAN = "SECRET_SCAN"
    CONTAINER_SCAN = "CONTAINER_SCAN"
    BUILD = "BUILD"
    SBOM = "SBOM"
    PROVENANCE = "PROVENANCE"
    SIGN = "SIGN"
    PUBLISH = "PUBLISH"


@dataclass
class TestEvidence:
    """Structured, verifiable test execution evidence (Req 18)."""
    test_run_id: str = field(default_factory=lambda: f"test-{uuid.uuid4().hex[:8]}")
    suite: str = "core-test-suite"
    tests_collected: int = 0
    passed: int = 0
    failed: int = 0
    skipped: int = 0
    duration: float = 0.0
    coverage: float = 0.0
    environment: str = "ci"
    commit_sha: str = ""
    artifact_digest: str = ""
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    @property
    def is_successful(self) -> bool:
        return self.failed == 0 and self.tests_collected > 0 and self.passed == self.tests_collected - self.skipped

    def to_dict(self) -> Dict[str, Any]:
        return {
            "test_run_id": self.test_run_id,
            "suite": self.suite,
            "tests_collected": self.tests_collected,
            "passed": self.passed,
            "failed": self.failed,
            "skipped": self.skipped,
            "duration": self.duration,
            "coverage": self.coverage,
            "environment": self.environment,
            "commit_sha": self.commit_sha,
            "artifact_digest": self.artifact_digest,
            "timestamp": self.timestamp.isoformat(),
            "is_successful": self.is_successful,
        }


@dataclass
class BuildStageResult:
    """Outcome of a single build pipeline stage."""
    stage_type: PipelineStageType
    passed: bool
    duration_ms: float
    output_data: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class BuildResult:
    """Consolidated build execution record with reproducibility metadata (Req 19)."""
    build_id: str
    source_commit: str
    build_tool_version: str
    dependencies_hash: str
    base_image_digest: str
    build_parameters: Dict[str, Any]
    build_environment: str
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    artifact_digest: Optional[str] = None
    stage_results: List[BuildStageResult] = field(default_factory=list)
    test_evidence: Optional[TestEvidence] = None
    success: bool = False
