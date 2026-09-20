"""
Domain Models for Health Check Architecture Verification Framework (Part 3H.1).
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Any, List, Optional


class HealthState(str, Enum):
    UNKNOWN = "UNKNOWN"
    INITIALIZING = "INITIALIZING"
    READY = "READY"
    DEGRADED = "DEGRADED"
    UNHEALTHY = "UNHEALTHY"
    RECOVERING = "RECOVERING"
    FAILED = "FAILED"


class HealthLayer(str, Enum):
    LAYER_1_PROCESS = "Layer 1: Process Health"
    LAYER_2_DEPENDENCY = "Layer 2: Dependency Health"
    LAYER_3_CAPABILITY = "Layer 3: Service Capability Health"
    LAYER_4_WORKFLOW = "Layer 4: Business Workflow Health"


class DependencyPriority(str, Enum):
    CRITICAL = "CRITICAL"    # Failure blocks service readiness
    IMPORTANT = "IMPORTANT"  # Failure degrades service into fallback mode
    OPTIONAL = "OPTIONAL"    # Failure causes zero operational impact


class HealthVisibilityLevel(str, Enum):
    PUBLIC = "PUBLIC"                    # Minimal liveness/readiness, 0 details
    INTERNAL = "INTERNAL"                # Dependency statuses, latency
    ADMIN_DIAGNOSTIC = "ADMIN_DIAGNOSTIC"# Detailed telemetry with auth


class HealthArchitectureTier(str, Enum):
    FAILED = "Failed"                                         # < 80
    NEEDS_IMPROVEMENT = "Needs Improvement"                   # 80 - 89
    PRODUCTION_READY = "Production Ready"                     # 90 - 94
    ENTERPRISE_READY = "Enterprise Health Architecture Ready" # 95 - 100


@dataclass
class HealthStateModelReport:
    total_states: int
    states: List[HealthState]
    layers_evaluated: List[HealthLayer]
    state_machine_valid: bool
    transition_coverage_pct: float
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class HealthContractReport:
    liveness_contract_valid: bool
    liveness_isolated_from_dependencies: bool
    readiness_contract_valid: bool
    readiness_enforces_critical_deps: bool
    full_health_contract_valid: bool
    endpoints_tested: List[str] = field(default_factory=list)
    passed: bool = True
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DependencyNodeSpec:
    dependency_id: str
    target_service: str
    priority: DependencyPriority
    timeout_ms: int
    failure_state: str
    recovery_strategy: str
    owner_team: str


@dataclass
class DependencyGraphReport:
    total_services_mapped: int
    total_dependencies: int
    critical_dependencies_count: int
    important_dependencies_count: int
    optional_dependencies_count: int
    dependency_graph: Dict[str, List[str]] = field(default_factory=dict)
    dependency_specs: List[DependencyNodeSpec] = field(default_factory=list)
    passed: bool = True
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class FailurePolicyReport:
    policies_defined_count: int
    detection_mechanisms_verified: bool
    classification_rules_enforced: bool
    response_actions_automated: bool
    recovery_strategies_documented: bool
    passed: bool = True
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SecurityAuditReport:
    public_endpoint_leak_free: bool
    internal_endpoint_leak_free: bool
    admin_diagnostic_auth_enforced: bool
    credentials_leaked_count: int
    urls_leaked_count: int
    passed: bool = True
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AutomationIntegrationReport:
    docker_healthcheck_compatible: bool
    kubernetes_liveness_compatible: bool
    kubernetes_readiness_compatible: bool
    kubernetes_startup_compatible: bool
    cicd_predeployment_gating_supported: bool
    passed: bool = True
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class HealthScorecard:
    health_model_score: float         # Weight 20%
    contract_implementation_score: float # Weight 20%
    dependency_modeling_score: float  # Weight 20%
    failure_classification_score: float # Weight 15%
    security_design_score: float      # Weight 10%
    automation_readiness_score: float # Weight 15%
    overall_health_score: float       # Composite 0 - 100
    certification_tier: HealthArchitectureTier
    certification_verdict: str        # CERTIFIED / REJECTED
    ci_cd_deployment_approved: bool
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)
