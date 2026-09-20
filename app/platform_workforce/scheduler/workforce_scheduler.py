"""
13. Autonomous Workforce Scheduler Subsystem
"""
from typing import Dict, List
from app.platform_workforce.models.schemas import WorkforceScheduleEntry

class WorkforceScheduler:
    def __init__(self):
        self._schedules: Dict[str, Dict[str, WorkforceScheduleEntry]] = {}
        self._seed_default_schedules()

    def _seed_default_schedules(self):
        tenant = "default-tenant"
        scheds = [
            WorkforceScheduleEntry(id="sch-01", employee_id="emp-ceo-01", shift_name="EXECUTIVE_ALWAYS_ON", start_hour=0, end_hour=24),
            WorkforceScheduleEntry(id="sch-02", employee_id="emp-eng-vp", shift_name="US_CORE_DEVELOPMENT", start_hour=8, end_hour=16),
            WorkforceScheduleEntry(id="sch-03", employee_id="emp-doc-spec-01", shift_name="APAC_FOLLOW_THE_SUN", start_hour=16, end_hour=24),
            WorkforceScheduleEntry(id="sch-04", employee_id="emp-qa-rev-01", shift_name="EMEA_MAINTENANCE_SWEEP", start_hour=0, end_hour=8)
        ]
        self._schedules[tenant] = {s.id: s for s in scheds}

    def get_schedules(self, tenant_id: str = "default-tenant") -> List[WorkforceScheduleEntry]:
        return list(self._schedules.get(tenant_id, {}).values())

    def create_schedule_entry(self, employee_id: str, shift_name: str, start_hour: int, end_hour: int, tenant_id: str = "default-tenant") -> WorkforceScheduleEntry:
        entry = WorkforceScheduleEntry(
            tenant_id=tenant_id,
            employee_id=employee_id,
            shift_name=shift_name,
            start_hour=start_hour,
            end_hour=end_hour
        )
        if tenant_id not in self._schedules:
            self._schedules[tenant_id] = {}
        self._schedules[tenant_id][entry.id] = entry
        return entry

workforce_scheduler = WorkforceScheduler()
