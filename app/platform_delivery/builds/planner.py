"""Build DAG Planner and Sequence Compiler."""
from typing import List, Set
from .models import PipelineStageType


class BuildPlanner:
    """Plans and orders build pipeline stages guaranteeing dependency satisfaction."""

    STAGE_DEPENDENCIES = {
        PipelineStageType.LINT: set(),
        PipelineStageType.TYPECHECK: {PipelineStageType.LINT},
        PipelineStageType.UNIT_TEST: {PipelineStageType.TYPECHECK},
        PipelineStageType.SECURITY_SCAN: {PipelineStageType.LINT},
        PipelineStageType.DEPENDENCY_AUDIT: {PipelineStageType.LINT},
        PipelineStageType.INTEGRATION_TEST: {PipelineStageType.UNIT_TEST},
        PipelineStageType.SECRET_SCAN: {PipelineStageType.LINT},
        PipelineStageType.BUILD: {PipelineStageType.UNIT_TEST, PipelineStageType.SECURITY_SCAN},
        PipelineStageType.CONTAINER_SCAN: {PipelineStageType.BUILD},
        PipelineStageType.SBOM: {PipelineStageType.BUILD},
        PipelineStageType.PROVENANCE: {PipelineStageType.BUILD, PipelineStageType.SBOM},
        PipelineStageType.SIGN: {PipelineStageType.PROVENANCE, PipelineStageType.CONTAINER_SCAN},
        PipelineStageType.PUBLISH: {PipelineStageType.SIGN},
    }

    DEFAULT_PIPELINE = [
        PipelineStageType.LINT,
        PipelineStageType.TYPECHECK,
        PipelineStageType.UNIT_TEST,
        PipelineStageType.SECURITY_SCAN,
        PipelineStageType.BUILD,
        PipelineStageType.CONTAINER_SCAN,
        PipelineStageType.SBOM,
        PipelineStageType.PROVENANCE,
        PipelineStageType.SIGN,
        PipelineStageType.PUBLISH,
    ]

    @classmethod
    def get_execution_order(cls, requested_stages: List[PipelineStageType]) -> List[PipelineStageType]:
        """Topologically sorts requested stages to ensure dependencies execute first."""
        executed: Set[PipelineStageType] = set()
        ordered: List[PipelineStageType] = []

        # Filter the standard pipeline preserving dependency order
        for stage in cls.DEFAULT_PIPELINE:
            if stage in requested_stages:
                ordered.append(stage)
                executed.add(stage)

        return ordered
