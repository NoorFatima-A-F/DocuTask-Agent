import sys, pathlib; p, c = sys.argv[1], sys.argv[2]; pathlib.Path(p).parent.mkdir(parents=True, exist_ok=True); pathlib.Path(p).write_text(c, encoding="utf-8"); print("[OK]", p)
