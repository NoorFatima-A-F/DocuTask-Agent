"""
Flamegraph & Collapsed Stack Generator.

Converts sampled call stacks into collapsed text format and hierarchical JSON trees
for interactive flamegraph rendering.
"""

from __future__ import annotations

import logging
from typing import Dict, List
from pydantic import BaseModel, Field

from app.infrastructure.observability.profiling.cpu import CPUProfileSample

logger = logging.getLogger("infrastructure.observability.profiling.flamegraphs")


class FlamegraphNode(BaseModel):
    """Hierarchical node in an interactive flamegraph visualization."""
    name: str
    value: float = 0.0
    children: List[FlamegraphNode] = Field(default_factory=list)


class FlamegraphGenerator:
    """
    Generates collapsed stack formats and hierarchical flamegraph JSON.
    """

    @staticmethod
    def generate_collapsed_stacks(samples: List[CPUProfileSample]) -> List[str]:
        """Convert samples into folded stack lines (e.g. 'root;parent;func 10')."""
        stack_counts: Dict[str, float] = {}

        for sample in samples:
            if not sample.frames:
                continue
            stack_str = ";".join(f.function_name for f in sample.frames)
            stack_counts[stack_str] = stack_counts.get(stack_str, 0.0) + sample.duration_ms

        lines = [f"{k} {int(v)}" for k, v in sorted(stack_counts.items())]
        return lines

    @classmethod
    def generate_tree(cls, samples: List[CPUProfileSample]) -> FlamegraphNode:
        """Convert samples into nested FlamegraphNode tree."""
        root = FlamegraphNode(name="root", value=0.0)

        for sample in samples:
            if not sample.frames:
                continue

            root.value += sample.duration_ms
            current = root

            for frame in sample.frames:
                fn_name = frame.function_name
                child = next((c for c in current.children if c.name == fn_name), None)
                if not child:
                    child = FlamegraphNode(name=fn_name, value=0.0)
                    current.children.append(child)
                child.value += sample.duration_ms
                current = child

        return root
