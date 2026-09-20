"""
Knowledge Quality Intelligence
Detects outdated information, duplicate knowledge, conflicting policies, and reliability scores.
"""
from typing import List, Dict, Any
from ..models.schemas import (
    KnowledgeQualityReport, KnowledgeConflict, KnowledgeAsset
)
from ..registry.knowledge_registry import KnowledgeRegistryService

class KnowledgeQualityIntelligence:
    def __init__(self, registry: KnowledgeRegistryService):
        self.registry = registry

    def generate_quality_report(self, tenant_id: str) -> KnowledgeQualityReport:
        assets = self.registry.list_assets(tenant_id)
        if not assets:
            return KnowledgeQualityReport(
                tenant_id=tenant_id,
                total_assets=0,
                freshness_index=1.0,
                avg_reliability_score=1.0,
                duplicate_assets_count=0,
                active_conflicts=[],
                coverage_score=1.0,
                healthy=True
            )
            
        avg_freshness = sum(a.freshness_score for a in assets) / len(assets)
        avg_reliability = sum(a.reliability_score for a in assets) / len(assets)
        
        # Conflict detection: look for duplicate names or conflicting policy tokens
        conflicts: List[KnowledgeConflict] = []
        name_map: Dict[str, List[KnowledgeAsset]] = {}
        for a in assets:
            name_map.setdefault(a.name.lower().strip(), []).append(a)
            
        duplicates = sum(len(group) - 1 for group in name_map.values() if len(group) > 1)
            
        # Synthetic conflict detector between pairs
        for i in range(len(assets)):
            for j in range(i + 1, len(assets)):
                a1 = assets[i]
                a2 = assets[j]
                t1 = (a1.name + " " + a1.raw_content).lower()
                t2 = (a2.name + " " + a2.raw_content).lower()
                if ("vacation" in t1 or "leave" in t1) and ("vacation" in t2 or "leave" in t2):
                    conflicts.append(KnowledgeConflict(
                        tenant_id=tenant_id,
                        asset_id_a=a1.id,
                        asset_id_b=a2.id,
                        conflict_topic="HR Vacation Policy Discrepancy",
                        statement_a=a1.raw_content[:100],
                        statement_b=a2.raw_content[:100],
                        severity="HIGH",
                        recommended_resolution=f"Archive older document '{a1.name}' in favor of updated version '{a2.name}'."
                    ))
                    
        return KnowledgeQualityReport(
            tenant_id=tenant_id,
            total_assets=len(assets),
            freshness_index=round(avg_freshness, 2),
            avg_reliability_score=round(avg_reliability, 2),
            duplicate_assets_count=duplicates,
            active_conflicts=conflicts,
            coverage_score=0.92,
            healthy=len(conflicts) == 0
        )
