"""
Configurable Architecture Rule Engine.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional
import uuid
from app.platform_verification.architecture_verification.domain.interfaces import IArchitectureRuleEngine
from app.platform_verification.architecture_verification.domain.models import (
    ArchitectureDependency,
    ArchitectureRule,
    ArchitectureViolation,
    CircularDependencyCycle,
    RuleCategory,
    RuleFailureAction,
    RuleSeverity,
)


class EnterpriseArchitectureRuleEngine(IArchitectureRuleEngine):
    """Evaluates layer isolation, naming constraints, and complexity rules."""

    def __init__(self):
        self._rules: Dict[str, ArchitectureRule] = {}
        self._initialize_default_rules()

    def register_rule(self, rule: ArchitectureRule) -> None:
        self._rules[rule.id] = rule

    def evaluate_rules(
        self,
        dependencies: List[ArchitectureDependency],
        file_metrics: Dict[str, Any],
        circular_cycles: List[CircularDependencyCycle],
    ) -> List[ArchitectureViolation]:
        violations: List[ArchitectureViolation] = []

        # 1. Circular dependency violations
        for cycle in circular_cycles:
            violations.append(
                ArchitectureViolation(
                    violation_id=f"VIOL-CIRC-{uuid.uuid4().hex[:6].upper()}",
                    rule_id="ARCH_CIRCULAR_001",
                    rule_name="Zero Circular Dependencies",
                    category=RuleCategory.DEPENDENCY,
                    severity=RuleSeverity.CRITICAL,
                    source_file=cycle.cycle_path[0] if cycle.cycle_path else "unknown",
                    line_number=1,
                    message=cycle.description,
                    failure_action=RuleFailureAction.BLOCK_PIPELINE,
                )
            )

        # 2. Dependency layer isolation rules
        for dep in dependencies:
            for rule in self._rules.values():
                if rule.category == RuleCategory.DEPENDENCY:
                    for src_pat, tgt_pat in rule.forbidden_import_patterns:
                        if src_pat in dep.source_module and tgt_pat in dep.target_module:
                            dep.allowed = False
                            dep.violation_rule_id = rule.id
                            dep.severity = rule.severity
                            violations.append(
                                ArchitectureViolation(
                                    violation_id=f"VIOL-{uuid.uuid4().hex[:6].upper()}",
                                    rule_id=rule.id,
                                    rule_name=rule.name,
                                    category=rule.category,
                                    severity=rule.severity,
                                    source_file=dep.source_module,
                                    line_number=dep.line_number,
                                    message=f"Layer violation: '{dep.source_module}' is forbidden from importing '{dep.target_module}' ({rule.description})",
                                    failure_action=rule.failure_action,
                                )
                            )

        # 3. Complexity rules
        for rel_path, metrics in file_metrics.items():
            lines = metrics.get("line_count", 0)
            if lines > 1200:
                violations.append(
                    ArchitectureViolation(
                        violation_id=f"VIOL-COMPLEX-{uuid.uuid4().hex[:6].upper()}",
                        rule_id="ARCH_COMPLEXITY_001",
                        rule_name="File Complexity Limit",
                        category=RuleCategory.COMPLEXITY,
                        severity=RuleSeverity.MEDIUM,
                        source_file=rel_path,
                        line_number=1,
                        message=f"File exceeds maximum line limit ({lines} > 1200 lines).",
                        failure_action=RuleFailureAction.WARN_ONLY,
                    )
                )

        return violations

    def _initialize_default_rules(self) -> None:
        # Rule 1: Domain cannot import Infrastructure
        self.register_rule(
            ArchitectureRule(
                id="ARCH_DEP_001",
                name="Domain Layer Isolation",
                category=RuleCategory.DEPENDENCY,
                severity=RuleSeverity.CRITICAL,
                description="Domain entities and aggregates must not depend on concrete infrastructure",
                forbidden_import_patterns=[
                    ("domain", "infrastructure"),
                    ("domain", "sqlalchemy"),
                    ("domain", "fastapi"),
                    ("domain", "google.generativeai"),
                ],
                failure_action=RuleFailureAction.BLOCK_PIPELINE,
            )
        )

        # Rule 2: Shared Kernel must not depend on Application layers
        self.register_rule(
            ArchitectureRule(
                id="ARCH_DEP_002",
                name="Shared Kernel Purity",
                category=RuleCategory.DEPENDENCY,
                severity=RuleSeverity.CRITICAL,
                description="Shared Kernel must only depend on primitive standard libraries",
                forbidden_import_patterns=[
                    ("shared_kernel", "app.api"),
                    ("shared_kernel", "app.services"),
                    ("shared_kernel", "app.infrastructure"),
                ],
                failure_action=RuleFailureAction.BLOCK_PIPELINE,
            )
        )
