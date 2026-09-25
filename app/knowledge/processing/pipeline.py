"""
Enterprise Knowledge Fabric, Memory Intelligence & Retrieval Platform (EKF-MIRP) - Document Intelligence Pipeline.
Orchestrates document validation, OCR normalization, layout structure analysis,
metadata enrichment, and entity extraction.
"""

from __future__ import annotations

import logging
import re
from typing import Any, Dict, List
from pydantic import BaseModel, Field

from app.knowledge.core.models import KnowledgeDocument

logger = logging.getLogger(__name__)


class DocumentSection(BaseModel):
    """Structural layout section within a parsed document."""
    heading: str = ""
    level: int = 1
    content: str
    section_type: str = "paragraph"  # heading, paragraph, table, list, code


class ProcessedDocument(BaseModel):
    """Enriched document representation after passing through the intelligence pipeline."""
    document_id: str
    title: str
    clean_text: str
    sections: List[DocumentSection] = Field(default_factory=list)
    entities: List[Dict[str, Any]] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    classification_tag: str = "GENERAL"


class DocumentIntelligencePipeline:
    """
    Multi-stage document processing engine preparing raw documents for intelligent chunking and indexing.
    """

    def process(self, document: KnowledgeDocument) -> ProcessedDocument:
        """
        Executes full document intelligence pipeline:
        Validation -> OCR Normalization -> Layout Parsing -> Metadata -> Entities -> Classification.
        """
        # 1. Validation & Normalization
        text = document.raw_content or document.normalized_text or ""
        clean_text = self._normalize_text(text)

        # 2. Layout Structure Analysis
        sections = self._parse_layout(clean_text)

        # 3. Entity Extraction
        entities = self._extract_entities(clean_text)

        # 4. Metadata Extraction
        words = clean_text.split()
        word_count = len(words)
        token_estimate = int(word_count * 1.3)

        metadata = {
            "file_type": document.file_type,
            "byte_size": document.byte_size or len(clean_text.encode("utf-8")),
            "word_count": word_count,
            "token_estimate": token_estimate,
            "section_count": len(sections),
            "entity_count": len(entities),
        }

        # 5. Classification
        classification = self._classify_document(clean_text, document.file_type)

        return ProcessedDocument(
            document_id=document.id,
            title=document.title,
            clean_text=clean_text,
            sections=sections,
            entities=entities,
            metadata=metadata,
            classification_tag=classification,
        )

    def _normalize_text(self, text: str) -> str:
        """Cleans and standardizes document text."""
        # Replace multiple spaces with single space, normalize newlines
        t = text.replace("\r\n", "\n").replace("\r", "\n")
        # Remove null bytes or non-printable ASCII
        t = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", t)
        return t.strip()

    def _parse_layout(self, text: str) -> List[DocumentSection]:
        """Heuristically segments text into structural headings and paragraphs."""
        lines = text.split("\n")
        sections: List[DocumentSection] = []
        current_heading = "Introduction"
        current_buffer: List[str] = []

        for line in lines:
            trimmed = line.strip()
            if not trimmed:
                continue

            # Heading detection: Markdown # or all caps short line
            if trimmed.startswith("#"):
                if current_buffer:
                    sections.append(DocumentSection(
                        heading=current_heading,
                        content="\n".join(current_buffer),
                        section_type="paragraph",
                    ))
                    current_buffer = []
                current_heading = trimmed.lstrip("#").strip()
            elif len(trimmed) < 60 and (trimmed.isupper() or trimmed.endswith(":")):
                if current_buffer:
                    sections.append(DocumentSection(
                        heading=current_heading,
                        content="\n".join(current_buffer),
                        section_type="paragraph",
                    ))
                    current_buffer = []
                current_heading = trimmed.rstrip(":")
            else:
                current_buffer.append(trimmed)

        if current_buffer:
            sections.append(DocumentSection(
                heading=current_heading,
                content="\n".join(current_buffer),
                section_type="paragraph",
            ))

        return sections if sections else [DocumentSection(heading="Body", content=text, section_type="paragraph")]

    def _extract_entities(self, text: str) -> List[Dict[str, Any]]:
        """Extracts common named entities (emails, dates, monetary amounts, URLs)."""
        entities: List[Dict[str, Any]] = []

        # Emails
        emails = re.findall(r"[\w\.-]+@[\w\.-]+\.\w+", text)
        for e in set(emails):
            entities.append({"type": "EMAIL", "value": e})

        # Monetary amounts ($100, $1,500.00, 50 USD, €200)
        money = re.findall(r"\$[\d,]+(?:\.\d{2})?|\b\d+(?:,\d{3})*(?:\.\d{2})?\s*(?:USD|EUR|GBP|INR)\b", text)
        for m in set(money):
            entities.append({"type": "MONEY", "value": m})

        # Dates (YYYY-MM-DD, MM/DD/YYYY)
        dates = re.findall(r"\b\d{4}-\d{2}-\d{2}\b|\b\d{1,2}/\d{1,2}/\d{2,4}\b", text)
        for d in set(dates):
            entities.append({"type": "DATE", "value": d})

        return entities

    def _classify_document(self, text: str, file_type: str) -> str:
        """Classifies document genre based on keyword signatures."""
        t = text.lower()
        if "agreement" in t or "contract" in t or "terms and conditions" in t or "master services" in t:
            return "CONTRACT"
        elif "invoice" in t or "bill to" in t or "total amount due" in t:
            return "INVOICE"
        elif "policy" in t or "compliance" in t or "security standard" in t:
            return "POLICY"
        elif file_type in ("py", "js", "ts", "java", "cpp", "go") or "def " in t or "class " in t:
            return "CODE"
        return "GENERAL"
