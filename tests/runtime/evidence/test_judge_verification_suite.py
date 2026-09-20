"""Tests for Judge Verification Suite and Ledger Verification."""

import pytest
from app.runtime.judge_verification.verification_suite import (
    HashChainVerifier,
    VerificationSuite,
)


def test_hash_chain_verifier():
    chains = HashChainVerifier.verify_all_ledgers()
    assert "decision_ledger_chain" in chains
    assert "tool_ledger_chain" in chains
    assert "evidence_graph_integrity" in chains


def test_judge_verification_suite_run():
    report = VerificationSuite.run_judge_verification()
    assert report.total_checks == 7
    assert report.passed_checks >= 6
    assert report.verdict in ["CERTIFIED_AUTONOMOUS", "FAILED_VERIFICATION"]
    assert len(report.cryptographic_root_hash) == 64
    assert len(report.judge_instructions) > 0
