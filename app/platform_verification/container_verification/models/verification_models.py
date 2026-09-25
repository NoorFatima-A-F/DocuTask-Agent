"""
Domain models for Part 3A: Enterprise Container & Runtime Verification Framework.
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional
from datetime import datetime, timezone


class ContainerCertificationTier(str, Enum):
    ENTERPRISE_CONTAINER_READY = "ENTERPRISE_CONTAINER_READY"
    PRODUCTION_READY = "PRODUCTION_READY"
    NEEDS_IMPROVEMENT = "NEEDS_IMPROVEMENT"
    FAILED = "FAILED"


ContainerCertificationTier.__test__ = False


class VulnerabilitySeverity(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INFO = "INFO"


class RestartPolicy(str, Enum):
    UNLESS_STOPPED = "unless-stopped"
    ALWAYS = "always"
    ON_FAILURE = "on-failure"
    NO = "no"


@dataclass
class ServiceDefinition:
    name: str
    image: str
    ports: List[str] = field(default_factory=list)
    depends_on: List[str] = field(default_factory=list)
    environment: Dict[str, str] = field(default_factory=dict)
    volumes: List[str] = field(default_factory=list)
    networks: List[str] = field(default_factory=list)
    restart_policy: str = "unless-stopped"
    cpu_limit: Optional[str] = "1.0"
    memory_limit: Optional[str] = "1G"
    user: Optional[str] = "appuser"
    read_only_root: bool = False
    drop_capabilities: List[str] = field(default_factory=lambda: ["ALL"])


@dataclass
class NetworkDefinition:
    name: str
    driver: str = "bridge"
    internal_only: bool = False


@dataclass
class VolumeDefinition:
    name: str
    driver: str = "local"


@dataclass
class ContainerArchitectureModel:
    services: Dict[str, ServiceDefinition] = field(default_factory=dict)
    networks: Dict[str, NetworkDefinition] = field(default_factory=dict)
    volumes: Dict[str, VolumeDefinition] = field(default_factory=dict)


@dataclass
class ArchitectureDiscoveryReport:
    total_services: int
    total_networks: int
    total_volumes: int
    undocumented_services: List[str] = field(default_factory=list)
    hidden_dependencies: List[str] = field(default_factory=list)
    status: str = "PASS"


@dataclass
class ContainerBoundaryReport:
    containers_count: int
    coupling_score: float
    isolation_score: float
    god_containers: List[str] = field(default_factory=list)
    shared_mutable_volumes: List[str] = field(default_factory=list)
    status: str = "PASS"


@dataclass
class DockerfileQualityReport:
    base_image_pinned: bool
    base_image_name: str
    runs_as_non_root: bool
    runtime_user: str
    layer_optimization_score: float
    dev_dependencies_found: List[str] = field(default_factory=list)
    multi_stage_build: bool = True
    status: str = "PASS"
    issues: List[str] = field(default_factory=list)


@dataclass
class ImageVulnerability:
    cve_id: str
    package_name: str
    installed_version: str
    fixed_version: Optional[str]
    severity: VulnerabilitySeverity
    description: str


@dataclass
class ImageSecurityReport:
    critical_vulnerabilities: int
    high_vulnerabilities: int
    medium_vulnerabilities: int
    low_vulnerabilities: int
    vulnerabilities: List[ImageVulnerability] = field(default_factory=list)
    hardcoded_secrets: List[str] = field(default_factory=list)
    status: str = "PASS"


@dataclass
class ImageEfficiencyReport:
    image_name: str
    compressed_size_mb: float
    uncompressed_size_mb: float
    layer_count: int
    unnecessary_files_detected: List[str] = field(default_factory=list)
    meets_efficiency_target: bool = True


@dataclass
class BuildReproducibilityReport:
    source_commit: str
    digest_build_1: str
    digest_build_2: str
    is_deterministic: bool
    diff_entries: List[str] = field(default_factory=list)
    status: str = "PASS"


@dataclass
class RuntimeHealthReport:
    service_name: str
    startup_time_seconds: float
    health_endpoint_verified: bool
    live_endpoint_verified: bool
    ready_endpoint_verified: bool
    status: str = "PASS"


@dataclass
class ContainerFailureReport:
    simulated_scenarios: int
    recovery_success_count: int
    data_loss_detected: bool = False
    average_restart_time_seconds: float = 2.4
    status: str = "PASS"
    issues: List[str] = field(default_factory=list)


@dataclass
class ResourceLimitReport:
    all_limits_defined: bool
    unbounded_services: List[str] = field(default_factory=list)
    oom_resilience_verified: bool = True
    status: str = "PASS"


@dataclass
class NetworkSecurityReport:
    publicly_exposed_internal_ports: List[str] = field(default_factory=list)
    unauthorized_cross_network_access: bool = False
    status: str = "PASS"


@dataclass
class SbomPackage:
    name: str
    version: str
    license_type: str
    purl: str
    sha256_hash: str


@dataclass
class SbomReport:
    total_packages: int
    packages: List[SbomPackage] = field(default_factory=list)
    untrusted_packages: List[str] = field(default_factory=list)
    license_compliance_passed: bool = True


@dataclass
class ContainerCertificationReport:
    architecture_quality_score: float
    security_score: float
    reproducibility_score: float
    isolation_score: float
    runtime_reliability_score: float
    efficiency_score: float
    composite_score: float
    tier: ContainerCertificationTier
    evaluation_timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class ContainerVerificationEvidencePackage:
    package_id: str
    commit_sha: str
    scorecard: ContainerCertificationReport
    architecture_report: ArchitectureDiscoveryReport
    boundary_report: ContainerBoundaryReport
    dockerfile_report: DockerfileQualityReport
    image_security_report: ImageSecurityReport
    efficiency_report: ImageEfficiencyReport
    reproducibility_report: BuildReproducibilityReport
    runtime_report: RuntimeHealthReport
    failure_report: ContainerFailureReport
    resource_report: ResourceLimitReport
    network_report: NetworkSecurityReport
    sbom_report: SbomReport
    package_sha256: str = ""
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
