"""
AMCN-SIP Phase 13.8 - Collective Swarm Learning & Shared Intelligence
Cross-agent knowledge graph, shared memory indices, emergent strategy mining, and pattern recognition.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
import hashlib
from typing import Any, Dict, List, Optional, Set


@dataclass
class SwarmKnowledgeNode:
    node_id: str
    node_type: str  # 'AGENT', 'SKILL', 'TASK_PATTERN', 'DOMAIN', 'STRATEGY'
    label: str
    properties: Dict[str, Any] = field(default_factory=dict)
    confidence: float = 1.0
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class SwarmKnowledgeEdge:
    source_id: str
    target_id: str
    relationship: str  # 'COLLABORATED_WITH', 'EXPERT_IN', 'RESOLVED_BY', 'OPTIMAL_FOR'
    weight: float = 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CoordinationPattern:
    pattern_id: str
    name: str
    pattern_type: str  # 'DECOMPOSITION_PIPELINE', 'CROSS_VALIDATION_TRIAD', 'HIERARCHICAL_DELEGATION'
    roles_involved: List[str]
    success_rate: float
    avg_latency_ms: float
    usage_count: int = 1
    description: str = ""
    mined_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class SwarmKnowledgeGraph:
    """
    Maintains semantic knowledge graph across all agent interactions in the swarm.
    """

    def __init__(self):
        self._nodes: Dict[str, SwarmKnowledgeNode] = {}
        self._edges: List[SwarmKnowledgeEdge] = []
        self._seed_default_graph()

    def add_node(self, node: SwarmKnowledgeNode):
        self._nodes[node.node_id] = node

    def add_edge(self, edge: SwarmKnowledgeEdge):
        # Update if already exists, else append
        for existing in self._edges:
            if existing.source_id == edge.source_id and existing.target_id == edge.target_id and existing.relationship == edge.relationship:
                existing.weight = edge.weight
                existing.metadata.update(edge.metadata)
                return
        self._edges.append(edge)

    def get_neighbors(self, node_id: str) -> List[Dict[str, Any]]:
        results = []
        for edge in self._edges:
            if edge.source_id == node_id:
                tgt = self._nodes.get(edge.target_id)
                if tgt:
                    results.append({"node": tgt, "relationship": edge.relationship, "weight": edge.weight})
            elif edge.target_id == node_id:
                src = self._nodes.get(edge.source_id)
                if src:
                    results.append({"node": src, "relationship": edge.relationship, "weight": edge.weight})
        return results

    def get_summary(self) -> Dict[str, Any]:
        return {
            "total_nodes": len(self._nodes),
            "total_edges": len(self._edges),
            "nodes": [
                {
                    "node_id": n.node_id,
                    "node_type": n.node_type,
                    "label": n.label,
                    "confidence": n.confidence,
                    "properties": n.properties,
                }
                for n in self._nodes.values()
            ],
            "edges": [
                {
                    "source": e.source_id,
                    "target": e.target_id,
                    "relationship": e.relationship,
                    "weight": e.weight,
                }
                for e in self._edges
            ],
        }

    def _seed_default_graph(self):
        # Core domain nodes
        domains = ["DocumentParsing", "OCRVerification", "FraudDetection", "ComplianceAudit", "ResourceScheduling"]
        for d in domains:
            self.add_node(SwarmKnowledgeNode(node_id=f"domain_{d.lower()}", node_type="DOMAIN", label=d))

        # Core Agent nodes
        agents = [
            ("agent-exec-01", "Executive Director", "EXECUTIVE"),
            ("agent-plan-01", "Lead Planner", "PLANNER"),
            ("agent-coord-01", "Swarm Coordinator", "COORDINATOR"),
            ("agent-spec-ocr", "OCR Specialist", "SPECIALIST"),
            ("agent-val-sec", "Security Validator", "VALIDATOR"),
            ("agent-res-opt", "Resource Governor", "RESOURCE"),
        ]
        for aid, label, role in agents:
            self.add_node(SwarmKnowledgeNode(node_id=aid, node_type="AGENT", label=label, properties={"role": role}))

        # Edges
        self.add_edge(SwarmKnowledgeEdge("agent-spec-ocr", "domain_ocrverification", "EXPERT_IN", weight=0.98))
        self.add_edge(SwarmKnowledgeEdge("agent-val-sec", "domain_complianceaudit", "EXPERT_IN", weight=0.99))
        self.add_edge(SwarmKnowledgeEdge("agent-plan-01", "domain_resourcescheduling", "OPTIMAL_FOR", weight=0.94))
        self.add_edge(SwarmKnowledgeEdge("agent-exec-01", "agent-plan-01", "COLLABORATED_WITH", weight=0.97))
        self.add_edge(SwarmKnowledgeEdge("agent-plan-01", "agent-coord-01", "COLLABORATED_WITH", weight=0.96))
        self.add_edge(SwarmKnowledgeEdge("agent-coord-01", "agent-spec-ocr", "COLLABORATED_WITH", weight=0.95))
        self.add_edge(SwarmKnowledgeEdge("agent-spec-ocr", "agent-val-sec", "COLLABORATED_WITH", weight=0.99))


class CollaborationPatternMiner:
    """
    Identifies high-performing agent combinations and emergent collective workflows.
    """

    def __init__(self):
        self._patterns: Dict[str, CoordinationPattern] = {}
        self._seed_default_patterns()

    def mine_pattern(
        self,
        name: str,
        pattern_type: str,
        roles_involved: List[str],
        success_rate: float,
        latency_ms: float,
        description: str,
    ) -> CoordinationPattern:
        pid = f"pat_{hashlib.sha256(f'{name}_{pattern_type}_{''.join(roles_involved)}'.encode()).hexdigest()[:8]}"
        pat = CoordinationPattern(
            pattern_id=pid,
            name=name,
            pattern_type=pattern_type,
            roles_involved=roles_involved,
            success_rate=success_rate,
            avg_latency_ms=latency_ms,
            description=description,
        )
        self._patterns[pid] = pat
        return pat

    def get_patterns(self) -> List[CoordinationPattern]:
        return list(self._patterns.values())

    def _seed_default_patterns(self):
        self.mine_pattern(
            name="Triadic Verification Pipeline",
            pattern_type="CROSS_VALIDATION_TRIAD",
            roles_involved=["SPECIALIST", "VALIDATOR", "REVIEWER"],
            success_rate=0.998,
            latency_ms=310.0,
            description="Specialist extracts metadata, validator checks cryptographic checksums, reviewer verifies business invariants.",
        )
        self.mine_pattern(
            name="Hierarchical Delegation Matrix",
            pattern_type="HIERARCHICAL_DELEGATION",
            roles_involved=["EXECUTIVE", "PLANNER", "COORDINATOR", "RESOURCE"],
            success_rate=0.985,
            latency_ms=450.0,
            description="Executive partitions high-level mission into parallel sub-graphs governed by Coordinator under Resource budget constraints.",
        )
        self.mine_pattern(
            name="Bargaining-Based Task Allocation",
            pattern_type="DECOMPOSITION_PIPELINE",
            roles_involved=["NEGOTIATOR", "COORDINATOR", "SPECIALIST"],
            success_rate=0.992,
            latency_ms=220.0,
            description="Auctions high-priority extraction batches to available specialists using SLA & compute cost bargaining.",
        )


class CollectiveLearningEngine:
    """
    Master coordinator for swarm memory synthesis, knowledge distillation, and strategy evolution.
    """

    def __init__(self):
        self.knowledge_graph = SwarmKnowledgeGraph()
        self.pattern_miner = CollaborationPatternMiner()
        self._learned_insights: List[Dict[str, Any]] = []
        self._seed_insights()

    def record_coordination_event(
        self,
        task_type: str,
        agents_involved: List[str],
        success: bool,
        duration_ms: float,
        efficiency_score: float,
    ):
        # Update knowledge graph edges
        for i, a1 in enumerate(agents_involved):
            for a2 in agents_involved[i + 1:]:
                delta = 0.02 if success else -0.05
                current_weight = 0.85
                for e in self.knowledge_graph._edges:
                    if (e.source_id == a1 and e.target_id == a2) or (e.source_id == a2 and e.target_id == a1):
                        current_weight = e.weight
                        break
                new_w = round(max(0.1, min(1.0, current_weight + delta)), 3)
                self.knowledge_graph.add_edge(
                    SwarmKnowledgeEdge(
                        source_id=a1,
                        target_id=a2,
                        relationship="COLLABORATED_WITH",
                        weight=new_w,
                        metadata={"last_task": task_type, "success": success},
                    )
                )

        if success and efficiency_score > 0.90:
            self._learned_insights.append({
                "insight_id": f"ins_{datetime.now(timezone.utc).strftime('%H%M%S%f')[:10]}",
                "task_type": task_type,
                "agents": agents_involved,
                "efficiency_score": efficiency_score,
                "duration_ms": duration_ms,
                "discovered_at": datetime.now(timezone.utc).isoformat(),
                "recommendation": f"Pair {agents_involved[0]} with {agents_involved[-1]} for {task_type} missions.",
            })

    def get_collective_learning_summary(self) -> Dict[str, Any]:
        return {
            "knowledge_graph": self.knowledge_graph.get_summary(),
            "patterns": [p.__dict__ for p in self.pattern_miner.get_patterns()],
            "insights": self._learned_insights[-20:],
            "total_insights_mined": len(self._learned_insights),
        }

    def _seed_insights(self):
        self._learned_insights = [
            {
                "insight_id": "ins_001",
                "task_type": "PDF_EXTRACTION",
                "agents": ["agent-spec-ocr", "agent-val-sec"],
                "efficiency_score": 0.985,
                "duration_ms": 142.0,
                "discovered_at": datetime.now(timezone.utc).isoformat(),
                "recommendation": "Pairing OCR Specialist with Security Validator reduces schema verification latency by 44%.",
            },
            {
                "insight_id": "ins_002",
                "task_type": "RESOURCE_ARBITRATION",
                "agents": ["agent-res-opt", "agent-coord-01"],
                "efficiency_score": 0.962,
                "duration_ms": 188.0,
                "discovered_at": datetime.now(timezone.utc).isoformat(),
                "recommendation": "Pre-allocating token quota during consensus negotiation prevents auction thrashing under burst loads.",
            },
        ]
