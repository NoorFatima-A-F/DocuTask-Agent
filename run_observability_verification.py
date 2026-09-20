"""
Master CLI Runner: Part 3I Enterprise Observability Infrastructure Verification Framework
"""
import sys
import os

# Ensure workspace root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.platform_verification.observability_infrastructure.runtime.observability_runtime import (
    ObservabilityRuntime,
)


def main():
    print("=" * 80)
    print("  PART 3I: ENTERPRISE OBSERVABILITY INFRASTRUCTURE VERIFICATION")
    print("  3I.1 Logging (Structured/Trace/PII) + 3I.2 Metrics (Golden Signals/SLO/Alerts)")
    print("=" * 80)

    runtime = ObservabilityRuntime()
    output_dir = "observability_verification"
    print(f"\n[*] Executing unified observability verification pipelines and exporting manifests to '{output_dir}'...")

    results = runtime.run_full_verification(export_base_dir=output_dir)
    log_cert = results["logging"]["certification"]
    met_cert = results["metrics"]["certification"]
    uni_cert = results["unified_certification"]
    metadata = results["metadata"]

    print("\n" + "-" * 80)
    print("  PART 3I.1: ENTERPRISE LOGGING QUALITY SCORECARD")
    print("-" * 80)
    for p in log_cert.pillar_scores:
        print(f"  [{p.status:^17}] {p.pillar_name:<46} | Weight: {p.weight_pct:>4.1f}% | Achieved: {p.achieved_score_pct:>5.2f}% | Weighted: {p.weighted_score_pct:>5.2f}%")
    print(f"  --> LOGGING SCORE: {log_cert.overall_score_pct:.2f}% | TIER: {log_cert.certification_tier}")

    print("\n" + "-" * 80)
    print("  PART 3I.2: ENTERPRISE METRICS QUALITY SCORECARD")
    print("-" * 80)
    for p in met_cert.pillar_scores:
        print(f"  [{p.status:^17}] {p.pillar_name:<46} | Weight: {p.weight_pct:>4.1f}% | Achieved: {p.achieved_score_pct:>5.2f}% | Weighted: {p.weighted_score_pct:>5.2f}%")
    print(f"  --> METRICS SCORE: {met_cert.overall_score_pct:.2f}% | TIER: {met_cert.certification_tier}")

    print("\n" + "=" * 80)
    print(f"  UNIFIED OBSERVABILITY SCORE: {uni_cert.overall_score_pct:.2f}%  (Passing Threshold: 95.0%)")
    print(f"  CERTIFICATION TIER:          {uni_cert.certification_tier.value}")
    print(f"  CERTIFICATION STATUS:        {'GRANTED' if uni_cert.certification_granted else 'REJECTED'}")
    print(f"  EVIDENCE ARTIFACTS:          {metadata['logging_artifacts']} Logging + {metadata['metrics_artifacts']} Metrics JSON manifests (SHA-256 signed)")
    print("=" * 80)

    if not uni_cert.certification_granted:
        print("\n[!] FAILURE: Observability certification criteria not met.")
        sys.exit(1)
    else:
        print("\n[+] SUCCESS: Platform is certified for Part 3I Enterprise Observability Infrastructure.")
        sys.exit(0)


if __name__ == "__main__":
    main()
