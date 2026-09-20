"""
Living Benchmark Observatory Models (Phase 90C)
==============================================
Data schemas for continuous benchmark version tracking, leaderboard positioning,
and dataset availability without data fabrication.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional


class BenchmarkStatus(str, Enum):
    ACTIVE = "ACTIVE"
    DATASET_UNAVAILABLE = "DATASET_UNAVAILABLE"
    NOT_COLLECTED = "NOT_COLLECTED"
    DEPRECATED = "DEPRECATED"
    RULE_CHANGE = "RULE_CHANGE"


@dataclass(frozen=True)
class BenchmarkDatasetRecord:
    """Status and version tracking for an external public benchmark."""
    benchmark_id: str
    benchmark_name: str
    version: str
    expected_sample_count: int
    expected_sha256: str
    status: BenchmarkStatus
    last_verified_utc: str
    primary_metric: str
    sota_reference_score: float
    notes: str = ""


@dataclass(frozen=True)
class LeaderboardEntry:
    """Historical or active leaderboard position."""
    rank: int
    model_name: str
    model_version: str
    score: float
    is_measured_locally: bool
    status_label: str
    submission_date_utc: str
