"""
Module Boundary Validator enforcing explicit dependencies and forbidding hidden leaks.
"""
from __future__ import annotations
from typing import List, Optional
import uuid
from app.platform_verification.module_boundary.domain.interfaces import (
    IModuleBoundaryValidator,
    IModuleRegistry,
)
from app.platform_verification.module_boundary.domain.models import (
    BoundaryViolationSeverity,
    ModuleBoundaryViolation,
    ModuleDependencyEdge,
)


class EnterpriseModuleBoundaryValidator(IModuleBoundaryValidator):
    """Enforces that modules only communicate via exported contracts and allowed dependencies."""

    def __init__(self, registry: IModuleRegistry):
        self.registry = registry

    def validate_dependencies(
        self,
        dependencies: List[ModuleDependencyEdge],
    ) -> List[ModuleBoundaryViolation]:
        violations: List[ModuleBoundaryViolation] = []

        for dep in dependencies:
            src_manifest = self.registry.get_module(dep.source_module)
            if not src_manifest:
                continue

            # 1. Check if target is explicitly forbidden
            if dep.target_module in src_manifest.forbidden_dependencies:
                dep.is_allowed = False
                dep.severity = BoundaryViolationSeverity.CRITICAL
                dep.violation_reason = f"Module '{dep.source_module}' is explicitly forbidden from depending on '{dep.target_module}'."
                violations.append(
                    ModuleBoundaryViolation(
                        violation_id=f"MOD-VIOL-{uuid.uuid4().hex[:6].upper()}",
                        source_module=dep.source_module,
                        target_module=dep.target_module,
                        source_file=f"app/{dep.source_module}/",
                        line_number=1,
                        severity=BoundaryViolationSeverity.CRITICAL,
                        message=dep.violation_reason,
                        remediation=f"Decouple '{dep.source_module}' from '{dep.target_module}' using events or contracts in 'core'.",
                    )
                )

            # 2. Check if target is in allowed dependencies or is internal/core
            elif dep.target_module not in src_manifest.allowed_dependencies and dep.target_module != dep.source_module:
                if dep.target_module != "core":  # Core is generally available
                    dep.is_allowed = False
                    dep.severity = BoundaryViolationSeverity.HIGH
                    dep.violation_reason = f"Undeclared dependency: '{dep.source_module}' depends on '{dep.target_module}', which is not in its allowed list."
                    violations.append(
                        ModuleBoundaryViolation(
                            violation_id=f"MOD-VIOL-UNDEC-{uuid.uuid4().hex[:6].upper()}",
                            source_module=dep.source_module,
                            target_module=dep.target_module,
                            source_file=f"app/{dep.source_module}/",
                            line_number=1,
                            severity=BoundaryViolationSeverity.HIGH,
                            message=dep.violation_reason,
                            remediation=f"Declare '{dep.target_module}' in {dep.source_module}'s manifest or remove dependency.",
                        )
                    )

        return violations
