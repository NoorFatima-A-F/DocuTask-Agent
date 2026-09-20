"""Master CLI Runner for Phase 3H.4.4 — Grafana Operational Dashboard Verification Framework."""

import sys
import os

# Ensure app package is importable
sys.path.insert(0, os.path.abspath("."))

from app.platform_verification.grafana_verification.runtime.grafana_verification_runtime import (
    GrafanaVerificationRuntime,
)
from app.platform_verification.grafana_verification.domain.models import (
    DashboardCertificationTier,
)


def main():
    print("=" * 80)
    print("DocuTask Agent — Phase 3H.4.4: Grafana Dashboard Verification Framework")
    print("=" * 80)
    print("Initializing verification runtime and executing all 12 validation phases...")

    runtime = GrafanaVerificationRuntime(output_dir="grafana_verification")
    scorecard, manifests = runtime.execute_full_verification()

    print("\n" + "-" * 80)
    print("GRAFANA DASHBOARD OPERATIONAL QUALITY SCORECARD")
    print("-" * 80)
    print(f"Overall Composite Score:        {scorecard.overall_score:.2f}%")
    print(f"Certification Tier:             {scorecard.certification_tier.value}")
    print(f"Certification Verdict:          {scorecard.certification_verdict}")
    print(f"Certified Enterprise Ready:     {'YES (PASSED)' if scorecard.passed else 'NO (FAILED)'}")
    print("-" * 80)
    print("CATEGORY BREAKDOWN:")
    print(f"  • System Visibility (20%)             : {scorecard.system_visibility_score:.2f}%")
    print(f"  • AI Workload Visibility (20%)        : {scorecard.ai_workload_visibility_score:.2f}%")
    print(f"  • Infrastructure Visibility (15%)     : {scorecard.infrastructure_visibility_score:.2f}%")
    print(f"  • Incident Usefulness (15%)           : {scorecard.incident_usefulness_score:.2f}%")
    print(f"  • Provisioning Quality (10%)          : {scorecard.provisioning_quality_score:.2f}%")
    print(f"  • Performance & Scale (10%)           : {scorecard.performance_score:.2f}%")
    print(f"  • Security & Compliance (10%)         : {scorecard.security_score:.2f}%")
    print("-" * 80)
    print(f"Evidence manifests exported to 'grafana_verification/' directory ({len(manifests)} files):")
    for fname in sorted(manifests.keys()):
        print(f"  - {fname}")
    print("=" * 80)

    if scorecard.passed and scorecard.overall_score >= 95.0:
        print("[SUCCESS] Phase 3H.4.4 Grafana Dashboard Verification certified successfully.")
        sys.exit(0)
    else:
        print(f"[ERROR] Quality score ({scorecard.overall_score:.2f}%) fell below target (95.00%).")
        sys.exit(1)


if __name__ == "__main__":
    main()
