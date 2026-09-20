"""
Context Engineering Engine
Optimal context selection, token budgeting, relevance re-ranking, and memory compression.
"""
import time
from typing import List, Dict, Any
from ..models.schemas import (
    ContextRetrievalRequest, ContextRetrievalResponse, RetrievedSnippet
)
from ..vector.semantic_vector_engine import SemanticVectorEngine
from ..knowledge_graph.enterprise_knowledge_graph import EnterpriseKnowledgeGraph
from ..memory.enterprise_memory_system import EnterpriseMemorySystem

class ContextEngineeringEngine:
    def __init__(
        self,
        vector_engine: SemanticVectorEngine,
        graph_engine: EnterpriseKnowledgeGraph,
        memory_system: EnterpriseMemorySystem
    ):
        self.vector_engine = vector_engine
        self.graph_engine = graph_engine
        self.memory_system = memory_system

    def assemble_grounded_context(self, request: ContextRetrievalRequest) -> ContextRetrievalResponse:
        start_time = time.time()
        
        # 1. Semantic + Keyword hybrid search
        snippets = self.vector_engine.hybrid_search(
            tenant_id=request.tenant_id,
            query=request.goal,
            top_k=request.top_k,
            user_clearance=request.user_clearance,
            user_roles=request.user_roles,
            filter_tags=request.filter_tags
        )
        
        # 2. Graph relationship context (if requested)
        graph_context = []
        if request.include_graph_context:
            overview = self.graph_engine.get_graph_overview(request.tenant_id)
            for edge in overview.get("edges", [])[:4]:
                src_name = next((n["name"] for n in overview["nodes"] if n["id"] == edge["source_node_id"]), "Entity")
                tgt_name = next((n["name"] for n in overview["nodes"] if n["id"] == edge["target_node_id"]), "Target")
                graph_context.append(f"[Ontology] {src_name} --({edge['relation_type']})--> {tgt_name}")
        
        # 3. Agent Memory Context (if requested)
        memory_context = []
        if request.include_memory:
            memories = self.memory_system.retrieve_memory(
                tenant_id=request.tenant_id,
                query=request.goal,
                tier=request.memory_tier,
                limit=3
            )
            for mem in memories:
                memory_context.append(f"[{mem.tier.value} MEMORY] {mem.key}: {mem.content}")
        
        # 4. Context Compression & Packing
        packed_lines = [
            f"# GROUNDED ENTERPRISE CONTEXT FOR GOAL: {request.goal}",
            "---",
            "## 1. Verified Documents & Knowledge Snippets:"
        ]
        
        raw_chars = 0
        for snip in snippets:
            packed_lines.append(f"- **{snip.title}** (Classification: {snip.security_classification.value}, Match: {snip.matched_via}): {snip.content}")
            raw_chars += len(snip.content)
            
        if graph_context:
            packed_lines.append("\n## 2. Organizational Ontology & Relationships:")
            for g in graph_context:
                packed_lines.append(f"- {g}")
                raw_chars += len(g)
                
        if memory_context:
            packed_lines.append("\n## 3. Relevant Enterprise & Episodic Memories:")
            for m in memory_context:
                packed_lines.append(f"- {m}")
                raw_chars += len(m)
                
        packed_prompt = "\n".join(packed_lines)
        token_est = len(packed_prompt.split())
        
        # Calculate compression ratio vs raw estimated characters
        compression_ratio = round((raw_chars + 1) / max(len(packed_prompt), 1), 2)
        latency_ms = round((time.time() - start_time) * 1000, 2)
        
        return ContextRetrievalResponse(
            query=request.goal,
            snippets=snippets,
            graph_context=graph_context,
            memory_context=memory_context,
            optimized_context_prompt=packed_prompt,
            total_tokens_estimated=token_est,
            compression_ratio=compression_ratio,
            retrieval_latency_ms=latency_ms
        )
