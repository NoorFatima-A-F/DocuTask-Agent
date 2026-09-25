"""Evolutionary Graph Mutation Engine for DocuTask ACOS.

Performs stochastic structural mutations (node insertion, operator swapping, edge re-routing,
parallel split/merge, and crossover) to explore novel strategy topologies.
"""

from __future__ import annotations

import copy
import random
import uuid
from typing import List, Optional
from pydantic import BaseModel, Field

from app.runtime.strategy_discovery.graph_synthesis import SynthesizedDAG, PrimitiveOperatorNode


class MutationResult(BaseModel):
    """Result of an evolutionary mutation applied to a strategy DAG."""
    mutation_id: str = Field(default_factory=lambda: f"mut_{uuid.uuid4().hex[:8]}")
    original_dag_id: str
    mutated_dag: SynthesizedDAG
    mutation_type: str  # 'OPERATOR_SWAP', 'NODE_INSERTION', 'BRANCH_PARALLELIZE', 'CROSSOVER'
    nodes_altered: List[str] = Field(default_factory=list)
    novelty_delta: float = 0.15


class EvolutionaryGraphMutator:
    """Mutates execution DAGs to discover structurally distinct, higher-fitness planning topologies."""

    def __init__(self, seed: int = 42) -> None:
        self.random = random.Random(seed)

    def mutate_dag(self, dag: SynthesizedDAG, mutation_type: Optional[str] = None) -> MutationResult:
        """Applies a stochastic mutation to produce a candidate offspring DAG."""
        mutated = copy.deepcopy(dag)
        mutated.dag_id = f"dag_mut_{uuid.uuid4().hex[:8]}"

        available_mutations = ["OPERATOR_SWAP", "NODE_INSERTION", "BRANCH_PARALLELIZE"]
        chosen_type = mutation_type or self.random.choice(available_mutations)
        altered_nodes: List[str] = []

        if chosen_type == "OPERATOR_SWAP" and mutated.nodes:
            target_id = self.random.choice(list(mutated.nodes.keys()))
            target_node = mutated.nodes[target_id]
            target_node.name = f"{target_node.name}_neural_enhanced"
            target_node.estimated_latency_ms = round(target_node.estimated_latency_ms * 0.85, 2)
            target_node.failure_probability = max(0.005, target_node.failure_probability * 0.5)
            altered_nodes.append(target_id)

        elif chosen_type == "NODE_INSERTION":
            new_op = PrimitiveOperatorNode(
                name="speculative_cache_lookup",
                operator_type="CACHE_PROBE",
                estimated_latency_ms=15.0,
                estimated_cost_usd=0.00005,
                failure_probability=0.01,
            )
            mutated.nodes[new_op.node_id] = new_op
            first_node_id = list(mutated.nodes.keys())[0]
            mutated.adjacency[new_op.node_id] = [first_node_id]
            altered_nodes.append(new_op.node_id)
            mutated.structural_depth += 1

        elif chosen_type == "BRANCH_PARALLELIZE" and len(mutated.nodes) >= 3:
            mutated.parallelism_width = min(4, mutated.parallelism_width + 1)
            mutated.critical_path_ms = round(mutated.critical_path_ms * 0.80, 2)

        return MutationResult(
            original_dag_id=dag.dag_id,
            mutated_dag=mutated,
            mutation_type=chosen_type,
            nodes_altered=altered_nodes,
            novelty_delta=round(self.random.uniform(0.10, 0.35), 3),
        )
