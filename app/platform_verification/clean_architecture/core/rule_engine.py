"""
Clean Architecture Inward Dependency & Forbidden Imports Rule Engine.
"""
from __future__ import annotations
from typing import Dict, List, Optional
import uuid
from app.platform_verification.clean_architecture.domain.interfaces import IDependencyRuleEngine
from app.platform_verification.clean_architecture.domain.models import (
    ArchitectureExceptionWaiver,
    ArchitectureLayer,
    CleanArchAction,
    CleanArchDependencyEdge,
    CleanArchSeverity,
    CleanArchViolation,
    LayerDependencyRule,
)


class EnterpriseDependencyRuleEngine(IDependencyRuleEngine):
    """Enforces inward dependency rules (Outer -> Inner allowed, Inner -> Outer forbidden)."""

    def __init__(self):
        self._rules: Dict[ArchitectureLayer, LayerDependencyRule] = {}
        self._initialize_clean_architecture_rules()

    def register_layer_rule(self, rule: LayerDependencyRule) -> None:
        self._rules[rule.source_layer] = rule

    def evaluate_dependencies(
        self,
        edges: List[CleanArchDependencyEdge],
        waivers: Optional[List[ArchitectureExceptionWaiver]] = None,
    ) -> List[CleanArchViolation]:
        active_waivers = [w for w in (waivers or []) if w.is_active()]
        violations: List[CleanArchViolation] = []

        for edge in edges:
            # Check if waived
            is_waived = any(
                w.source_file in edge.source_module and (w.target_module in edge.target_module or w.target_module == "*")
                for w in active_waivers
            )
            if is_waived:
                edge.is_waived = True
                continue

            rule = self._rules.get(edge.source_layer)
            if not rule:
                continue

            # 1. Check forbidden layer target
            if edge.target_layer in rule.forbidden_target_layers and edge.target_layer != ArchitectureLayer.UNKNOWN:
                edge.is_allowed = False
                edge.violation_reason = f"Layer '{edge.source_layer.value}' is forbidden from depending on outer layer '{edge.target_layer.value}'."
                violations.append(
                    CleanArchViolation(
                        violation_id=f"VIOL-CA-{uuid.uuid4().hex[:6].upper()}",
                        rule_id=f"RULE_{edge.source_layer.value}_ISOLATION",
                        source_file=edge.source_module,
                        source_layer=edge.source_layer,
                        target_module=edge.target_module,
                        target_layer=edge.target_layer,
                        line_number=edge.line_number,
                        severity=CleanArchSeverity.CRITICAL,
                        message=edge.violation_reason,
                        suggested_fix=f"Invert dependency: extract interface/port in '{edge.source_layer.value}' and implement in '{edge.target_layer.value}'.",
                        action=CleanArchAction.BLOCK_BUILD,
                    )
                )

            # 2. Check forbidden external vendor packages
            for forbidden_pkg in rule.forbidden_external_packages:
                if forbidden_pkg.lower() in edge.target_module.lower():
                    edge.is_allowed = False
                    edge.violation_reason = f"Layer '{edge.source_layer.value}' is forbidden from importing external library '{forbidden_pkg}'."
                    violations.append(
                        CleanArchViolation(
                            violation_id=f"VIOL-EXT-{uuid.uuid4().hex[:6].upper()}",
                            rule_id=f"RULE_{edge.source_layer.value}_NO_{forbidden_pkg.upper()}",
                            source_file=edge.source_module,
                            source_layer=edge.source_layer,
                            target_module=edge.target_module,
                            target_layer=edge.target_layer,
                            line_number=edge.line_number,
                            severity=CleanArchSeverity.CRITICAL,
                            message=edge.violation_reason,
                            suggested_fix=f"Decouple '{forbidden_pkg}' via abstract adapter interface.",
                            action=CleanArchAction.BLOCK_BUILD,
                        )
                    )

        return violations

    def _initialize_clean_architecture_rules(self) -> None:
        # 1. DOMAIN LAYER: Completely Pure. Cannot depend on outer layers or external frameworks.
        self.register_layer_rule(
            LayerDependencyRule(
                source_layer=ArchitectureLayer.DOMAIN,
                allowed_target_layers=[ArchitectureLayer.DOMAIN],
                forbidden_target_layers=[
                    ArchitectureLayer.APPLICATION,
                    ArchitectureLayer.INTERFACES,
                    ArchitectureLayer.INFRASTRUCTURE,
                    ArchitectureLayer.API,
                    ArchitectureLayer.AGENTS,
                    ArchitectureLayer.RUNTIME,
                    ArchitectureLayer.WORKERS,
                ],
                forbidden_external_packages=[
                    "fastapi",
                    "sqlalchemy",
                    "redis",
                    "celery",
                    "google.generativeai",
                    "openai",
                    "requests",
                    "httpx",
                ],
                description="Domain Layer contains Enterprise Business Rules and must remain completely decoupled.",
            )
        )

        # 2. APPLICATION LAYER: Can depend on Domain and Interfaces. Cannot depend on Infrastructure or API.
        self.register_layer_rule(
            LayerDependencyRule(
                source_layer=ArchitectureLayer.APPLICATION,
                allowed_target_layers=[ArchitectureLayer.DOMAIN, ArchitectureLayer.INTERFACES],
                forbidden_target_layers=[
                    ArchitectureLayer.INFRASTRUCTURE,
                    ArchitectureLayer.API,
                    ArchitectureLayer.RUNTIME,
                ],
                forbidden_external_packages=["fastapi", "sqlalchemy", "redis"],
                description="Application Layer contains Use Cases and depends only on Domain and Interface ports.",
            )
        )

        # 3. INTERFACES LAYER: Can depend on Domain and Application.
        self.register_layer_rule(
            LayerDependencyRule(
                source_layer=ArchitectureLayer.INTERFACES,
                allowed_target_layers=[ArchitectureLayer.DOMAIN, ArchitectureLayer.APPLICATION],
                forbidden_target_layers=[ArchitectureLayer.API],
                forbidden_external_packages=[],
                description="Interface adapters bridge domain models to external ports.",
            )
        )
