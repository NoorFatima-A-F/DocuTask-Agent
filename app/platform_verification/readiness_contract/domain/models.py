"""
Domain Models for Enterprise Readiness Contract Architecture (Part 3H.3.1).
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Any, List


class ReadinessState(str, Enum):
    INITIALIZING = "INITIALIZING"
    CHECKING_DEPENDENCIES = "CHECKING_DEPENDENCIES"
    READY = "READY"
    DEGRADED = "DEGRADED"
    NOT_READY = "NOT_READY"
    RECOVERING = "RECOVERING"


class TrafficAction(str, Enum):
    ADMIT_TRAFFIC = "ADMIT_TRAFFIC"
    THROTTLE_TRAFFIC = "THROTTLE_TRAFFIC"
    WITHHOLD_TRAFFIC = "WITHHOLD_TRAFFIC"


class DependencyType(str, Enum):
    CRITICAL = "critical"
    NON_CRITICAL = "non_critical"


class ReadinessTier(str, Enum):
    FAILED = "Failed"                                         # < 80
    NEEDS_IMPROVEMENT = "Improvement Required"               # 80 - 89
    PRODUCTION_READY = "Production Ready"                     # 90 - 94
    ENTERPRISE_READY = "Enterprise Readiness Contract Certified" # 95 - 100


@dataclass
class ReadinessContractReport:
    endpoint: str
    status: str
    service: str
    version: str
    timestamp: str
    checks: Dict[str, str]
    contract_schema_valid: bool
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class StateMachineReport:
    total_states: int
    states: List[str]
    transition_matrix_valid: bool
    all_states_deterministic: bool
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DependencyPolicyReport:
    critical_dependencies: List[str]
    degraded_dependencies: List[str]
    policy_enforcement_valid: bool
    traffic_actions_mapped: bool
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class StartupValidationReport:
    startup_sequence_valid: bool
    false_readiness_prevented: bool
    total_steps_verified: int
    passed: bool
    steps: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class FailureTransitionReport:
    total_transitions_tested: int
    passed_transitions: int
    startup_to_ready_passed: bool
    db_failure_to_not_ready_passed: bool
    recovery_to_ready_passed: bool
    optional_dep_to_degraded_passed: bool
    passed: bool
    transitions: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class OrchestrationReport:
    kubernetes_readiness_probe_valid: bool
    docker_compose_compatible: bool
    cloud_runtimes_supported: List[str]
    probe_frequency_seconds: int
    failure_threshold: int
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ReadinessScorecard:
    contract_correctness_score: float   # Weight 25%
    state_model_quality_score: float    # Weight 20%
    dependency_modeling_score: float    # Weight 20%
    failure_handling_score: float       # Weight 15%
    security_score: float               # Weight 10%
    observability_score: float          # Weight 10%
    overall_readiness_score: float      # Composite 0 - 100
    certification_tier: ReadinessTier
    certification_verdict: str          # CERTIFIED / REJECTED
    traffic_admission_safe: bool
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)
