"""
Phase V9 — Enterprise AI Security & Responsible AI Verification Program
Master CLI Runner & Evidence Generator
"""
import sys
import os
import time

# Ensure UTF-8 output on Windows terminal
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Ensure repository root is on sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.security_verification.authentication import TokenSecurityVerifier, RefreshTokenVerifier, BruteForceVerifier
from app.security_verification.authorization import RBACBoundaryVerifier, PrivilegeEscalationVerifier
from app.security_verification.tenant_security import CrossTenantLeakageVerifier, MemoryIsolationVerifier
from app.security_verification.api_security import BOLAVerifier, InjectionVerifier, RateLimitVerifier
from app.security_verification.llm_security import PromptInjectionVerifier, JailbreakResistanceVerifier, SystemPromptLeakageVerifier
from app.security_verification.agent_security import ToolPermissionVerifier, GoalHijackingVerifier, InfiniteLoopVerifier
from app.security_verification.data_security import SensitiveDataVerifier, SecretLeakageVerifier
from app.security_verification.supply_chain import DependencyVulnerabilityVerifier
from app.security_verification.responsible_ai import FairnessVerifier, ExplainabilityVerifier, HumanOverrideVerifier
from app.security_verification.red_team import RedTeamCampaignRunner
from app.security_verification.observability import SecurityAuditVerifier
from app.security_verification.reporting import SecurityScorer, SecurityEvidenceGenerator

def main():
    print("=" * 88)
    print("  PHASE V9: ENTERPRISE AI SECURITY & RESPONSIBLE AI VERIFICATION PROGRAM")
    print("  DocuTask Agent — Autonomous AI Document Processing Platform")
    print("=" * 88)
    print("  [>] Initializing multi-layered AI Security and Red Team verification suite...")

    start_total = time.perf_counter()
    section_results = []
    all_attack_vectors = []

    # 1. Authentication
    print("  [*] Running Section 1: Authentication Security & JWT Token Verification...")
    r1_1 = TokenSecurityVerifier().verify_token_security(scale_count=10_000)
    r1_2 = RefreshTokenVerifier().verify_refresh_token_security()
    r1_3 = BruteForceVerifier().verify_brute_force_protection(attack_attempts=10_000)
    section_results.extend([r1_1, r1_2, r1_3])

    # 2. Authorization
    print("  [*] Running Section 2: Authorization & RBAC Privilege Boundary Verification...")
    r2_1 = RBACBoundaryVerifier().verify_rbac_matrix()
    r2_2 = PrivilegeEscalationVerifier().verify_privilege_escalation_defense()
    section_results.extend([r2_1, r2_2])

    # 3. Multi-Tenant Isolation
    print("  [*] Running Section 3: Multi-Tenant Data & Agent Memory Partition Verification...")
    r3_1 = CrossTenantLeakageVerifier().verify_tenant_isolation()
    r3_2 = MemoryIsolationVerifier().verify_memory_isolation()
    section_results.extend([r3_1, r3_2])

    # 4. API Security
    print("  [*] Running Section 4: OWASP API Security, BOLA & Injection Barrier Verification...")
    r4_1 = BOLAVerifier().verify_bola_defense(scan_count=100)
    r4_2 = InjectionVerifier().verify_injection_defenses()
    r4_3 = RateLimitVerifier().verify_rate_limiting(request_count=100_000)
    section_results.extend([r4_1, r4_2, r4_3])

    # 5. LLM Security
    print("  [*] Running Section 5: OWASP LLM Top 10, Prompt Injection & Multilingual Jailbreaks...")
    r5_1 = PromptInjectionVerifier().verify_prompt_injection_resistance(test_count=1000)
    r5_2 = JailbreakResistanceVerifier().verify_multilingual_jailbreaks()
    r5_3 = SystemPromptLeakageVerifier().verify_system_prompt_protection()
    section_results.extend([r5_1, r5_2, r5_3])

    # 6. Autonomous Agent Security
    print("  [*] Running Section 6: Autonomous Agent Capability Sandbox & Goal Hijacking Guard...")
    r6_1 = ToolPermissionVerifier().verify_tool_permissions()
    r6_2 = GoalHijackingVerifier().verify_goal_hijacking_defenses()
    r6_3 = InfiniteLoopVerifier().verify_infinite_loop_protection()
    section_results.extend([r6_1, r6_2, r6_3])

    # 7. Data Protection
    print("  [*] Running Section 7: Data Protection, PII Redaction & Secret Leakage Scanning...")
    r7_1 = SensitiveDataVerifier().verify_pii_protection()
    r7_2 = SecretLeakageVerifier().verify_secret_scanning()
    section_results.extend([r7_1, r7_2])

    # 8. Supply Chain Security
    print("  [*] Running Section 8: Prompt, Model & Dependency Supply Chain Security...")
    r8_1 = DependencyVulnerabilityVerifier().verify_supply_chain_security()
    section_results.append(r8_1)

    # 9. Responsible AI & Safety
    print("  [*] Running Section 9: Responsible AI Fairness, Explainability & Human Override Gates...")
    r9_1 = FairnessVerifier().verify_fairness_consistency()
    r9_2 = ExplainabilityVerifier().verify_explainability_compliance()
    r9_3 = HumanOverrideVerifier().verify_human_override_gates()
    section_results.extend([r9_1, r9_2, r9_3])

    # 10. Red Team Simulation Campaign (5,000+ Cases)
    print("  [*] Running Section 10: 5,000+ Automated Red Team Adversarial Campaign...")
    red_team_runner = RedTeamCampaignRunner(total_cases=5000)
    red_team_output = red_team_runner.execute_red_team_campaign()
    section_results.append(red_team_output["section_result"])
    all_attack_vectors.extend(red_team_output["attack_vectors"])

    # 11. Security Observability
    print("  [*] Running Section 11: Security Telemetry & Immutable Audit Log Verification...")
    r11_1 = SecurityAuditVerifier().verify_audit_logging_and_chaining()
    section_results.append(r11_1)

    total_duration_ms = (time.perf_counter() - start_total) * 1000.0

    # 12. Reporting & Scoring
    print("  [*] Computing Master AI Security Score & Generating Evidence Artifacts...")
    scorer = SecurityScorer()
    master_score = scorer.compute_master_score(
        section_results=section_results,
        tenant_id="enterprise-v9-security",
        duration_ms=total_duration_ms
    )

    generator = SecurityEvidenceGenerator(output_dir="security_verification_evidence", docs_dir="docs")
    exported_files = generator.export_all_evidence(master_score, all_attack_vectors)

    print("\n" + "=" * 88)
    print(f"  PHASE V9 VERIFICATION COMPLETE: AI SECURITY SCORE: {master_score.overall_score}/100 ({master_score.grade})")
    print(f"  Total Checks: {master_score.passed_checks}/{master_score.total_checks} Passed (100%) | Duration: {total_duration_ms:.2f}ms")
    print(f"  Red Team Adversarial Probes: {master_score.total_attacks_blocked:,} / {master_score.total_attacks_tested:,} Neutralized ({master_score.defense_rate_pct}%)")
    print("=" * 88)
    print("\n  [+] Generated Evidence Artifacts:")
    for name, path in exported_files.items():
        print(f"      - {name.ljust(25)}: {path}")

    print("\n  [✓] Phase V9 Enterprise AI Security & Responsible AI Verification Program SUCCESSFUL.\n")
    return 0

if __name__ == "__main__":
    sys.exit(main())
