"""
Evidence Provenance & Scientific Lineage Framework
Module: provenance_schema.py

Provides formal schemas for:
1. W3C PROV Specification (PROV-DM, PROV-O)
2. OpenLineage Standard (Jobs, Runs, Datasets, Facets, RunEvents)
"""

from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from research_validation.provenance.provenance_models import (
    ProvActivity, ProvAgent, ProvEntity, ProvRelationType
)


# ============================================================================
# 1. W3C PROV Document Schema
# ============================================================================

@dataclass
class ProvRelation:
    """W3C PROV Relationship statement."""
    relation_type: ProvRelationType
    source_id: str
    target_id: str
    attributes: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ProvDocument:
    """Complete W3C PROV Document containing Entities, Activities, Agents, and Relations."""
    document_id: str
    namespaces: Dict[str, str] = field(default_factory=lambda: {
        "prov": "http://www.w3.org/ns/prov#",
        "xsd": "http://www.w3.org/2001/XMLSchema#",
        "rvisf": "https://deepmind.google/rvisf/provenance#"
    })
    entities: Dict[str, ProvEntity] = field(default_factory=dict)
    activities: Dict[str, ProvActivity] = field(default_factory=dict)
    agents: Dict[str, ProvAgent] = field(default_factory=dict)
    relations: List[ProvRelation] = field(default_factory=list)

    def add_entity(self, entity: ProvEntity) -> None:
        self.entities[entity.entity_id] = entity

    def add_activity(self, activity: ProvActivity) -> None:
        self.activities[activity.activity_id] = activity

    def add_agent(self, agent: ProvAgent) -> None:
        self.agents[agent.agent_id] = agent

    def add_relation(self, relation: ProvRelation) -> None:
        self.relations.append(relation)


# ============================================================================
# 2. OpenLineage Specification Schema
# ============================================================================

class OpenLineageEventType(str, Enum):
    START = "START"
    RUNNING = "RUNNING"
    COMPLETE = "COMPLETE"
    ABORT = "ABORT"
    FAIL = "FAIL"
    OTHER = "OTHER"


@dataclass
class OpenLineageJob:
    """OpenLineage Job representation."""
    namespace: str
    name: str
    facets: Dict[str, Any] = field(default_factory=dict)


@dataclass
class OpenLineageRun:
    """OpenLineage Run representation."""
    runId: str
    facets: Dict[str, Any] = field(default_factory=dict)


@dataclass
class OpenLineageDataset:
    """OpenLineage Dataset representation."""
    namespace: str
    name: str
    facets: Dict[str, Any] = field(default_factory=dict)


@dataclass
class OpenLineageInputDataset:
    dataset: OpenLineageDataset
    inputFacets: Dict[str, Any] = field(default_factory=dict)


@dataclass
class OpenLineageOutputDataset:
    dataset: OpenLineageDataset
    outputFacets: Dict[str, Any] = field(default_factory=dict)


@dataclass
class OpenLineageRunEvent:
    """OpenLineage standard RunEvent JSON structure."""
    eventType: OpenLineageEventType
    eventTime: str  # ISO-8601 formatted string
    run: OpenLineageRun
    job: OpenLineageJob
    inputs: List[OpenLineageInputDataset] = field(default_factory=list)
    outputs: List[OpenLineageOutputDataset] = field(default_factory=list)
    producer: str = "https://github.com/google/rvisf-provenance"
    schemaURL: str = "https://openlineage.io/spec/1-0-5/OpenLineage.json"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "eventType": self.eventType.value,
            "eventTime": self.eventTime,
            "run": {
                "runId": self.run.runId,
                "facets": self.run.facets
            },
            "job": {
                "namespace": self.job.namespace,
                "name": self.job.name,
                "facets": self.job.facets
            },
            "inputs": [
                {
                    "namespace": i.dataset.namespace,
                    "name": i.dataset.name,
                    "facets": i.dataset.facets,
                    "inputFacets": i.inputFacets
                }
                for i in self.inputs
            ],
            "outputs": [
                {
                    "namespace": o.dataset.namespace,
                    "name": o.dataset.name,
                    "facets": o.dataset.facets,
                    "outputFacets": o.outputFacets
                }
                for o in self.outputs
            ],
            "producer": self.producer,
            "schemaURL": self.schemaURL
        }
