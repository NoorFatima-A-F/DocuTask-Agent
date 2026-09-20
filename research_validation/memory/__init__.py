"""
Scientific Memory Package (Phase 84C)
=====================================
"""

from research_validation.memory.experiment_memory import (
    ExperimentMemoryEntry, ExperimentMemoryStore
)
from research_validation.memory.failure_memory import (
    FailureCategory, FailureMemoryEntry, FailureMemoryStore
)
from research_validation.memory.success_memory import (
    SuccessMemoryEntry, SuccessMemoryStore
)
from research_validation.memory.regression_memory import (
    RegressionMemoryEntry, RegressionMemoryStore
)
from research_validation.memory.episodic_memory import (
    ResearchEpisode, EpisodicMemoryStore
)
from research_validation.memory.long_term_memory import (
    LongTermMemoryItem, LongTermMemoryStore
)
from research_validation.memory.memory_consolidation import (
    ConsolidationReport, ScientificMemoryConsolidator
)

__all__ = [
    "ExperimentMemoryEntry",
    "ExperimentMemoryStore",
    "FailureCategory",
    "FailureMemoryEntry",
    "FailureMemoryStore",
    "SuccessMemoryEntry",
    "SuccessMemoryStore",
    "RegressionMemoryEntry",
    "RegressionMemoryStore",
    "ResearchEpisode",
    "EpisodicMemoryStore",
    "LongTermMemoryItem",
    "LongTermMemoryStore",
    "ConsolidationReport",
    "ScientificMemoryConsolidator",
]
