"""
4. Task Marketplace & Internal Economy Subsystem
"""
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
from app.platform_workforce.models.schemas import TaskMarketplaceListing, TaskBid, EmployeeStatus
from app.platform_workforce.registry.workforce_registry import workforce_registry

class TaskMarketplace:
    def __init__(self):
        self._tasks: Dict[str, Dict[str, TaskMarketplaceListing]] = {}
        self._seed_default_tasks()

    def _seed_default_tasks(self):
        tenant = "default-tenant"
        tasks = [
            TaskMarketplaceListing(
                id="task-batch-ocr-99",
                title="Extract Multi-Page Financial Statements",
                description="High precision table extraction and ledger reconciliation.",
                required_skills=["Document Extraction", "OCR Verification"],
                priority="HIGH",
                budget_max_usd=25.0,
                status="BIDDING",
                bids=[
                    {
                        "bid_id": "bid-01",
                        "employee_id": "emp-doc-spec-01",
                        "bid_cost_usd": 12.50,
                        "estimated_duration_minutes": 15.0,
                        "confidence_score": 0.98,
                        "proposed_solution_outline": "Streamed parallel table parsing with bounding box verification."
                    }
                ]
            ),
            TaskMarketplaceListing(
                id="task-audit-guard-12",
                title="Autonomous Compliance & PII Redaction Audit",
                description="Verify zero confidential leakages in outbound reports.",
                required_skills=["Compliance Guardrails", "Automated Validation"],
                priority="CRITICAL",
                budget_max_usd=40.0,
                status="OPEN"
            )
        ]
        self._tasks[tenant] = {t.id: t for t in tasks}

    def get_tasks(self, tenant_id: str = "default-tenant", status: Optional[str] = None) -> List[TaskMarketplaceListing]:
        listings = list(self._tasks.get(tenant_id, {}).values())
        if status:
            listings = [t for t in listings if t.status == status]
        return listings

    def post_task(self, title: str, description: str, required_skills: List[str], budget_max_usd: float = 30.0, priority: str = "MEDIUM", tenant_id: str = "default-tenant") -> TaskMarketplaceListing:
        task = TaskMarketplaceListing(
            tenant_id=tenant_id,
            title=title,
            description=description,
            required_skills=required_skills,
            budget_max_usd=budget_max_usd,
            priority=priority,
            status="OPEN"
        )
        if tenant_id not in self._tasks:
            self._tasks[tenant_id] = {}
        self._tasks[tenant_id][task.id] = task
        return task

    def submit_bid(self, task_id: str, employee_id: str, bid_cost_usd: float, estimated_duration_minutes: float, solution_outline: str = "", tenant_id: str = "default-tenant") -> Optional[TaskMarketplaceListing]:
        task = self._tasks.get(tenant_id, {}).get(task_id)
        if not task:
            return None
        bid_entry = {
            "bid_id": f"bid-{datetime.now(timezone.utc).strftime('%M%S')}",
            "employee_id": employee_id,
            "bid_cost_usd": bid_cost_usd,
            "estimated_duration_minutes": estimated_duration_minutes,
            "confidence_score": 0.96,
            "proposed_solution_outline": solution_outline
        }
        task.bids.append(bid_entry)
        task.status = "BIDDING"
        return task

    def assign_optimal_bid(self, task_id: str, tenant_id: str = "default-tenant") -> Optional[TaskMarketplaceListing]:
        task = self._tasks.get(tenant_id, {}).get(task_id)
        if not task or not task.bids:
            return None
        # Pick best bid based on cost and confidence
        sorted_bids = sorted(task.bids, key=lambda b: (b.get("bid_cost_usd", 100), -b.get("confidence_score", 0)))
        winner = sorted_bids[0]
        task.assigned_employee_id = winner["employee_id"]
        task.status = "ASSIGNED"
        
        # Mark employee as busy
        workforce_registry.update_employee_status(winner["employee_id"], EmployeeStatus.BUSY, tenant_id)
        return task

task_marketplace = TaskMarketplace()
