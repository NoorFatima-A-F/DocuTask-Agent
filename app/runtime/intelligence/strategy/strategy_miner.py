"""
Strategy Miner for Phase 10 (AISLCOP).

Aggregates multiple operational experiences, calculates empirical performance
distributions, extracts failure modes, and synthesizes candidate strategies.
"""

from __future__ import annotations

import math
import uuid
from typing import List, Optional

from app.runtime.intelligence.experience.experience_record import ExperienceRecord
from app.runtime.intelligence.strategy.strategy_model import (
    ExecutionStrategy,
    MetricDistribution,
)


class StrategyMiner:
    """
    Mines reusable execution strategies from clusters of ExperienceRecords.
    """

    @staticmethod
    def _calc_distribution(values: List[float]) -> MetricDistribution:
        if not values:
            return MetricDistribution(0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        
        sorted_vals = sorted(values)
        n = len(sorted_vals)
        mean_val = sum(sorted_vals) / n
        
        if n > 1:
            variance = sum((x - mean_val) ** 2 for x in sorted_vals) / (n - 1)
            std_dev = math.sqrt(variance)
        else:
            std_dev = 0.0
            
        p50_idx = int(n * 0.5)
        p95_idx = min(int(n * 0.95), n - 1)
        
        return MetricDistribution(
            mean=round(mean_val, 4),
            std_dev=round(std_dev, 4),
            min_val=round(sorted_vals[0], 4),
            max_val=round(sorted_vals[-1], 4),
            p50=round(sorted_vals[p50_idx], 4),
            p95=round(sorted_vals[p95_idx], 4),
        )

    def mine_from_experiences(
        self,
        experiences: List[ExperienceRecord],
        strategy_name: Optional[str] = None,
        min_cluster_size: int = 1,
    ) -> Optional[ExecutionStrategy]:
        """
        Synthesizes an ExecutionStrategy from a cluster of experiences for the same domain/task.
        """
        if not experiences or len(experiences) < min_cluster_size:
            return None

        sample_exp = experiences[0]
        domain = sample_exp.document_type
        task = sample_exp.task_type
        
        latencies = [e.total_latency_ms for e in experiences]
        costs = [e.total_cost_usd for e in experiences]
        confidences = [e.final_confidence for e in experiences]
        
        successes = sum(1 for e in experiences if e.status == "SUCCESS")
        success_rate = round(successes / len(experiences), 4)
        
        total_retries = sum(e.retries_count for e in experiences)
        retry_frequency = round(total_retries / len(experiences), 4)

        # Collect unique failure modes and tools
        failure_modes = set()
        tools = set()
        exp_ids = []
        evidence_hashes = []

        for e in experiences:
            exp_ids.append(e.experience_id)
            if e.evidence_root_hash:
                evidence_hashes.append(e.evidence_root_hash)
            for path in e.recovery_paths_used:
                failure_modes.add(f"Recovered from: {path}")
            if e.validation_failures_count > 0:
                failure_modes.add(f"Validation failure rate: {e.validation_failures_count}")
            for t in e.tool_traces:
                tools.add(t.tool_name)

        strategy_id = f"strat_{uuid.uuid4().hex[:10]}"
        name = strategy_name or f"Optimized {domain.title()} {task.title()} Strategy"

        strategy = ExecutionStrategy(
            strategy_id=strategy_id,
            name=name,
            document_domain=domain,
            target_task=task,
            version="1.0.0",
            is_promoted=False,
            required_capabilities=[f"{domain.lower()}_processing", "schema_validation"],
            recommended_tools=list(tools) if tools else ["ocr_provider", "schema_validator"],
            dag_template_nodes=["extract_metadata", "ocr_parse", "validate_invariants", "sign_evidence"],
            sample_size=len(experiences),
            observed_success_rate=success_rate,
            latency_profile=self._calc_distribution(latencies),
            cost_profile=self._calc_distribution(costs),
            confidence_profile=self._calc_distribution(confidences),
            retry_frequency=retry_frequency,
            known_failure_modes=list(failure_modes),
            prerequisites=["api_credentials_valid", "schema_contract_loaded"],
            supporting_experience_ids=exp_ids,
            supporting_evidence_hashes=evidence_hashes,
        )

        return strategy
