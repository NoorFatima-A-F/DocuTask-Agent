"""Intent Classifier for Enterprise Autonomous Agent OS.

Performs deterministic, rule-based, and semantic pattern matching to classify
user document objectives into operational intent categories with confidence scoring.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Pattern


class IntentType(str, Enum):
    DOCUMENT_EXTRACTION = "DOCUMENT_EXTRACTION"
    INVOICE_PROCESSING = "INVOICE_PROCESSING"
    RECEIPT_ANALYSIS = "RECEIPT_ANALYSIS"
    CONTRACT_REVIEW = "CONTRACT_REVIEW"
    COMPLIANCE_AUDIT = "COMPLIANCE_AUDIT"
    FRAUD_DETECTION = "FRAUD_DETECTION"
    BATCH_INGESTION = "BATCH_INGESTION"
    DATA_TRANSFORMATION = "DATA_TRANSFORMATION"
    RECONCILIATION = "RECONCILIATION"
    GENERIC_TASK = "GENERIC_TASK"


@dataclass
class IntentResult:
    """Result of intent classification with confidence and auxiliary tags."""

    primary_intent: IntentType
    confidence: float
    secondary_intents: List[IntentType] = field(default_factory=list)
    matched_keywords: List[str] = field(default_factory=list)
    domain: str = "DOCUMENT_PROCESSING"
    attributes: Dict[str, Any] = field(default_factory=dict)


class IntentClassifier:
    """Production-grade intent classification engine with pattern recognition and scoring."""

    def __init__(self) -> None:
        self._intent_patterns: Dict[IntentType, List[Pattern[str]]] = {
            IntentType.INVOICE_PROCESSING: [
                re.compile(r"\b(invoices?|bills?|billing|accounts payable|ap invoice|vendor invoice)\b", re.IGNORECASE),
                re.compile(r"\b(line items?|subtotals?|tax amount|taxes|due date|po number|arithmetic)\b", re.IGNORECASE),
            ],
            IntentType.RECEIPT_ANALYSIS: [
                re.compile(r"\b(receipt|expense|reimbursement|till slip|merchant receipt)\b", re.IGNORECASE),
            ],
            IntentType.CONTRACT_REVIEW: [
                re.compile(r"\b(contract|agreement|nda|terms and conditions|clause|indemnification)\b", re.IGNORECASE),
            ],
            IntentType.COMPLIANCE_AUDIT: [
                re.compile(r"\b(compliance|audit|regulatory|gdpr|hipaa|sox|sanctions|kyc)\b", re.IGNORECASE),
            ],
            IntentType.FRAUD_DETECTION: [
                re.compile(r"\b(fraud|anomaly|tamper|forgery|altered|suspicious|irregularity)\b", re.IGNORECASE),
            ],
            IntentType.BATCH_INGESTION: [
                re.compile(r"\b(batch|bulk|directory|dataset|ingest all|multi-document)\b", re.IGNORECASE),
            ],
            IntentType.RECONCILIATION: [
                re.compile(r"\b(reconcile|reconciliation|match to po|3-way match|discrepancy)\b", re.IGNORECASE),
            ],
            IntentType.DATA_TRANSFORMATION: [
                re.compile(r"\b(convert|transform|export|csv|json|xml|pipeline|format)\b", re.IGNORECASE),
            ],
            IntentType.DOCUMENT_EXTRACTION: [
                re.compile(r"\b(extract|ocr|parse|read|transcribe|table extraction|key-value)\b", re.IGNORECASE),
            ],
        }

    def classify(self, text: str, context: Optional[Dict[str, Any]] = None) -> IntentResult:
        """Classify given text into an intent with confidence scoring."""
        if not text or not text.strip():
            return IntentResult(
                primary_intent=IntentType.GENERIC_TASK,
                confidence=0.1,
                matched_keywords=[],
                domain="DOCUMENT_PROCESSING",
            )

        clean_text = text.strip()
        scores: Dict[IntentType, float] = {}
        matched_words: Dict[IntentType, List[str]] = {}

        for intent, patterns in self._intent_patterns.items():
            matches: List[str] = []
            for pat in patterns:
                found = pat.findall(clean_text)
                if found:
                    for f in found:
                        word = f if isinstance(f, str) else f[0]
                        matches.append(word.lower())
            if matches:
                # Primary match base score 0.70 + 0.15 per additional match, max 1.0
                score = min(1.0, 0.70 + (len(matches) - 1) * 0.15)
                # Specific document type intents take precedence over cross-cutting concern keywords
                if intent in (IntentType.INVOICE_PROCESSING, IntentType.RECEIPT_ANALYSIS, IntentType.CONTRACT_REVIEW):
                    score = min(1.0, score + 0.10)
                scores[intent] = score
                matched_words[intent] = list(set(matches))

        # Check context overrides or hints
        if context:
            hint = context.get("intent_hint")
            if hint:
                for it in IntentType:
                    if it.value.lower() == str(hint).lower():
                        scores[it] = max(scores.get(it, 0.0), 0.95)

        if not scores:
            return IntentResult(
                primary_intent=IntentType.GENERIC_TASK,
                confidence=0.5,
                matched_keywords=[],
                domain="DOCUMENT_PROCESSING",
            )

        sorted_intents = sorted(scores.items(), key=lambda kv: kv[1], reverse=True)
        primary, top_score = sorted_intents[0]
        secondaries = [k for k, s in sorted_intents[1:] if s >= 0.3]

        return IntentResult(
            primary_intent=primary,
            confidence=round(top_score, 2),
            secondary_intents=secondaries,
            matched_keywords=matched_words.get(primary, []),
            domain="FINANCIAL_DOCUMENTS" if primary in (IntentType.INVOICE_PROCESSING, IntentType.RECONCILIATION) else "DOCUMENT_PROCESSING",
            attributes={"score_breakdown": scores},
        )
