"""Tests for Independent Audit Export and Manifest Signing."""

from app.runtime.audit_export.bundle_exporter import (
    BundleExporter,
    ManifestSigner,
)


def test_manifest_signing():
    hashes = {
        "file1.json": "a" * 64,
        "file2.json": "b" * 64,
    }
    manifest = ManifestSigner.sign_manifest(hashes, "c" * 64)
    assert manifest.total_files == 2
    assert manifest.merkle_root == "c" * 64
    assert manifest.signer_public_key.startswith("pub_docutask_")
    assert manifest.manifest_signature.startswith("sig_manifest_")


def test_audit_bundle_export():
    bundle = BundleExporter.export_audit_bundle()
    assert bundle.bundle_id.startswith("AUDIT-BUNDLE-")
    assert len(bundle.merkle_root) == 64
    assert bundle.signed_manifest is not None
    assert len(bundle.verification_script_python) > 100
    assert "verify_bundle" in bundle.verification_script_python
