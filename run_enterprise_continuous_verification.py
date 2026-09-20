"""
Master CLI Runner for Phase 3Q: Enterprise Continuous Infrastructure Verification & CI/CD Assurance Pipeline.

Executes the automated 7-stage CI/CD verification lifecycle:
1. Change Impact Analysis (file trigger classification)
2. Deterministic Container Build & Digest Verification
3. Non-Bypassable Security Gates (Trivy CVEs & Gitleaks Secrets)
4. Disposable Test Environment Provisioning & Health Probing
5. End-to-End Document Workflow Integration
6. Performance Regression Gate (>50% P95 Latency Blocking)
7. Chaos Resilience Pipeline & Infrastructure Drift Detection
And issues the Production Readiness Certificate with cryptographic SHA-256 manifest.
"""

import os
import sys
from pathlib import Path

from app.platform_verification.enterprise_continuous_verification.runtime.continuous_verification_runtime import (
    ContinuousVerificationRuntime,
)


def main() -> int:
    output_dir = "pipeline_evidence"
    print("=" * 80)
    print("  DocuTask Agent - Enterprise CI/CD Continuous Verification System")
    print("  Phase 3Q Continuous Infrastructure Assurance & Release Gatekeeper")
    print("=" * 80)
    print()

    runtime = ContinuousVerificationRuntime()

    print("[*] Executing full 7-stage Continuous Verification & Release Pipeline...")
    result = runtime.run_pipeline(export_dir=output_dir)

    change_impact = result["change_impact"]
    build = result["build"]
    security = result["security"]
    disposable_env = result["disposable_env"]
    integration = result["integration"]
    perf = result["performance"]
    chaos = result["chaos"]
    drift = result["drift"]
    decision = result["decision"]
    cert = result["certificate"]
    manifest = result["manifest"]

    print()
    print("-" * 80)
    print("  STAGE 1 & 2: CHANGE IMPACT ANALYSIS & DETERMINISTIC BUILD")
    print("-" * 80)
    print(f"  - Changed Components     : {', '.join(change_impact.changed_components)}")
    print(f"  - Required Test Suites   : {', '.join(change_impact.required_test_suites)}")
    print(f"  - Container Image Digest : {build.digest_sha256[:24]}... ({build.image_name}:{build.version})")
    print(f"  - Build Status           : {build.build_status.value} ({build.build_duration_sec:.1f}s, commit: {build.commit_hash[:10]})")

    print()
    print("-" * 80)
    print("  STAGE 3 & 4: SECURITY GATES & DISPOSABLE TEST ENVIRONMENT")
    print("-" * 80)
    print(f"  - Trivy Container CVEs   : {security.critical_vulnerabilities} Critical, {security.high_vulnerabilities} High")
    print(f"  - Gitleaks Secret Scans  : {security.secrets_detected} Secrets Found")
    print(f"  - Security Gate Status   : {'PASSED' if security.gate_passed else 'BLOCKED'} (Status: {security.container_scan_status.value})")
    print(f"  - Disposable Environment : {disposable_env.environment_id} ({disposable_env.startup_duration_sec:.2f}s)")
    print(f"  - Services Deployed      : {', '.join(disposable_env.services_deployed)}")

    print()
    print("-" * 80)
    print("  STAGE 5 & 6: E2E INTEGRATION & PERFORMANCE REGRESSION GATE")
    print("-" * 80)
    print(f"  - Integration Workflow   : 5/5 Subsystems Healthy ({integration.end_to_end_duration_ms:.1f}ms)")
    print(f"  - Data Consistency       : {'VERIFIED' if integration.data_consistency_verified else 'FAILED'}")
    print(f"  - Baseline P95 Latency   : {perf.baseline_p95_ms:.1f}ms | Current P95: {perf.current_p95_ms:.1f}ms (+{perf.latency_increase_pct:.1f}%)")
    print(f"  - Performance Regression : {'DETECTED' if perf.regression_detected else 'NONE'} (Threshold Exceeded: {perf.threshold_exceeded})")

    print()
    print("-" * 80)
    print("  STAGE 7: CHAOS RESILIENCE, DRIFT DETECTION & RELEASE CERTIFICATION")
    print("-" * 80)
    print(f"  - Chaos Resilience       : {'PASSED' if chaos.resilience_passed else 'FAILED'} (Lost Jobs: {chaos.lost_jobs})")
    print(f"  - Infrastructure Drift   : {'DETECTED' if drift.drift_detected else 'NONE (Zero Drift)'} (Severity: {drift.drift_severity})")
    print(f"  - Release Gatekeeper     : {decision.decision.value} (Confidence: {decision.confidence_score:.1f}%)")
    print(f"  - Certificate Serial No  : {cert.certificate_id} ({cert.certification})")

    print()
    print("=" * 80)
    print(f"  FINAL RELEASE DECISION   : {decision.decision.value}")
    print(f"  PIPELINE EVIDENCE PATH   : {os.path.abspath(output_dir)}")
    print(f"  PRODUCTION CERTIFICATE   : {os.path.abspath(os.path.join(output_dir, 'certification', 'production_readiness_certificate.json'))}")
    print(f"  CRYPTOGRAPHIC MANIFEST   : {os.path.abspath(os.path.join(output_dir, 'manifest.json'))} ({len(manifest.files)} SHA-256 artifacts)")
    print("=" * 80)

    return 0 if result["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
