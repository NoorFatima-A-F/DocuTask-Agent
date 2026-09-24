"""
PostgreSQL / SQL-compatible Persistent Context Store.
Uses relational tables with JSONB fields for transactional integrity and durable checkpoint histories.
"""

import json
from typing import Any, Dict, List, Optional
from app.agents.runtime.context_store.context_store import ContextStore
from app.agents.runtime.runtime_context import RuntimeContext


class PostgresContextStore(ContextStore):
    """
    Relational SQL / Postgres Context Store.
    Operates over an async database session or executor that supports query execution.
    """

    DDL_STATEMENTS = [
        """
        CREATE TABLE IF NOT EXISTS runtime_contexts (
            runtime_id VARCHAR(128) PRIMARY KEY,
            tenant_id VARCHAR(128) NOT NULL,
            workspace_id VARCHAR(128) NOT NULL,
            context_data JSON NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS runtime_checkpoints (
            runtime_id VARCHAR(128) NOT NULL,
            version INTEGER NOT NULL,
            state_snapshot JSON NOT NULL,
            context_metadata JSON,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (runtime_id, version)
        );
        """
    ]

    def __init__(self, db_executor: Any) -> None:
        """
        db_executor is an async interface with:
          - execute(query: str, params: tuple)
          - fetch_one(query: str, params: tuple) -> Optional[dict/tuple]
          - fetch_all(query: str, params: tuple) -> List[dict/tuple]
        """
        self.db = db_executor

    async def initialize_schema(self) -> None:
        for stmt in self.DDL_STATEMENTS:
            await self.db.execute(stmt, ())

    async def save_context(self, context: RuntimeContext, ttl_seconds: Optional[int] = None) -> None:
        raw_json = context.model_dump_json()
        query = """
        INSERT INTO runtime_contexts (runtime_id, tenant_id, workspace_id, context_data)
        VALUES (:runtime_id, :tenant_id, :workspace_id, :context_data)
        ON CONFLICT (runtime_id) DO UPDATE SET
            tenant_id = EXCLUDED.tenant_id,
            workspace_id = EXCLUDED.workspace_id,
            context_data = EXCLUDED.context_data,
            updated_at = CURRENT_TIMESTAMP;
        """
        params = {
            "runtime_id": context.runtime_id,
            "tenant_id": context.tenant_id,
            "workspace_id": context.workspace_id,
            "context_data": raw_json,
        }
        await self.db.execute(query, params)

    async def load_context(self, runtime_id: str) -> Optional[RuntimeContext]:
        query = "SELECT context_data FROM runtime_contexts WHERE runtime_id = :runtime_id;"
        row = await self.db.fetch_one(query, {"runtime_id": runtime_id})
        if not row:
            return None
        data = row[0] if isinstance(row, (list, tuple)) else row.get("context_data")
        if isinstance(data, str):
            data = json.loads(data)
        return RuntimeContext(**data)

    async def checkpoint_context(
        self,
        runtime_id: str,
        state_snapshot: Dict[str, Any],
        expected_version: Optional[int] = None,
    ) -> int:
        query_ver = "SELECT MAX(version) FROM runtime_checkpoints WHERE runtime_id = :runtime_id;"
        row = await self.db.fetch_one(query_ver, {"runtime_id": runtime_id})
        current_ver = (row[0] if isinstance(row, (list, tuple)) else (row.get("max") if row else None)) or 0

        if expected_version is not None and current_ver != expected_version:
            raise ValueError(
                f"Concurrency conflict: expected version {expected_version} but current is {current_ver}"
            )

        next_ver = current_ver + 1
        ctx = await self.load_context(runtime_id)
        metadata = ctx.model_dump() if ctx else {}

        query_ins = """
        INSERT INTO runtime_checkpoints (runtime_id, version, state_snapshot, context_metadata)
        VALUES (:runtime_id, :version, :state_snapshot, :context_metadata);
        """
        params = {
            "runtime_id": runtime_id,
            "version": next_ver,
            "state_snapshot": json.dumps(state_snapshot),
            "context_metadata": json.dumps(metadata),
        }
        await self.db.execute(query_ins, params)
        return next_ver

    async def restore_context(
        self,
        runtime_id: str,
        version: Optional[int] = None,
    ) -> Optional[Dict[str, Any]]:
        if version is None:
            query = """
            SELECT state_snapshot FROM runtime_checkpoints
            WHERE runtime_id = :runtime_id
            ORDER BY version DESC LIMIT 1;
            """
            params = {"runtime_id": runtime_id}
        else:
            query = """
            SELECT state_snapshot FROM runtime_checkpoints
            WHERE runtime_id = :runtime_id AND version = :version;
            """
            params = {"runtime_id": runtime_id, "version": version}

        row = await self.db.fetch_one(query, params)
        if not row:
            return None
        snapshot = row[0] if isinstance(row, (list, tuple)) else row.get("state_snapshot")
        if isinstance(snapshot, str):
            snapshot = json.loads(snapshot)
        return snapshot

    async def list_checkpoints(self, runtime_id: str) -> List[int]:
        query = "SELECT version FROM runtime_checkpoints WHERE runtime_id = :runtime_id ORDER BY version ASC;"
        rows = await self.db.fetch_all(query, {"runtime_id": runtime_id})
        versions = []
        for r in rows:
            v = r[0] if isinstance(r, (list, tuple)) else r.get("version")
            versions.append(int(v))
        return versions

    async def delete_context(self, runtime_id: str) -> bool:
        del_chk = "DELETE FROM runtime_checkpoints WHERE runtime_id = :runtime_id;"
        del_ctx = "DELETE FROM runtime_contexts WHERE runtime_id = :runtime_id;"
        await self.db.execute(del_chk, {"runtime_id": runtime_id})
        await self.db.execute(del_ctx, {"runtime_id": runtime_id})
        return True
