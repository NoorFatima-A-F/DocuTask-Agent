"""
Section 12.1: Master AI Security Scoring Engine
Computes the weighted AI Security Score across the 8 core enterprise domains.
"""
from typing import Dict, List
from ..domain.models import SecuritySectionResult, MasterSecurityScore, SecurityCategory

WEIGHT_DISTRIBUTION: Dict[SecurityCategory, float] = {
    SecurityCategory.AUTHENTICATION: 10.0,
    SecurityCategory.AUTHORIZATION: 15.0,
    SecurityCategory.TENANT_ISOLATION: 15.0,
    SecurityCategory.API_SECURITY: 10.0,
    SecurityCategory.LLM_SECURITY: 20.0,
    SecurityCategory.AGENT_SECURITY: 15.0,
    SecurityCategory.DATA_PROTECTION: 10.0,
    SecurityCategory.RESPONSIBLE_AI: 5.0,
}

class SecurityScorer:
    def __init__(self):
        pass

    def compute_master_score(self, section_results: List[SecuritySectionResult], tenant_id: str = "enterprise-v9-security", duration_ms: float = 0.0) -> MasterSecurityScore:
        category_scores: Dict[str, float] = {}
        category_weights: Dict[str, float] = {}
        
        total_checks = sum(s.total_checks for s in section_results)
        passed_checks = sum(s.passed_checks for s in section_results)
        failed_checks = total_checks - passed_checks
        
        total_attacks_tested = sum(s.attacks_tested for s in section_results)
        total_attacks_blocked = sum(s.attacks_blocked for s in section_results)
        
        category_scores_list: Dict[str, List[float]] = {}
        for sec in section_results:
            cat_str = sec.category.value
            if cat_str not in category_scores_list:
                category_scores_list[cat_str] = []
            category_scores_list[cat_str].append(sec.score)
            category_weights[cat_str] = WEIGHT_DISTRIBUTION.get(sec.category, 5.0)
            
        for cat_str, scores in category_scores_list.items():
            category_scores[cat_str] = round(sum(scores) / len(scores), 2)
            
        # Compute weighted sum
        weighted_sum = 0.0
        total_weight = 0.0
        for cat_str, score in category_scores.items():
            w = category_weights.get(cat_str, 5.0)
            weighted_sum += (score * w)
            total_weight += w
            
        overall_score = round(weighted_sum / total_weight, 2) if total_weight > 0 else 100.0
        
        if overall_score >= 95.0:
            grade = "A+ (Enterprise Hardened)"
        elif overall_score >= 90.0:
            grade = "A (Production Ready)"
        else:
            grade = "B (Requires Hardening)"
            
        defense_rate = round((total_attacks_blocked / max(total_attacks_tested, 1)) * 100.0, 2)
        
        return MasterSecurityScore(
            tenant_id=tenant_id,
            overall_score=overall_score,
            grade=grade,
            category_scores=category_scores,
            section_results=section_results,
            total_checks=total_checks,
            passed_checks=passed_checks,
            failed_checks=failed_checks,
            total_attacks_tested=total_attacks_tested,
            total_attacks_blocked=total_attacks_blocked,
            defense_rate_pct=defense_rate,
            verification_duration_ms=round(duration_ms, 2)
        )
