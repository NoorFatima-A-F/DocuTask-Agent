"""CI/CD Pipeline Stages, Types, and Results."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional


class StageType(str, Enum):
    """Supported pipeline stage categories."""
    SOURCE = "source"
    BUILD = "build"
    TEST = "test"
    SECURITY_SCAN = "security_scan"
    ARTIFACT_SIGN = "artifact_sign"
    PUBLISH = "publish"
    DEPLOY = "deploy"
    VERIFY = "verify"


class StageStatus(str, Enum):
    """Status of a pipeline stage execution."""
    PENDING = "pending"
    RUNNING = "running"
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class StageExecutionResult:
    """Outcome of a single pipeline stage execution."""
    stage_name: str
    stage_type: StageType
    status: StageStatus = StageStatus.PENDING
    duration_ms: float = 0.0
    output_artifacts: List[str] = field(default_factory=list)
    logs: List[str] = field(default_factory=list)
    error_message: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None


@dataclass
class PipelineStageConfig:
    """Configuration definition for a pipeline stage."""
    name: str
    stage_type: StageType
    enabled: bool = True
    required: bool = True
    parallel_group: Optional[str] = None  # Group identifier for parallel execution
    handler: Optional[Callable[[Dict[str, Any]], Dict[str, Any]]] = None
    retry_count: int = 1
    timeout_seconds: float = 300.0
    parameters: Dict[str, Any] = field(default_factory=dict)
