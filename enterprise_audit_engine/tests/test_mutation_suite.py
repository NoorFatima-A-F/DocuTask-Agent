"""Tests for Audit Mutation Suite & Defect Detection."""

from enterprise_audit_engine.certification_authority.testing.mutation_suite import AuditMutationSuite


def test_audit_mutation_suite_all_detected():
    res = AuditMutationSuite.run_all_mutation_tests()

    assert res["all_mutations_detected"] is True
    assert res["detected_count"] == 5
    assert res["status"] == "MUTATION_TEST_SUITE_PASSED"


def test_individual_mutations():
    assert AuditMutationSuite.test_unbacked_claim_promotion_mutation()["detected"] is True
    assert AuditMutationSuite.test_corrupted_record_hash_mutation()["detected"] is True
    assert AuditMutationSuite.test_unproven_marketing_injection_mutation()["detected"] is True
    assert AuditMutationSuite.test_forged_certificate_signature_mutation()["detected"] is True
    assert AuditMutationSuite.test_dropped_evidence_record_mutation()["detected"] is True
