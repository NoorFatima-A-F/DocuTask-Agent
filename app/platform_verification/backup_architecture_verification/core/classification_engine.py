"""
Part 2: Backup Classification Engine.
Classifies assets into Tier 0 (Mission Critical), Tier 1 (Business Critical),
Tier 2 (Operational), and Tier 3 (Rebuildable) with RPO/RTO metrics.
"""
from typing import List, Dict, Any
from app.platform_verification.backup_architecture_verification.domain.models import (
    CriticalityTier,
    AssetInventoryItem,
    ClassificationEntry,
)
from app.platform_verification.backup_architecture_verification.domain.interfaces import (
    IClassificationEngine,
)


class ClassificationEngine(IClassificationEngine):
    """
    Evaluates discovered assets and applies automated classification
    rules, assigning recovery priority, maximum RPO, and RTO parameters.
    """

    def classify_assets(self, assets: List[AssetInventoryItem]) -> Dict[str, ClassificationEntry]:
        matrix: Dict[str, ClassificationEntry] = {}
        for asset in assets:
            if asset.criticality == CriticalityTier.TIER_0:
                priority = "Immediate"
                max_rpo = 0  # Near-zero (Continuous WAL / sync)
                max_rto = 300  # 5 minutes
                tolerance = "Zero Data Loss Allowed (Strict Point-in-Time Recovery)"
                rationale = "Mission Critical: Platform cannot operate or maintain audit integrity without this asset."
            elif asset.criticality == CriticalityTier.TIER_1:
                priority = "High"
                max_rpo = 900  # 15 minutes
                max_rto = 1800  # 30 minutes
                tolerance = "Low Data Loss Tolerance (Max 15m delta recoverable from logs)"
                rationale = "Business Critical: Document processing pipeline or AI workflows degrade significantly."
            elif asset.criticality == CriticalityTier.TIER_2:
                priority = "Standard"
                max_rpo = 86400  # 24 hours
                max_rto = 14400  # 4 hours
                tolerance = "Moderate (Historical telemetry and metrics can be regenerated or backfilled)"
                rationale = "Operational: Telemetry, metrics, and visualization dashboards for observability."
            else:  # Tier 3
                priority = "Best Effort / Rebuild on Demand"
                max_rpo = 0  # Rebuildable from raw source
                max_rto = 28800  # 8 hours
                tolerance = "High (Disposable temporary caches and thumbnails derived from Tier 0 assets)"
                rationale = "Rebuildable: Temporary cache, user sessions, or generated previews that require no persistent backup."

            entry = ClassificationEntry(
                asset_name=asset.name,
                category=asset.category,
                criticality=asset.criticality,
                recovery_priority=priority,
                max_rpo_seconds=max_rpo,
                max_rto_seconds=max_rto,
                data_loss_tolerance=tolerance,
                recovery_tier_rationale=rationale,
            )
            matrix[asset.name] = entry
        return matrix

    def export_classification_matrix_json(
        self, classification_matrix: Dict[str, ClassificationEntry]
    ) -> Dict[str, Any]:
        """Formats the classification matrix to JSON dictionary."""
        return {
            "total_classified_assets": len(classification_matrix),
            "tier_summary": {
                "Tier0_Mission_Critical": len([c for c in classification_matrix.values() if c.criticality == CriticalityTier.TIER_0]),
                "Tier1_Business_Critical": len([c for c in classification_matrix.values() if c.criticality == CriticalityTier.TIER_1]),
                "Tier2_Operational": len([c for c in classification_matrix.values() if c.criticality == CriticalityTier.TIER_2]),
                "Tier3_Rebuildable": len([c for c in classification_matrix.values() if c.criticality == CriticalityTier.TIER_3]),
            },
            "classification_matrix": [
                {
                    "asset_name": c.asset_name,
                    "category": c.category.value,
                    "criticality": c.criticality.value,
                    "recovery_priority": c.recovery_priority,
                    "max_rpo_seconds": c.max_rpo_seconds,
                    "max_rto_seconds": c.max_rto_seconds,
                    "data_loss_tolerance": c.data_loss_tolerance,
                    "recovery_tier_rationale": c.recovery_tier_rationale,
                }
                for c in classification_matrix.values()
            ],
        }
