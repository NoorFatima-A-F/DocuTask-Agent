"""
Domain models for Enterprise Verification Test Harness Framework (PART 3).
"""
from __future__ import annotations
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional


class TestLifecycleState(str, Enum):
    __test__ = False
    CREATED = "CREATED"
    VALIDATED = "VALIDATED"
    SCHEDULED = "SCHEDULED"
    EXECUTING = "EXECUTING"
    COLLECTING_EVIDENCE = "COLLECTING_EVIDENCE"
    EVALUATING = "EVALUATING"
    COMPLETED = "COMPLETED"
    ARCHIVED = "ARCHIVED"


class TestCategory(str, Enum):
    __test__ = False
    FUNCTIONAL = "functional"
    AI_QUALITY = "ai_quality"
    PERFORMANCE = "performance"
    SECURITY = "security"
    CHAOS = "chaos"
    REGRESSION = "regression"
    COMPLIANCE = "compliance"


class TestHarnessLevel(str, Enum):
    __test__ = False
    UNIT = "unit"
    COMPONENT = "component"
    INTEGRATION = "integration"
    SYSTEM = "system"
    PRODUCTION = "production"
    ADVERSARIAL = "adversarial"
    CERTIFICATION = "certification"


class ExecutionMode(str, Enum):
    SEQUENTIAL = "SEQUENTIAL"
    PARALLEL = "PARALLEL"
    CONDITIONAL = "CONDITIONAL"


class WorkerStatus(str, Enum):
    IDLE = "IDLE"
    BUSY = "BUSY"
    UNHEALTHY = "UNHEALTHY"
    OFFLINE = "OFFLINE"


@dataclass(frozen=True)
class RetryPolicy:
    """Configures retry attempts and exponential backoff."""
    max_retries: int = 3
    initial_delay_ms: float = 50.0
    backoff_factor: float = 2.0
    max_delay_ms: float = 1000.0


@dataclass
class VerificationTestSpec:
    """Declarative specification for a verification test case."""
    __test__ = False
    id: str
    name: str
    description: str
    category: TestCategory
    level: TestHarnessLevel
    environment: str
    dataset: Dict[str, str]  # {"id": "ds_01", "version": "v1.0"}
    dependencies: List[str] = field(default_factory=list)
    execution: Dict[str, Any] = field(default_factory=dict)
    validation: Dict[str, Any] = field(default_factory=dict)
    metrics: List[str] = field(default_factory=list)
    evidence: List[str] = field(default_factory=list)
    timeout_ms: int = 5000
    retry_policy: RetryPolicy = field(default_factory=RetryPolicy)


@dataclass
class VerificationContext:
    """Hermetic execution context with isolated filesystem sandboxes."""
    execution_id: str
    test_id: str
    environment: str
    dataset_version: str
    model_version: str
    config_hash: str
    start_time: str
    workspace_root: Path
    input_dir: Path
    output_dir: Path
    logs_dir: Path
    traces_dir: Path
    metrics_dir: Path
    evidence_dir: Path
    is_cleaned_up: bool = False


@dataclass
class WorkerNode:
    """Registered execution worker node in distributed worker pool."""
    worker_id: str
    hostname: str
    capabilities: List[TestCategory]
    status: WorkerStatus = WorkerStatus.IDLE
    active_job_id: Optional[str] = None
    last_heartbeat: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class ExecutionJob:
    """Represents a scheduled unit of verification work."""
    job_id: str
    test_spec: VerificationTestSpec
    context: VerificationContext
    state: TestLifecycleState = TestLifecycleState.CREATED
    retry_count: int = 0
    assigned_worker_id: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    started_at: Optional[str] = None
    completed_at: Optional[str] = None


@dataclass
class HarnessExecutionResult:
    """Detailed outcome of a single test specification execution."""
    job_id: str
    test_id: str
    state: TestLifecycleState
    passed: bool
    exit_code: int
    output_data: Dict[str, Any] = field(default_factory=dict)
    metrics_collected: Dict[str, float] = field(default_factory=dict)
    evidence_paths: List[str] = field(default_factory=list)
    error_message: Optional[str] = None
    duration_ms: float = 0.0
    retry_attempts: int = 0


@dataclass
class HarnessExecutionReport:
    """Composite report summarizing an execution batch or DAG."""
    report_id: str
    execution_mode: ExecutionMode
    total_jobs: int
    passed_jobs: int
    failed_jobs: int
    results: List[HarnessExecutionResult] = field(default_factory=list)
    duration_ms: float = 0.0
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
