from typing import Dict, Any, Callable
from ..domain.execution_domain import ExecutionAggregate, ExecutionStarted, ExecutionCompleted
from app.shared_kernel import Result, Ok, Err, get_event_bus
import inspect

class ExecutionService:
    def __init__(self, repo):
        self.repo = repo

    async def execute_task(self, task_id: str, spec_id: str, workload: Callable) -> Result[Dict[str, Any], str]:
        exec_agg = ExecutionAggregate(id=task_id, spec_id=spec_id, status="RUNNING", attempts=1)
        self.repo.save(exec_agg)
        await get_event_bus().publish(ExecutionStarted(execution_id=task_id, spec_id=spec_id))

        try:
            res = await workload() if inspect.iscoroutinefunction(workload) else workload()
            exec_agg.status = "COMPLETED"
            exec_agg.results = res if isinstance(res, dict) else {"output": res}
            self.repo.save(exec_agg)
            await get_event_bus().publish(ExecutionCompleted(execution_id=task_id, status="COMPLETED"))
            return Ok(exec_agg.results)
        except Exception as e:
            exec_agg.status = "FAILED"
            self.repo.save(exec_agg)
            return Err(str(e))
