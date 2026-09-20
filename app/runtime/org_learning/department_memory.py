"""
AMAEOP Pillar 7 - Department Specialized Memory Engine
Maintains isolated and cross-shared memory domains per department (e.g. OCR contrast heuristics, Extraction prompt adapters).
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
import time
import uuid


@dataclass
class DepartmentKnowledgeItem:
    item_id: str
    department_id: str
    category: str  # HEURISTIC | PROMPT_TEMPLATE | SCHEMA_RULE | RECOVERY_STRATEGY
    title: str
    content: str
    accuracy_delta: float
    confidence: float
    created_at: float

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class DepartmentMemoryManager:
    """Stores and retrieves domain-specific procedural knowledge per department."""

    def __init__(self):
        self.knowledge_base: Dict[str, List[DepartmentKnowledgeItem]] = {}
        self._seed_memory()

    def _seed_memory(self):
        self.knowledge_base["dept_ocr"] = [
            DepartmentKnowledgeItem(
                item_id="kn_ocr_01",
                department_id="dept_ocr",
                category="HEURISTIC",
                title="Bilateral Filtering for Thermal Receipts",
                content="Apply bilateral filter with diameter 9 and sigmaColor 75 when document luminance variance is < 12.0.",
                accuracy_delta=0.038,
                confidence=0.96,
                created_at=time.time() - 86400.0,
            )
        ]
        self.knowledge_base["dept_extraction"] = [
            DepartmentKnowledgeItem(
                item_id="kn_ext_01",
                department_id="dept_extraction",
                category="PROMPT_TEMPLATE",
                title="European VAT Multi-Rate Extraction Anchor",
                content="Explicitly prompt Gemini 2.5 Flash with table line-item VAT rate mapping when vendor country is EU.",
                accuracy_delta=0.045,
                confidence=0.98,
                created_at=time.time() - 43200.0,
            )
        ]
        self.knowledge_base["dept_validation"] = [
            DepartmentKnowledgeItem(
                item_id="kn_val_01",
                department_id="dept_validation",
                category="SCHEMA_RULE",
                title="Dynamic Currency Symbol Normalization",
                content="Strip non-breaking currency whitespace characters prior to decimal invariant arithmetic evaluation.",
                accuracy_delta=0.012,
                confidence=0.99,
                created_at=time.time() - 21600.0,
            )
        ]

    def add_knowledge(
        self,
        department_id: str,
        category: str,
        title: str,
        content: str,
        accuracy_delta: float,
        confidence: float = 0.95,
    ) -> DepartmentKnowledgeItem:
        items = self.knowledge_base.setdefault(department_id, [])
        item_id = f"kn_{department_id}_{uuid.uuid4().hex[:4]}"
        item = DepartmentKnowledgeItem(
            item_id=item_id,
            department_id=department_id,
            category=category,
            title=title,
            content=content,
            accuracy_delta=accuracy_delta,
            confidence=confidence,
            created_at=time.time(),
        )
        items.insert(0, item)
        return item

    def get_department_knowledge(self, department_id: str) -> List[Dict[str, Any]]:
        return [k.to_dict() for k in self.knowledge_base.get(department_id, [])]

    def list_all_knowledge(self) -> Dict[str, List[Dict[str, Any]]]:
        return {k: [item.to_dict() for item in v] for k, v in self.knowledge_base.items()}


department_memory_manager = DepartmentMemoryManager()
