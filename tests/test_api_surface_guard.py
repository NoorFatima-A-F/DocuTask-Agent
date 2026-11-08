"""Guards for the remediated API surface and code size.

* at most 40 operations;
* every route outside an explicit public allowlist rejects unauthenticated calls with 401;
* app/ stays under 10k lines.
"""

from __future__ import annotations

import re
from pathlib import Path

import fastapi.routing
import pytest
from fastapi.routing import APIRoute
from httpx import AsyncClient

from app.core.config import settings
from app.main import app

MAX_OPERATIONS = 40
MAX_APP_LINES = 10_000
PUBLIC = {
    ("GET", "/healthz"),
    ("GET", "/readyz"),
    ("POST", f"{settings.API_V1_STR}/auth/login"),
    ("POST", f"{settings.API_V1_STR}/auth/register"),
    ("POST", f"{settings.API_V1_STR}/auth/refresh"),
}
DUMMY = "00000000-0000-0000-0000-000000000001"
APP_DIR = Path(__file__).resolve().parent.parent / "app"


def _operations() -> list[tuple[str, str]]:
    """Every API operation: documented routes plus hidden aliases under the API prefix.

    The SPA shell routes (``/``, ``/upload`` ...) only serve static HTML and are public by design.
    """
    ops = []
    for path, methods, in_schema in _api_routes():
        if in_schema or path.startswith(settings.API_V1_STR):
            ops.extend((method, path) for method in sorted(methods))
    return ops


def _api_routes() -> list[tuple[str, frozenset[str], bool]]:
    """(path, methods, include_in_schema) for every APIRoute, however the app nests routers.

    FastAPI >= 0.16x keeps included routers nested, so ``app.routes`` no longer lists their
    routes; ``iter_route_contexts`` walks them with the full path. Older FastAPI flattens them.
    """
    iter_contexts = getattr(fastapi.routing, "iter_route_contexts", None)
    if iter_contexts is not None:
        return [
            (c.path, frozenset(c.methods or ()), c.route.include_in_schema)
            for c in iter_contexts(app.routes)
            if isinstance(c.route, APIRoute)
        ]
    return [(r.path, frozenset(r.methods or ()), r.include_in_schema) for r in app.routes if isinstance(r, APIRoute)]


def _schema_operations() -> set[tuple[str, str]]:
    return {
        (m.upper(), p)
        for p, item in app.openapi()["paths"].items()
        for m in item
        if m in {"get", "post", "put", "patch", "delete"}
    }


def test_operation_budget() -> None:
    schema_ops = [
        (m, p) for p, item in app.openapi()["paths"].items() for m in item if m in {"get", "post", "put", "patch", "delete"}
    ]
    assert len(schema_ops) <= MAX_OPERATIONS, f"{len(schema_ops)} operations > {MAX_OPERATIONS}"


def test_public_allowlist_routes_exist() -> None:
    assert PUBLIC <= set(_operations())


def test_route_discovery_sees_every_documented_operation() -> None:
    """If route discovery silently finds nothing, the auth guard below would test nothing."""
    assert _schema_operations() <= set(_operations())


@pytest.mark.parametrize(("method", "path"), [op for op in _operations() if op not in PUBLIC])
async def test_non_public_route_requires_auth(client: AsyncClient, method: str, path: str) -> None:
    url = re.sub(r"\{[^}]+\}", DUMMY, path)
    kwargs = {"json": {}} if method in {"POST", "PUT", "PATCH"} else {}
    response = await client.request(method, url, **kwargs)
    assert response.status_code == 401, f"{method} {path} -> {response.status_code}"


def _python_files() -> list[Path]:
    return [p for p in APP_DIR.rglob("*.py") if "__pycache__" not in p.parts]


def test_app_size_budget() -> None:
    lines = sum(len(p.read_text("utf-8").splitlines()) for p in _python_files())
    assert lines < MAX_APP_LINES, f"app/ has {lines} lines"
