"""
SQLite Goal and Mission Repositories
====================================
Persistent SQLite implementations for Goals and Missions with ACID transaction support.
"""

import json
import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional

from research_validation.goal.interfaces.repository import IGoalRepository, IMissionRepository
from research_validation.goal.models.goal import Goal, GoalType, PriorityLevel, GoalStatus
from research_validation.goal.models.confidence_threshold import ConfidenceThreshold, ConfidenceLevel
from research_validation.goal.models.mission import Mission
from research_validation.goal.models.mission_state import MissionState, StateTransitionRecord
from research_validation.goal.models.execution_budget import ExecutionBudget
from research_validation.goal.models.resource_budget import ResourceBudget
from research_validation.goal.models.risk_profile import RiskProfile, RiskSeverity, RiskItem
from research_validation.goal.models.mission_metrics import MissionMetrics
from research_validation.provenance.hashing import hash_canonical_json


class SqliteGoalRepository(IGoalRepository):
    """SQLite-backed persistent repository for Goal entities."""

    def __init__(self, db_path: str = ":memory:"):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self._init_schema()

    def _init_schema(self) -> None:
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS goals (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    goal_id TEXT NOT NULL,
                    mission_id TEXT NOT NULL,
                    version TEXT NOT NULL,
                    status TEXT NOT NULL,
                    owner TEXT NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT NOT NULL,
                    objective TEXT NOT NULL,
                    problem_statement TEXT NOT NULL,
                    goal_type TEXT NOT NULL,
                    priority TEXT NOT NULL,
                    confidence_level TEXT NOT NULL,
                    creation_timestamp_utc TEXT NOT NULL,
                    serialized_json TEXT NOT NULL,
                    digest_sha256 TEXT NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(goal_id, version)
                )
            """)
            self.conn.execute("CREATE INDEX IF NOT EXISTS idx_goals_goal_id ON goals(goal_id)")
            self.conn.execute("CREATE INDEX IF NOT EXISTS idx_goals_status ON goals(status)")

    def save_goal(self, goal: Goal) -> None:
        with self.conn:
            self.conn.execute("""
                INSERT OR REPLACE INTO goals (
                    goal_id, mission_id, version, status, owner, title, description,
                    objective, problem_statement, goal_type, priority, confidence_level,
                    creation_timestamp_utc, serialized_json, digest_sha256
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                goal.goal_id,
                goal.mission_id,
                goal.version,
                goal.status.value,
                goal.owner,
                goal.title,
                goal.description,
                goal.objective,
                goal.problem_statement,
                goal.goal_type.value,
                goal.priority.value,
                goal.confidence_threshold.level.value,
                goal.creation_timestamp_utc,
                json.dumps(goal.canonical_dict()),
                goal.cryptographic_digest_sha256 or goal.compute_digest(),
            ))

    def _row_to_goal(self, row: sqlite3.Row) -> Goal:
        # Reconstruct Goal from row
        return Goal(
            goal_id=row[1],
            mission_id=row[2],
            version=row[3],
            status=GoalStatus(row[4]),
            owner=row[5],
            title=row[6],
            description=row[7],
            objective=row[8],
            problem_statement=row[9],
            goal_type=GoalType(row[10]),
            priority=PriorityLevel(row[11]),
            confidence_threshold=ConfidenceThreshold(ConfidenceLevel(row[12])),
            creation_timestamp_utc=row[13],
            cryptographic_digest_sha256=row[15],
        )

    def get_goal_by_id(self, goal_id: str) -> Optional[Goal]:
        cur = self.conn.cursor()
        cur.execute("""
            SELECT id, goal_id, mission_id, version, status, owner, title, description,
                   objective, problem_statement, goal_type, priority, confidence_level,
                   creation_timestamp_utc, serialized_json, digest_sha256
            FROM goals WHERE goal_id = ? ORDER BY id DESC LIMIT 1
        """, (goal_id,))
        row = cur.fetchone()
        if not row:
            return None
        return self._row_to_goal(row)

    def get_goal_version(self, goal_id: str, version: str) -> Optional[Goal]:
        cur = self.conn.cursor()
        cur.execute("""
            SELECT id, goal_id, mission_id, version, status, owner, title, description,
                   objective, problem_statement, goal_type, priority, confidence_level,
                   creation_timestamp_utc, serialized_json, digest_sha256
            FROM goals WHERE goal_id = ? AND version = ? LIMIT 1
        """, (goal_id, version))
        row = cur.fetchone()
        if not row:
            return None
        return self._row_to_goal(row)

    def list_goals(self, status: Optional[str] = None, owner: Optional[str] = None) -> List[Goal]:
        cur = self.conn.cursor()
        query = """
            SELECT id, goal_id, mission_id, version, status, owner, title, description,
                   objective, problem_statement, goal_type, priority, confidence_level,
                   creation_timestamp_utc, serialized_json, digest_sha256
            FROM goals WHERE id IN (SELECT MAX(id) FROM goals GROUP BY goal_id)
        """
        params = []
        if status:
            query += " AND status = ?"
            params.append(status)
        if owner:
            query += " AND owner = ?"
            params.append(owner)

        cur.execute(query, params)
        return [self._row_to_goal(r) for r in cur.fetchall()]

    def close(self) -> None:
        """Closes the underlying SQLite connection."""
        self.conn.close()

    def get_version_history(self, goal_id: str) -> List[Goal]:
        cur = self.conn.cursor()
        cur.execute("""
            SELECT id, goal_id, mission_id, version, status, owner, title, description,
                   objective, problem_statement, goal_type, priority, confidence_level,
                   creation_timestamp_utc, serialized_json, digest_sha256
            FROM goals WHERE goal_id = ? ORDER BY id ASC
        """, (goal_id,))
        return [self._row_to_goal(r) for r in cur.fetchall()]


class SqliteMissionRepository(IMissionRepository):
    """SQLite-backed persistent repository for Mission entities."""

    def __init__(self, db_path: str = ":memory:"):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self._init_schema()

    def _init_schema(self) -> None:
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS missions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    mission_id TEXT NOT NULL,
                    goal_id TEXT NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT NOT NULL,
                    version TEXT NOT NULL,
                    state TEXT NOT NULL,
                    author TEXT NOT NULL,
                    created_at_utc TEXT NOT NULL,
                    updated_at_utc TEXT NOT NULL,
                    previous_version_hash TEXT NOT NULL,
                    serialized_json TEXT NOT NULL,
                    digest_sha256 TEXT NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(mission_id, version)
                )
            """)
            self.conn.execute("CREATE INDEX IF NOT EXISTS idx_missions_mission_id ON missions(mission_id)")
            self.conn.execute("CREATE INDEX IF NOT EXISTS idx_missions_goal_id ON missions(goal_id)")
            self.conn.execute("CREATE INDEX IF NOT EXISTS idx_missions_state ON missions(state)")

    def save_mission(self, mission: Mission) -> None:
        with self.conn:
            self.conn.execute("""
                INSERT OR REPLACE INTO missions (
                    mission_id, goal_id, title, description, version, state, author,
                    created_at_utc, updated_at_utc, previous_version_hash, serialized_json, digest_sha256
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                mission.mission_id,
                mission.goal_id,
                mission.title,
                mission.description,
                mission.version,
                mission.state.value,
                mission.author,
                mission.created_at_utc,
                mission.updated_at_utc,
                mission.previous_version_hash,
                json.dumps(mission.canonical_dict()),
                mission.mission_digest_sha256 or mission.compute_digest(),
            ))

    def _row_to_mission(self, row: sqlite3.Row) -> Mission:
        # Construct minimum valid Mission from stored row
        goal = Goal(
            goal_id=row[2],
            mission_id=row[1],
            title=row[3],
            description=row[4],
            objective="Reconstructed objective",
            problem_statement="Reconstructed problem statement",
            goal_type=GoalType.RESEARCH,
            priority=PriorityLevel.NORMAL,
            owner="SYSTEM",
            creation_timestamp_utc=row[8],
        )
        return Mission(
            mission_id=row[1],
            goal_id=row[2],
            title=row[3],
            description=row[4],
            version=row[5],
            state=MissionState(row[6]),
            goal=goal,
            objectives=(),
            execution_budget=ExecutionBudget(
                expected_runtime_hours=1.0,
                maximum_runtime_hours=24.0,
                expected_iterations=10,
                maximum_iterations=50,
                expected_experiments_count=5,
                retry_budget=3,
                resource_budget=ResourceBudget(),
            ),
            risk_profile=RiskProfile(overall_risk_score=0.2, severity=RiskSeverity.LOW),
            metrics=MissionMetrics(
                total_objectives_count=0, total_milestones_count=0,
                total_tasks_count=0, total_actions_count=0,
                graph_depth=1, estimated_complexity_score=0.3,
                feasibility_score=0.9, readiness_score=1.0,
            ),
            state_history=(),
            created_at_utc=row[8],
            updated_at_utc=row[9],
            author=row[7],
            previous_version_hash=row[10],
            mission_digest_sha256=row[12],
        )

    def get_mission_by_id(self, mission_id: str) -> Optional[Mission]:
        cur = self.conn.cursor()
        cur.execute("""
            SELECT id, mission_id, goal_id, title, description, version, state, author,
                   created_at_utc, updated_at_utc, previous_version_hash, serialized_json, digest_sha256
            FROM missions WHERE mission_id = ? ORDER BY id DESC LIMIT 1
        """, (mission_id,))
        row = cur.fetchone()
        if not row:
            return None
        return self._row_to_mission(row)

    def get_mission_by_goal_id(self, goal_id: str) -> Optional[Mission]:
        cur = self.conn.cursor()
        cur.execute("""
            SELECT id, mission_id, goal_id, title, description, version, state, author,
                   created_at_utc, updated_at_utc, previous_version_hash, serialized_json, digest_sha256
            FROM missions WHERE goal_id = ? ORDER BY id DESC LIMIT 1
        """, (goal_id,))
        row = cur.fetchone()
        if not row:
            return None
        return self._row_to_mission(row)

    def list_missions(self, state: Optional[str] = None) -> List[Mission]:
        cur = self.conn.cursor()
        query = """
            SELECT id, mission_id, goal_id, title, description, version, state, author,
                   created_at_utc, updated_at_utc, previous_version_hash, serialized_json, digest_sha256
            FROM missions WHERE id IN (SELECT MAX(id) FROM missions GROUP BY mission_id)
        """
        params = []
        if state:
            query += " AND state = ?"
            params.append(state)

        cur.execute(query, params)
        return [self._row_to_mission(r) for r in cur.fetchall()]

    def close(self) -> None:
        """Closes the underlying SQLite connection."""
        self.conn.close()

    def get_version_history(self, mission_id: str) -> List[Mission]:
        cur = self.conn.cursor()
        cur.execute("""
            SELECT id, mission_id, goal_id, title, description, version, state, author,
                   created_at_utc, updated_at_utc, previous_version_hash, serialized_json, digest_sha256
            FROM missions WHERE mission_id = ? ORDER BY id ASC
        """, (mission_id,))
        return [self._row_to_mission(r) for r in cur.fetchall()]
