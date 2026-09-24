"""Indirect Prompt Injection Detection for Untrusted Third-Party Documents & RAG Contexts."""

import re
from typing import List, Tuple
from ..gateway.context import SourceTrustLevel, KnowledgeChunk
from ..gateway.decision import SafetyCategory, ViolationSeverity, SafetyViolation


class IndirectInjectionDetector:
    """Detects adversarial instructions embedded inside third-party documents, emails, PDFs, and web chunks."""

    INDIRECT_PATTERNS = [
        (r"(?i)\b(attention\s+(ai|assistant|model|agent)|note\s+to\s+(ai|agent|model)):", "Direct address to AI inside document", ViolationSeverity.HIGH),
        (r"(?i)\[\s*(hidden\s+instruction|system\s+override|ai\s+command):.*\]", "Bracketed hidden AI command in document", ViolationSeverity.CRITICAL),
        (r"(?i)\b(ignore\s+the\s+(document|text|content|invoice|table)\s+above|instead\s+output)\b", "Document parsing diversion command", ViolationSeverity.CRITICAL),
        (r"(?i)\b(send|post|transmit|exfiltrate)\s+(all|the|extracted|confidential)\s+(data|info|tokens|credentials)\s+to\s+https?://", "Data exfiltration command in document", ViolationSeverity.CRITICAL),
        (r"(?i)\b(do\s+not\s+extract\s+the\s+real\s+values|substitute\s+the\s+amount\s+with)\b", "Document extraction manipulation attempt", ViolationSeverity.HIGH),
    ]

    def scan_chunk(self, chunk: KnowledgeChunk) -> List[SafetyViolation]:
        violations: List[SafetyViolation] = []
        
        # High trust sources (SYSTEM, DEVELOPER) are not flagged for indirect injection
        if chunk.trust_level in [SourceTrustLevel.SYSTEM, SourceTrustLevel.DEVELOPER]:
            return violations

        for pattern, desc, severity in self.INDIRECT_PATTERNS:
            match = re.search(pattern, chunk.content)
            if match:
                violations.append(
                    SafetyViolation(
                        category=SafetyCategory.INDIRECT_INJECTION,
                        severity=severity,
                        message=f"{desc} in source '{chunk.source_name or chunk.source_type}' (Trust: {chunk.trust_level.value})",
                        location=f"chunk_{chunk.chunk_id}",
                        rule_id="INJ-IND-001",
                        evidence=match.group(0)[:120],
                        details={"trust_level": chunk.trust_level.value, "chunk_id": chunk.chunk_id}
                    )
                )
        return violations

    def scan_knowledge_chunks(self, chunks: List[KnowledgeChunk]) -> Tuple[bool, List[SafetyViolation]]:
        all_violations: List[SafetyViolation] = []
        for chunk in chunks:
            violations = self.scan_chunk(chunk)
            all_violations.extend(violations)
        return len(all_violations) > 0, all_violations
