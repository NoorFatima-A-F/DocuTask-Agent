"""
Domain Models for Multi-Region / Cloud Failover Verification Framework (Part 3G.6).
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Any, List, Optional


class CloudRegion(str, Enum):
    PRIMARY = "us-east-1"      # Primary Region (N. Virginia)
    SECONDARY = "us-west-2"    # Secondary Region (Oregon)


class FailoverMode(str, Enum):
    ACTIVE_STANDBY = "ACTIVE_STANDBY"
    ACTIVE_ACTIVE = "ACTIVE_ACTIVE"
    PILOT_LIGHT = "PILOT_LIGHT"


class ReplicationHealth(str, Enum):
    HEALTHY = "HEALTHY"        # Lag < 5s
    DEGRADED = "DEGRADED"      # Lag 5-30s
    CRITICAL = "CRITICAL"      # Lag > 60s


class AvailabilityTier(str, Enum):
    THREE_NINES = "99.9% (High Availability)"              # 8.7 hrs/yr
    FOUR_NINES = "99.99% (Enterprise High Availability)"   # 52.6 min/yr
    FIVE_NINES = "99.999% (Carrier Grade Resilient)"       # 5.2 min/yr


@dataclass
class RegionalServiceItem:
    service_name: str
    primary_status: str
    secondary_status: str
    replication_mode: str
    is_replicated: bool


@dataclass
class MultiRegionArchitectureReport:
    total_critical_services: int
    replicated_services_count: int
    primary_region: CloudRegion
    secondary_region: CloudRegion
    services: List[RegionalServiceItem] = field(default_factory=list)
    passed: bool = True
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CloudPortabilityReport:
    compute_portability_verified: bool
    storage_abstraction_verified: bool
    ai_provider_abstraction_verified: bool
    hardcoded_cloud_dependencies_count: int
    supported_clouds: List[str] = field(default_factory=list)
    passed: bool = True
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DatabaseReplicationReport:
    replication_health: ReplicationHealth
    current_primary_lsn: str
    replica_replay_lsn: str
    replication_lag_seconds: float
    wal_shipping_active: bool
    standby_promotion_latency_sec: float
    data_loss_bytes: int
    passed: bool = True
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class StorageReplicationReport:
    total_documents_tested: int
    replicated_documents_count: int
    sha256_checksum_match_pct: float
    cross_region_sync_lag_sec: float
    zero_data_loss_verified: bool
    passed: bool = True
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TrafficFailoverReport:
    dns_propagation_time_sec: float
    detection_time_sec: float
    traffic_migration_time_sec: float
    total_failover_time_sec: float
    dropped_requests_pct: float
    global_traffic_manager: str
    passed: bool = True
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class WorkflowCheckpointReport:
    total_workflows_tested: int
    midflight_crashes_simulated: int
    workflows_resumed_successfully: int
    duplicate_extractions_detected: int
    corrupted_jobs_count: int
    checkpoint_accuracy_pct: float
    passed: bool = True
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ChaosOutageReport:
    simulations_executed: int
    region_shutdown_passed: bool
    network_partition_passed: bool
    cloud_provider_outage_passed: bool
    zero_split_brain_verified: bool
    passed: bool = True
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AvailabilityMetricsReport:
    annual_uptime_target_pct: float
    availability_tier: AvailabilityTier
    measured_regional_rto_seconds: float
    measured_regional_rpo_seconds: float
    rto_sla_met: bool
    rpo_sla_met: bool
    availability_score: float
    passed: bool = True
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class MultiRegionScorecard:
    architecture_score: float         # Weight 15%
    portability_score: float          # Weight 10%
    database_failover_score: float    # Weight 20%
    storage_replication_score: float  # Weight 15%
    traffic_migration_score: float    # Weight 15%
    workflow_continuity_score: float  # Weight 15%
    availability_metrics_score: float # Weight 10%
    overall_failover_score: float     # Composite 0 - 100
    availability_tier: AvailabilityTier
    certification_verdict: str        # ENTERPRISE_CLOUD_RESILIENT
    ci_cd_deployment_approved: bool
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)
