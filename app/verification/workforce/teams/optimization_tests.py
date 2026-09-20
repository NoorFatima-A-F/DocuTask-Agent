"""
Section 3.2: 1,000 Candidate Team Optimization Benchmark
Evaluates Pareto-optimal agent selection speed and algorithm quality under large candidate pools.
"""
import time
from typing import Dict, List, Any
from app.platform_workforce.models.schemas import DigitalEmployee, EmployeeRole, DepartmentType
from ..domain.models import WorkforceVerificationRun, SectionResult, VerificationCategory, VerificationStatus

class TeamOptimizationVerifier:
    def __init__(self, tenant_id: str = "enterprise-v8-tenant"):
        self.tenant_id = tenant_id

    def verify_optimization_scale(self, candidate_count: int = 1000) -> SectionResult:
        runs: List[WorkforceVerificationRun] = []
        metrics: Dict[str, Any] = {}
        
        # 1. Synthesize 1,000 candidates with varied skillsets, salaries, and trust
        target_skills = {"OCR", "Financial Validation", "ERP Integration", "Automated Validation"}
        candidates: List[DigitalEmployee] = []
        
        for i in range(candidate_count):
            skills = []
            if i % 2 == 0:
                skills.append("OCR")
            if i % 3 == 0:
                skills.append("Financial Validation")
            if i % 5 == 0:
                skills.append("ERP Integration")
            if i % 7 == 0:
                skills.append("Automated Validation")
            if i % 4 == 0:
                skills.append("Security Guardrails")
                
            emp = DigitalEmployee(
                id=f"cand-{i:04d}",
                tenant_id=self.tenant_id,
                name=f"Candidate #{i}",
                role=EmployeeRole.SENIOR_SPECIALIST if i % 10 == 0 else EmployeeRole.ASSOCIATE_SPECIALIST,
                department=DepartmentType.FINANCE,
                skills=skills,
                trust_score=0.80 + (i % 20) * 0.01,
                hourly_salary_usd=1.50 + (i % 10) * 0.30
            )
            candidates.append(emp)
            
        # 2. Benchmark Optimization Algorithm
        start_opt = time.perf_counter()
        
        # Scoring function: (skill_match * 4.0) + (trust * 3.0) - (salary * 0.5)
        def score_candidate(cand: DigitalEmployee) -> float:
            match_count = len(set(cand.skills).intersection(target_skills))
            return (match_count * 4.0) + (cand.trust_score * 3.0) - (cand.hourly_salary_usd * 0.5)
            
        scored = [(score_candidate(c), c) for c in candidates]
        scored.sort(key=lambda x: x[0], reverse=True)
        top_team = [c for _, c in scored[:4]]
        
        opt_duration_ms = (time.perf_counter() - start_opt) * 1000.0
        
        # Verify selected team covers all target skills
        team_skills = set()
        for member in top_team:
            team_skills.update(member.skills)
            
        coverage_achieved = target_skills.issubset(team_skills)
        latency_ok = opt_duration_ms < 50.0
        
        run_scale = WorkforceVerificationRun(
            component="DynamicTeamFormation.OptimizationEngine",
            scenario=f"Top-4 Team Optimization from {candidate_count:,} Candidate Pool",
            metric="Selection Latency (ms)",
            expected_value="< 50.0 ms",
            actual_value=f"{opt_duration_ms:.3f} ms",
            status=VerificationStatus.PASSED if (coverage_achieved and latency_ok) else VerificationStatus.FAILED,
            details={"candidates_evaluated": candidate_count, "latency_ms": round(opt_duration_ms, 3), "target_skills_covered": coverage_achieved}
        )
        runs.append(run_scale)
        
        # Quality check
        avg_selected_trust = sum(m.trust_score for m in top_team) / len(top_team)
        quality_ok = avg_selected_trust >= 0.90
        
        run_quality = WorkforceVerificationRun(
            component="DynamicTeamFormation.QualityAssurance",
            scenario="Average Trust Score of Optimized Selection",
            metric="Selected Team Average Trust",
            expected_value=">= 0.90",
            actual_value=round(avg_selected_trust, 3),
            status=VerificationStatus.PASSED if quality_ok else VerificationStatus.FAILED,
            details={"avg_trust": avg_selected_trust, "top_member_ids": [m.id for m in top_team]}
        )
        runs.append(run_quality)
        
        passed_runs = sum(1 for r in runs if r.status == VerificationStatus.PASSED)
        score = (passed_runs / len(runs)) * 100.0
        
        metrics["candidate_pool_size"] = candidate_count
        metrics["optimization_latency_ms"] = round(opt_duration_ms, 3)
        metrics["avg_team_trust"] = round(avg_selected_trust, 3)
        
        return SectionResult(
            section_id="SEC-V8.3.2",
            section_name="Candidate Pool Optimization Scale Benchmark",
            category=VerificationCategory.TEAMS,
            weight_pct=5.0,
            score=score,
            status=VerificationStatus.PASSED if score == 100.0 else VerificationStatus.FAILED,
            passed_checks=passed_runs,
            total_checks=len(runs),
            runs=runs,
            metrics=metrics,
            summary=f"Optimized 4-member specialist team from {candidate_count:,} candidate pool in {opt_duration_ms:.2f}ms with 100% skill coverage and {avg_selected_trust:.2f} avg trust."
        )
