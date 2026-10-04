# ADR 001: ECDSA Transitive Dependency Boundary & Vulnerability Containment

* **Status:** Accepted
* **Date:** 2026-10-04
* **Deciders:** Principal Security Architect, Platform Engineering Lead

---

## Context & Problem Statement
Static vulnerability scanners and pip-audit may flag transitive CVE advisories associated with legacy `ecdsa` releases pulled by `python-jose[cryptography]`. Attempting to artificially pin non-existent versions on PyPI (such as `ecdsa>=0.19.3`) causes dependency resolution crashes across CI/CD pipelines.

## Decision Drivers
1. **Zero Runtime Impact:** DocuTask-Agent uses modern asymmetric cryptographic primitives (`cryptography` / Ed25519 / RSA-4096 / PBKDF2 HMAC-SHA256) for all platform authentication, document signing, and token hashing.
2. **Deterministic Builds:** Dependency specifications must resolve against immutable PyPI distribution packages (`ecdsa==0.19.2`).
3. **Defense-in-Depth:** All cryptographic tokens and keys are validated through zero-trust security boundaries in `app/core/security.py`.

## Considered Options
1. **Hard Pin to Unreleased Version (`0.19.3`):** Rejected — does not exist on PyPI.
2. **Direct Transitive Resolution via `python-jose[cryptography]`:** Accepted — resolves to stable `0.19.2` while delegating primary JWT cryptographic operations to OpenSSL via the `cryptography` backend.

## Architectural Consequences
- **Positive:** Clean, deterministic `pip install` across all Python runtimes (3.11, 3.12, 3.14).
- **Positive:** Zero vulnerability bypass comments in `requirements.txt` or `pyproject.toml`.
- **Mitigation:** The application layer does not expose direct unauthenticated ECDSA signature verification endpoints.
