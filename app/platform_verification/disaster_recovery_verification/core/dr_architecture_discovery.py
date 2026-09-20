"""
Disaster Recovery Architecture Discovery & Criticality Classification Engine.
"""
from typing import Dict, List
from app.platform_verification.disaster_recovery_verification.domain.models import (
    DRServiceInventory,
    ComponentTier,
    ComponentCriticalityEntry,
    BusinessImpactAnalysisEntry,
)
from app.platform_verification.disaster_recovery_verification.domain.interfaces import (
    IDRArchitectureDiscovery,
)


class DRArchitectureDiscovery(IDRArchitectureDiscovery):
    """Discovers services, component criticality tiers, and business impact."""

    def discover_inventory(self) -> DRServiceInventory:
        return DRServiceInventory(
            services=["api", "worker", "postgres", "redis", "storage", "auth", "knowledge"],
            critical_components=["postgres", "storage", "auth", "agent_state"],
            backup_dependencies=["postgres_wal", "s3_versioned_bucket", "vault_kms"],
            recovery_dependencies=["infrastructure", "postgres", "redis", "workers", "api"],
        )

    def classify_components(self) -> Dict[str, ComponentCriticalityEntry]:
        return {
            "postgres": ComponentCriticalityEntry(
                component_name="postgres",
                tier=ComponentTier.TIER_0_MISSION_CRITICAL,
                impact_description="Complete platform outage; metadata and workflow state unavailable",
                recovery_priority=1,
                max_tolerable_downtime_minutes=15,
                max_tolerable_data_loss_minutes=5,
            ),
            "storage": ComponentCriticalityEntry(
                component_name="storage",
                tier=ComponentTier.TIER_0_MISSION_CRITICAL,
                impact_description="Uploaded raw documents and generated evidence inaccessible",
                recovery_priority=2,
                max_tolerable_downtime_minutes=30,
                max_tolerable_data_loss_minutes=5,
            ),
            "auth": ComponentCriticalityEntry(
                component_name="auth",
                tier=ComponentTier.TIER_0_MISSION_CRITICAL,
                impact_description="Users and microservices cannot authenticate",
                recovery_priority=3,
                max_tolerable_downtime_minutes=15,
                max_tolerable_data_loss_minutes=0,
            ),
            "redis_queue": ComponentCriticalityEntry(
                component_name="redis_queue",
                tier=ComponentTier.TIER_1_CRITICAL,
                impact_description="Async document processing jobs stalled",
                recovery_priority=4,
                max_tolerable_downtime_minutes=60,
                max_tolerable_data_loss_minutes=10,
            ),
            "workers": ComponentCriticalityEntry(
                component_name="workers",
                tier=ComponentTier.TIER_1_CRITICAL,
                impact_description="Document OCR and AI extraction tasks stalled",
                recovery_priority=5,
                max_tolerable_downtime_minutes=60,
                max_tolerable_data_loss_minutes=0,
            ),
        }

    def generate_bia(self) -> List[BusinessImpactAnalysisEntry]:
        return [
            BusinessImpactAnalysisEntry(
                business_function="document_processing",
                impact="HIGH",
                max_downtime="30 minutes",
                max_data_loss="5 minutes",
                recovery_priority=1,
            ),
            BusinessImpactAnalysisEntry(
                business_function="audit_and_evidence",
                impact="HIGH",
                max_downtime="60 minutes",
                max_data_loss="0 minutes",
                recovery_priority=2,
            ),
            BusinessImpactAnalysisEntry(
                business_function="user_dashboard",
                impact="MEDIUM",
                max_downtime="120 minutes",
                max_data_loss="15 minutes",
                recovery_priority=3,
            ),
        ]
