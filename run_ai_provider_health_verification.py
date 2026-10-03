"""Master CLI Runner for Phase 3H.3.8 - AI Provider Health Verification Framework.

Executes all 15 dimensions of AI Provider Health verification, prints detailed tables,
and exports 8 structured JSON manifests to ai_health_verification/.
"""

import sys
import os
import io

# Enforce UTF-8 stdout for Windows terminals
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app.platform_verification.ai_provider_health.runtime.ai_provider_health_runtime import AIProviderHealthRuntime


def main():
    print("=" * 90)
    print(" DOCUTASK AGENT - ENTERPRISE AI PROVIDER HEALTH VERIFICATION FRAMEWORK")
    print(" PHASE 3H.3.8: LLMOps RELIABILITY, FAILOVER, LATENCY & RECOVERY CERTIFICATION")
    print("=" * 90)

    runtime = AIProviderHealthRuntime()
    print("\n[*] Initializing 15-dimension AI Health verification pipeline...")
    results = runtime.run_full_verification()

    health_rep = results["health_report"]
    results["auth_report"]
    results["connectivity_report"]
    lat_rep = results["latency_report"]
    quota_rep = results["quota_report"]
    results["integrity_report"]
    results["timeout_report"]
    results["failure_report"]
    results["degraded_report"]
    failover_rep = results["failover_report"]
    results["monitoring_report"]
    results["security_report"]
    sim_rep = results["simulation_report"]
    scorecard = results["scorecard"]
    manifests = results["exported_manifests"]

    # 1. AI Provider Health Contracts Table
    print("\n" + "-" * 90)
    print(" 1. AI PROVIDER HEALTH CONTRACTS & STATUS")
    print("-" * 90)
    print(f" {'PROVIDER':<18} | {'STATUS':<14} | {'LATENCY':<10} | {'AUTH':<10} | {'QUOTA':<12} | {'MODEL':<18}")
    print("-" * 90)
    for p in health_rep.providers:
        print(f" {p.provider:<18} | {p.status.value:<14} | {p.latency_ms:>7.1f}ms | {p.authentication:<10} | {p.quota_status:<12} | {p.model:<18}")

    # 2. Latency Distributions Table
    print("\n" + "-" * 90)
    print(" 2. INFERENCE LATENCY DISTRIBUTIONS (P50, P95, P99)")
    print("-" * 90)
    print(f" {'PROVIDER':<18} | {'MODEL':<20} | {'P50 (ms)':<10} | {'P95 (ms)':<10} | {'P99 (ms)':<10} | {'TARGET':<10}")
    print("-" * 90)
    for lat in lat_rep.latencies:
        print(f" {lat.provider:<18} | {lat.model:<20} | {lat.p50_latency_ms:>8.1f} | {lat.p95_latency_ms:>8.1f} | {lat.p99_latency_ms:>8.1f} | < {lat.threshold_p95_ms:.0f}ms")

    # 3. Quota & Rate Limit Headroom Table
    print("\n" + "-" * 90)
    print(" 3. QUOTA & BURST RATE-LIMIT UTILIZATION")
    print("-" * 90)
    print(f" {'PROVIDER':<18} | {'RPM UTIL %':<12} | {'TPM UTIL %':<12} | {'429 EVENTS':<12} | {'BACKOFF PASS':<14}")
    print("-" * 90)
    for q in quota_rep.quotas:
        backoff_str = "VERIFIED [PASS]" if q.backoff_strategy_verified else "FAILED"
        print(f" {q.provider:<18} | {q.current_rpm_utilization_pct:>10.1f}% | {q.current_tpm_utilization_pct:>10.1f}% | {q.rate_limit_429_count:>10} | {backoff_str:<14}")

    # 4. Multi-Provider Failover Performance Table
    print("\n" + "-" * 90)
    print(" 4. MULTI-PROVIDER FAILOVER PERFORMANCE & CONSISTENCY")
    print("-" * 90)
    print(f" {'SCENARIO':<14} | {'FROM -> TO':<28} | {'SWITCH TIME':<12} | {'SUCCESS %':<10} | {'CONSISTENT':<12}")
    print("-" * 90)
    for fo in failover_rep.failovers:
        route_str = f"{fo.from_provider} -> {fo.to_provider}"
        cons_str = "VERIFIED [PASS]" if fo.data_consistency_verified else "FAILED"
        print(f" {fo.failover_id:<14} | {route_str:<28} | {fo.failover_latency_ms:>9.1f}ms | {fo.success_rate_pct:>8.1f}% | {cons_str:<12}")

    # 5. Chaos Failure Simulation Results
    print("\n" + "-" * 90)
    print(" 5. CHAOS FAILURE SIMULATION EXPERIMENTS")
    print("-" * 90)
    for sim in sim_rep.simulations:
        print(f" [✓] {sim.scenario_id}: {sim.name}")
        print(f"     Injected: {sim.injected_fault}")
        print(f"     Observed: {sim.observed_behavior}")

    # 6. AI Health Quality Scorecard
    print("\n" + "=" * 90)
    print(" PLATFORM AI PROVIDER HEALTH & RELIABILITY QUALITY SCORECARD")
    print("=" * 90)
    print(f" 1. Availability Detection (Weight 20%):       {scorecard.availability_score:>6.2f} / 100")
    print(f" 2. Authentication Verification (Weight 15%): {scorecard.authentication_score:>6.2f} / 100")
    print(f" 3. Latency Monitoring (Weight 15%):          {scorecard.latency_score:>6.2f} / 100")
    print(f" 4. Failure Handling (Weight 20%):            {scorecard.failure_handling_score:>6.2f} / 100")
    print(f" 5. Response Quality Validation (Weight 15%): {scorecard.response_quality_score:>6.2f} / 100")
    print(f" 6. Security & PII Protection (Weight 15%):   {scorecard.security_score:>6.2f} / 100")
    print("-" * 90)
    print(f" OVERALL WEIGHTED AI HEALTH SCORE:            {scorecard.overall_score:>6.2f}%")
    print(f" CERTIFICATION TIER:                         {scorecard.certification_tier.value}")
    print(f" VERDICT:                                    {scorecard.certification_verdict}")
    print("=" * 90)

    # 7. Manifests Export List
    print("\n[+] Exported 8 Structured Audit Evidence Manifests:")
    for fname, path in manifests.items():
        print(f"    - {fname:<32} -> {path}")

    if scorecard.passed and scorecard.overall_score >= 95.0:
        print("\n[SUCCESS] Phase 3H.3.8 AI Provider Health Verification PASSED with Tier 'AI Reliability Certified' (>= 95.00%).")
        return 0
    else:
        print(f"\n[FAILURE] Phase 3H.3.8 Verification did not meet target (Score: {scorecard.overall_score}%).")
        return 1


if __name__ == "__main__":
    sys.exit(main())
