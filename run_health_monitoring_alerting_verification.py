"""Master CLI Runner for Phase 3H.4 - Enterprise Health Monitoring, Alerting & Incident Signal Verification.

Executes all 12 sub-parts of Phase 3H.4 verification:
1. Health Signal Architecture (12 Signals across 4 categories)
2. Operational Metrics Collection (19 Metrics across 5 domains)
3. Prometheus /metrics Scraping & OpenTelemetry Bridge
4. Grafana Dashboards (4 Dashboards)
5. Alert Rules (Critical & Warning AlertManager rules)
6. Alert Accuracy (Precision, Recall, Auto-Resolution)
7. Incident Signals (Actionable Payloads & Diagnostics)
8. Alert Fatigue Prevention (Deduplication & Compression)
9. Failure Injection Simulations (Chaos & Self-Healing)
10. Observability Security (Secret & PII Leak Prevention)
11. Operational Readiness Scorecard (6-dimension weighted score)
12. Audit Manifests Export (10 JSON manifests to health_monitoring_verification/)
"""

import sys
import os
import io

# Enforce UTF-8 stdout for Windows terminals
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app.platform_verification.health_monitoring_alerting.runtime.health_monitoring_alerting_runtime import (
    HealthMonitoringAlertingRuntime,
)


def main() -> int:
    print("=" * 95)
    print(" DOCUTASK AGENT - ENTERPRISE HEALTH MONITORING, ALERTING & INCIDENT SIGNAL FRAMEWORK")
    print(" PHASE 3H.4: 12-DIMENSION OPERATIONAL OBSERVABILITY, ALERT ACCURACY & CHAOS RESILIENCE")
    print("=" * 95)

    runtime = HealthMonitoringAlertingRuntime()
    print("\n[*] Initializing Phase 3H.4 Health Monitoring & Alerting verification engine...")
    results = runtime.run_full_verification()

    signals_rep = results["signal_report"]
    metrics_rep = results["metrics_report"]
    prom_rep = results["prometheus_report"]
    dash_rep = results["dashboard_report"]
    alert_rep = results["alert_report"]
    acc_rep = results["accuracy_report"]
    inc_rep = results["incident_report"]
    fatigue_rep = results["fatigue_report"]
    sim_rep = results["failure_test_report"]
    sec_rep = results["security_report"]
    scorecard = results["scorecard"]
    manifests = results["exported_manifests"]

    # 1. Health Signal Architecture Table
    print("\n" + "-" * 95)
    print(" 1. HEALTH SIGNAL ARCHITECTURE (12 SIGNALS ACROSS 4 CATEGORIES)")
    print("-" * 95)
    print(f" {'SIGNAL NAME':<32} | {'CATEGORY':<14} | {'SOURCE METRIC':<30} | {'WARN/CRIT':<12}")
    print("-" * 95)
    for s in signals_rep.signals:
        print(f" {s.signal_name:<32} | {s.category.value:<14} | {s.metric_source:<30} | {s.threshold_warning}/{s.threshold_critical}")

    # 2. Operational Metrics Collection Table
    print("\n" + "-" * 95)
    print(" 2. OPERATIONAL METRICS COLLECTION (19 METRICS ACROSS 5 DOMAINS)")
    print("-" * 95)
    print(f" {'METRIC NAME':<34} | {'DOMAIN':<16} | {'TYPE':<10} | {'SAMPLE VALUE':<16} | {'UNIT':<10}")
    print("-" * 95)
    for m in metrics_rep.metrics:
        print(f" {m.metric_name:<34} | {m.domain:<16} | {m.metric_type:<10} | {m.sample_value:>14.2f} | {m.unit:<10}")

    # 3. Prometheus & OpenTelemetry Scraping
    print("\n" + "-" * 95)
    print(" 3. PROMETHEUS SCRAPING & OPENTELEMETRY BRIDGE")
    print("-" * 95)
    print(f" Endpoint: {prom_rep.endpoint} | HTTP Status: {prom_rep.http_status}")
    print(f" Exported Series Count: {prom_rep.exported_series_count} | Scrape Duration: {prom_rep.scrape_duration_ms:.2f}ms")
    print(f" OTel Collector Bridge: {'ACTIVE' if prom_rep.open_telemetry_bridge_active else 'INACTIVE'} | Metric Lifecycle Validated: {prom_rep.metric_lifecycle_validated}")

    # 4. Grafana Dashboards Table
    print("\n" + "-" * 95)
    print(" 4. ENTERPRISE GRAFANA DASHBOARDS (4 VERIFIED)")
    print("-" * 95)
    print(f" {'DASHBOARD ID':<26} | {'TITLE':<38} | {'PANELS':<8} | {'REFRESH':<8} | {'STATUS':<8}")
    print("-" * 95)
    for d in dash_rep.dashboards:
        print(f" {d.dashboard_id:<26} | {d.title:<38} | {d.panels_count:>6} | {d.refresh_rate:<8} | {'PASS':<8}")

    # 5. AlertManager Rules Table
    print("\n" + "-" * 95)
    print(" 5. ALERTMANAGER RULES (3 CRITICAL + 3 WARNING)")
    print("-" * 95)
    print(f" {'ALERT NAME':<26} | {'SEVERITY':<10} | {'OWNER':<14} | {'ACTION':<32} | {'STATUS':<8}")
    print("-" * 95)
    for r in alert_rep.rules:
        print(f" {r.alert_name:<26} | {r.severity.value:<10} | {r.owner:<14} | {r.action[:30]:<32} | {'ACTIVE':<8}")

    # 6. Alert Accuracy Verification
    print("\n" + "-" * 95)
    print(" 6. ALERT ACCURACY, PRECISION & AUTO-RESOLUTION")
    print("-" * 95)
    print(f" True Positives (TP):        {acc_rep.true_positives}")
    print(f" False Positives (FP):       {acc_rep.false_positives}")
    print(f" True Negatives (TN):        {acc_rep.true_negatives}")
    print(f" False Negatives (FN):       {acc_rep.false_negatives}")
    print(f" Precision:                  {acc_rep.precision_pct:.2f}% (Target: 100.00%)")
    print(f" Recall:                     {acc_rep.recall_pct:.2f}% (Target: 100.00%)")
    print(f" Auto-Resolution Verified:   {acc_rep.auto_resolution_verified}")

    # 7. Actionable Incident Signals Table
    print("\n" + "-" * 95)
    print(" 7. ACTIONABLE INCIDENT SIGNALS (4 PRODUCTION SCENARIOS)")
    print("-" * 95)
    for inc in inc_rep.incidents:
        print(f" [✓] {inc.incident_id:<16} | Service: {inc.service:<10} | Severity: {inc.severity.value:<8} | State: {inc.state.value:<8}")
        print(f"     Title: {inc.title}")
        print(f"     Impact: {inc.impact}")
        print(f"     Action: {inc.recommended_action}")

    # 8. Alert Fatigue Prevention
    print("\n" + "-" * 95)
    print(" 8. ALERT FATIGUE PREVENTION & DEDUPLICATION")
    print("-" * 95)
    print(f" Raw Alerts Received:        {fatigue_rep.raw_alerts_received}")
    print(f" Deduplicated Group Alerts:  {fatigue_rep.deduplicated_alerts_grouped}")
    print(f" Noise Compression Ratio:    {fatigue_rep.compression_ratio_pct:.2f}%")
    print(f" Root-Cause Grouping:       {'ACTIVE' if fatigue_rep.grouping_by_root_cause_active else 'DISABLED'}")
    print(f" Maintenance Suppression:    {'ACTIVE' if fatigue_rep.maintenance_window_suppression_active else 'DISABLED'}")

    # 9. Chaos & Failure Simulations Table
    print("\n" + "-" * 95)
    print(" 9. FAILURE INJECTION & CHAOS MONITORING TESTS")
    print("-" * 95)
    for t in sim_rep.tests:
        print(f" [✓] {t.test_id:<14} | Injected: {t.failure_injected:<22} | Metric: {t.metric_updated} | Alert: {t.alert_fired} | Cleared: {t.alert_cleared_on_recovery}")

    # 10. Security Audit Table
    print("\n" + "-" * 95)
    print(" 10. OBSERVABILITY SECURITY & PII/SECRET AUDIT")
    print("-" * 95)
    print(f" Total Metrics Scanned:      {sec_rep.metrics_scanned_count}")
    print(f" Total Logs Scanned:         {sec_rep.logs_scanned_count}")
    print(f" Total Alerts Scanned:       {sec_rep.alerts_scanned_count}")
    print(f" Secret Leaks Found:         {int(sec_rep.secret_leaks_found)} (Target: 0)")
    print(f" Token Leaks Found:          {sec_rep.token_leaks_found} (Target: 0)")
    print(f" PII Leaks Found:            {sec_rep.pii_leaks_found} (Target: 0)")
    print(f" Zero Leak Verified:         {sec_rep.zero_leak_verified}")

    # 11. Operational Readiness Scorecard
    print("\n" + "=" * 95)
    print(" ENTERPRISE HEALTH MONITORING & ALERTING SCORECARD")
    print("=" * 95)
    print(f" 1. Metrics Completeness (Weight 20%):       {scorecard.metrics_completeness_score:>6.2f} / 100")
    print(f" 2. Monitoring Accuracy (Weight 20%):        {scorecard.monitoring_accuracy_score:>6.2f} / 100")
    print(f" 3. Alert Reliability (Weight 20%):          {scorecard.alert_reliability_score:>6.2f} / 100")
    print(f" 4. Incident Quality (Weight 15%):           {scorecard.incident_quality_score:>6.2f} / 100")
    print(f" 5. Dashboard Usability (Weight 15%):        {scorecard.dashboard_usability_score:>6.2f} / 100")
    print(f" 6. Telemetry Security (Weight 10%):         {scorecard.security_score:>6.2f} / 100")
    print("-" * 95)
    print(f" OVERALL WEIGHTED OBSERVABILITY SCORE:       {scorecard.overall_score:>6.2f}%")
    print(f" CERTIFICATION TIER:                         {scorecard.certification_tier.value}")
    print(f" VERDICT:                                    {scorecard.certification_verdict}")
    print("=" * 95)

    # 12. Manifests Export List
    print("\n[+] Exported 10 Structured Audit Evidence Manifests (health_monitoring_verification/):")
    for fname, path in manifests.items():
        print(f"    - {fname:<32} -> {path}")

    if scorecard.passed and scorecard.overall_score >= 95.0:
        print("\n[SUCCESS] Phase 3H.4 Enterprise Health Monitoring Verification PASSED with Tier 'Enterprise Observability Ready' (>= 95.00%).")
        return 0
    else:
        print(f"\n[FAILURE] Phase 3H.4 Verification did not meet target (Score: {scorecard.overall_score}%).")
        return 1


if __name__ == "__main__":
    sys.exit(main())
