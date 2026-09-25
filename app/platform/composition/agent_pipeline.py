"""Agent Pipeline Interface."""

from __future__ import annotations

from app.platform.composition.composition_engine import (
    AgentPipeline,
    CompositionEngine,
    CompositionStep,
    global_composition_engine,
)

__all__ = [
    "CompositionStep",
    "AgentPipeline",
    "CompositionEngine",
    "global_composition_engine",
]
