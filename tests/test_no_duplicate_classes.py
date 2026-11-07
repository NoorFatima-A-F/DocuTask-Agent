"""No two top-level classes in app/ share a name (e.g. the old pair of ``JobState`` enums)."""

from __future__ import annotations

import ast
from collections import defaultdict
from pathlib import Path

APP = Path(__file__).resolve().parent.parent / "app"


def test_top_level_class_names_are_unique() -> None:
    seen: dict[str, list[str]] = defaultdict(list)
    for path in APP.rglob("*.py"):
        for node in ast.parse(path.read_text("utf-8")).body:
            if isinstance(node, ast.ClassDef):
                seen[node.name].append(path.relative_to(APP.parent).as_posix())
    duplicates = {name: files for name, files in seen.items() if len(files) > 1}
    assert not duplicates, duplicates
