"""Report API surface metrics: path/operation counts and unauthenticated routes.

Two measurements:

* **static**: an operation is "protected" when its dependency tree contains one of the
  auth dependencies (``get_current_user`` and friends).
* **live**: every parameter-free GET is called without credentials (5 s timeout each);
  we count how many return 200.

Usage::

    python tooling/api_metrics.py [--list] [--root PATH]
"""

from __future__ import annotations

import argparse
import asyncio
import os
import sys
import time
from pathlib import Path

AUTH_DEPENDENCY_NAMES = {
    "get_current_user",
    "get_current_active_user",
    "get_current_superuser",
    "get_current_admin_user",
    "require_reviewer",
    "require_admin",
    "require_roles",
    "role_checker",
    "RoleChecker",
}


def _dep_names(dependant) -> set[str]:  # type: ignore[no-untyped-def]
    names: set[str] = set()
    stack = [dependant]
    while stack:
        dep = stack.pop()
        call = getattr(dep, "call", None)
        if call is not None:
            names.add(getattr(call, "__name__", type(call).__name__))
        stack.extend(getattr(dep, "dependencies", []))
    return names


async def _probe(app, paths: list[str]) -> dict[str, int]:  # type: ignore[no-untyped-def]
    from httpx import ASGITransport, AsyncClient  # noqa: PLC0415

    results: dict[str, int] = {}
    transport = ASGITransport(app=app, raise_app_exceptions=False)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        for path in paths:
            try:
                resp = await asyncio.wait_for(client.get(path), timeout=5)
                results[path] = resp.status_code
            except Exception:  # noqa: BLE001 - metrics script: record and continue
                results[path] = -1
    return results


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--list", action="store_true", help="List unprotected operations")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument("--no-live", action="store_true", help="Skip live GET probing")
    args = parser.parse_args(argv)

    sys.path.insert(0, str(args.root))
    os.chdir(args.root)
    os.environ.setdefault("ENVIRONMENT", "test")

    t0 = time.perf_counter()
    from app.main import app  # noqa: PLC0415

    import_s = time.perf_counter() - t0
    from fastapi.routing import APIRoute  # noqa: PLC0415

    schema = app.openapi()
    paths = schema.get("paths", {})
    ops = [(m.upper(), p) for p, item in paths.items() for m in item if m in {"get", "post", "put", "patch", "delete"}]

    import fastapi.routing

    # FastAPI >= 0.16x nests included routers; iter_route_contexts walks both layouts.
    iter_contexts = getattr(fastapi.routing, "iter_route_contexts", None)
    routes = (
        [(c.path, c.methods, c.route) for c in iter_contexts(app.routes)]
        if iter_contexts
        else [(r.path, getattr(r, "methods", None), r) for r in app.routes]
    )
    unprotected: list[tuple[str, str]] = []
    for path, methods, route in routes:
        if not isinstance(route, APIRoute) or not route.include_in_schema:
            continue
        protected = bool(_dep_names(route.dependant) & AUTH_DEPENDENCY_NAMES)
        if not protected:
            for method in sorted(methods or []):
                unprotected.append((method, path))

    print(f"app_import_seconds: {import_s:.2f}")
    print(f"api_paths: {len(paths)}")
    print(f"api_operations: {len(ops)}")
    print(f"operations_without_auth_dependency: {len(unprotected)}")
    files = {
        Path(sys.modules[route.endpoint.__module__].__file__ or "").as_posix()
        for path, methods, route in routes
        if isinstance(route, APIRoute) and (sorted(methods or [""])[0], path) in set(unprotected)
    }
    print(f"route_modules_with_unprotected_operations: {len(files)}")

    if not args.no_live:
        get_paths = sorted({p for m, p in ops if m == "GET" and "{" not in p})
        codes = asyncio.run(_probe(app, get_paths))
        ok = [p for p, c in codes.items() if c == 200]
        print(f"param_free_GET: {len(get_paths)}, returning 200 without token: {len(ok)}")

    if args.list:
        for method, path in unprotected:
            print(f"  {method:6s} {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
