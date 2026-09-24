"""
9. Workforce Performance Intelligence Subsystem
"""
from app.platform_workforce.models.schemas import WorkforcePerformanceMetric
from app.platform_workforce.registry.workforce_registry import workforce_registry

class WorkforcePerformanceIntelligence:
    def get_workforce_metrics(self, tenant_id: str = "default-tenant") -> WorkforcePerformanceMetric:
        employees = workforce_registry.get_employees(tenant_id)
        total = len(employees)
        if total == 0:
            return WorkforcePerformanceMetric(tenant_id=tenant_id)
            
        active = sum(1 for e in employees if e.availability_status == "ACTIVE")
        avg_trust = sum(e.trust_score for e in employees) / total
        avg_success = sum(e.task_success_rate for e in employees) / total
        avg_burnout = sum(e.burnout_risk_score for e in employees) / total
        total_salary = sum(e.hourly_salary_usd * 160 for e in employees)  # 160 hrs/mo
        
        return WorkforcePerformanceMetric(
            tenant_id=tenant_id,
            total_workforce_headcount=total,
            active_employees_count=active,
            workforce_utilization_rate=round(active / max(total, 1), 2),
            average_trust_score=round(avg_trust, 3),
            average_task_success_rate=round(avg_success, 3),
            collaboration_index=0.94,
            innovation_velocity_score=0.91,
            workforce_burnout_risk=round(avg_burnout, 3),
            monthly_salary_burn_usd=round(total_salary, 2)
        )

workforce_performance_intelligence = WorkforcePerformanceIntelligence()
