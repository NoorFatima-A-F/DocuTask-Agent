import os
import re
from dataclasses import dataclass
from typing import List

DEBT_TAG_REGEX = re.compile(r"#\s*DEBT\((?P<debt_id>DEBT-\d+)\):\s*(?P<description>.*)", re.IGNORECASE)

@dataclass(frozen=True)
class CodebaseDebtItem:
    debt_id: str
    description: str
    file_path: str
    line_number: int

class TechnicalDebtTracker:
    @staticmethod
    def scan_codebase(base_dir: str = ".") -> List[CodebaseDebtItem]:
        items = []
        for root, _, files in os.walk(base_dir):
            if ".git" in root or "__pycache__" in root or "venv" in root:
                continue
            for f in files:
                if f.endswith((".py", ".md", ".yaml", ".yml")):
                    full = os.path.join(root, f)
                    try:
                        with open(full, "r", encoding="utf-8") as source:
                            for lineno, line in enumerate(source, start=1):
                                m = DEBT_TAG_REGEX.search(line)
                                if m:
                                    items.append(CodebaseDebtItem(
                                        debt_id=m.group("debt_id"),
                                        description=m.group("description").strip(),
                                        file_path=os.path.relpath(full, base_dir),
                                        line_number=lineno
                                    ))
                    except Exception:
                        pass
        return items

if __name__ == "__main__":
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    found = TechnicalDebtTracker.scan_codebase(root)
    print(f"Scanned technical debt items: {len(found)}")
