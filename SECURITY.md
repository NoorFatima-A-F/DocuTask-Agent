# Security Policy

DocuTask Agent is designed for enterprise document intelligence and autonomous document processing. Security, confidentiality, and deterministic data integrity are core architectural priorities.

---

## 1. Supported Versions

Security updates and critical vulnerability patches are actively provided for the following release branches:

| Version | Supported | Status |
| :--- | :---: | :--- |
| **v1.x** | :white_check_mark: Yes | **Current Active Release (Supported)** |
| **< v1.0** | :x: No | Deprecated (Unsupported) |

---

## 2. Reporting a Vulnerability

We deeply appreciate responsible security research and take all vulnerability disclosures seriously. If you discover a vulnerability or potential security risk in DocuTask Agent, **please do not disclose it publicly via GitHub issues, pull requests, or public discussions.**

### Responsible Disclosure Process

1. **Private Reporting Channel**:
   - Open a private security advisory on GitHub under the [Security Advisories](https://github.com/NoorFatima-A-F/DocuTask-Agent/security/advisories) tab.
   - Or email the maintainer directly via GitHub profile: [@NoorFatima-A-F](https://github.com/NoorFatima-A-F).

2. **Required Report Information**:
   - **Type of Issue**: (e.g. Authentication bypass, privilege escalation, injection, SSRF, data leakage).
   - **Affected Components**: Specific endpoints, classes, or configuration files involved.
   - **Proof of Concept (PoC)**: Minimal, reproducible steps or script demonstrating the issue.
   - **Impact Assessment**: Estimated CVSS score and potential real-world consequences.

3. **Response & Remediation SLAs**:
   - **Initial Acknowledgement**: Within **48 hours** of report receipt.
   - **Triage & Severity Confirmation**: Within **5 business days**.
   - **Remediation & Patch Delivery**: Priority patch deployed according to CVSS severity (Critical: < 7 days, High: < 14 days, Medium: < 30 days).
   - **Public Advisory / CVE Release**: Coordinated disclosure after the patch is published (standard 90-day responsible disclosure window).

---

## 3. Security Scope & Control Architecture

The following operational and application domains are actively maintained within our security perimeter:

### 3.1 Authentication & Credential Hygiene
- **JWT Standard**: HMAC-SHA256 with cryptographically generated random keys (`JWT_SECRET`).
- **Token Format Verification**: Dynamic validation of authorization headers with algorithmic downgrade protection (explicitly blocks `alg: "none"`).
- **Zero Hardcoded Secrets**: All API keys (Google Gemini, OpenAI, Claude) and database credentials are read exclusively from environment variables or secure vault stores.

### 3.2 Authorization & Role-Based Access Control (RBAC)
- **Granular Scopes**: Role separation across `Viewer`, `Operator`, `Auditor`, and `Admin`.
- **Multi-Tenant Isolation**: Enforced row-level data segregation preventing cross-tenant document access.

### 3.3 Document Uploads & Content Sanitization
- **File Validation**: Strict MIME-type inspection, file size boundaries (capped at 50MB), and magic-byte validation (PDF, PNG, TIFF).
- **Path Traversal Protection**: Uploaded files are converted to immutable UUID identifiers, isolated from host file system paths.

### 3.4 AI Processing & LLM Pipeline Security
- **Strict Structured Outputs**: Pydantic schema validation for all LLM extractions, preventing ungrounded payload execution.
- **Prompt Injection Defense**: Multi-stage prompt sanitization isolating untrusted document content from system prompt directives.
- **Telemetry Redaction**: Automatic masking of PII, credit card numbers, CNICs, and API keys before metrics or logs are recorded.

### 3.5 Database & Storage Security
- **Parameterized Queries**: SQLAlchemy asynchronous ORM preventing SQL injection vulnerabilities.
- **ACID Transaction Boundaries**: Automated rollback handlers guaranteeing zero residual writes on mid-pipeline failures.

### 3.6 API Security
- **Rate Limiting**: Configurable token bucket rate limiting on public and inference endpoints.
- **CORS Configuration**: Explicit origin whitelist with credential protections.
