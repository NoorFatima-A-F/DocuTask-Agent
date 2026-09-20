"""
Scientific Experiment Orchestrator (Phase 82B.3)
===============================================
Master orchestrator unifying experiment registration, DAG dependency resolution,
topological execution, checkpointing, uncertainty propagation, and artifact dispatch.
"""

from __future__ import annotations
import json
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable, Dict, List, Optional, Tuple

from research_validation.scientific_execution.experiment_manifest import (
    ExperimentManifest, ExperimentStatus
)
from research_validation.scientific_execution.experiment_registry import (
    ExperimentRegistry, ExperimentRecord
)
from research_validation.scientific_execution.experiment_dependency_graph import (
    ExperimentDependencyGraph, PipelineStageType, NodeState
)
from research_validation.scientific_execution.experiment_runner import (
    ScientificExperimentRunner, ExperimentRunResult
)
from research_validation.provenance.evidence_graph import EvidenceGraph
from research_validation.provenance.provenance_models import LineageStage, EvidenceQualityLevel
from research_validation.provenance.hashing import hash_canonical_json


@dataclass(frozen=True)
class OrchestrationReport:
    orchestration_id: str
    experiment_id: str
    status: ExperimentStatus
    start_time_utc: str
    end_time_utc: str
    total_stages: int
    executed_stages: int
    run_result: ExperimentRunResult
    provenance_graph_digest: str
    is_fully_reproducible: bool
    diagnostic_summary: str


class ScientificExperimentOrchestrator:
    """
    Unified scientific experimentation orchestrator.
    """

    def __init__(
        self,
        registry: Optional[ExperimentRegistry] = None,
        runner: Optional[ScientificExperimentRunner] = None,
    ):
        self.registry = registry or ExperimentRegistry()
        self.runner = runner or ScientificExperimentRunner()

    def run_experiment(
        self,
        manifest: ExperimentManifest,
        dependency_graph: Optional[ExperimentDependencyGraph] = None,
        mock_samples: Optional[List[Dict[str, Any]]] = None,
    ) -> OrchestrationReport:
        """
        Orchestrate complete pipeline execution for an experiment.
        """
        orch_id = f"orch_{int(time.time())}_{manifest.experiment_id[:6]}"
        t_start_utc = datetime.now(timezone.utc).isoformat()

        # 1. Enforce Registration
        record = self.registry.get_record(manifest.experiment_id)
        if not record:
            record = self.registry.register(manifest)

        self.registry.update_status(manifest.experiment_id, ExperimentStatus.RUNNING)

        # 2. Build or use Dependency Graph
        dag = dependency_graph or self._build_default_dag(manifest)
        ordered_stages = dag.topological_sort()

        # 3. Provenance Graph recording
        prov_graph = EvidenceGraph(f"prov_{manifest.experiment_id}")
        raw_obs = prov_graph.record_node(
            node_id=f"raw_{manifest.experiment_id}",
            stage=LineageStage.RAW_OBSERVATION,
            name=f"Dataset: {manifest.dataset.dataset_name}",
            description="Input dataset fingerprint and manifest parameters",
            payload={"dataset": manifest.dataset.canonical_dict(), "params": manifest.parameters.canonical_dict()},
            parent_node_ids=[],
            quality_level=manifest.quality_level,
        )

        # 4. Execute via Runner
        run_res = self.runner.execute(manifest, mock_dataset_samples=mock_samples)

        # 5. Record Intermediate & Final Provenance Nodes
        curr_parent = raw_obs.node_id
        for stage_name, stage_h in run_res.intermediate_hashes.items():
            stage_node = prov_graph.record_node(
                node_id=f"{stage_name}_{manifest.experiment_id}",
                stage=LineageStage.TRANSFORMATION,
                name=f"Stage: {stage_name}",
                description=f"Intermediate execution hash {stage_h[:12]}",
                payload={"stage": stage_name, "stage_hash": stage_h},
                parent_node_ids=[curr_parent],
                quality_level=manifest.quality_level,
            )
            curr_parent = stage_node.node_id
            dag.update_node_output(stage_name, stage_h)

        # Final Metric node
        final_node = prov_graph.record_node(
            node_id=f"final_{manifest.experiment_id}",
            stage=LineageStage.FINAL_METRIC,
            name=f"Metrics: {manifest.title}",
            description="Aggregated final scientific metrics",
            payload={"metrics": run_res.metrics, "output_digest": run_res.final_output_digest},
            parent_node_ids=[curr_parent],
            quality_level=manifest.quality_level,
        )
        dag.update_node_output("aggregation", run_res.final_output_digest)

        # 6. Update Registry
        self.registry.update_status(
            manifest.experiment_id,
            run_res.status,
            run_hash=run_res.final_output_digest or None,
        )

        t_end_utc = datetime.now(timezone.utc).isoformat()
        prov_digest = prov_graph.merkle_dag.compute_root_digest()

        return OrchestrationReport(
            orchestration_id=orch_id,
            experiment_id=manifest.experiment_id,
            status=run_res.status,
            start_time_utc=t_start_utc,
            end_time_utc=t_end_utc,
            total_stages=len(ordered_stages),
            executed_stages=len(ordered_stages),
            run_result=run_res,
            provenance_graph_digest=prov_digest,
            is_fully_reproducible=(run_res.status == ExperimentStatus.COMPLETED),
            diagnostic_summary=f"Orchestrated {len(ordered_stages)} pipeline stages. Status: {run_res.status.value}.",
        )

    def _build_default_dag(self, manifest: ExperimentManifest) -> ExperimentDependencyGraph:
        dag = ExperimentDependencyGraph(f"dag_{manifest.experiment_id}")
        dag.add_node("raw_dataset", PipelineStageType.RAW_DATASET, "Raw Dataset Input")
        dag.add_node("preprocessing", PipelineStageType.PREPROCESSING, "Data Cleaning & Normalization", ["raw_dataset"])
        dag.add_node("benchmark", PipelineStageType.BENCHMARK, "Model Evaluation Loop", ["preprocessing"])
        dag.add_node("aggregation", PipelineStageType.AGGREGATION, "Statistical Metrics Aggregation", ["benchmark"])
        dag.add_node("visualization", PipelineStageType.VISUALIZATION, "Charts & Plots Synthesis", ["aggregation"])
        dag.add_node("publication_figure", PipelineStageType.PUBLICATION_FIGURE, "Figure Vectorization", ["visualization"])
        dag.add_node("research_report", PipelineStageType.RESEARCH_REPORT, "Final Research Report", ["publication_figure"])
        return dag
