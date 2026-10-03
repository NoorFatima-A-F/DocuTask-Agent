"""Master Verification Runner for Phase 3H.3.4: Predictive Health Intelligence & Early Failure Detection.

Executes all 15 verification subsystems, validates telemetry, detects anomalies,
evaluates failure risk probabilities, generates early warnings and recommendations,
benchmarks precision/recall, exports Prometheus metrics and 8 audit evidence manifests.
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

from app.platform_verification.predictive_health_intelligence.runtime.predictive_health_runtime import (
    PredictiveHealthRuntime,
)


def main() -> int:
    print("=" * 80)
    print("  PHASE 3H.3.4 - PREDICTIVE HEALTH INTELLIGENCE & EARLY FAILURE DETECTION")
    print("  DocuTask Agent Enterprise Platform Reliability Verification")
    print("=" * 80)
    print()

    export_dir = WORKSPACE_ROOT / "health_verification"
    baseline_path = WORKSPACE_ROOT / "health_baseline.yaml"

    print(f"[*] Initializing Predictive Health Runtime...")
    print(f"    - Baseline Path: {baseline_path}")
    print(f"    - Export Directory: {export_dir}")
    print()

    runtime = PredictiveHealthRuntime(
        baseline_path=baseline_path,
        export_dir=export_dir,
    )

    print("[*] Executing full verification lifecycle across all 15 parts...")
    results = runtime.run_full_verification()
    scorecard = results["scorecard"]
    manifests = results["manifest_files"]

    print()
    print("-" * 80)
    print("  PREDICTIVE HEALTH INTELLIGENCE SCORECARD")
    print("-" * 80)
    print(f"  Overall Score:           {scorecard.overall_score:.2f} / 100.00")
    print(f"  Reliability Tier:        {scorecard.certification_tier.value.upper()}")
    print(f"  Certification Verdict:   {scorecard.certification_verdict}")
    print(f"  Production Ready:        {'YES [PASS]' if scorecard.passed else 'NO [FAIL]'}")
    print("-" * 80)
    print("  DIMENSION BREAKDOWN:")
    print(f"    - {'Telemetry Quality (20%)':<32}: {scorecard.telemetry_quality_score:>6.2f}%")
    print(f"    - {'Anomaly Detection (20%)':<32}: {scorecard.anomaly_detection_score:>6.2f}%")
    print(f"    - {'Prediction Accuracy (20%)':<32}: {scorecard.prediction_accuracy_score:>6.2f}%")
    print(f"    - {'Early Warning (15%)':<32}: {scorecard.early_warning_score:>6.2f}%")
    print(f"    - {'Preventive Actions (15%)':<32}: {scorecard.preventive_actions_score:>6.2f}%")
    print(f"    - {'Observability (10%)':<32}: {scorecard.observability_score:>6.2f}%")
    print("-" * 80)
    print()

    print("[*] Exported Evidence Manifests (8 JSON files):")
    for name, path in manifests.items():
        print(f"    [x] {name:<25} -> {path}")
    print()

    if scorecard.passed:
        print(">>> SUCCESS: Phase 3H.3.4 Predictive Health Intelligence certified for Production!")
        return 0
    else:
        print(">>> FAILURE: Phase 3H.3.4 did not meet production readiness threshold (>= 95.00%).")
        return 1


if __name__ == "__main__":
    sys.exit(main())
