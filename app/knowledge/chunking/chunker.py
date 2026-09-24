"""
Enterprise Knowledge Fabric, Memory Intelligence & Retrieval Platform (EKF-MIRP) - Intelligent Chunking Engine.
Provides pluggable, structure-aware chunking strategies: Fixed, Semantic, Heading, Table, Code, Conversation,
and Hierarchical Parent-Child chunk graphs.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
import logging
import re
from typing import Dict, List, Optional
import uuid

from app.knowledge.core.models import KnowledgeChunk, KnowledgeDocument

logger = logging.getLogger(__name__)


class BaseChunker(ABC):
    """Abstract base class for document chunking algorithms."""

    @abstractmethod
    def chunk(self, document: KnowledgeDocument) -> List[KnowledgeChunk]:
        pass


class FixedChunker(BaseChunker):
    """Chunks text by fixed character or token count with sliding window overlap."""

    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk(self, document: KnowledgeDocument) -> List[KnowledgeChunk]:
        text = document.normalized_text or document.raw_content or ""
        if not text:
            return []

        chunks: List[KnowledgeChunk] = []
        pos = 0
        start = 0

        while start < len(text):
            end = min(start + self.chunk_size, len(text))
            chunk_text = text[start:end].strip()

            if chunk_text:
                chk = KnowledgeChunk(
                    chunk_id=f"kchk-{uuid.uuid4().hex[:10]}",
                    document_id=document.id,
                    knowledge_id=document.knowledge_id,
                    position=pos,
                    content=chunk_text,
                    token_count=int(len(chunk_text.split()) * 1.3),
                    page_number=1,
                    metadata={"strategy": "FIXED", "start_char": start, "end_char": end},
                )
                chunks.append(chk)
                pos += 1

            if end >= len(text):
                break
            start += max(1, self.chunk_size - self.chunk_overlap)

        return chunks


class SemanticChunker(BaseChunker):
    """Segments text on sentence and natural paragraph boundaries."""

    def __init__(self, max_tokens_per_chunk: int = 250):
        self.max_tokens = max_tokens_per_chunk

    def chunk(self, document: KnowledgeDocument) -> List[KnowledgeChunk]:
        text = document.normalized_text or document.raw_content or ""
        if not text:
            return []

        paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
        chunks: List[KnowledgeChunk] = []
        pos = 0
        current_chunk_sentences: List[str] = []
        current_tokens = 0

        for para in paragraphs:
            sentences = re.split(r"(?<=[.!?])\s+", para)
            for s in sentences:
                s_tokens = int(len(s.split()) * 1.3)
                if current_tokens + s_tokens > self.max_tokens and current_chunk_sentences:
                    chunk_content = " ".join(current_chunk_sentences)
                    chk = KnowledgeChunk(
                        chunk_id=f"kchk-{uuid.uuid4().hex[:10]}",
                        document_id=document.id,
                        knowledge_id=document.knowledge_id,
                        position=pos,
                        content=chunk_content,
                        token_count=current_tokens,
                        metadata={"strategy": "SEMANTIC"},
                    )
                    chunks.append(chk)
                    pos += 1
                    current_chunk_sentences = []
                    current_tokens = 0

                current_chunk_sentences.append(s)
                current_tokens += s_tokens

        if current_chunk_sentences:
            chunk_content = " ".join(current_chunk_sentences)
            chk = KnowledgeChunk(
                chunk_id=f"kchk-{uuid.uuid4().hex[:10]}",
                document_id=document.id,
                knowledge_id=document.knowledge_id,
                position=pos,
                content=chunk_content,
                token_count=current_tokens,
                metadata={"strategy": "SEMANTIC"},
            )
            chunks.append(chk)

        return chunks


class HeadingChunker(BaseChunker):
    """Segments document along structural header hierarchy (Markdown # / section titles)."""

    def chunk(self, document: KnowledgeDocument) -> List[KnowledgeChunk]:
        text = document.normalized_text or document.raw_content or ""
        lines = text.split("\n")
        chunks: List[KnowledgeChunk] = []
        pos = 0
        current_heading = "Overview"
        current_lines: List[str] = []

        for line in lines:
            trimmed = line.strip()
            if trimmed.startswith("#"):
                if current_lines:
                    chunk_content = "\n".join(current_lines).strip()
                    if chunk_content:
                        chunks.append(KnowledgeChunk(
                            chunk_id=f"kchk-{uuid.uuid4().hex[:10]}",
                            document_id=document.id,
                            knowledge_id=document.knowledge_id,
                            position=pos,
                            content=chunk_content,
                            token_count=int(len(chunk_content.split()) * 1.3),
                            heading_hierarchy=[current_heading],
                            metadata={"strategy": "HEADING", "heading": current_heading},
                        ))
                        pos += 1
                    current_lines = []
                current_heading = trimmed.lstrip("#").strip()
            else:
                current_lines.append(line)

        if current_lines:
            chunk_content = "\n".join(current_lines).strip()
            if chunk_content:
                chunks.append(KnowledgeChunk(
                    chunk_id=f"kchk-{uuid.uuid4().hex[:10]}",
                    document_id=document.id,
                    knowledge_id=document.knowledge_id,
                    position=pos,
                    content=chunk_content,
                    token_count=int(len(chunk_content.split()) * 1.3),
                    heading_hierarchy=[current_heading],
                    metadata={"strategy": "HEADING", "heading": current_heading},
                ))

        return chunks if chunks else FixedChunker().chunk(document)


class TableChunker(BaseChunker):
    """Preserves tabular rows and column schemas without breaking cells."""

    def chunk(self, document: KnowledgeDocument) -> List[KnowledgeChunk]:
        # Emits table as discrete contextual chunk
        text = document.normalized_text or document.raw_content or ""
        return [
            KnowledgeChunk(
                chunk_id=f"kchk-{uuid.uuid4().hex[:10]}",
                document_id=document.id,
                knowledge_id=document.knowledge_id,
                position=0,
                content=text,
                token_count=int(len(text.split()) * 1.3),
                metadata={"strategy": "TABLE"},
            )
        ]


class CodeChunker(BaseChunker):
    """Splits source code along class, function, or block boundaries."""

    def chunk(self, document: KnowledgeDocument) -> List[KnowledgeChunk]:
        text = document.normalized_text or document.raw_content or ""
        lines = text.split("\n")
        chunks: List[KnowledgeChunk] = []
        pos = 0
        current_block: List[str] = []

        for line in lines:
            if line.startswith("def ") or line.startswith("class ") or line.startswith("function "):
                if current_block:
                    code_content = "\n".join(current_block).strip()
                    if code_content:
                        chunks.append(KnowledgeChunk(
                            chunk_id=f"kchk-{uuid.uuid4().hex[:10]}",
                            document_id=document.id,
                            knowledge_id=document.knowledge_id,
                            position=pos,
                            content=code_content,
                            token_count=int(len(code_content.split()) * 1.3),
                            metadata={"strategy": "CODE"},
                        ))
                        pos += 1
                    current_block = []
            current_block.append(line)

        if current_block:
            code_content = "\n".join(current_block).strip()
            if code_content:
                chunks.append(KnowledgeChunk(
                    chunk_id=f"kchk-{uuid.uuid4().hex[:10]}",
                    document_id=document.id,
                    knowledge_id=document.knowledge_id,
                    position=pos,
                    content=code_content,
                    token_count=int(len(code_content.split()) * 1.3),
                    metadata={"strategy": "CODE"},
                ))

        return chunks if chunks else FixedChunker().chunk(document)


class ConversationChunker(BaseChunker):
    """Splits dialogue transcripts and chat logs by speaker turn."""

    def chunk(self, document: KnowledgeDocument) -> List[KnowledgeChunk]:
        text = document.normalized_text or document.raw_content or ""
        lines = text.split("\n")
        chunks: List[KnowledgeChunk] = []
        pos = 0

        for line in lines:
            trimmed = line.strip()
            if trimmed:
                chunks.append(KnowledgeChunk(
                    chunk_id=f"kchk-{uuid.uuid4().hex[:10]}",
                    document_id=document.id,
                    knowledge_id=document.knowledge_id,
                    position=pos,
                    content=trimmed,
                    token_count=int(len(trimmed.split()) * 1.3),
                    metadata={"strategy": "CONVERSATION"},
                ))
                pos += 1

        return chunks if chunks else FixedChunker().chunk(document)


class HierarchicalChunker(BaseChunker):
    """
    Creates a multi-level chunk hierarchy:
    Parent chunk (Section) -> Child chunks (Paragraphs)
    """

    def __init__(self, parent_size: int = 1000, child_size: int = 250):
        self.parent_size = parent_size
        self.child_size = child_size

    def chunk(self, document: KnowledgeDocument) -> List[KnowledgeChunk]:
        parent_chunker = FixedChunker(chunk_size=self.parent_size, chunk_overlap=100)
        parents = parent_chunker.chunk(document)

        all_chunks: List[KnowledgeChunk] = []
        for p in parents:
            p.metadata["hierarchy_level"] = "PARENT"
            all_chunks.append(p)

            # Sub-chunk parent content into children
            child_doc = KnowledgeDocument(
                id=f"{document.id}-sub",
                knowledge_id=document.knowledge_id,
                title=f"{document.title} Child",
                normalized_text=p.content,
            )
            child_chunker = FixedChunker(chunk_size=self.child_size, chunk_overlap=30)
            children = child_chunker.chunk(child_doc)

            for c in children:
                c.parent_chunk_id = p.chunk_id
                c.metadata["hierarchy_level"] = "CHILD"
                p.child_chunk_ids.append(c.chunk_id)
                all_chunks.append(c)

        return all_chunks


class ChunkingEngine:
    """
    Orchestrates strategy selection based on document metadata or file type.
    """

    def __init__(self):
        self._strategies: Dict[str, BaseChunker] = {
            "fixed": FixedChunker(),
            "semantic": SemanticChunker(),
            "heading": HeadingChunker(),
            "table": TableChunker(),
            "code": CodeChunker(),
            "conversation": ConversationChunker(),
            "hierarchical": HierarchicalChunker(),
        }

    def register_strategy(self, name: str, chunker: BaseChunker) -> None:
        """Registers a custom chunking strategy."""
        self._strategies[name.lower()] = chunker

    def chunk_document(
        self,
        document: KnowledgeDocument,
        strategy: Optional[str] = None,
    ) -> List[KnowledgeChunk]:
        """
        Chunks a document using the specified strategy or autodetects by document file type.
        """
        strat_name = (strategy or self._auto_detect_strategy(document)).lower()
        chunker = self._strategies.get(strat_name, self._strategies["semantic"])
        chunks = chunker.chunk(document)
        logger.info(f"Chunked document '{document.id}' into {len(chunks)} chunks using strategy '{strat_name}'")
        return chunks

    def _auto_detect_strategy(self, document: KnowledgeDocument) -> str:
        ft = document.file_type.lower()
        if ft in ("py", "js", "ts", "java", "cpp", "go", "sql"):
            return "code"
        elif ft in ("csv", "xlsx"):
            return "table"
        elif ft in ("md", "markdown"):
            return "heading"
        return "semantic"
