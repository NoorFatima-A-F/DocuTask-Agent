---
name: Security Vulnerability Report
about: Report a security vulnerability or sensitive finding privately
title: '[SECURITY] '
labels: 'security, priority-high'
assignees: 'NoorFatima-A-F'
---

> [!IMPORTANT]
> If this vulnerability affects a live production deployment or exposes customer data, please report it via the private channel in [SECURITY.md](../../SECURITY.md) instead of opening a public issue.

## Vulnerability Description
A clear and concise description of the security vulnerability.

## Component Affected
- [ ] Authentication & JWT Handling
- [ ] Authorization / Role-Based Access Control (RBAC)
- [ ] Document Upload Validation & Path Traversal
- [ ] LLM Prompt Injection & Output Grounding
- [ ] Database Query Execution / SQL Injection
- [ ] Supply Chain / Dependency Vulnerability

## Proof of Concept / Reproduction Steps
1. Send request with payload: `...`
2. Observe vulnerable behavior: `...`

## Impact Assessment
- Severity: (Critical / High / Medium / Low)
- Potential impact: (e.g. Unauthorized data access, privilege escalation, denial of service)

## Suggested Remediation
(Optional) Recommended fix or mitigation.
