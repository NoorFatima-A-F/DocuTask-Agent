"""Static import-reachability report for the ``app`` package.

Walks the AST import graph starting from one or more entry modules (default:
``app.main`` plus the Celery worker entry point when it exists) and reports which
modules under ``app/`` are reachable and which are not.

Only static ``import``/``from ... import`` statements are followed (including those
inside functions). Dynamic imports (``importlib``) are not detected.

Usage::

    python tooling/reachability.py                 # summary
    python tooling/reachability.py --list unreachable
    python tooling/reachability.py --json report.json
"""

from __future__ import annotations

import argparse
import ast
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PACKAGE = "app"
DEFAULT_ENTRIES = ["app.main", "app.jobs.celery_app", "app.jobs.tasks"]


def discover_modules(root: Path) -> dict[str, Path]:
    """Map dotted module name -> file path for every .py file under ``app/``."""
    modules: dict[str, Path] = {}
    for path in (root / PACKAGE).rglob("*.py"):
        if "__pycache__" in path.parts:
            continue
        rel = path.relative_to(root).with_suffix("")
        parts = list(rel.parts)
        if parts[-1] == "__init__":
            parts = parts[:-1]
        modules[".".join(parts)] = path
    return modules


def _resolve_relative(module: str, is_pkg: bool, level: int, target: str | None) -> str:
    base = module.split(".")
    if not is_pkg:
        base = base[:-1]
    if level > 1:
        base = base[: len(base) - (level - 1)]
    if target:
        base = base + target.split(".")
    return ".".join(base)


def imports_of(name: str, path: Path, modules: dict[str, Path]) -> set[str]:
    """Return the set of in-package modules imported by ``name``."""
    try:
        tree = ast.parse(path.read_text(encoding="utf-8", errors="replace"))
    except SyntaxError:
        return set()
    is_pkg = path.name == "__init__.py"
    found: set[str] = set()

    def add(candidate: str) -> None:
        # Importing ``a.b.c`` also executes ``a`` and ``a.b`` packages.
        parts = candidate.split(".")
        for i in range(1, len(parts) + 1):
            prefix = ".".join(parts[:i])
            if prefix in modules:
                found.add(prefix)

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.split(".")[0] == PACKAGE:
                    add(alias.name)
        elif isinstance(node, ast.ImportFrom):
            base = _resolve_relative(name, is_pkg, node.level, node.module) if node.level else node.module or ""
            if base.split(".")[0] != PACKAGE:
                continue
            add(base)
            for alias in node.names:
                sub = f"{base}.{alias.name}"
                if sub in modules:
                    add(sub)
    found.discard(name)
    return found


def reachable_from(entries: list[str], modules: dict[str, Path]) -> set[str]:
    seen: set[str] = set()
    stack = [e for e in entries if e in modules]
    while stack:
        mod = stack.pop()
        if mod in seen:
            continue
        seen.add(mod)
        stack.extend(imports_of(mod, modules[mod], modules) - seen)
    return seen


def loc(path: Path) -> int:
    try:
        return sum(1 for _ in path.open(encoding="utf-8", errors="replace"))
    except OSError:
        return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--entry", action="append", help="Entry module (repeatable)")
    parser.add_argument("--list", choices=["reachable", "unreachable"], help="Print module list")
    parser.add_argument("--packages", action="store_true", help="Summarise by top-level package")
    parser.add_argument("--json", type=Path, help="Write full report as JSON")
    args = parser.parse_args(argv)

    modules = discover_modules(REPO_ROOT)
    entries = args.entry or DEFAULT_ENTRIES
    reach = reachable_from(entries, modules)
    unreach = set(modules) - reach

    total_loc = sum(loc(p) for p in modules.values())
    reach_loc = sum(loc(modules[m]) for m in reach)
    pct_mod = 100.0 * len(reach) / max(len(modules), 1)
    pct_loc = 100.0 * reach_loc / max(total_loc, 1)

    print(f"entries: {', '.join(e for e in entries if e in modules)}")
    print(f"modules: {len(reach)}/{len(modules)} reachable ({pct_mod:.1f}%)")
    print(f"lines:   {reach_loc}/{total_loc} reachable ({pct_loc:.1f}%)")

    if args.packages:
        by_pkg: dict[str, list[int]] = {}
        for mod in modules:
            parts = mod.split(".")
            pkg = ".".join(parts[:2]) if len(parts) > 1 else parts[0]
            stats = by_pkg.setdefault(pkg, [0, 0])
            stats[0] += 1
            stats[1] += mod in reach
        for pkg, (n, r) in sorted(by_pkg.items(), key=lambda kv: (kv[1][1] > 0, kv[0])):
            print(f"  {pkg:60s} {r:5d}/{n:<5d}")

    if args.list:
        for mod in sorted(reach if args.list == "reachable" else unreach):
            print(mod)

    if args.json:
        args.json.write_text(
            json.dumps(
                {
                    "entries": entries,
                    "reachable": sorted(reach),
                    "unreachable": sorted(unreach),
                    "module_pct": round(pct_mod, 2),
                    "loc_pct": round(pct_loc, 2),
                },
                indent=2,
            ),
            encoding="utf-8",
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
