"""Workflow DSL Parser and Compiler.

Compiles declarative YAML/JSON workflow specifications into executable WorkflowDefinitions
and APDLE Dynamic DAG tasks.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from app.platform.workflow.workflow_graph import (
    WorkflowDefinition,
    WorkflowEdge,
    WorkflowNode,
)


@dataclass
class DSLStepSpec:
    name: str
    capability: str
    depends_on: List[str] = field(default_factory=list)
    config: Dict[str, Any] = field(default_factory=dict)
    retry_max: int = 2
    timeout_ms: float = 5000.0


@dataclass
class DSLWorkflowSpec:
    mission_id: str
    title: str
    steps: List[DSLStepSpec]
    retry_policy: Dict[str, Any] = field(default_factory=dict)
    reflection_enabled: bool = True
    governance_policies: List[str] = field(default_factory=list)


class DSLParser:
    @staticmethod
    def parse_dict(data: Dict[str, Any]) -> DSLWorkflowSpec:
        mission_id = data.get("mission_id", "dsl-mission-001")
        title = data.get("title", "Declarative Mission")
        steps_raw = data.get("steps", [])

        steps: List[DSLStepSpec] = []
        for i, s in enumerate(steps_raw):
            if isinstance(s, str):
                steps.append(DSLStepSpec(name=f"step_{i+1}_{s}", capability=s))
            elif isinstance(s, dict):
                steps.append(
                    DSLStepSpec(
                        name=s.get("name", f"step_{i+1}"),
                        capability=s.get("capability", "general"),
                        depends_on=s.get("depends_on", []),
                        config=s.get("config", {}),
                        retry_max=s.get("retry_max", 2),
                        timeout_ms=s.get("timeout_ms", 5000.0),
                    )
                )

        return DSLWorkflowSpec(
            mission_id=mission_id,
            title=title,
            steps=steps,
            retry_policy=data.get("retry_policy", {"max": 3}),
            reflection_enabled=data.get("reflection", True),
            governance_policies=data.get("policies", ["soc2_standard"]),
        )


class DSLCompiler:
    @staticmethod
    def compile_to_workflow_definition(spec: DSLWorkflowSpec) -> WorkflowDefinition:
        wf = WorkflowDefinition(
            workflow_id=spec.mission_id,
            name=spec.title,
            description=f"Compiled DSL workflow with {len(spec.steps)} steps",
        )

        for i, step in enumerate(spec.steps):
            node = WorkflowNode(
                node_id=step.name,
                capability_name=step.capability,
                label=step.name.replace("_", " ").title(),
                config=step.config,
                position={"x": i * 180.0, "y": 100.0},
            )
            wf.nodes[step.name] = node

            # Link dependencies or chain linearly
            if step.depends_on:
                for dep in step.depends_on:
                    wf.edges.append(
                        WorkflowEdge(
                            edge_id=f"edge_{dep}_to_{step.name}",
                            source_node_id=dep,
                            target_node_id=step.name,
                        )
                    )
            elif i > 0:
                prev_step = spec.steps[i - 1]
                wf.edges.append(
                    WorkflowEdge(
                        edge_id=f"edge_{prev_step.name}_to_{step.name}",
                        source_node_id=prev_step.name,
                        target_node_id=step.name,
                    )
                )

        return wf
