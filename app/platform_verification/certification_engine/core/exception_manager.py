"""
Exception Management Engine for formal risk acceptance and temporary gate waivers.
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Dict, List, Optional
import uuid
from app.platform_verification.certification_engine.domain.interfaces import IExceptionManager
from app.platform_verification.certification_engine.domain.models import (
    ExceptionRequest,
    ExceptionStatus,
)


class EnterpriseExceptionManager(IExceptionManager):
    """Manages time-bounded quality gate waivers with expiration enforcement."""

    def __init__(self):
        self._exceptions: Dict[str, ExceptionRequest] = {}

    def request_exception(self, request: ExceptionRequest) -> ExceptionRequest:
        if not request.exception_id:
            request.exception_id = f"EXC-{uuid.uuid4().hex[:8].upper()}"
        self._exceptions[request.exception_id] = request
        return request

    def approve_exception(self, exception_id: str, approver: str) -> ExceptionRequest:
        req = self._exceptions.get(exception_id)
        if not req:
            raise KeyError(f"Exception request '{exception_id}' not found.")

        req.status = ExceptionStatus.APPROVED
        req.approver = approver
        req.approved_at = datetime.now(timezone.utc).isoformat()
        return req

    def get_active_exceptions_for_system(self, system_id: str) -> List[ExceptionRequest]:
        now_dt = datetime.now(timezone.utc)
        active: List[ExceptionRequest] = []
        for req in self._exceptions.values():
            if req.system_id == system_id and req.status == ExceptionStatus.APPROVED:
                expires_dt = datetime.fromisoformat(req.expires_at)
                if now_dt <= expires_dt:
                    active.append(req)
                else:
                    req.status = ExceptionStatus.EXPIRED
        return active
