"""Evidence Quality Index (EQI) Calculator."""

from typing import List, Dict, Any
from datetime import datetime, timezone
from enterprise_audit_engine.domain.evidence.models import EvidenceRecord
from enterprise_audit_engine.certification_authority.domain.models import EQIBreakdown


class EvidenceQualityIndexCalculator:
    """Calculates the Evidence Quality Index (EQI) based on quantifiable empirical factors."""

    @classmethod
    def calculate_eqi(
        cls,
        records: List[EvidenceRecord],
        coverage_pct: float = 100.0,
        is_reproducible: bool = True,
        verification_depth_map: Dict[str, float] = None,
    ) -> EQIBreakdown:
        total_records = len(records)
        
        # 1. Evidence Coverage Score (max 25)
        coverage_score = (min(max(coverage_pct, 0.0), 100.0) / 100.0) * 25.0

        # 2. Verification Depth Score (max 25)
        # Evaluates multi-source depth: static source code, configuration, runtime execution, tests
        depth_map = verification_depth_map or {}
        static_weight = depth_map.get("static", 1.0)
        runtime_weight = depth_map.get("runtime", 0.9)
        test_weight = depth_map.get("testing", 1.0)
        security_weight = depth_map.get("security", 1.0)
        
        avg_depth = (static_weight + runtime_weight + test_weight + security_weight) / 4.0
        depth_score = min(max(avg_depth, 0.0), 1.0) * 25.0

        # 3. Reproducibility Score (max 20)
        reproducibility_score = 20.0 if is_reproducible else 0.0

        # 4. Integrity Score (max 15)
        # Check percentage of valid hashes
        valid_hashes = sum(1 for r in records if r.content_hash and r.content_hash == r.calculate_hash())
        integrity_ratio = (valid_hashes / total_records) if total_records > 0 else 1.0
        integrity_score = integrity_ratio * 15.0

        # 5. Freshness Score (max 15)
        # Verify evidence timestamps are recent (within 7 days = full score)
        freshness_score = 15.0
        now = datetime.now(timezone.utc)
        for r in records:
            try:
                rec_dt = datetime.fromisoformat(r.timestamp)
                age_days = (now - rec_dt).total_seconds() / 86400.0
                if age_days > 30:
                    freshness_score = 10.0
                elif age_days > 90:
                    freshness_score = 5.0
            except Exception:
                pass

        total_eqi = round(coverage_score + depth_score + reproducibility_score + integrity_score + freshness_score, 2)

        if total_eqi >= 90.0:
            rating = "ENTERPRISE_GRADE"
        elif total_eqi >= 75.0:
            rating = "ACCEPTABLE"
        else:
            rating = "DEGRADED"

        return EQIBreakdown(
            evidence_coverage_score=round(coverage_score, 2),
            verification_depth_score=round(depth_score, 2),
            reproducibility_score=round(reproducibility_score, 2),
            integrity_score=round(integrity_score, 2),
            freshness_score=round(freshness_score, 2),
            total_eqi=total_eqi,
            rating=rating,
        )
