"""
Master CLI Runner for Health Check Architecture Verification (Part 3H.1).
"""
import sys
import os

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Ensure project root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.platform_verification.health_architecture.runtime.health_runtime import (
    HealthVerificationRuntime,
)


def main():
    print("=" * 80)
    print(" DOCUTASK AGENT — PART 3H.1 ENTERPRISE HEALTH CHECK ARCHITECTURE VERIFIER")
    print("=" * 80)
    print("Initializing Multi-Dimensional Health Verification Engine...\n")

    runtime = HealthVerificationRuntime(output_dir="health_architecture_verification")
    results = runtime.run_full_verification(export=True)

    scorecard = results["scorecard"]
    model_rep = results["model_report"]
    contract_rep = results["contract_report"]
    deps_rep = results["dependency_report"]
    policy_rep = results["policy_report"]
    sec_rep = results["security_report"]
    auto_rep = results["automation_report"]
    exported = results["exported_files"]

    print("—" * 80)
    print("1. HEALTH STATE MACHINE & FOUR-LAYER MODEL")
    print("—" * 80)
    print(f"Total States Evaluated:       {model_rep.total_states} (UNKNOWN, INITIALIZING, READY, DEGRADED, UNHEALTHY, RECOVERING, FAILED)")
    print(f"Architectural Layers:         {len(model_rep.layers_evaluated)} (Process, Dependency, Capability, Workflow)")
    print(f"Transition Matrix Valid:      {'[PASS]' if model_rep.state_machine_valid else '[FAIL]'}")
    print(f"Transition Coverage:          {model_rep.transition_coverage_pct:.1f}%")

    print("\n" + "—" * 80)
    print("2. UNIVERSAL HEALTH CONTRACTS (/live, /ready, /health)")
    print("—" * 80)
    print(f"Liveness Contract Valid:      {'[PASS]' if contract_rep.liveness_contract_valid else '[FAIL]'}")
    print(f"Liveness Isolated From Deps:  {'[PASS]' if contract_rep.liveness_isolated_from_dependencies else '[FAIL]'} (Zero DB/External Network Calls)")
    print(f"Readiness Contract Valid:     {'[PASS]' if contract_rep.readiness_contract_valid else '[FAIL]'}")
    print(f"Readiness Dependency Aware:   {'[PASS]' if contract_rep.readiness_enforces_critical_deps else '[FAIL]'} (Withholds traffic on critical failures)")
    print(f"Full Health Diagnostics:      {'[PASS]' if contract_rep.full_health_contract_valid else '[FAIL]'}")

    print("\n" + "—" * 80)
    print("3. DEPENDENCY GRAPH & CRITICALITY MATRIX")
    print("—" * 80)
    print(f"Mapped Services:              {deps_rep.total_services_mapped} (API Gateway, Worker Cluster, Vector Engine)")
    print(f"Total Dependencies:           {deps_rep.total_dependencies}")
    print(f"Critical Dependencies:        {deps_rep.critical_dependencies_count} (Timeout <= 1000ms, strictly gated)")
    print(f"Important Dependencies:       {deps_rep.important_dependencies_count} (Timeout <= 2000ms, fallback enabled)")
    print(f"Optional Dependencies:        {deps_rep.optional_dependencies_count} (Fail-open telemetry)")

    print("\n" + "—" * 80)
    print("4. FAILURE CLASSIFICATION & AUTOMATED RESPONSE WORKFLOW")
    print("—" * 80)
    print(f"Policies Enforced:            {policy_rep.policies_defined_count}")
    print(f"Detection Verified:           {'[PASS]' if policy_rep.detection_mechanisms_verified else '[FAIL]'}")
    print(f"Response Automated:           {'[PASS]' if policy_rep.response_actions_automated else '[FAIL]'}")
    print(f"Recovery Strategies:          {'[PASS]' if policy_rep.recovery_strategies_documented else '[FAIL]'}")

    print("\n" + "—" * 80)
    print("5. ROLE-BASED HEALTH SECURITY & ZERO LEAK AUDIT")
    print("—" * 80)
    print(f"Public Endpoint Clean:        {'[PASS]' if sec_rep.public_endpoint_leak_free else '[FAIL]'} (No internal IPs/Hostnames)")
    print(f"Internal Endpoint Clean:      {'[PASS]' if sec_rep.internal_endpoint_leak_free else '[FAIL]'} (No Passwords/DB Strings)")
    print(f"Admin Diagnostic RBAC:        {'[PASS]' if sec_rep.admin_diagnostic_auth_enforced else '[FAIL]'} (Bearer / VPC Auth Enforced)")
    print(f"Credentials Leaked Count:     {sec_rep.credentials_leaked_count}")

    print("\n" + "—" * 80)
    print("6. ORCHESTRATION & AUTOMATION READINESS")
    print("—" * 80)
    print(f"Docker HEALTHCHECK:           {'[PASS]' if auto_rep.docker_healthcheck_compatible else '[FAIL]'}")
    print(f"Kubernetes Liveness Probe:    {'[PASS]' if auto_rep.kubernetes_liveness_compatible else '[FAIL]'}")
    print(f"Kubernetes Readiness Probe:   {'[PASS]' if auto_rep.kubernetes_readiness_compatible else '[FAIL]'}")
    print(f"Kubernetes Startup Probe:     {'[PASS]' if auto_rep.kubernetes_startup_compatible else '[FAIL]'}")
    print(f"CI/CD Pre-Deployment Gating:  {'[PASS]' if auto_rep.cicd_predeployment_gating_supported else '[FAIL]'}")

    print("\n" + "=" * 80)
    print(" COMPREHENSIVE ARCHITECTURAL HEALTH SCORECARD")
    print("=" * 80)
    print(f"  Health Model Score (20%):             {scorecard.health_model_score:>6.2f} / 100.00")
    print(f"  Contract Implementation (20%):        {scorecard.contract_implementation_score:>6.2f} / 100.00")
    print(f"  Dependency Modeling (20%):            {scorecard.dependency_modeling_score:>6.2f} / 100.00")
    print(f"  Failure Classification (15%):         {scorecard.failure_classification_score:>6.2f} / 100.00")
    print(f"  Security Design (10%):                {scorecard.security_design_score:>6.2f} / 100.00")
    print(f"  Automation Readiness (15%):           {scorecard.automation_readiness_score:>6.2f} / 100.00")
    print("  " + "-" * 50)
    print(f"  OVERALL HEALTH SCORE:                 {scorecard.overall_health_score:>6.2f} / 100.00")
    print(f"  CERTIFICATION TIER:                   {scorecard.certification_tier.value}")
    print(f"  CERTIFICATION VERDICT:                {scorecard.certification_verdict}")
    print(f"  CI/CD DEPLOYMENT APPROVED:            {'YES' if scorecard.ci_cd_deployment_approved else 'NO'}")
    print("=" * 80)

    print(f"\nAudit Evidence Manifests Exported ({len(exported)} files to health_architecture_verification/):")
    for fname, fpath in exported.items():
        print(f"  [+] {fname} -> {fpath}")

    print("\nVerification Complete.")
    if scorecard.passed:
        print("[SUCCESS] Platform Health Architecture meets Enterprise Tier Requirements.")
        sys.exit(0)
    else:
        print("[FAILURE] Platform Health Architecture does not meet minimum quality threshold.")
        sys.exit(1)


if __name__ == "__main__":
    main()
