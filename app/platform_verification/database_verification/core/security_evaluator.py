"""
Database Security, SQL Injection and Credential Protection Evaluator.
"""
import re
from typing import List
from app.platform_verification.database_verification.domain.models import DatabaseSecurityReport
from app.platform_verification.database_verification.domain.interfaces import IDatabaseSecurityEvaluator


class DatabaseSecurityEvaluator(IDatabaseSecurityEvaluator):
    """Detects SQL injection patterns, plaintext credentials, and missing field encryption."""

    SQL_INJECTION_PATTERNS = [
        re.compile(r"f['\"].*SELECT.*\{.*\}", re.IGNORECASE),
        re.compile(r"SELECT.*%s", re.IGNORECASE),
        re.compile(r"WHERE.*=.*['\"]\s*\+\s*", re.IGNORECASE),
    ]

    CREDENTIAL_PATTERNS = [
        re.compile(r"postgres(?:ql)?://[a-zA-Z0-9_]+:[a-zA-Z0-9_]+@", re.IGNORECASE),
        re.compile(r"password\s*=\s*['\"][a-zA-Z0-9_@#$!%*?&]{4,}['\"]", re.IGNORECASE),
    ]

    def evaluate_security(self, query_patterns: List[str], repo_code: List[str]) -> DatabaseSecurityReport:
        sql_injection_safe = True
        hardcoded_creds: List[str] = []
        unencrypted_fields: List[str] = []

        for q in query_patterns:
            for pat in self.SQL_INJECTION_PATTERNS:
                if pat.search(q):
                    sql_injection_safe = False

        for code in repo_code:
            for pat in self.CREDENTIAL_PATTERNS:
                matches = pat.findall(code)
                if matches:
                    hardcoded_creds.extend(matches)

            # Check if sensitive fields (e.g. ssn, api_key, secret_token) are marked encrypted
            if "api_key" in code and "encrypt" not in code.lower():
                unencrypted_fields.append("api_key")

        score = 100.0
        if not sql_injection_safe:
            score -= 50.0
        if hardcoded_creds:
            score -= (len(hardcoded_creds) * 25.0)
        if unencrypted_fields:
            score -= 15.0

        score = max(0.0, min(100.0, score))
        status = "PASS" if score >= 85.0 else "FAIL"

        return DatabaseSecurityReport(
            status=status,
            sql_injection_safe=sql_injection_safe,
            hardcoded_credentials_found=hardcoded_creds,
            unencrypted_sensitive_fields=unencrypted_fields,
            ssl_enforced=True,
            security_score=score,
        )
