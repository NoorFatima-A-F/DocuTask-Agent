"""Traffic Router and Dynamic Route Rule Matching."""

from __future__ import annotations

import random
import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from ..mesh.data_plane import MeshRequest


@dataclass
class MatchCondition:
    path: Optional[str] = None
    path_type: str = "prefix"  # "exact", "prefix", "regex"
    method: Optional[str] = None
    headers: Dict[str, str] = field(default_factory=dict)
    query_params: Dict[str, str] = field(default_factory=dict)


@dataclass
class RouteDestination:
    service_name: str
    namespace: str = "default"
    version: str = "v1"
    weight: int = 100
    host: Optional[str] = None
    port: Optional[int] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RouteRule:
    rule_id: str
    name: str
    matches: List[MatchCondition] = field(default_factory=list)
    destinations: List[RouteDestination] = field(default_factory=list)
    priority: int = 100  # Lower number = evaluated first
    timeout_ms: float = 5000.0
    retries: int = 3
    enabled: bool = True


class TrafficRouter:
    """Evaluates mesh requests against dynamic routing rules to select target destinations."""

    def __init__(self):
        self._rules: Dict[str, RouteRule] = {}

    def add_rule(self, rule: RouteRule) -> None:
        self._rules[rule.rule_id] = rule

    def remove_rule(self, rule_id: str) -> bool:
        if rule_id in self._rules:
            del self._rules[rule_id]
            return True
        return False

    def list_rules(self) -> List[RouteRule]:
        return list(self._rules.values())

    def match_route(self, request: MeshRequest) -> Optional[RouteDestination]:
        """Find the highest-priority matching route rule and pick a destination by weight."""
        sorted_rules = sorted(
            [r for r in self._rules.values() if r.enabled],
            key=lambda r: r.priority,
        )

        for rule in sorted_rules:
            if self._evaluate_rule_matches(rule, request):
                return self._select_destination(rule.destinations)

        # Fallback default destination if no rule matched
        return RouteDestination(
            service_name=request.target_service,
            namespace=request.target_namespace,
            version="default",
            weight=100,
        )

    def _evaluate_rule_matches(self, rule: RouteRule, request: MeshRequest) -> bool:
        if not rule.matches:
            return True

        for match in rule.matches:
            if not self._evaluate_single_match(match, request):
                return False
        return True

    def _evaluate_single_match(self, match: MatchCondition, request: MeshRequest) -> bool:
        # Method check
        if match.method and match.method.upper() != request.method.upper():
            return False

        # Path check
        if match.path:
            if match.path_type == "exact" and request.path != match.path:
                return False
            elif match.path_type == "prefix" and not request.path.startswith(match.path):
                return False
            elif match.path_type == "regex" and not re.match(match.path, request.path):
                return False

        # Header check
        for h_key, h_val in match.headers.items():
            actual_val = request.headers.get(h_key)
            if actual_val != h_val:
                return False

        return True

    def _select_destination(self, destinations: List[RouteDestination]) -> Optional[RouteDestination]:
        if not destinations:
            return None
        if len(destinations) == 1:
            return destinations[0]

        total_weight = sum(d.weight for d in destinations)
        if total_weight <= 0:
            return destinations[0]

        rand_val = random.uniform(0, total_weight)
        current = 0.0
        for dest in destinations:
            current += dest.weight
            if rand_val <= current:
                return dest
        return destinations[-1]
