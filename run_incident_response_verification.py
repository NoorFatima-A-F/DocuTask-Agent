"""Master Verification Runner for Phase 3H.3.6: Incident Response Automation & Self-Healing.

Executes all 13 verification subsystems:
1. Incident Management Architecture Verification
2. Multi-Signal Incident Detection Automation
3. Failure Classification & Severity Rating (SEV-1 to SEV-4)
4. Declarative Runbook Automation Engine
5. Self-Healing Execution & MTTR Benchmarking
6. Recovery Safety & Approval Policy Gatekeeper
7. Multi-Signal Incident Correlation (Causal Chain)
8. Operational Incident Knowledge Base
9. Automated Blameless Postmortem Generation
10. Incident Automation Security Audit
11. CI/CD Deployment Failure Verification Pipeline
12. Audit Manifest Evidence Generation (10 JSON Files)
13. Composite Quality Scoring & Autonomous Certification
"""

from __future__ import annotations

import io
import sys
from pathlib import Path

# Ensure UTF-8 output encoding on Windows consoles
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# Add workspace root to sys.path
WORKSPACE_ROOT = Path(__file__).resolve().parent
if str(WORKSPACE_ROOT) not in sys.path:
    sys.path.insert(0, str(WORKSPACE_ROOT))

from app.platform_verification.incident_response_automation.runtime.incident_automation_runtime import (
    IncidentAutomationRuntime,
)


def main() -> int:
    print("=" * 80)
    print("  PHASE 3H.3.6 - INCIDENT RESPONSE AUTOMATION & SELF-HEALING VERIFICATION")
    print("  DocuTask Agent Enterprise AIOps & Autonomous Recovery Framework")
    print("=" * 80)
    print()

    runbooks_dir = WORKSPACE_ROOT / "runbooks"
    export_dir = WORKSPACE_ROOT / "incident_response_verification"

    print(f"[*] Initializing Incident Automation Runtime...")
    print(f"    - Runbooks Directory: {runbooks_dir}")
    print(f"    - Target Export Directory: {export_dir}")
    print()

    runtime = IncidentAutomationRuntime(
        runbooks_dir=runbooks_dir,
        export_dir=export_dir,
    )

    print("[*] Executing full verification lifecycle across all 13 subsystems...")
    results = runtime.run_full_verification()
    scorecard = results["scorecard"]
    manifests = results["manifest_files"]

    print()
    print("-" * 80)
    print("  INCIDENT RESPONSE AUTOMATION SCORECARD")
    print("-" * 80)
    print(f"  Overall Score:           {scorecard.overall_score:.2f} / 100.00")
    print(f"  Automation Tier:         {scorecard.certification_tier.value.upper()}")
    print(f"  Certification Verdict:   {scorecard.certification_verdict}")
    print(f"  Production Ready:        {'YES [PASS]' if scorecard.passed else 'NO [FAIL]'}")
    print("-" * 80)
    print("  DIMENSION BREAKDOWN:")
    print(f"    - {'Detection Accuracy (20%)':<32}: {scorecard.detection_accuracy_score:>6.2f}%")
    print(f"    - {'Recovery Automation (20%)':<32}: {scorecard.recovery_automation_score:>6.2f}%")
    print(f"    - {'Safety Controls (20%)':<32}: {scorecard.safety_controls_score:>6.2f}%")
    print(f"    - {'Incident Diagnosis (15%)':<32}: {scorecard.incident_diagnosis_score:>6.2f}%")
    print(f"    - {'Operational Learning (15%)':<32}: {scorecard.operational_learning_score:>6.2f}%")
    print(f"    - {'Security & Audit (10%)':<32}: {scorecard.security_score:>6.2f}%")
    print("-" * 80)
    print()

    print("[*] Exported Evidence Manifests (10 JSON files):")
    for name, path in manifests.items():
        print(f"    [x] {name:<30} -> {path}")
    print()

    if scorecard.passed:
        print(">>> SUCCESS: Phase 3H.3.6 Incident Response Automation certified for Production!")
        return 0
    else:
        print(">>> FAILURE: Phase 3H.3.6 did not meet autonomous incident response threshold (>= 95.00%).")
        return 1


if __name__ == "__main__":
    sys.exit(main())
