"""
Automated Security Tests for URL & Network Target Validation.
Validates CWE-20, SSRF defenses, scheme restrictions, and prefix-collision attack prevention.
"""

import pytest
from app.core.security import validate_safe_url, UnsafeUrlError
from app.connectors.sandbox.sandbox import ConnectorSandbox, SandboxConfig
from app.connectors.core.exceptions import SandboxViolationError


class TestURLValidation:
    """Test suite for URL parsing and validation primitives."""

    def test_valid_allowed_domain_url(self):
        """Verify valid URLs with allowed domain pass validation."""
        url = "https://api.trusted.com/v1/documents"
        validated = validate_safe_url(url, allowed_domains=["trusted.com"])
        assert validated == url

    def test_subdomain_allowed(self):
        """Verify subdomains of allowed domain are permitted."""
        url = "https://sub.service.trusted.com/callback"
        validated = validate_safe_url(url, allowed_domains=["trusted.com"])
        assert validated == url

    def test_prefix_collision_attack_rejected(self):
        """
        Verify prefix collision attacks (e.g. trusted.com.attacker.com or trusted.com-evil.org)
        are strictly rejected and not confused with trusted.com.
        """
        attacker_url1 = "https://trusted.com.attacker.com/steal"
        attacker_url2 = "https://trusted.com-attacker.org/steal"

        with pytest.raises(UnsafeUrlError) as exc1:
            validate_safe_url(attacker_url1, allowed_domains=["trusted.com"])
        assert "not in allowed domains" in str(exc1.value)

        with pytest.raises(UnsafeUrlError) as exc2:
            validate_safe_url(attacker_url2, allowed_domains=["trusted.com"])
        assert "not in allowed domains" in str(exc2.value)

    def test_disallowed_domain_rejected(self):
        """Verify disallowed domains and subdomains are blocked."""
        disallowed_url = "https://evil.org/malware"
        with pytest.raises(UnsafeUrlError) as exc:
            validate_safe_url(disallowed_url, disallowed_domains=["evil.org"])
        assert "matches disallowed domain" in str(exc.value)

        disallowed_sub = "https://c2.evil.org/ping"
        with pytest.raises(UnsafeUrlError):
            validate_safe_url(disallowed_sub, disallowed_domains=["evil.org"])

    def test_forbidden_schemes_rejected(self):
        """Verify dangerous schemes like javascript:, file:, ftp:, data: are rejected."""
        dangerous_urls = [
            "javascript:alert(document.cookie)",
            "file:///etc/passwd",
            "ftp://ftp.example.com/dump.tar",
            "data:text/html,<script>alert(1)</script>",
        ]
        for bad_url in dangerous_urls:
            with pytest.raises(UnsafeUrlError) as exc:
                validate_safe_url(bad_url, allowed_domains=["example.com"])
            assert "is not permitted" in str(exc.value) or "has no valid hostname" in str(exc.value)

    def test_missing_or_empty_url(self):
        """Verify empty or non-string URLs raise UnsafeUrlError."""
        with pytest.raises(UnsafeUrlError):
            validate_safe_url("")
        with pytest.raises(UnsafeUrlError):
            validate_safe_url(None)  # type: ignore

    def test_custom_allowed_schemes(self):
        """Verify custom allowed schemes work as configured."""
        url = "http://internal.service.local/api"
        # http permitted by default
        assert validate_safe_url(url, allowed_domains=["service.local"]) == url
        # only https allowed
        with pytest.raises(UnsafeUrlError):
            validate_safe_url(url, allowed_domains=["service.local"], allowed_schemes={"https"})


class TestConnectorSandboxNetworkTargetValidation:
    """Test suite for ConnectorSandbox network target domain policy enforcement."""

    def test_sandbox_allows_whitelisted_domain(self):
        config = SandboxConfig(allowed_domains=["trusted-api.com"])
        sandbox = ConnectorSandbox(config)
        # Should not raise
        sandbox.validate_network_target("https://trusted-api.com/v1/resource")
        sandbox.validate_network_target("https://sub.trusted-api.com/v1/resource")

    def test_sandbox_blocks_prefix_collision(self):
        config = SandboxConfig(allowed_domains=["trusted-api.com"])
        sandbox = ConnectorSandbox(config)
        with pytest.raises(SandboxViolationError):
            sandbox.validate_network_target("https://trusted-api.com.attacker.com/v1")

    def test_sandbox_blocks_disallowed_domain(self):
        config = SandboxConfig(disallowed_domains=["malicious.com"])
        sandbox = ConnectorSandbox(config)
        with pytest.raises(SandboxViolationError):
            sandbox.validate_network_target("https://malicious.com/endpoint")
        with pytest.raises(SandboxViolationError):
            sandbox.validate_network_target("https://bot.malicious.com/endpoint")
