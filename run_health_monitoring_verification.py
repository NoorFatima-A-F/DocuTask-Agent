"""Master Verification Runner for Phase 3H.3.5: Enterprise Health Monitoring Integration.

Executes all 12 verification subsystems:
1. Observability Architecture Verification
2. Health Metrics Inventory Collection
3. Prometheus Scraping & Query Verification
4. Grafana Operational Dashboards Validation
5. AlertManager Rule Configuration
6. Alert Quality & Fatigue Evaluation
7. Cross-Signal Incident Visibility & Correlation
8. Failure Simulation & SLA Benchmarking
9. Distributed Tracing Context Propagation
10. Monitoring Security & Credential Redaction Audit
11. Audit Manifest Evidence Generation (10 JSON Files)
12. Composite Observability Quality Scoring & Certification
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

from app.platform_verification.health_monitoring_integration.runtime.monitoring_integration_runtime import (
    MonitoringIntegrationRuntime,
)


def main() -> int:
    print("=" * 80)
    print("  PHASE 3H.3.5 - ENTERPRISE HEALTH MONITORING INTEGRATION VERIFICATION")
    print("  DocuTask Agent Production Observability & SRE Reliability Framework")
    print("=" * 80)
    print()

    export_dir = WORKSPACE_ROOT / "health_monitoring_verification"

    print(f"[*] Initializing Monitoring Integration Runtime...")
    print(f"    - Target Export Directory: {export_dir}")
    print()

    runtime = MonitoringIntegrationRuntime(export_dir=export_dir)

    print("[*] Executing full verification lifecycle across all 12 subsystems...")
    results = runtime.run_full_verification()
    scorecard = results["scorecard"]
    manifests = results["manifest_files"]

    print()
    print("-" * 80)
    print("  ENTERPRISE HEALTH MONITORING SCORECARD")
    print("-" * 80)
    print(f"  Overall Score:           {scorecard.overall_score:.2f} / 100.00")
    print(f"  Observability Tier:      {scorecard.certification_tier.value.upper()}")
    print(f"  Certification Verdict:   {scorecard.certification_verdict}")
    print(f"  Production Ready:        {'YES [PASS]' if scorecard.passed else 'NO [FAIL]'}")
    print("-" * 80)
    print("  DIMENSION BREAKDOWN:")
    print(f"    - {'Metric Coverage (20%)':<32}: {scorecard.metric_coverage_score:>6.2f}%")
    print(f"    - {'Alert Accuracy (20%)':<32}: {scorecard.alert_accuracy_score:>6.2f}%")
    print(f"    - {'Dashboard Quality (15%)':<32}: {scorecard.dashboard_quality_score:>6.2f}%")
    print(f"    - {'Trace Visibility (15%)':<32}: {scorecard.trace_visibility_score:>6.2f}%")
    print(f"    - {'Incident Diagnosis (15%)':<32}: {scorecard.incident_diagnosis_score:>6.2f}%")
    print(f"    - {'Security & Redaction (15%)':<32}: {scorecard.security_score:>6.2f}%")
    print("-" * 80)
    print()

    print("[*] Exported Evidence Manifests (10 JSON files):")
    for name, path in manifests.items():
        print(f"    [x] {name:<35} -> {path}")
    print()

    if scorecard.passed:
        print(">>> SUCCESS: Phase 3H.3.5 Enterprise Health Monitoring certified for Production!")
        return 0
    else:
        print(">>> FAILURE: Phase 3H.3.5 did not meet enterprise observability threshold (>= 95.00%).")
        return 1


if __name__ == "__main__":
    sys.exit(main())
