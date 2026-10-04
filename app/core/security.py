"""
Security & Cryptography Core Module.
Provides password hashing via bcrypt, JWT token generation/decoding, and token hashing.
"""

import hashlib
import os
import re
from pathlib import Path
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional, Set, Union
try:
    from jose import JWTError, jwt
except ImportError:
    try:
        import jwt
        class JWTError(Exception):
            pass
    except ImportError:
        jwt = None
        class JWTError(Exception):
            pass

from app.core.config import settings
from app.core.exceptions import TokenException

PROHIBITED_SECRETS = {"changeme", "secret", "password", "123456", "admin", "default", "placeholder"}


def validate_secret_key_strength(secret_key: str) -> bool:
    """
    Validates secret key strength: length >= 32 chars and not in prohibited set.
    Raises ValueError if key is weak.
    """
    if len(secret_key) < 32:
        raise ValueError("Security Violation: Secret key must be at least 32 characters long.")
    if secret_key.lower().strip() in PROHIBITED_SECRETS:
        raise ValueError(f"Security Violation: Prohibited secret key '{secret_key}' detected.")
    return True


class UnsafePathError(ValueError):
    """Raised when a path traversal, directory escape, or malicious segment attempt is detected."""
    pass


class UnsafeUrlError(ValueError):
    """Raised when an untrusted, malformed, or SSRF-prone URL is detected."""
    pass


PathInput = Union[str, Path, os.PathLike]


def validate_safe_url(
    url: str,
    allowed_domains: Optional[Union[List[str], Set[str]]] = None,
    disallowed_domains: Optional[Union[List[str], Set[str]]] = None,
    allowed_schemes: Optional[Set[str]] = None,
) -> str:
    """
    Validates and parses a URL, enforcing allowed schemes (http, https) and strict
    domain/hostname matching without substring vulnerability (CWE-20 / SSRF prevention).
    Rejects prefix collision attacks (e.g. 'https://trusted.com.attacker.com').
    """
    import urllib.parse

    if not url or not isinstance(url, str):
        raise UnsafeUrlError("URL cannot be empty or non-string.")

    schemes = allowed_schemes or {"http", "https"}
    parsed = urllib.parse.urlparse(url.strip())

    if not parsed.scheme or parsed.scheme.lower() not in schemes:
        raise UnsafeUrlError(f"Security violation: Scheme '{parsed.scheme}' is not permitted (allowed: {sorted(schemes)}).")

    hostname = (parsed.hostname or "").lower().strip()
    if not hostname:
        raise UnsafeUrlError(f"Security violation: URL '{url}' has no valid hostname.")

    if disallowed_domains:
        for disallowed in disallowed_domains:
            dis_d = disallowed.lower().strip()
            if hostname == dis_d or hostname.endswith("." + dis_d):
                raise UnsafeUrlError(f"Security violation: Hostname '{hostname}' matches disallowed domain '{disallowed}'.")

    if allowed_domains is not None:
        matched = False
        for allowed in allowed_domains:
            al_d = allowed.lower().strip()
            if hostname == al_d or hostname.endswith("." + al_d):
                matched = True
                break
        if not matched:
            raise UnsafeUrlError(f"Security violation: Hostname '{hostname}' is not in allowed domains {allowed_domains}.")

    return url


def validate_safe_filename_segment(value: str) -> str:
    r"""
    Validates and sanitizes a single filename segment (report ID, runbook ID, evidence ID, etc.).
    Rejects path traversal characters (/ \ .. null bytes).
    """
    if not value or not isinstance(value, str):
        raise UnsafePathError("Filename segment cannot be empty or non-string.")
    if "\x00" in value or "/" in value or "\\" in value or ".." in value:
        raise UnsafePathError(f"Security violation: Filename segment contains illegal path traversal characters: '{value}'")
    sanitized = re.sub(r"[^a-zA-Z0-9_.\-]", "_", value.strip())
    if not sanitized or sanitized in (".", ".."):
        raise UnsafePathError(f"Security violation: Invalid filename segment '{value}'")
    return sanitized


def resolve_safe_path(
    base_dir: PathInput,
    untrusted_path: PathInput,
    *,
    allow_base: bool = True,
) -> Path:
    """
    CodeQL recognized pattern for py/path-injection prevention.
    Relies on os.path.commonpath boundary verification and strict token parsing.
    """
    if untrusted_path is None:
        raise UnsafePathError("Empty or None path provided")

    untrusted_str = str(untrusted_path).strip()
    if not untrusted_str:
        raise UnsafePathError("Empty path provided")

    if "\x00" in untrusted_str:
        raise UnsafePathError("Null byte detected in path expression")

    # 1. Reject Windows-style drive letters (e.g., C:\...)
    if len(untrusted_str) >= 2 and untrusted_str[1] == ":" and untrusted_str[0].isalpha():
        raise UnsafePathError(f"Security violation: Candidate path '{untrusted_path}' escapes trusted base directory '{base_dir}'")

    # 2. Normalize backslashes to forward slashes to defend against Windows-style traversal on POSIX
    normalized = untrusted_str.replace("\\", "/")

    # 3. Check for raw absolute paths
    if normalized.startswith("/") or Path(normalized).is_absolute():
        raise UnsafePathError(f"Security violation: Candidate path '{untrusted_path}' escapes trusted base directory '{base_dir}'")

    # 4. Check for traversal tokens
    parts = [p for p in normalized.split("/") if p]
    if ".." in parts:
        raise UnsafePathError(f"Security violation: Candidate path '{untrusted_path}' escapes trusted base directory '{base_dir}'")

    if normalized == ".":
        if allow_base:
            return Path(os.path.abspath(str(base_dir)))
        raise UnsafePathError("Security violation: Candidate path matches base directory when allow_base=False")

    base = os.path.abspath(str(base_dir))
    target = os.path.abspath(os.path.join(base, *parts))

    try:
        common = os.path.commonpath([base, target])
    except ValueError:
        raise UnsafePathError(f"Security violation: Candidate path '{untrusted_path}' escapes trusted base directory '{base_dir}'")

    if common != base:
        raise UnsafePathError(f"Security violation: Candidate path '{untrusted_path}' escapes trusted base directory '{base_dir}'")

    if target == base and not allow_base:
        raise UnsafePathError(f"Security violation: Candidate path '{untrusted_path}' escapes trusted base directory '{base_dir}'")

    return Path(target)


def sanitize_file_path(
    base_dir: PathInput,
    untrusted_path: PathInput,
    *,
    allow_base: bool = True,
) -> str:
    """
    CodeQL recognized pattern for py/path-injection prevention.
    Returns validated canonical path string.
    """
    safe_path = resolve_safe_path(base_dir, untrusted_path, allow_base=allow_base)
    return str(safe_path)


get_safe_path = resolve_safe_path


def sanitize_log_input(value: Any) -> str:
    """
    Sanitizes user/external input for safe logging by removing newline/CR characters (CWE-117).
    Prevents log injection / log forging.
    """
    if value is None:
        return ""
    clean = str(value).replace("\r", "_").replace("\n", "_")
    clean = re.sub(r"[\x00-\x1f\x7f-\x9f]", "_", clean)
    if len(clean) > 256:
        return clean[:253] + "..."
    return clean




try:
    import bcrypt

    def hash_password(password: str) -> str:
        """Hashes plain text password using bcrypt."""
        pwd_bytes = password.encode("utf-8")[:72]
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(pwd_bytes, salt).decode("utf-8")

    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verifies plain text password against bcrypt hash."""
        try:
            pwd_bytes = plain_password.encode("utf-8")[:72]
            return bcrypt.checkpw(pwd_bytes, hashed_password.encode("utf-8"))
        except Exception:
            return False
except ImportError:
    import hmac

    def hash_password(password: str) -> str:
        """Fallback PBKDF2 hashing when bcrypt is unavailable."""
        salt = b"docutask_pwd_salt_pbkdf2_v1"
        return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100000).hex()

    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Fallback PBKDF2 verification when bcrypt is unavailable."""
        computed = hash_password(plain_password)
        return hmac.compare_digest(computed, hashed_password)


def create_access_token(subject: str, expires_delta: Optional[timedelta] = None) -> str:
    """
    Creates JWT Access Token signed with application secret key.
    Includes unique JWT ID (jti) for collision-resistant token identification.
    
    :param subject: User ID or subject identifier
    :param expires_delta: Optional custom duration override
    :return: Encoded JWT string
    """
    now = datetime.now(timezone.utc)
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode: Dict[str, Any] = {
        "sub": str(subject),
        "jti": str(uuid.uuid4()),
        "exp": expire,
        "iat": now,
        "type": "access"
    }
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


def create_refresh_token(subject: str, expires_delta: Optional[timedelta] = None) -> tuple[str, datetime]:
    """
    Creates JWT Refresh Token with unique JWT ID (jti).
    
    :param subject: User ID or subject identifier
    :param expires_delta: Optional custom duration override
    :return: Tuple of (raw_refresh_token, expiration_datetime)
    """
    now = datetime.now(timezone.utc)
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    
    to_encode: Dict[str, Any] = {
        "sub": str(subject),
        "jti": str(uuid.uuid4()),
        "exp": expire,
        "iat": now,
        "type": "refresh"
    }
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt, expire


def hash_token(raw_token: str) -> str:
    """
    Computes SHA-256 hash of a raw token for secure database storage.
    Prevents cleartext token storage in the database.
    """
    return hashlib.sha256(raw_token.encode("utf-8")).hexdigest()


def decode_token(token: str, expected_type: str = "access") -> Dict[str, Any]:
    """
    Decodes and validates a JWT token.
    
    :param token: Raw JWT string
    :param expected_type: 'access' or 'refresh'
    :return: Payload dictionary if valid
    :raises TokenException: If decoding fails or token type mismatches
    """
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        token_type: str = payload.get("type", "")
        if token_type != expected_type:
            raise TokenException(f"Invalid token type. Expected {expected_type}, got {token_type}")
        
        subject: Optional[str] = payload.get("sub")
        if not subject:
            raise TokenException("Token missing subject identifier")
            
        return payload
    except JWTError as e:
        raise TokenException(f"Could not validate token: {str(e)}")
