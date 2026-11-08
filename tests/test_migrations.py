"""Alembic migrations apply cleanly to an empty SQLite database and match the failure-record columns."""

from __future__ import annotations

import sqlite3
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


def test_alembic_upgrade_head_and_downgrade(tmp_path: Path) -> None:
    db = tmp_path / "m.db"
    env = {"DATABASE_URL": f"sqlite+aiosqlite:///{db.as_posix()}", "ENVIRONMENT": "test", "PATH": ""}
    import os

    env = {**os.environ, **env}
    up = subprocess.run(
        [sys.executable, "-m", "alembic", "upgrade", "head"], cwd=REPO, env=env, capture_output=True, text=True
    )
    assert up.returncode == 0, up.stderr[-2000:]
    cols = {r[1]: r for r in sqlite3.connect(db).execute("PRAGMA table_info(ai_extractions)")}
    assert {"status", "error_code", "error_message"} <= cols.keys()
    assert cols["structured_json"][3] == 0  # notnull flag off
    assert cols["confidence"][3] == 0
    tables = {r[0] for r in sqlite3.connect(db).execute("SELECT name FROM sqlite_master WHERE type='table'")}
    assert "review_events" in tables

    down = subprocess.run(
        [sys.executable, "-m", "alembic", "downgrade", "006_add_user_roles_and_verified"],
        cwd=REPO,
        env=env,
        capture_output=True,
        text=True,
    )
    assert down.returncode == 0, down.stderr[-2000:]


def test_migrations_match_the_models(tmp_path: Path) -> None:
    """`alembic upgrade head` produces exactly the schema the ORM models declare (no drift)."""
    import os

    from alembic.autogenerate import compare_metadata
    from alembic.migration import MigrationContext
    from sqlalchemy import create_engine

    from app.models import Base

    db = tmp_path / "drift.db"
    env = {**os.environ, "DATABASE_URL": f"sqlite+aiosqlite:///{db.as_posix()}", "ENVIRONMENT": "test"}
    up = subprocess.run(
        [sys.executable, "-m", "alembic", "upgrade", "head"], cwd=REPO, env=env, capture_output=True, text=True
    )
    assert up.returncode == 0, up.stderr[-2000:]
    engine = create_engine(f"sqlite:///{db.as_posix()}")
    with engine.connect() as conn:
        diff = compare_metadata(MigrationContext.configure(conn, opts={"compare_type": False}), Base.metadata)
    engine.dispose()
    assert diff == [], diff
