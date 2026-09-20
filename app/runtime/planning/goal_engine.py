"""Goal Understanding Engine for DocuTask Autonomous Planning Platform.

Parses unstructured mission intents, natural language requests, and structured payloads into a
deterministic, validated GoalGraph consisting of semantic objectives, deliverables, and completion criteria.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class ObjectiveType(str, Enum):
    EXTRACTION = "EXTRACTION"
    VALIDATION = "VALIDATION"
    TRANSFORMATION = "TRANSFORMATION"
    CLASSIFICATION = "CLASSIFICATION"
    RECONCILIATION = "RECONCILIATION"
    AUDIT = "AUDIT"
    COMPLIANCE_CHECK = "COMPLIANCE_CHECK"
    CUSTOM = "CUSTOM"


class PriorityLevel(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class CompletionCriteria(BaseModel):
    """Specific measurable criterion for goal completion."""
    criterion_id: str = Field(default_factory=lambda: f"crit_{uuid.uuid4().hex[:8]}")
    metric_name: str
    target_value: float
    comparator: str = Field(default=">=", description="'>=', '<=', '==', '>', '<'")
    tolerance: float = 0.0
    is_hard_gate: bool = True
    description: str = ""

    def evaluate(self, actual_value: float) -> bool:
        if self.comparator == ">=":
            return actual_value >= (self.target_value - self.tolerance)
        elif self.comparator == "<=":
            return actual_value <= (self.target_value + self.tolerance)
        elif self.comparator == "==":
            return abs(actual_value - self.target_value) <= self.tolerance
        elif self.comparator == ">":
            return actual_value > self.target_value
        elif self.comparator == "<":
            return actual_value < self.target_value
        return False


class Deliverable(BaseModel):
    """Concrete deliverable produced by the goal hierarchy."""
    deliverable_id: str = Field(default_factory=lambda: f"deliv_{uuid.uuid4().hex[:8]}")
    name: str
    mime_type: str = "application/json"
    schema_definition: Optional[Dict[str, Any]] = None
    required_fields: List[str] = Field(default_factory=list)
    storage_path: Optional[str] = None
    status: str = "PENDING"


class SemanticObjective(BaseModel):
    """Atomic semantic objective node within the GoalGraph."""
    objective_id: str = Field(default_factory=lambda: f"obj_{uuid.uuid4().hex[:8]}")
    parent_id: Optional[str] = None
    name: str
    description: str
    objective_type: ObjectiveType
    priority: PriorityLevel = PriorityLevel.HIGH
    deliverables: List[Deliverable] = Field(default_factory=list)
    completion_criteria: List[CompletionCriteria] = Field(default_factory=list)
    required_capabilities: List[str] = Field(default_factory=list)
    estimated_complexity: float = Field(default=1.0, ge=0.1, le=10.0)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class GoalGraph(BaseModel):
    """Deterministic, DAG-structured Goal Representation."""
    graph_id: str = Field(default_factory=lambda: f"goal_graph_{uuid.uuid4().hex[:10]}")
    mission_id: str
    root_intent: str
    objectives: Dict[str, SemanticObjective] = Field(default_factory=dict)
    root_objective_ids: List[str] = Field(default_factory=list)
    dependencies: Dict[str, List[str]] = Field(default_factory=dict, description="objective_id -> list of prerequisite objective_ids")
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    version: str = "1.0.0"

    def add_objective(self, objective: SemanticObjective, prerequisite_ids: Optional[List[str]] = None) -> None:
        self.objectives[objective.objective_id] = objective
        if not objective.parent_id and objective.objective_id not in self.root_objective_ids:
            self.root_objective_ids.append(objective.objective_id)
        if prerequisite_ids:
            self.dependencies[objective.objective_id] = prerequisite_ids
        elif objective.objective_id not in self.dependencies:
            self.dependencies[objective.objective_id] = []

    def get_topological_order(self) -> List[str]:
        """Returns topological ordering of objective IDs."""
        in_degree: Dict[str, int] = {k: 0 for k in self.objectives}
        adj: Dict[str, List[str]] = {k: [] for k in self.objectives}

        for obj_id, prereqs in self.dependencies.items():
            for p in prereqs:
                if p in adj:
                    adj[p].append(obj_id)
                    in_degree[obj_id] = in_degree.get(obj_id, 0) + 1

        queue = [k for k, deg in in_degree.items() if deg == 0]
        order: List[str] = []

        while queue:
            curr = queue.pop(0)
            order.append(curr)
            for neighbor in adj.get(curr, []):
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        if len(order) != len(self.objectives):
            # Fallback to key order if cycle exists
            return list(self.objectives.keys())
        return order


class GoalUnderstandingEngine:
    """Parses natural language requests and structured intents into a structured GoalGraph."""

    def __init__(self) -> None:
        self._keyword_type_map = {
            "extract": ObjectiveType.EXTRACTION,
            "ocr": ObjectiveType.EXTRACTION,
            "validate": ObjectiveType.VALIDATION,
            "verify": ObjectiveType.VALIDATION,
            "transform": ObjectiveType.TRANSFORMATION,
            "convert": ObjectiveType.TRANSFORMATION,
            "classify": ObjectiveType.CLASSIFICATION,
            "reconcile": ObjectiveType.RECONCILIATION,
            "audit": ObjectiveType.AUDIT,
            "compliance": ObjectiveType.COMPLIANCE_CHECK,
        }

    def parse_intent(
        self,
        mission_id: str,
        raw_intent: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> GoalGraph:
        """Deterministically decomposes raw intent into a hierarchical GoalGraph."""
        context = context or {}
        goal_graph = GoalGraph(mission_id=mission_id, root_intent=raw_intent)
        lower_intent = raw_intent.lower()

        # Step 1: Root Objective
        root_obj = SemanticObjective(
            name="Primary Mission Goal",
            description=raw_intent,
            objective_type=self._classify_intent(lower_intent),
            priority=PriorityLevel.CRITICAL,
            completion_criteria=[
                CompletionCriteria(
                    metric_name="overall_confidence",
                    target_value=0.90,
                    comparator=">=",
                    description="Overall mission confidence threshold",
                ),
                CompletionCriteria(
                    metric_name="schema_compliance",
                    target_value=1.0,
                    comparator="==",
                    description="100% schema compliance for extracted deliverables",
                ),
            ],
            estimated_complexity=2.0,
        )
        goal_graph.add_objective(root_obj)

        # Step 2: Extract structured sub-objectives based on semantic patterns
        sub_objectives: List[SemanticObjective] = []

        # Document Ingestion & Optical Recognition
        ingest_obj = SemanticObjective(
            parent_id=root_obj.objective_id,
            name="Document Ingestion & Multi-modal Preprocessing",
            description="Ingest document, preprocess image/PDF layers, deskew and detect layout regions",
            objective_type=ObjectiveType.EXTRACTION,
            priority=PriorityLevel.HIGH,
            required_capabilities=["ocr_engine", "vision_processor", "layout_analyzer"],
            completion_criteria=[
                CompletionCriteria(metric_name="ocr_char_confidence", target_value=0.85, comparator=">=")
            ],
            estimated_complexity=1.2,
        )
        sub_objectives.append(ingest_obj)

        # Entity Extraction & Schema Alignment
        extract_obj = SemanticObjective(
            parent_id=root_obj.objective_id,
            name="Semantic Entity & Field Extraction",
            description="Extract structured key-value entities, tables, and line items with provenance coordinates",
            objective_type=ObjectiveType.EXTRACTION,
            priority=PriorityLevel.HIGH,
            required_capabilities=["llm_extractor", "regex_extractor", "table_parser"],
            deliverables=[
                Deliverable(
                    name="extracted_document_entities.json",
                    mime_type="application/json",
                    required_fields=["document_type", "entities", "line_items", "metadata"],
                )
            ],
            completion_criteria=[
                CompletionCriteria(metric_name="field_recall", target_value=0.92, comparator=">=")
            ],
            estimated_complexity=1.8,
        )
        sub_objectives.append(extract_obj)

        # Validation & Cross-Check Verification
        val_obj = SemanticObjective(
            parent_id=root_obj.objective_id,
            name="Deterministic Rule & Cross-Field Validation",
            description="Apply math cross-checks, tax calculations, date validity, and cross-reference lookups",
            objective_type=ObjectiveType.VALIDATION,
            priority=PriorityLevel.CRITICAL,
            required_capabilities=["rule_engine", "cross_validator", "math_verifier"],
            completion_criteria=[
                CompletionCriteria(metric_name="validation_pass_rate", target_value=1.0, comparator="==")
            ],
            estimated_complexity=1.0,
        )
        sub_objectives.append(val_obj)

        # Enterprise Memory Indexing & Reflection
        memory_obj = SemanticObjective(
            parent_id=root_obj.objective_id,
            name="Episodic Memory Indexing & Self-Reflection",
            description="Index mission execution trace and learned patterns into organizational memory",
            objective_type=ObjectiveType.AUDIT,
            priority=PriorityLevel.MEDIUM,
            required_capabilities=["memory_indexer", "reflection_engine"],
            completion_criteria=[
                CompletionCriteria(metric_name="memory_indexed", target_value=1.0, comparator="==")
            ],
            estimated_complexity=0.8,
        )
        sub_objectives.append(memory_obj)

        # Wire dependencies: Ingest -> Extract -> Validate -> Memory
        goal_graph.add_objective(ingest_obj, prerequisite_ids=[])
        goal_graph.add_objective(extract_obj, prerequisite_ids=[ingest_obj.objective_id])
        goal_graph.add_objective(val_obj, prerequisite_ids=[extract_obj.objective_id])
        goal_graph.add_objective(memory_obj, prerequisite_ids=[val_obj.objective_id])

        return goal_graph

    def _classify_intent(self, intent_text: str) -> ObjectiveType:
        for kw, obj_type in self._keyword_type_map.items():
            if kw in intent_text:
                return obj_type
        return ObjectiveType.EXTRACTION
