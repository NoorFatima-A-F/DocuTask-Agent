from dataclasses import dataclass, field
import hashlib
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
import uuid
from app.platform_verification.lifecycle.states import LifecycleState

@dataclass
class StageResult:
    stage_name: str
    status: str
    executed_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    produced_artifacts: Dict[str, Any] = field(default_factory=dict)
    details: Dict[str, Any] = field(default_factory=dict)

@dataclass
class VerificationExecutionContext:
    definition_id: str
    tenant_id: str
    initiator: str = "Automated System"
    execution_id: str = field(default_factory=lambda: f"exec_{uuid.uuid4().hex[:12]}")
    current_state: LifecycleState = LifecycleState.CREATED
    stage_results: List[StageResult] = field(default_factory=list)
    state_history: List[LifecycleState] = field(default_factory=list)
    config_fingerprint: str = field(default_factory=lambda: hashlib.sha256(b"default-config").hexdigest())
    archival_bundle_hash: Optional[str] = None
    certification_decision: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
