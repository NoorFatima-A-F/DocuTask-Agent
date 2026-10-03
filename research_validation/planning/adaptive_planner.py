"""
Adaptive Experiment Planner (Phase 87C)
=======================================
Synthesizes end-to-end scientific experiment DAGs dynamically based on
hypotheses, available datasets, and target statistical confidence criteria.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from research_validation.hypothesis.hypothesis_model import ScientificHypothesis
from research_validation.planning.execution_strategy import (
    AdaptiveExecutionStrategy, TargetHardware
)
from research_validation.scientific_execution.experiment_manifest import (
    ExperimentManifest, ExperimentParameters, DatasetFingerprint
)
from research_validation.scientific_execution.experiment_dependency_graph import (
    ExperimentDependencyGraph, PipelineStageType
)
from research_validation.provenance.hashing import hash_canonical_json


@dataclass(frozen=True)
class PlannedExperimentDAG:
    """Complete executable plan ready for orchestrator execution."""
    plan_id: str
    hypothesis_id: str
    manifest: ExperimentManifest
    strategy: AdaptiveExecutionStrategy
    dependency_graph: ExperimentDependencyGraph
    estimated_duration_sec: float
    created_at_utc: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    plan_digest_sha256: str = field(default="")


class AdaptiveExperimentPlanner:
    """
    Transforms scientific hypotheses into fully configured executable experiment plans.
    """

    @classmethod
    def build_plan(
        cls,
        hypothesis: ScientificHypothesis,
        strategy: Optional[AdaptiveExecutionStrategy] = None,
        custom_params: Optional[Dict[str, Any]] = None,
    ) -> PlannedExperimentDAG:
        strat = strategy or AdaptiveExecutionStrategy(
            target_hardware=TargetHardware.AUTO,
            max_concurrency=4,
            max_retries_per_stage=3,
            checkpoint_cadence_seconds=10.0,
            confidence_target=0.95,
            max_ci_width=0.04,
            early_stopping_patience_steps=5,
            timeout_seconds=hypothesis.estimated_runtime_sec * 2.0,
        )

        plan_id = f"plan_{hypothesis.hypothesis_id}_{int(datetime.now(timezone.utc).timestamp())}"
        
        # 1. Build Manifest Parameters
        params_dict = {
            "hypothesis_id": hypothesis.hypothesis_id,
            "target_metric": "f1",
            "seed": 42,
            "confidence_target": strat.confidence_target,
        }
        if custom_params:
            params_dict.update(custom_params)

        target_ds_name = hypothesis.required_datasets[0] if hypothesis.required_datasets else "funsd"
        dataset_fp = DatasetFingerprint(
            dataset_name=target_ds_name,
            dataset_version="1.0",
            expected_sample_count=100,
            sha256_checksum=f"hash_{target_ds_name}_v1",
        )

        exp_params = ExperimentParameters(
            sample_count=100,
            seed=42,
            batch_size=32,
            target_metrics=("f1", "precision", "recall", "latency_p99_ms"),
            custom_parameters=params_dict,
        )

        env = {
            "os": "Linux/Windows",
            "python_version": "3.11+",
            "hardware_spec": strat.target_hardware.value,
        }

        manifest = ExperimentManifest.create(
            title=f"Plan: {hypothesis.title}",
            description=hypothesis.statement,
            parameters=exp_params,
            dataset=dataset_fp,
            environment=env,
            tags=("autonomous_plan", hypothesis.hypothesis_id),
        )

        # 2. Build Dependency Graph
        dep_graph = ExperimentDependencyGraph(graph_id=f"dag_{plan_id}")
        stages = [
            ("raw_dataset", PipelineStageType.RAW_DATASET, "Raw Dataset Ingestion", []),
            ("preprocessing", PipelineStageType.PREPROCESSING, "Document Preprocessing", ["raw_dataset"]),
            ("benchmark", PipelineStageType.BENCHMARK, "Model Execution & Evaluation", ["preprocessing"]),
            ("aggregation", PipelineStageType.AGGREGATION, "Metric Aggregation", ["benchmark"]),
            ("visualization", PipelineStageType.VISUALIZATION, "Uncertainty & Diagnostic Plotting", ["aggregation"]),
            ("publication_figure", PipelineStageType.PUBLICATION_FIGURE, "Vector Figure Generation", ["visualization"]),
            ("research_report", PipelineStageType.RESEARCH_REPORT, "Scientific Report Synthesis", ["publication_figure"]),
        ]

        for s_id, s_type, s_name, parents in stages:
            dep_graph.add_node(
                node_id=s_id,
                stage_type=s_type,
                name=s_name,
                parent_ids=parents,
            )

        payload = {
            "plan_id": plan_id,
            "hypothesis_id": hypothesis.hypothesis_id,
            "manifest_digest": manifest.manifest_digest_sha256,
            "strategy": strat.target_hardware.value,
        }
        digest = hash_canonical_json(payload)

        return PlannedExperimentDAG(
            plan_id=plan_id,
            hypothesis_id=hypothesis.hypothesis_id,
            manifest=manifest,
            strategy=strat,
            dependency_graph=dep_graph,
            estimated_duration_sec=hypothesis.estimated_runtime_sec,
            plan_digest_sha256=digest,
        )
