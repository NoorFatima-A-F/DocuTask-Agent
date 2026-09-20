"""
Enterprise Knowledge Graph Engine
Constructs organizational ontology, entity resolution, and multi-hop graph traversal.
"""
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
from ..models.schemas import GraphNode, GraphEdge, EntityType

class EnterpriseKnowledgeGraph:
    def __init__(self):
        self._nodes: Dict[str, GraphNode] = {}
        self._edges: Dict[str, GraphEdge] = {}

    def add_node(self, node: GraphNode) -> GraphNode:
        self._nodes[node.id] = node
        return node

    def add_edge(self, edge: GraphEdge) -> GraphEdge:
        self._edges[edge.id] = edge
        return edge

    def get_node(self, node_id: str, tenant_id: str) -> Optional[GraphNode]:
        n = self._nodes.get(node_id)
        if n and n.tenant_id == tenant_id:
            return n
        return None

    def find_nodes_by_type(self, tenant_id: str, entity_type: EntityType) -> List[GraphNode]:
        return [n for n in self._nodes.values() if n.tenant_id == tenant_id and n.entity_type == entity_type]

    def query_subgraph(self, tenant_id: str, start_node_id: str, max_depth: int = 2) -> Dict[str, Any]:
        visited_nodes = set()
        matched_edges = []
        
        queue = [(start_node_id, 0)]
        while queue:
            curr_id, depth = queue.pop(0)
            if curr_id in visited_nodes or depth > max_depth:
                continue
            visited_nodes.add(curr_id)
            
            for edge in self._edges.values():
                if edge.tenant_id != tenant_id:
                    continue
                if edge.source_node_id == curr_id:
                    matched_edges.append(edge)
                    if edge.target_node_id not in visited_nodes:
                        queue.append((edge.target_node_id, depth + 1))
                elif edge.target_node_id == curr_id:
                    matched_edges.append(edge)
                    if edge.source_node_id not in visited_nodes:
                        queue.append((edge.source_node_id, depth + 1))
                        
        nodes = [self._nodes[nid] for nid in visited_nodes if nid in self._nodes and self._nodes[nid].tenant_id == tenant_id]
        return {
            "nodes": [n.model_dump() for n in nodes],
            "edges": [e.model_dump() for e in matched_edges]
        }

    def seed_default_enterprise_ontology(self, tenant_id: str):
        # Seed an illustrative enterprise graph if empty
        if any(n.tenant_id == tenant_id for n in self._nodes.values()):
            return
        
        n_dept = self.add_node(GraphNode(
            tenant_id=tenant_id,
            name="Finance & Accounting",
            entity_type=EntityType.DEPARTMENT,
            properties={"headcount": 45, "cost_center": "CC-901"}
        ))
        n_emp = self.add_node(GraphNode(
            tenant_id=tenant_id,
            name="Sarah Connor (VP Finance)",
            entity_type=EntityType.EMPLOYEE,
            properties={"email": "sconnor@enterprise.io", "role": "VP"}
        ))
        n_agent = self.add_node(GraphNode(
            tenant_id=tenant_id,
            name="InvoiceReconciliationAgent",
            entity_type=EntityType.AI_AGENT,
            properties={"model": "gemini-1.5-pro", "version": "v1.4.0"}
        ))
        n_sys = self.add_node(GraphNode(
            tenant_id=tenant_id,
            name="SAP ERP Gateway",
            entity_type=EntityType.SYSTEM,
            properties={"endpoint": "https://erp.internal", "protocol": "OData"}
        ))
        n_pol = self.add_node(GraphNode(
            tenant_id=tenant_id,
            name="PO-Threshold Policy (>$50k requires 2 Approvals)",
            entity_type=EntityType.POLICY,
            properties={"policy_code": "FIN-2026-A"}
        ))
        
        self.add_edge(GraphEdge(tenant_id=tenant_id, source_node_id=n_emp.id, target_node_id=n_dept.id, relation_type="works_for"))
        self.add_edge(GraphEdge(tenant_id=tenant_id, source_node_id=n_dept.id, target_node_id=n_agent.id, relation_type="owns"))
        self.add_edge(GraphEdge(tenant_id=tenant_id, source_node_id=n_agent.id, target_node_id=n_sys.id, relation_type="depends_on"))
        self.add_edge(GraphEdge(tenant_id=tenant_id, source_node_id=n_agent.id, target_node_id=n_pol.id, relation_type="governed_by"))

    def get_graph_overview(self, tenant_id: str) -> Dict[str, Any]:
        tenant_nodes = [n for n in self._nodes.values() if n.tenant_id == tenant_id]
        tenant_edges = [e for e in self._edges.values() if e.tenant_id == tenant_id]
        
        return {
            "total_nodes": len(tenant_nodes),
            "total_edges": len(tenant_edges),
            "nodes": [n.model_dump() for n in tenant_nodes],
            "edges": [e.model_dump() for e in tenant_edges],
            "entity_counts": {
                et.value: len([n for n in tenant_nodes if n.entity_type == et])
                for et in EntityType
            }
        }
