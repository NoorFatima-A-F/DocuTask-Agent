"""FastAPI Routes for Global Workload Scheduling and Diagnostics."""

from typing import Any, Dict, List, Optional
from fastapi import APIRouter, HTTPException, status

from app.infrastructure.executions.workload import WorkloadRequest
from app.infrastructure.sdk.scheduling import SchedulingSDK

router = APIRouter(prefix="/api/v1/infrastructure/scheduling", tags=["Execution Scheduler"])

scheduling_sdk = SchedulingSDK()


@router.post("/submit", response_model=Dict[str, Any], status_code=status.HTTP_200_OK)
def submit_workload(workload: WorkloadRequest) -> Dict[str, Any]:
    success, assignment, decision = scheduling_sdk.submit(workload)
    return {
        "success": success,
        "workload_id": workload.workload_id,
        "assignment": assignment.model_dump(mode="json") if assignment else None,
        "decision": decision.model_dump(mode="json"),
    }


@router.get("/workloads/{workload_id}", response_model=Dict[str, Any])
def get_workload_status(workload_id: str) -> Dict[str, Any]:
    state = scheduling_sdk.status(workload_id)
    if not state:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Workload '{workload_id}' not found.",
        )
    return {"workload_id": workload_id, "state": state.value}


@router.post("/workloads/{workload_id}/cancel", response_model=Dict[str, Any])
def cancel_workload(workload_id: str) -> Dict[str, Any]:
    cancelled = scheduling_sdk.cancel(workload_id)
    if not cancelled:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Workload '{workload_id}' not found.",
        )
    return {"workload_id": workload_id, "status": "CANCELLED"}


@router.post("/workloads/{workload_id}/reschedule", response_model=Dict[str, Any])
def reschedule_workload(workload_id: str) -> Dict[str, Any]:
    success, assignment, decision = scheduling_sdk.reschedule(workload_id)
    if decision is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Workload '{workload_id}' not found.",
        )
    return {
        "success": success,
        "workload_id": workload_id,
        "assignment": assignment.model_dump(mode="json") if assignment else None,
        "decision": decision.model_dump(mode="json"),
    }


@router.get("/workloads/{workload_id}/diagnostics", response_model=Dict[str, Any])
def get_workload_diagnostics(workload_id: str) -> Dict[str, Any]:
    report = scheduling_sdk.diagnostics(workload_id)
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Workload '{workload_id}' not found.",
        )
    return report.model_dump(mode="json")


@router.post("/recover", response_model=List[Dict[str, Any]])
def recover_lost_workers() -> List[Dict[str, Any]]:
    recovered = scheduling_sdk.recover_lost_workers()
    return [{"workload_id": wid, "classification": cls.value} for wid, cls in recovered]
