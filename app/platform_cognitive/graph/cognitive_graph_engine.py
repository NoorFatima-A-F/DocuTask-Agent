"""
Enterprise Cognitive Graph Engine
Performs multi-hop causal reasoning over relational organizational entities.
"""
from typing import Dict, Optional, Any
from ..models.schemas import CognitiveNode, CognitiveEdge, ReasoningNodeType, ReasoningRelationType

class CognitiveGraphEngine:
    def __init__(self):
        self._nodes: Dict[str, CognitiveNode] = {}
        self._edges: Dict[str, CognitiveEdge] = {}

    def add_node(self, node: CognitiveNode) -> CognitiveNode:
        self._nodes[node.id] = node
        return node

    def add_edge(self, edge: CognitiveEdge) -> CognitiveEdge:
        self._edges[edge.id] = edge
        return edge

    def get_node(self, node_id: str, tenant_id: str) -> Optional[CognitiveNode]:
        n = self._nodes.get(node_id)
        if n and n.tenant_id == tenant_id:
            return n
        return None

    def query_causal_path(self, tenant_id: str, start_node_id: str, max_depth: int = 3) -> Dict[str, Any]:
        visited = set()
        matched_edges = []
        queue = [(start_node_id, 0)]
        
        while queue:
            curr_id, depth = queue.pop(0)
            if curr_id in visited or depth > max_depth:
                continue
            visited.add(curr_id)
            
            for edge in self._edges.values():
                if edge.tenant_id != tenant_id:
                    continue
                if edge.source_node_id == curr_id:
                    matched_edges.append(edge)
                    if edge.target_node_id not in visited:
                        queue.append((edge.target_node_id, depth + 1))
                elif edge.target_node_id == curr_id:
                    matched_edges.append(edge)
                    if edge.source_node_id not in visited:
                        queue.append((edge.source_node_id, depth + 1))
                        
        nodes = [self._nodes[nid] for nid in visited if nid in self._nodes and self._nodes[nid].tenant_id == tenant_id]
        return {
            "tenant_id": tenant_id,
            "root_node_id": start_node_id,
            "nodes": [n.model_dump() for n in nodes],
            "edges": [e.model_dump() for e in matched_edges]
        }

    def seed_default_cognitive_graph(self, tenant_id: str):
        if any(n.tenant_id == tenant_id for n in self._nodes.values()):
            return
            
        n_kpi = self.add_node(CognitiveNode(
            tenant_id=tenant_id,
            node_type=ReasoningNodeType.KPI,
            name="Quarterly Operating Margin (+22%)",
            description="Corporate margin target"
        ))
        n_goal = self.add_node(CognitiveNode(
            tenant_id=tenant_id,
            node_type=ReasoningNodeType.BUSINESS_GOAL,
            name="Automate 90% of Vendor Invoices",
            description="Reduce processing cycle time"
        ))
        n_agent = self.add_node(CognitiveNode(
            tenant_id=tenant_id,
            node_type=ReasoningNodeType.AGENT,
            name="InvoiceReconciliationAgent_v2",
            description="Autonomous invoice reconciliation fleet"
        ))
        n_risk = self.add_node(CognitiveNode(
            tenant_id=tenant_id,
            node_type=ReasoningNodeType.RISK,
            name="Supplier B Duplicate Billing Discrepancies",
            description="High exception frequency in PO matching"
        ))
        n_hyp = self.add_node(CognitiveNode(
            tenant_id=tenant_id,
            node_type=ReasoningNodeType.HYPOTHESIS,
            name="Switching Supplier B to EDI API will eliminate 94% of errors",
            description="Autonomous hypothesis derived from error logs"
        ))
        
        self.add_edge(CognitiveEdge(tenant_id=tenant_id, source_node_id=n_goal.id, target_node_id=n_kpi.id, relation=ReasoningRelationType.INFLUENCES))
        self.add_edge(CognitiveEdge(tenant_id=tenant_id, source_node_id=n_agent.id, target_node_id=n_goal.id, relation=ReasoningRelationType.IMPROVES))
        self.add_edge(CognitiveEdge(tenant_id=tenant_id, source_node_id=n_risk.id, target_node_id=n_goal.id, relation=ReasoningRelationType.BLOCKED_BY))
        self.add_edge(CognitiveEdge(tenant_id=tenant_id, source_node_id=n_hyp.id, target_node_id=n_risk.id, relation=ReasoningRelationType.RECOMMENDS))

    def get_overview(self, tenant_id: str) -> Dict[str, Any]:
        t_nodes = [n for n in self._nodes.values() if n.tenant_id == tenant_id]
        t_edges = [e for e in self._edges.values() if e.tenant_id == tenant_id]
        return {
            "total_nodes": len(t_nodes),
            "total_edges": len(t_edges),
            "nodes": [n.model_dump() for n in t_nodes],
            "edges": [e.model_dump() for e in t_edges]
        }
