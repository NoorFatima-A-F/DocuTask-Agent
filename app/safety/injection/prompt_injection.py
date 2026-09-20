"""Direct Prompt Injection Detection Engine."""

import re
from typing import List, Tuple
from ..gateway.decision import SafetyCategory, ViolationSeverity, SafetyViolation


class PromptInjectionDetector:
    """Detects direct prompt injection, delimiter tampering, and instruction hijacking."""

    INJECTION_PATTERNS = [
        # Instruction Overrides
        (r"(?i)\b(ignore|disregard|forget|bypass|override)\s+(all\s+)?(previous|prior|above|former)\s+(instructions|directives|prompts|rules|commands|constraints)", "Instruction override directive", ViolationSeverity.CRITICAL),
        (r"(?i)\b(you\s+must\s+now|from\s+now\s+on\s+you\s+are)\s+(unrestricted|in\s+developer\s+mode|freed|jailbroken)", "Developer/unrestricted mode switch attempt", ViolationSeverity.CRITICAL),
        (r"(?i)\b(new\s+operating\s+instructions?|system\s+update:)\s*[\r\n]", "Fake system directive header", ViolationSeverity.HIGH),
        (r"(?i)\bdo\s+not\s+follow\s+(any\s+)?(safety|system|original)\s+(guidelines|filters|protocols)", "Safety guideline bypass instruction", ViolationSeverity.CRITICAL),
        
        # Delimiter & Special Token Tampering
        (r"(<\|im_start\|>|<\|im_end\|>|<\|system\|>|<\|user\|>|<\|assistant\|>)", "ChatML delimiter injection", ViolationSeverity.CRITICAL),
        (r"(\[INST\]|\[/INST\]|<<SYS>>|<</SYS>>)", "Llama instruction tag injection", ViolationSeverity.CRITICAL),
        (r"(###\s*System:?|###\s*Human:?|###\s*Assistant:?)", "Markdown role delimiter injection", ViolationSeverity.HIGH),
        (r"(<\s*system_instructions\s*>|<\s*/\s*system_instructions\s*>)", "XML system block injection", ViolationSeverity.CRITICAL),
        
        # System Prompt Extraction
        (r"(?i)\b(print|reveal|repeat|output|show|echo|leak|dump)\s+(your\s+)?(initial|original|system|hidden|confidential)\s+(prompt|instructions|rules|preamble)", "System prompt extraction attempt", ViolationSeverity.HIGH),
        (r"(?i)\bwhat\s+(is|are)\s+the\s+exact\s+(text|words|instructions)\s+above", "Preamble extraction probe", ViolationSeverity.MEDIUM),
    ]

    def detect(self, text: str) -> Tuple[bool, List[SafetyViolation]]:
        violations: List[SafetyViolation] = []
        if not text:
            return False, violations

        for pattern, desc, severity in self.INJECTION_PATTERNS:
            match = re.search(pattern, text)
            if match:
                violations.append(
                    SafetyViolation(
                        category=SafetyCategory.PROMPT_INJECTION,
                        severity=severity,
                        message=desc,
                        location="input",
                        rule_id="INJ-DIR-001",
                        evidence=match.group(0)[:120],
                    )
                )

        return len(violations) > 0, violations
