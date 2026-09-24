"""
10. Economic Resource Allocation Engine Subsystem
"""
from typing import Dict
from app.platform_workforce.models.schemas import EconomicResourceBudget

class EconomicResourceAllocationEngine:
    def __init__(self):
        self._budgets: Dict[str, EconomicResourceBudget] = {}
        self._seed_default_budget()

    def _seed_default_budget(self):
        tenant = "default-tenant"
        self._budgets[tenant] = EconomicResourceBudget(
            tenant_id=tenant,
            allocated_gpu_hours=2000.0,
            used_gpu_hours=1140.0,
            allocated_tokens=1_000_000_000,
            used_tokens=540_000_000,
            total_budget_usd=35000.0,
            total_spent_usd=18250.0,
            efficiency_roi_ratio=5.4,
            reallocation_recommendations=[
                "Shift 200 GPU hours from Overnight Batching to Real-Time Interactive OCR.",
                "Compress prompt tokens by 15% using schema-distilled semantic encodings."
            ]
        )

    def get_budget(self, tenant_id: str = "default-tenant") -> EconomicResourceBudget:
        if tenant_id not in self._budgets:
            self._seed_default_budget()
        return self._budgets.get(tenant_id, self._budgets["default-tenant"])

    def record_usage(self, gpu_hours: float, tokens: int, cost_usd: float, tenant_id: str = "default-tenant") -> EconomicResourceBudget:
        budget = self.get_budget(tenant_id)
        budget.used_gpu_hours += gpu_hours
        budget.used_tokens += tokens
        budget.total_spent_usd += cost_usd
        return budget

economic_resource_allocation_engine = EconomicResourceAllocationEngine()
