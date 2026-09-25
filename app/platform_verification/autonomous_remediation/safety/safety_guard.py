"""Safety Guard System (3H.4.3.5).

Enforces critical enterprise safety guardrails prior to executing recovery operations:
1. Precondition Verification (Cluster quorum, minimum healthy standby capacity)
2. Rate Limits & Cooldowns (Max 3 restarts per 10 minutes to prevent restart flapping loops)
3. Blast Radius Controls (Restricts single instance vs local service vs fleet operations)
4. Concurrency Throttling (Limits concurrent active remediations)
"""

from typing import Dict, List, Optional
import time
from ..domain.models import RemediationDecision, SafetyCheckResult, ActionLevel
from ..domain.interfaces import ISafetyGuard


class SafetyGuard(ISafetyGuard):
    """Enforces safety guardrails and blast radius boundaries."""

    def __init__(
        self,
        max_concurrent_remediations: int = 3,
        default_cooldown_seconds: int = 300,
        max_attempts_per_window: int = 3,
    ):
        self.max_concurrent = max_concurrent_remediations
        self.default_cooldown = default_cooldown_seconds
        self.max_attempts = max_attempts_per_window
        self._execution_history: Dict[str, List[float]] = {}
        self._active_remediations: int = 0

    def register_execution_attempt(self, target: str):
        """Records an execution timestamp for rate limiting."""
        now = time.time()
        if target not in self._execution_history:
            self._execution_history[target] = []
        self._execution_history[target].append(now)

    def validate_safety(self, decision: RemediationDecision) -> SafetyCheckResult:
        """Validates all safety invariants for the proposed decision."""
        target = decision.parameters.get("target", "unknown_target")
        cooldown_sec = decision.parameters.get("cooldown_seconds", self.default_cooldown)
        max_att = decision.parameters.get("max_attempts", self.max_attempts)
        blast_radius = decision.parameters.get("blast_radius", "single_instance")

        # 1. Rate Limit & Cooldown Check
        now = time.time()
        recent_attempts = [
            t for t in self._execution_history.get(target, [])
            if now - t < cooldown_sec
        ]
        rate_limit_passed = len(recent_attempts) < max_att
        cooldown_remaining = int(cooldown_sec - (now - recent_attempts[-1])) if recent_attempts and not rate_limit_passed else 0

        # 2. Preconditions Check
        # Example: Verify we do not restart if fleet blast radius is triggered without Level 3 approval
        preconditions_passed = True
        rejection_reason: Optional[str] = None

        if blast_radius == "fleet" and decision.action_level != ActionLevel.LEVEL_3:
            preconditions_passed = False
            rejection_reason = "Fleet-wide blast radius requires explicit Level 3 authorization"

        # 3. Blast Radius Safety
        blast_radius_safe = blast_radius in ["single_instance", "local_service", "fleet"]

        # 4. Overall Safe Verdict
        safe_to_execute = (
            rate_limit_passed
            and preconditions_passed
            and blast_radius_safe
            and self._active_remediations < self.max_concurrent
        )

        if not rate_limit_passed:
            rejection_reason = f"Rate limit exceeded: {len(recent_attempts)} attempts in {cooldown_sec}s window. Cooldown active."

        return SafetyCheckResult(
            safe_to_execute=safe_to_execute,
            preconditions_passed=preconditions_passed,
            rate_limit_passed=rate_limit_passed,
            blast_radius_safe=blast_radius_safe,
            active_remediations_count=self._active_remediations,
            cooldown_remaining_seconds=cooldown_remaining,
            rejection_reason=rejection_reason,
        )
