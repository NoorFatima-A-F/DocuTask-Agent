"""Structured JSON Log Formatter with PII and Credential Masking."""

from __future__ import annotations

import json
import time
from typing import Any, Dict, Optional

from ..core.context import ObservabilityContext, get_current_context

SENSITIVE_KEYS = {"password", "secret", "token", "api_key", "authorization", "bearer", "private_key", "credit_card"}


class JSONLogFormatter:
    """Formats log records into structured JSON compliant with enterprise SRE schemas."""

    def __init__(self, mask_pii: bool = True):
        self.mask_pii = mask_pii

    def _mask_value(self, key: str, value: Any) -> Any:
        if not self.mask_pii:
            return value
        if any(sens in key.lower() for sens in SENSITIVE_KEYS):
            return "******[MASKED]******"
        if isinstance(value, dict):
            return {k: self._mask_value(k, v) for k, v in value.items()}
        if isinstance(value, list):
            return [self._mask_value(key, item) for item in value]
        return value

    def format(
        self,
        level: str,
        message: str,
        context: Optional[ObservabilityContext] = None,
        extra_metadata: Optional[Dict[str, Any]] = None,
        service_name: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Produce a structured log dictionary."""
        ctx = context or get_current_context()
        now = time.time()
        effective_service = service_name or ctx.service_name

        metadata = dict(ctx.metadata)
        if extra_metadata:
            metadata.update(extra_metadata)

        masked_metadata = {k: self._mask_value(k, v) for k, v in metadata.items()}

        return {
            "timestamp": now,
            "service": effective_service,
            "version": ctx.service_version,
            "level": level.upper(),
            "message": message,
            "trace_id": ctx.trace_id,
            "span_id": ctx.span_id,
            "tenant_id": ctx.tenant_id,
            "org_id": ctx.org_id,
            "environment": ctx.environment,
            "region": ctx.region,
            "cluster_id": ctx.cluster_id,
            "workflow_id": ctx.workflow_id,
            "agent_id": ctx.agent_id,
            "metadata": masked_metadata,
        }

    def format_json_string(
        self,
        level: str,
        message: str,
        context: Optional[ObservabilityContext] = None,
        extra_metadata: Optional[Dict[str, Any]] = None,
        service_name: Optional[str] = None,
    ) -> str:
        record = self.format(level, message, context, extra_metadata, service_name=service_name)
        return json.dumps(record)
