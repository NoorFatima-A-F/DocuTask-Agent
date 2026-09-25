"""
Digital Twin Runtime - Safety Sandbox
Provides an isolated, non-destructive virtual environment for executing shadow and experimental missions.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
import uuid
import time


@dataclass
class SandboxSecurityPolicy:
    allow_external_network: bool = False
    allow_database_writes: bool = False
    allow_filesystem_mutations: bool = False
    max_execution_time_sec: float = 30.0
    mock_responses_enabled: bool = True


@dataclass
class SandboxExecutionRecord:
    sandbox_id: str
    target_pipeline_id: str
    status: str  # ISOLATED_SUCCESS | INTERCEPTED_MUTATION | TIMEOUT | FAILED
    intercepted_mutations: List[Dict[str, Any]] = field(default_factory=list)
    simulated_duration_ms: float = 0.0
    virtual_state: Dict[str, Any] = field(default_factory=dict)
    created_at: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "sandbox_id": self.sandbox_id,
            "target_pipeline_id": self.target_pipeline_id,
            "status": self.status,
            "intercepted_mutations": self.intercepted_mutations,
            "simulated_duration_ms": self.simulated_duration_ms,
            "virtual_state": self.virtual_state,
            "created_at": self.created_at,
        }


class SafetySandbox:
    """Isolates runtime execution to prevent side effects during shadow evaluation."""

    def __init__(self, policy: Optional[SandboxSecurityPolicy] = None):
        self.policy = policy or SandboxSecurityPolicy()

    def create_sandbox(self, pipeline_id: str) -> str:
        return f"sbx_{pipeline_id}_{uuid.uuid4().hex[:8]}"

    def execute_in_sandbox(
        self,
        sandbox_id: str,
        pipeline_id: str,
        simulated_actions: List[Dict[str, Any]],
    ) -> SandboxExecutionRecord:
        record = SandboxExecutionRecord(
            sandbox_id=sandbox_id,
            target_pipeline_id=pipeline_id,
            status="ISOLATED_SUCCESS",
        )

        t0 = time.perf_counter()
        for action in simulated_actions:
            action_type = action.get("type", "UNKNOWN")
            is_mutation = action.get("is_mutation", False)

            if is_mutation:
                # Intercept destructive operations
                record.intercepted_mutations.append({
                    "action_type": action_type,
                    "target": action.get("target", "DB/FILE"),
                    "payload_preview": str(action.get("payload", {}))[:100],
                    "blocked_at": time.time(),
                })
                # Apply strictly to virtual state
                record.virtual_state[action.get("key", f"var_{len(record.virtual_state)}")] = action.get("value", "mocked_value")
            else:
                record.virtual_state[action.get("key", f"read_{len(record.virtual_state)}")] = "read_success"

        elapsed_ms = (time.perf_counter() - t0) * 1000.0
        record.simulated_duration_ms = round(elapsed_ms + 120.0, 2)  # Base simulated latency
        if record.intercepted_mutations:
            record.status = "INTERCEPTED_MUTATION"

        return record
