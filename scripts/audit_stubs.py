"""
Audit Stub Report Generator.
"""
import os
import re
import json

os.makedirs("docs/audit", exist_ok=True)

RUNTIME_DIR = "app/agents/runtime"
STUB_PATTERNS = [
    r"\bpass\b",
    r"\bTODO\b",
    r"\bFIXME\b",
    r"\bNotImplementedError\b",
    r"simulation",
    r"mock",
    r"default_handler",
    r"fake",
]

findings = []

for root, dirs, files in os.walk(RUNTIME_DIR):
    for file in files:
        if file.endswith(".py"):
            path = os.path.join(root, file)
            with open(path, "r", encoding="utf-8") as f:
                lines = f.readlines()
            for idx, line in enumerate(lines, start=1):
                for pat in STUB_PATTERNS:
                    if re.search(pat, line, re.IGNORECASE):
                        is_abstract = "raise NotImplementedError" in line and ("abstractmethod" in "".join(lines[max(0, idx-4):idx]))
                        is_exc_pass = "pass" in line and ("class " in "".join(lines[max(0, idx-3):idx])) and ("Error" in "".join(lines[max(0, idx-3):idx]) or "Exception" in "".join(lines[max(0, idx-3):idx]))
                        severity = "critical" if not (is_abstract or is_exc_pass) else "low"
                        findings.append({
                            "module": os.path.relpath(path, RUNTIME_DIR).replace("\\", "/"),
                            "line": idx,
                            "code": line.strip(),
                            "pattern": pat,
                            "severity": severity,
                            "is_exception_or_abstract": is_abstract or is_exc_pass
                        })

print(f"Total findings: {len(findings)}")
critical_findings = [f for f in findings if f["severity"] == "critical"]
print(f"Critical findings: {len(critical_findings)}")

with open("docs/audit/runtime_stub_report.json", "w", encoding="utf-8") as f:
    json.dump(findings, f, indent=2)
print("Saved to docs/audit/runtime_stub_report.json")
