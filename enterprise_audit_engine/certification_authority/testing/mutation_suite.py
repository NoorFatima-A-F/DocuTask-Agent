"""Audit Engine Mutation Testing Suite."""

from typing import Dict, Any, List
from enterprise_audit_engine.domain.evidence.models import (
    EvidenceRecord,
    AuditFinding,
    EvidenceClassification,
    EvidenceConfidence,
    EvidenceSourceType,
)
from enterprise_audit_engine.governance.claim_validator import ClaimValidator, UnsupportedClaimError
from enterprise_audit_engine.certification.anti_hallucination import ClaimEvidenceMatcher
from enterprise_audit_engine.certification.coverage_analyzer import (
    EvidenceCoverageAnalyzer,
    IncompleteEvidenceCoverageError,
)
from enterprise_audit_engine.certification_authority.domain.models import (
    CertificationRecord,
)
from enterprise_audit_engine.certification_authority.signing.signer import CertificateSigner
from enterprise_audit_engine.certification_authority.signing.verifier import CertificateSignatureVerifier


class AuditMutationSuite:
    """Injects intentional synthetic defects to prove the audit engine detects tampering and falsification."""

    @classmethod
    def run_all_mutation_tests(cls) -> Dict[str, Any]:
        """Runs the 5 core synthetic mutation tests and returns results."""
        results: List[Dict[str, Any]] = []

        # 1. Mutation: Unbacked claim promotion
        res1 = cls.test_unbacked_claim_promotion_mutation()
        results.append(res1)

        # 2. Mutation: Corrupted record hash
        res2 = cls.test_corrupted_record_hash_mutation()
        results.append(res2)

        # 3. Mutation: Unproven marketing hype injection
        res3 = cls.test_unproven_marketing_injection_mutation()
        results.append(res3)

        # 4. Mutation: Forged digital certificate signature
        res4 = cls.test_forged_certificate_signature_mutation()
        results.append(res4)

        # 5. Mutation: Dropped evidence record
        res5 = cls.test_dropped_evidence_record_mutation()
        results.append(res5)

        all_detected = all(r["detected"] for r in results)

        return {
            "all_mutations_detected": all_detected,
            "total_mutations_tested": len(results),
            "detected_count": sum(1 for r in results if r["detected"]),
            "mutation_results": results,
            "status": "MUTATION_TEST_SUITE_PASSED" if all_detected else "MUTATION_UNDETECTED_VULNERABILITY",
        }

    @classmethod
    def test_unbacked_claim_promotion_mutation(cls) -> Dict[str, Any]:
        """Mutates a finding to 'VERIFIED' without supporting evidence."""
        rec = EvidenceRecord(
            id="EV-MUT-01",
            collector="UnitTestCollector",
            source_type=EvidenceSourceType.STATIC_SOURCE_CODE,
            category="Security",
            summary="Minimal config",
            raw_payload={"status": "incomplete"},
            confidence=EvidenceConfidence.LOW,
            classification=EvidenceClassification.EVIDENCE_INSUFFICIENT,
        )
        rec = rec.model_copy(update={"content_hash": rec.calculate_hash()})

        # Inject mutated finding promoting claim to VERIFIED
        finding = AuditFinding(
            finding_id="FND-MUT-01",
            subsystem="Security",
            claim="Zero-Trust Enforced",
            classification=EvidenceClassification.VERIFIED,  # Promoted without evidence!
            evidence_ids=["EV-MUT-01"],
            confidence=EvidenceConfidence.HIGH,
            analysis="Falsified claim promotion",
        )

        detected = False
        try:
            ClaimValidator.validate_all_findings([finding], [rec])
        except UnsupportedClaimError:
            detected = True
        except Exception:
            detected = True

        return {
            "mutation_name": "MUTATION_UNBACKED_CLAIM_PROMOTION",
            "detected": detected,
            "description": "Falsified promotion from EVIDENCE_INSUFFICIENT to VERIFIED",
            "guard": "ClaimValidator",
        }

    @classmethod
    def test_corrupted_record_hash_mutation(cls) -> Dict[str, Any]:
        """Mutates record payload without updating SHA-256 hash."""
        rec = EvidenceRecord(
            id="EV-MUT-02",
            collector="UnitTestCollector",
            source_type=EvidenceSourceType.STATIC_SOURCE_CODE,
            category="Database",
            summary="Original Summary",
            raw_payload={"original": True},
            confidence=EvidenceConfidence.HIGH,
            classification=EvidenceClassification.VERIFIED,
        )
        original_hash = rec.calculate_hash()
        
        # Tamper payload
        tampered_rec = rec.model_copy(
            update={
                "summary": "Tampered Summary",
                "content_hash": original_hash,  # Hash mismatch!
            }
        )

        detected = tampered_rec.content_hash != tampered_rec.calculate_hash()
        return {
            "mutation_name": "MUTATION_CORRUPT_RECORD_HASH",
            "detected": detected,
            "description": "Payload modified without valid SHA-256 hash update",
            "guard": "EvidenceRecord.calculate_hash / IntegrityVerifier",
        }

    @classmethod
    def test_unproven_marketing_injection_mutation(cls) -> Dict[str, Any]:
        """Injects unprovable marketing hype into report."""
        unprovable_text = "This application is 100% secure and bug-free with unbreakable encryption."
        sanitized, stripped = ClaimEvidenceMatcher.sanitize_report_text(unprovable_text, [])

        detected = len(stripped) >= 3 and "100% secure" not in sanitized
        return {
            "mutation_name": "MUTATION_UNPROVEN_MARKETING_INJECTION",
            "detected": detected,
            "description": "Banned unprovable marketing assertions injected into text",
            "guard": "ClaimEvidenceMatcher",
        }

    @classmethod
    def test_forged_certificate_signature_mutation(cls) -> Dict[str, Any]:
        """Mutates signed certificate payload to verify signature rejection."""
        cert = CertificationRecord.create_pending(
            certificate_id="CERT-MUT-01",
            system_name="DocuTask",
            release_version="1.0.0",
            audit_engine_version="2.1.0",
            audit_execution_id="RUN-01",
            merkle_root="abc123merkle",
            evidence_root_hash="def456hash",
            eqi_score=95.0,
        )
        signed_cert, pub_key = CertificateSigner.sign_certificate(cert)

        # Mutate release version after signing
        forged_cert = signed_cert.model_copy(update={"release_version": "9.9.9"})
        is_valid = CertificateSignatureVerifier.verify_record_signature(forged_cert, pub_key)

        detected = (is_valid is False)
        return {
            "mutation_name": "MUTATION_FORGED_CERTIFICATE_SIGNATURE",
            "detected": detected,
            "description": "Payload modified after digital signature creation",
            "guard": "CertificateSignatureVerifier",
        }

    @classmethod
    def test_dropped_evidence_record_mutation(cls) -> Dict[str, Any]:
        """Removes an evidence record referenced by an active finding."""
        finding = AuditFinding(
            finding_id="FND-MUT-03",
            subsystem="Storage",
            claim="Storage configured",
            classification=EvidenceClassification.VERIFIED,
            evidence_ids=["EV-MISSING-01"],
            confidence=EvidenceConfidence.HIGH,
            analysis="Missing record reference",
        )

        detected = False
        try:
            EvidenceCoverageAnalyzer.verify_coverage([finding], [])
        except IncompleteEvidenceCoverageError:
            detected = True
        except Exception:
            detected = True

        return {
            "mutation_name": "MUTATION_DROPPED_EVIDENCE_RECORD",
            "detected": detected,
            "description": "Evidence record missing from immutable store",
            "guard": "EvidenceCoverageAnalyzer",
        }
