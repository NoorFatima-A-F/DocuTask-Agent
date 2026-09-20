"""Unified Injection Scanner combining Direct and Indirect Analyzers."""

from typing import List, Tuple, Optional
from pydantic import BaseModel, Field
from ..gateway.context import SafetyContext
from ..gateway.decision import SafetyViolation
from .prompt_injection import PromptInjectionDetector
from .indirect_injection import IndirectInjectionDetector


class InjectionScanResult(BaseModel):
    is_safe: bool
    confidence: float
    violations: List[SafetyViolation] = Field(default_factory=list)
    has_direct_injection: bool = False
    has_indirect_injection: bool = False


class InjectionScanner:
    """Master scanner coordinating direct prompt injection and indirect document injection checks."""

    def __init__(self):
        self.direct_detector = PromptInjectionDetector()
        self.indirect_detector = IndirectInjectionDetector()

    def scan_context(self, context: SafetyContext) -> InjectionScanResult:
        violations: List[SafetyViolation] = []
        has_direct = False
        has_indirect = False

        # 1. Scan direct user / raw input
        if context.raw_input:
            has_dir, dir_viols = self.direct_detector.detect(context.raw_input)
            if has_dir:
                has_direct = True
                violations.extend(dir_viols)

        # 2. Scan indirect knowledge chunks / document contents
        if context.knowledge_chunks:
            has_ind, ind_viols = self.indirect_detector.scan_knowledge_chunks(context.knowledge_chunks)
            if has_ind:
                has_indirect = True
                violations.extend(ind_viols)

        is_safe = len(violations) == 0
        confidence = 0.95 if not is_safe else 0.99

        return InjectionScanResult(
            is_safe=is_safe,
            confidence=confidence,
            violations=violations,
            has_direct_injection=has_direct,
            has_indirect_injection=has_indirect,
        )
