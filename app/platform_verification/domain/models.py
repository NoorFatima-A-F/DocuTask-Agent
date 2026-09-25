"""
Enterprise Verification Core Domain Models.
Defines types and data models for all 15 core architectural components.
"""
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
import uuid


class VerificationStage(str, Enum):
    PRE_FLIGHT_DISCOVERY = "PRE_FLIGHT_DISCOVERY"
    DATASET_ACQUISITION = "DATASET_ACQUISITION"
    ENVIRONMENT_PROVISIONING = "ENVIRONMENT_PROVISIONING"
    INVARIANT_REGISTRATION = "INVARIANT_REGISTRATION"
    PROBABILISTIC_EXECUTION = "PROBABILISTIC_EXECUTION"
    METRIC_COMPUTATION = "METRIC_COMPUTATION"
    STATISTICAL_ANALYSIS = "STATISTICAL_ANALYSIS"
    EVIDENCE_SEALING = "EVIDENCE_SEALING"
    QUALITY_GATE_EVALUATION = "QUALITY_GATE_EVALUATION"
    COMPLIANCE_CERTIFICATION = "COMPLIANCE_CERTIFICATION"
    TELEMETRY_EXPORT = "TELEMETRY_EXPORT"
    POST_FLIGHT_TEARDOWN = "POST_FLIGHT_TEARDOWN"


class VerificationStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    IN_PROGRESS = "IN_PROGRESS"
    PASSED = "PASSED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    ERROR = "ERROR"


class VerificationLifecycleStage(str, Enum):
    STAGE_1_DEFINITION = "STAGE_1_DEFINITION"
    STAGE_2_ENVIRONMENT = "STAGE_2_ENVIRONMENT"
    STAGE_3_DATASET = "STAGE_3_DATASET"
    STAGE_4_PLANNING = "STAGE_4_PLANNING"
    STAGE_5_EXECUTION = "STAGE_5_EXECUTION"
    STAGE_6_EVIDENCE = "STAGE_6_EVIDENCE"
    STAGE_7_METRICS = "STAGE_7_METRICS"
    STAGE_8_STATISTICAL = "STAGE_8_STATISTICAL"
    STAGE_9_QUALITY_GATES = "STAGE_9_QUALITY_GATES"
    STAGE_9_QUALITY_GATE = "STAGE_9_QUALITY_GATE"
    STAGE_10_REPORT = "STAGE_10_REPORT"
    STAGE_10_CERTIFICATION = "STAGE_10_CERTIFICATION"
    STAGE_11_CERTIFICATION = "STAGE_11_CERTIFICATION"
    STAGE_11_TELEMETRY = "STAGE_11_TELEMETRY"
    STAGE_12_ARCHIVAL = "STAGE_12_ARCHIVAL"


class StageExecutionRecord(BaseModel):
    stage: Any
    started_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    completed_at: Optional[str] = None
    duration_ms: float = 0.0
    status: VerificationStatus = VerificationStatus.PASSED
    summary: str = ""
    details: Dict[str, Any] = Field(default_factory=dict)


class DatasetClass(str, Enum):
    HAPPY_PATH = "HAPPY_PATH"
    BOUNDARY = "BOUNDARY"
    NEGATIVE = "NEGATIVE"
    ADVERSARIAL = "ADVERSARIAL"
    REGRESSION = "REGRESSION"
    STRESS = "STRESS"
    SYNTHETIC = "SYNTHETIC"
    PRODUCTION_SNAPSHOT = "PRODUCTION_SNAPSHOT"
    MULTILINGUAL = "MULTILINGUAL"
    BENCHMARK = "BENCHMARK"
    SMOKE = "SMOKE"


class EnvironmentType(str, Enum):
    DEVELOPMENT = "DEVELOPMENT"
    INTEGRATION = "INTEGRATION"
    STAGING = "STAGING"
    PRODUCTION_SHADOW = "PRODUCTION_SHADOW"
    CHAOS = "CHAOS"
    SECURITY_LAB = "SECURITY_LAB"
    BENCHMARK = "BENCHMARK"


class EvidenceType(str, Enum):
    LOG = "LOG"
    TRACE = "TRACE"
    INPUT = "INPUT"
    OUTPUT = "OUTPUT"
    METRIC = "METRIC"
    ARTIFACT = "ARTIFACT"
    SCREENSHOT = "SCREENSHOT"
    DOCUMENT = "DOCUMENT"
    API_EXCHANGE = "API_EXCHANGE"
    PROMPT = "PROMPT"
    MODEL_RESPONSE = "MODEL_RESPONSE"
    TOOL_INVOCATION = "TOOL_INVOCATION"
    EXCEPTION = "EXCEPTION"


class MetricCategory(str, Enum):
    CORRECTNESS = "CORRECTNESS"
    PERFORMANCE = "PERFORMANCE"
    RESOURCE = "RESOURCE"
    AI_QUALITY = "AI_QUALITY"
    SECURITY = "SECURITY"
    COST = "COST"
    RELIABILITY = "RELIABILITY"
    STATISTICAL = "STATISTICAL"


class ReportFormat(str, Enum):
    TECHNICAL = "TECHNICAL"
    EXECUTIVE = "EXECUTIVE"
    COMPLIANCE = "COMPLIANCE"
    BENCHMARK = "BENCHMARK"
    AI_EVALUATION = "AI_EVALUATION"


class AuditEventType(str, Enum):
    DEFINITION_PUBLISHED = "DEFINITION_PUBLISHED"
    EXECUTION_STARTED = "EXECUTION_STARTED"
    EXECUTION_COMPLETED = "EXECUTION_COMPLETED"
    GATE_EVALUATED = "GATE_EVALUATED"
    CERTIFICATE_ISSUED = "CERTIFICATE_ISSUED"
    EVIDENCE_SEALED = "EVIDENCE_SEALED"
    MANUAL_OVERRIDE = "MANUAL_OVERRIDE"


class ConfidenceInterval(BaseModel):
    lower: float = 0.0
    upper: float = 1.0
    lower_bound: float = 0.0
    upper_bound: float = 1.0
    confidence_level: float = 0.95
    sample_size: int = 1000
    p_value: Optional[float] = None
    p_value_against_baseline: Optional[float] = None
    drift_detected: bool = False

    def __init__(self, **data):
        if "lower_bound" in data and "lower" not in data:
            data["lower"] = data["lower_bound"]
        elif "lower" in data and "lower_bound" not in data:
            data["lower_bound"] = data["lower"]
        if "upper_bound" in data and "upper" not in data:
            data["upper"] = data["upper_bound"]
        elif "upper" in data and "upper_bound" not in data:
            data["upper_bound"] = data["upper"]
        if "p_value" in data and "p_value_against_baseline" not in data:
            data["p_value_against_baseline"] = data["p_value"]
        elif "p_value_against_baseline" in data and "p_value" not in data:
            data["p_value"] = data["p_value_against_baseline"]
        super().__init__(**data)


class MetricResult(BaseModel):
    name: str = ""
    metric_name: str = ""
    value: float = 0.0
    unit: str = ""
    category: str = "DETERMINISTIC"
    threshold: Optional[float] = None
    target_threshold: Optional[float] = None
    is_passed: bool = True
    passed: bool = True
    confidence_interval: Optional[ConfidenceInterval] = None
    details: Dict[str, Any] = Field(default_factory=dict)

    def __init__(self, **data):
        if "metric_name" in data and "name" not in data:
            data["name"] = data["metric_name"]
        elif "name" in data and "metric_name" not in data:
            data["metric_name"] = data["name"]
        if "target_threshold" in data and "threshold" not in data:
            data["threshold"] = data["target_threshold"]
        elif "threshold" in data and "target_threshold" not in data:
            data["target_threshold"] = data["threshold"]
        if "passed" in data and "is_passed" not in data:
            data["is_passed"] = data["passed"]
        elif "is_passed" in data and "passed" not in data:
            data["passed"] = data["is_passed"]
        super().__init__(**data)


class QualityGateRule(BaseModel):
    rule_id: Optional[str] = None
    metric_name: str
    operator: str = ">="
    threshold: Optional[float] = None
    min_threshold: Optional[float] = None
    max_threshold: Optional[float] = None
    mandatory: bool = True
    is_hard_blocker: bool = True


class QualityGateResult(BaseModel):
    is_approved: bool = True
    gate_passed: bool = True
    overall_score: float = 1.0
    violations: List[str] = Field(default_factory=list)
    hard_violations_count: int = 0
    soft_violations_count: int = 0
    evaluated_rules: List[Any] = Field(default_factory=list)
    evaluated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def __init__(self, **data):
        if "gate_passed" in data and "is_approved" not in data:
            data["is_approved"] = data["gate_passed"]
        elif "is_approved" in data and "gate_passed" not in data:
            data["gate_passed"] = data["is_approved"]
        super().__init__(**data)


class RuntimeEnvironmentProfile(BaseModel):
    python_version: str = "3.14.0"
    os_name: str = "Windows"
    host_os: str = "Windows"
    git_commit: str = "main-verified"
    app_version: str = "1.0.0-phase13.23"
    hardware_summary: Dict[str, Any] = Field(default_factory=dict)
    active_model_name: str = "gemini-2.5-flash"
    cpu_count: int = 8
    memory_total_gb: float = 32.0
    active_threads: int = 4
    config_hash: str = "cfg_hash_default"
    prompt_hash: str = "prompt_hash_default"
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class ImmutableEvidenceRecord(BaseModel):
    evidence_id: str = Field(default_factory=lambda: f"ev_{uuid.uuid4().hex[:8]}")
    payload_hash: str = ""
    sha256_hash: str = ""
    byte_size: int = 128
    payload_type: str = "GENERIC"
    payload_summary: str = ""
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    merkle_root: Optional[str] = None

    def __init__(self, **data):
        if "sha256_hash" in data and "payload_hash" not in data:
            data["payload_hash"] = data["sha256_hash"]
        elif "payload_hash" in data and "sha256_hash" not in data:
            data["sha256_hash"] = data["payload_hash"]
        super().__init__(**data)



# 1. Definition Manager Models
class VerificationDefinition(BaseModel):
    id: Optional[str] = None
    definition_id: str = Field(default_factory=lambda: f"def_{uuid.uuid4().hex[:8]}")
    tenant_id: str = "default-tenant"
    name: str
    description: str
    target_domain: str = "ENTERPRISE_PLATFORM"
    plugin_name: Optional[str] = None
    target_subsystem: Optional[str] = None
    quality_gates: List[QualityGateRule] = Field(default_factory=list)
    version: str = "1.0.0"
    dataset_version: str = "1.0.0"
    repetition_count: int = 1
    is_immutable: bool = True
    owner: str = "Enterprise QA Architecture"
    tags: List[str] = Field(default_factory=list)
    dataset_ids: List[str] = Field(default_factory=list)
    required_invariants: List[str] = Field(default_factory=list)
    config_template: Dict[str, Any] = Field(default_factory=dict)
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def __init__(self, **data):
        if "id" in data and "definition_id" not in data:
            data["definition_id"] = data["id"]
        elif "definition_id" in data and "id" not in data:
            data["id"] = data["definition_id"]
        super().__init__(**data)
        if self.id is None:
            self.id = self.definition_id


# 2. Execution Models
class ExecutionTask(BaseModel):
    task_id: str = Field(default_factory=lambda: f"task_{uuid.uuid4().hex[:8]}")
    name: str
    target_plugin: str
    parameters: Dict[str, Any] = Field(default_factory=dict)
    timeout_seconds: int = 300
    retry_limit: int = 3
    retry_count: int = 0
    status: VerificationStatus = VerificationStatus.PENDING
    error_message: Optional[str] = None
    output_payload: Dict[str, Any] = Field(default_factory=dict)


class VerificationPlan(BaseModel):
    plan_id: str = Field(default_factory=lambda: f"plan_{uuid.uuid4().hex[:8]}")
    definition_id: str
    tasks: List[ExecutionTask] = Field(default_factory=list)
    execution_strategy: str = "SEQUENTIAL"  # SEQUENTIAL, PARALLEL, ASYNC
    environment_id: str = "env_default"
    config_hash: str = ""
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class VerificationRun(BaseModel):
    id: Optional[str] = None
    run_id: str = Field(default_factory=lambda: f"vrun_{uuid.uuid4().hex[:8]}")
    tenant_id: str = "default-tenant"
    definition_id: str = "def_default"
    plan_id: str = "plan_default"
    name: str = "Verification Run"
    plugin_name: Optional[str] = None
    target_subsystem: Optional[str] = None
    environment_profile: Optional[Any] = None
    status: VerificationStatus = VerificationStatus.PENDING
    current_stage: Any = VerificationStage.PRE_FLIGHT_DISCOVERY
    stage_progress_pct: float = 0.0
    overall_score: float = 0.0
    passed_invariants_count: int = 0
    failed_invariants_count: int = 0
    stage_history: List[StageExecutionRecord] = Field(default_factory=list)
    evidence_records: List[Any] = Field(default_factory=list)
    metrics: List[MetricResult] = Field(default_factory=list)
    certificate: Optional[Any] = None
    summary_report: Optional[str] = None
    quality_gate_result: Optional[Any] = None
    start_time: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    end_time: Optional[str] = None
    completed_at: Optional[Any] = None
    correlation_id: str = Field(default_factory=lambda: f"corr_{uuid.uuid4().hex[:8]}")

    def __init__(self, **data):
        if "id" in data and "run_id" not in data:
            data["run_id"] = data["id"]
        elif "run_id" in data and "id" not in data:
            data["id"] = data["run_id"]
        super().__init__(**data)
        if self.id is None:
            self.id = self.run_id


# 3. Dataset Models
class DatasetRecord(BaseModel):
    dataset_id: str = Field(default_factory=lambda: f"ds_{uuid.uuid4().hex[:8]}")
    name: str
    dataset_class: DatasetClass = DatasetClass.HAPPY_PATH
    version: str = "1.0.0"
    sample_count: int = 100
    sha256_checksum: str
    lineage_parent_id: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    is_archived: bool = False
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# 4. Environment Models
class EnvironmentReadiness(BaseModel):
    environment_id: str = Field(default_factory=lambda: f"env_{uuid.uuid4().hex[:8]}")
    name: str
    env_type: EnvironmentType = EnvironmentType.INTEGRATION
    is_ready: bool = True
    cpu_utilization_pct: float = 24.5
    memory_available_mb: int = 8192
    network_latency_ms: float = 4.2
    active_sandboxes: int = 1
    last_health_check: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# 5. Configuration Models
class ConfigurationSnapshot(BaseModel):
    config_id: str = Field(default_factory=lambda: f"cfg_{uuid.uuid4().hex[:8]}")
    version: str = "1.0.0"
    parameters: Dict[str, Any] = Field(default_factory=dict)
    sha256_hash: str
    is_locked: bool = True
    environment: str = "INTEGRATION"
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# 6. Evidence Models
class EvidenceItem(BaseModel):
    evidence_id: str = Field(default_factory=lambda: f"ev_{uuid.uuid4().hex[:8]}")
    run_id: str
    evidence_type: EvidenceType = EvidenceType.OUTPUT
    payload_hash: str
    content_preview: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# 7. Metrics & Statistical Models
class MetricValue(BaseModel):
    name: str
    category: MetricCategory
    value: float
    unit: str = ""
    is_passed: bool = True
    threshold: Optional[float] = None


class StatisticalSummary(BaseModel):
    metric_name: str
    sample_size: int
    mean: float
    variance: float
    std_dev: float
    ci_lower_95: float
    ci_upper_95: float
    baseline_mean: Optional[float] = None
    p_value_against_baseline: Optional[float] = None
    drift_detected: bool = False


# 8. Quality Gate & Certification Models
class QualityGatePolicy(BaseModel):
    policy_id: str = Field(default_factory=lambda: f"qg_{uuid.uuid4().hex[:8]}")
    name: str = "Enterprise Strict Certification Policy"
    min_overall_score: float = 0.85
    max_critical_failures: int = 0
    mandatory_metrics: List[str] = Field(default_factory=lambda: ["accuracy", "latency_p99", "zero_fabrication"])
    allow_warnings: bool = False


class QualityGateEvaluation(BaseModel):
    policy_id: str
    run_id: str
    is_approved: bool
    overall_score: float
    violations: List[str] = Field(default_factory=list)
    evaluated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class ComplianceCertificate(BaseModel):
    certificate_id: str = Field(default_factory=lambda: f"cert_{uuid.uuid4().hex[:8]}")
    run_id: str = "run_default"
    verification_run_id: str = "run_default"
    suite_id: str = "suite_default"
    tenant_id: str = "default-tenant"
    status: VerificationStatus = VerificationStatus.PASSED
    overall_score: float = 1.0
    score: float = 1.0
    is_valid: bool = True
    hmac_sha256_signature: str = ""
    issued_at: Any = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    authority: str = "DocuTask Enterprise CA v1.0"

    def __init__(self, **data):
        if "run_id" in data and "verification_run_id" not in data:
            data["verification_run_id"] = data["run_id"]
        elif "verification_run_id" in data and "run_id" not in data:
            data["run_id"] = data["verification_run_id"]
        if "score" in data and "overall_score" not in data:
            data["overall_score"] = data["score"]
        elif "overall_score" in data and "score" not in data:
            data["score"] = data["overall_score"]
        super().__init__(**data)


CryptographicCertificate = ComplianceCertificate


# 9. Reporting Models
class VerificationReport(BaseModel):
    report_id: str = Field(default_factory=lambda: f"rep_{uuid.uuid4().hex[:8]}")
    run_id: str
    format: ReportFormat = ReportFormat.TECHNICAL
    title: str
    summary: str
    metrics_summary: Dict[str, float] = Field(default_factory=dict)
    statistical_findings: List[str] = Field(default_factory=list)
    certificate_id: Optional[str] = None
    generated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# 10. Audit & Traceability Models
class AuditEntry(BaseModel):
    audit_id: str = Field(default_factory=lambda: f"aud_{uuid.uuid4().hex[:8]}")
    event_type: AuditEventType
    entity_id: str
    actor: str = "SYSTEM"
    details: Dict[str, Any] = Field(default_factory=dict)
    sha256_prev_hash: str = "GENESIS"
    sha256_entry_hash: str = ""
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class TraceabilityNode(BaseModel):
    node_id: str
    node_type: str  # DEFINITION, DATASET, CONFIG, RUN, METRIC, EVIDENCE, CERTIFICATE, REPORT
    label: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    connections: List[str] = Field(default_factory=list)


# 11. Plugin & Registry Models
class PluginDescriptor(BaseModel):
    plugin_id: str
    name: str
    domain: str
    version: str = "1.0.0"
    capabilities: List[str] = Field(default_factory=list)
    is_enabled: bool = True
    priority: int = 100
    health_status: str = "HEALTHY"


# 12. Cross-Cutting Component Health Model
class ComponentHealth(BaseModel):
    component_name: str
    status: str = "HEALTHY"
    throughput_ops_sec: float = 120.0
    latency_ms: float = 2.4
    error_rate_pct: float = 0.0
    uptime_seconds: int = 3600
    active_connections: int = 4
