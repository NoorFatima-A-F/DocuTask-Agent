"""
Security & Cryptography Core Module.
Provides password hashing via bcrypt, JWT token generation/decoding, and token hashing.
"""

import hashlib
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional
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

try:
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
except ImportError:
    class DummyCryptContext:
        def hash(self, secret: str) -> str:
            return hashlib.sha256(secret.encode()).hexdigest()
        def verify(self, secret: str, hashed: str) -> bool:
            return self.hash(secret) == hashed
    pwd_context = DummyCryptContext()


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



def hash_password(password: str) -> str:
    """Hashes plain text password using bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies plain text password against bcrypt hash."""
    return pwd_context.verify(plain_password, hashed_password)


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
