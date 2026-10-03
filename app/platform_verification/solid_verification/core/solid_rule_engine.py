"""
SOLID Principle Evaluation Engine.
"""
from __future__ import annotations
from typing import Dict, List
import uuid
from app.platform_verification.solid_verification.domain.interfaces import ISolidRuleEvaluator
from app.platform_verification.solid_verification.domain.models import (
    ClassDesignMetrics,
    InterfaceDesignMetrics,
    SolidPrinciple,
    SolidViolation,
    SolidViolationSeverity,
)


class EnterpriseSolidRuleEvaluator(ISolidRuleEvaluator):
    """Evaluates classes and interfaces against SRP, OCP, LSP, ISP, and DIP invariants."""

    def evaluate_srp(self, class_metrics: Dict[str, ClassDesignMetrics]) -> List[SolidViolation]:
        violations: List[SolidViolation] = []
        for key, cm in class_metrics.items():
            # 1. Responsibility Concentration (God Class)
            if len(cm.detected_responsibilities) >= 4:
                violations.append(
                    SolidViolation(
                        violation_id=f"VIOL-SRP-{uuid.uuid4().hex[:6].upper()}",
                        principle=SolidPrinciple.SRP,
                        class_name=cm.class_name,
                        file_path=cm.file_path,
                        line_number=1,
                        severity=SolidViolationSeverity.CRITICAL,
                        message=f"God Class violation: '{cm.class_name}' handles {len(cm.detected_responsibilities)} distinct responsibilities ({', '.join(cm.detected_responsibilities)}).",
                        suggested_refactoring="Decompose into cohesive single-purpose domain services.",
                    )
                )

            # 2. Excessive constructor dependencies
            if cm.constructor_param_count >= 8:
                violations.append(
                    SolidViolation(
                        violation_id=f"VIOL-SRP-DEP-{uuid.uuid4().hex[:6].upper()}",
                        principle=SolidPrinciple.SRP,
                        class_name=cm.class_name,
                        file_path=cm.file_path,
                        line_number=1,
                        severity=SolidViolationSeverity.HIGH,
                        message=f"Excessive dependencies in '{cm.class_name}': constructor receives {cm.constructor_param_count} parameters.",
                        suggested_refactoring="Introduce parameter object or decompose class responsibilities.",
                    )
                )

            # 3. Massive class size
            if cm.line_count > 600 or cm.method_count > 25:
                violations.append(
                    SolidViolation(
                        violation_id=f"VIOL-SRP-SIZE-{uuid.uuid4().hex[:6].upper()}",
                        principle=SolidPrinciple.SRP,
                        class_name=cm.class_name,
                        file_path=cm.file_path,
                        line_number=1,
                        severity=SolidViolationSeverity.MEDIUM,
                        message=f"Class size limit exceeded in '{cm.class_name}' ({cm.line_count} lines, {cm.method_count} methods).",
                        suggested_refactoring="Extract helper classes and delegate non-core behaviors.",
                    )
                )

        return violations

    def evaluate_ocp(self, class_metrics: Dict[str, ClassDesignMetrics]) -> List[SolidViolation]:
        violations: List[SolidViolation] = []
        for key, cm in class_metrics.items():
            if cm.has_type_switch_violation:
                violations.append(
                    SolidViolation(
                        violation_id=f"VIOL-OCP-{uuid.uuid4().hex[:6].upper()}",
                        principle=SolidPrinciple.OCP,
                        class_name=cm.class_name,
                        file_path=cm.file_path,
                        line_number=1,
                        severity=SolidViolationSeverity.HIGH,
                        message=f"Open/Closed violation in '{cm.class_name}': conditional type switching on providers/types detected.",
                        suggested_refactoring="Replace conditional branching with Strategy or Factory polymorphism.",
                    )
                )
        return violations

    def evaluate_lsp(self, class_metrics: Dict[str, ClassDesignMetrics]) -> List[SolidViolation]:
        violations: List[SolidViolation] = []
        for key, cm in class_metrics.items():
            if cm.has_unsupported_operation_override:
                violations.append(
                    SolidViolation(
                        violation_id=f"VIOL-LSP-{uuid.uuid4().hex[:6].upper()}",
                        principle=SolidPrinciple.LSP,
                        class_name=cm.class_name,
                        file_path=cm.file_path,
                        line_number=1,
                        severity=SolidViolationSeverity.CRITICAL,
                        message=f"Liskov Substitution violation in '{cm.class_name}': overrides base contract by raising UnsupportedOperation.",
                        suggested_refactoring="Segregate interface to prevent implementing unsupportable operations.",
                    )
                )
        return violations

    def evaluate_isp(self, interface_metrics: Dict[str, InterfaceDesignMetrics]) -> List[SolidViolation]:
        violations: List[SolidViolation] = []
        for key, im in interface_metrics.items():
            if im.is_oversized or im.total_methods >= 12:
                violations.append(
                    SolidViolation(
                        violation_id=f"VIOL-ISP-{uuid.uuid4().hex[:6].upper()}",
                        principle=SolidPrinciple.ISP,
                        class_name=im.interface_name,
                        file_path=im.file_path,
                        line_number=1,
                        severity=SolidViolationSeverity.HIGH,
                        message=f"Interface Segregation violation in '{im.interface_name}': oversized interface with {im.total_methods} methods (Usage ratio: {im.avg_usage_ratio:.0%}).",
                        suggested_refactoring="Split fat interface into focused role-specific interfaces.",
                    )
                )
        return violations

    def evaluate_dip(self, class_metrics: Dict[str, ClassDesignMetrics]) -> List[SolidViolation]:
        violations: List[SolidViolation] = []
        for key, cm in class_metrics.items():
            if cm.has_direct_instantiation_violation:
                violations.append(
                    SolidViolation(
                        violation_id=f"VIOL-DIP-{uuid.uuid4().hex[:6].upper()}",
                        principle=SolidPrinciple.DIP,
                        class_name=cm.class_name,
                        file_path=cm.file_path,
                        line_number=1,
                        severity=SolidViolationSeverity.CRITICAL,
                        message=f"Dependency Inversion violation in '{cm.class_name}': directly instantiates concrete client/infrastructure within high-level module.",
                        suggested_refactoring="Inject abstract provider interface via constructor injection.",
                    )
                )
        return violations
