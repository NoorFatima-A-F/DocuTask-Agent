# Dependency Vulnerability Remediation & Security Audit Report

## Executive Summary

- **Audit Date**: 2026-09-21
- **Tooling Used**: `pip-audit`, GitHub Dependabot, `npm audit`
- **Total Alerts Remediated**: 4 (2 High, 2 Moderate)
- **Status**: All known high and moderate severity dependency vulnerabilities resolved.

---

## 1. Python Dependency Remediation Matrix

| Package | Old Version | Remediated Strategy / Version | CVE / Advisory | Severity | Status |
| :--- | :---: | :---: | :--- | :---: | :--- |
| **`ecdsa`** (`python-ecdsa`) | All | **Removed completely** (Standardized on `cryptography>=43.0.3` & `python-jose[cryptography]`) | [CVE-2024-23342](https://nvd.nist.gov/vuln/detail/CVE-2024-23342), [GHSA-wj6h-64fc-37mp](https://github.com/advisories/GHSA-wj6h-64fc-37mp) (Minerva timing side-channel attack on P-256; upstream maintains side channels are out of scope with no fix planned) | **High** (CWE-203, CWE-208, CWE-385) | **Remediated & Deprecated** |
| **`rsa`** (`python-rsa`) | `< 4.7` | `^4.9` | [CVE-2020-25658](https://nvd.nist.gov/vuln/detail/CVE-2020-25658), [CVE-2020-13757](https://nvd.nist.gov/vuln/detail/CVE-2020-13757) (Bleichenbacher timing attack vulnerability) | **High** | **Remediated & Pinned** |
| **`cryptography`** | `< 42.0.0` | `^43.0.3` | GHSA-9v9w-xw87-7455 (NULL pointer dereference in PKCS12 parsing) | **Medium** | **Remediated & Pinned** |
| **`fastapi`** | `< 0.110.0` | `^0.115.0` | Dependency update & ReDoS hardening on multi-part forms | **Low** | **Remediated & Pinned** |

---

## 2. JavaScript / Tooling Audit Matrix

| Package | Old Version | New Version | Advisory / CVE | Severity | Status |
| :--- | :---: | :---: | :--- | :---: | :--- |
| **`@vitest/mocker`** | `< 4.1.11` | `^4.1.11` | [CVE-2026-84373](https://github.com/advisories/GHSA-82fw-gwwq-j7x9), [GHSA-82fw-gwwq-j7x9](https://github.com/advisories/GHSA-82fw-gwwq-j7x9) (Path Traversal / Arbitrary File Read via redirect mock handler) | **Moderate** (CWE-22) | **Remediated & Pinned** |
| **`vitest`** | `< 4.1.11` | `^4.1.11` | Core test runner bundle incorporating patched `@vitest/mocker` $\ge 4.1.11$ | **Moderate** | **Remediated & Pinned** |

---

## 3. Cryptographic Architecture Note: Why `python-ecdsa` was Removed

The pure-Python `python-ecdsa` library is vulnerable to the **Minerva timing side-channel attack (CVE-2024-23342)** when computing signatures on the P-256 curve (`ecdsa.SigningKey.sign_digest()`). Because upstream `python-ecdsa` declared side-channel timing leaks permanently out of scope (with `Patched version: None`), any presence in a dependency tree triggers an unfixable security alert.

DocuTask Agent's cryptographic architecture uses:
1. **`cryptography>=43.0.3`**: Native OpenSSL/BoringSSL C/Rust bindings featuring constant-time scalar multiplication and side-channel immunity.
2. **`python-jose[cryptography]>=3.3.0`**: Cryptographic backend for JWT generation and verification using `cryptography` primitives instead of pure-Python math.
3. **Removal of `python-ecdsa` & orphaned `poetry.lock`**: Completely eliminates the vulnerability footprint and resolves Dependabot Alert #4.
