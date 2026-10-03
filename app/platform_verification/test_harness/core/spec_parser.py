"""
Declarative Verification Test Specification Parser and Validator.
"""
from __future__ import annotations
from typing import Any, Dict
from app.platform_verification.test_harness.domain.models import (
    VerificationTestSpec,
    TestCategory,
    TestHarnessLevel,
    RetryPolicy,
)


class TestSpecParser:
    """Parses and validates declarative verification test specifications."""
    __test__ = False

    @staticmethod
    def parse_dict(data: Dict[str, Any]) -> VerificationTestSpec:
        if "id" not in data or "name" not in data:
            raise ValueError("Test specification must contain 'id' and 'name'.")

        cat_str = data.get("category", "functional").lower()
        level_str = data.get("level", "component").lower()

        category = TestCategory(cat_str) if cat_str in [c.value for c in TestCategory] else TestCategory.FUNCTIONAL
        level = TestHarnessLevel(level_str) if level_str in [l.value for l in TestHarnessLevel] else TestHarnessLevel.COMPONENT

        retry_dict = data.get("retry_policy", {})
        retry_policy = RetryPolicy(
            max_retries=retry_dict.get("max_retries", 3),
            initial_delay_ms=retry_dict.get("initial_delay_ms", 50.0),
            backoff_factor=retry_dict.get("backoff_factor", 2.0),
            max_delay_ms=retry_dict.get("max_delay_ms", 1000.0),
        )

        return VerificationTestSpec(
            id=data["id"],
            name=data["name"],
            description=data.get("description", ""),
            category=category,
            level=level,
            environment=data.get("environment", "staging"),
            dataset=data.get("dataset", {"id": "default_ds", "version": "v1.0"}),
            dependencies=data.get("dependencies", []),
            execution=data.get("execution", {}),
            validation=data.get("validation", {}),
            metrics=data.get("metrics", ["accuracy", "latency"]),
            evidence=data.get("evidence", ["logs", "traces"]),
            timeout_ms=data.get("timeout_ms", 5000),
            retry_policy=retry_policy,
        )
