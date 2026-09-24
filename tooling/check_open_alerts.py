import subprocess
import json

cmd = [r"C:\Program Files\GitHub CLI\gh.exe", "api", "/repos/NoorFatima-A-F/DocuTask-Agent/code-scanning/alerts?state=open", "--paginate"]
res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
alerts = json.loads(res.stdout)
print(f"Total open alerts: {len(alerts)}")
for a in alerts:
    num = a.get("number")
    rule = a.get("rule", {}).get("id")
    loc = a.get("most_recent_instance", {}).get("location", {})
    path = loc.get("path")
    line = loc.get("start_line")
    print(f"#{num} | {rule} | {path}:{line}")
