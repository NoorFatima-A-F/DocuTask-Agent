"""Tests for 50+ Expanded Adversarial Mutation Attacks."""

import pytest
from enterprise_audit_engine.assurance.testing.expanded_mutation_suite import ExpandedMutationSuite


def test_expanded_mutation_suite_execution():
    results = ExpandedMutationSuite.run_all_mutations()
    assert results["all_mutations_detected"] is True
    assert results["total_mutations_tested"] == 50
    assert results["detected_count"] == 50
    assert results["status"] == "EXPANDED_MUTATIONS_50_PASS"


@pytest.mark.parametrize("mut_id", list(range(1, 16)))
def test_individual_evidence_mutations(mut_id):
    res = ExpandedMutationSuite._run_evidence_mutation(mut_id)
    assert res["detected"] is True, f"Failed on evidence mutation {mut_id}: {res['description']}"


@pytest.mark.parametrize("mut_id", list(range(1, 16)))
def test_individual_classification_mutations(mut_id):
    res = ExpandedMutationSuite._run_classification_mutation(mut_id)
    assert res["detected"] is True, f"Failed on classification mutation {mut_id}: {res['description']}"


@pytest.mark.parametrize("mut_id", list(range(1, 11)))
def test_individual_cryptographic_mutations(mut_id):
    res = ExpandedMutationSuite._run_cryptographic_mutation(mut_id)
    assert res["detected"] is True, f"Failed on cryptographic mutation {mut_id}: {res['description']}"


@pytest.mark.parametrize("mut_id", list(range(1, 11)))
def test_individual_policy_mutations(mut_id):
    res = ExpandedMutationSuite._run_policy_mutation(mut_id)
    assert res["detected"] is True, f"Failed on policy mutation {mut_id}: {res['description']}"
