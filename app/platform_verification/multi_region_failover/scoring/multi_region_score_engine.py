"""
Multi-Region Failover Scoring Engine (Part 3G.6).
Computes composite multi-region resilience score and assigns cloud certification tiers.
"""

from app.platform_verification.multi_region_failover.domain.models import (
    MultiRegionArchitectureReport,
    CloudPortabilityReport,
    DatabaseReplicationReport,
    StorageReplicationReport,
    TrafficFailoverReport,
    WorkflowCheckpointReport,
    ChaosOutageReport,
    AvailabilityMetricsReport,
    MultiRegionScorecard,
)
from app.platform_verification.multi_region_failover.domain.interfaces import (
    IMultiRegionScoreEngine,
)


class MultiRegionScoreEngine(IMultiRegionScoreEngine):
    """
    Evaluates 7 core dimensions of multi-region disaster resilience.
    """

    WEIGHTS = {
        "architecture": 0.15,
        "portability": 0.10,
        "database_failover": 0.20,
        "storage_replication": 0.15,
        "traffic_migration": 0.15,
        "workflow_continuity": 0.15,
        "availability_metrics": 0.10,
    }

    def calculate_scorecard(
        self,
        arch: MultiRegionArchitectureReport,
        portability: CloudPortabilityReport,
        db_rep: DatabaseReplicationReport,
        storage_rep: StorageReplicationReport,
        traffic: TrafficFailoverReport,
        workflow: WorkflowCheckpointReport,
        chaos: ChaosOutageReport,
        avail: AvailabilityMetricsReport,
    ) -> MultiRegionScorecard:
        arch_score = 100.0 if arch.passed else 50.0
        port_score = 100.0 if portability.passed else 50.0
        db_score = 100.0 if db_rep.passed else 50.0
        storage_score = 100.0 if storage_rep.passed else 50.0
        traffic_score = 100.0 if traffic.passed else 50.0
        workflow_score = 100.0 if (workflow.passed and chaos.passed) else 50.0
        avail_score = avail.availability_score

        composite = (
            arch_score * self.WEIGHTS["architecture"]
            + port_score * self.WEIGHTS["portability"]
            + db_score * self.WEIGHTS["database_failover"]
            + storage_score * self.WEIGHTS["storage_replication"]
            + traffic_score * self.WEIGHTS["traffic_migration"]
            + workflow_score * self.WEIGHTS["workflow_continuity"]
            + avail_score * self.WEIGHTS["availability_metrics"]
        )
        composite = round(composite, 2)

        passed = (composite >= 95.0) and all(
            [arch.passed, portability.passed, db_rep.passed, storage_rep.passed, traffic.passed, workflow.passed, chaos.passed, avail.passed]
        )

        verdict = "ENTERPRISE_CLOUD_RESILIENT" if passed else "MULTI_REGION_FAILOVER_REJECTED"

        details = {
            "weights": self.WEIGHTS,
            "dimension_scores": {
                "architecture": arch_score,
                "portability": port_score,
                "database_failover": db_score,
                "storage_replication": storage_score,
                "traffic_migration": traffic_score,
                "workflow_continuity": workflow_score,
                "availability_metrics": avail_score,
            },
            "availability_tier": avail.availability_tier.value,
            "framework_version": "3G.6-MULTI-REGION-ENTERPRISE",
        }

        return MultiRegionScorecard(
            architecture_score=arch_score,
            portability_score=port_score,
            database_failover_score=db_score,
            storage_replication_score=storage_score,
            traffic_migration_score=traffic_score,
            workflow_continuity_score=workflow_score,
            availability_metrics_score=avail_score,
            overall_failover_score=composite,
            availability_tier=avail.availability_tier,
            certification_verdict=verdict,
            ci_cd_deployment_approved=passed,
            passed=passed,
            details=details,
        )
