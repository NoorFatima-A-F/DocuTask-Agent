"""Workload Identity, SPIFFE ID Management, and SVID Token Handling."""

from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
import hashlib
import hmac
import json
import re
from typing import Any, Dict, Optional
import uuid


@dataclass
class SPIFFEIdentity:
    """Represents a validated SPIFFE Workload Identity."""
    trust_domain: str
    namespace: str
    service_account: str
    workload_name: str
    cluster_id: str = "cluster-alpha"
    region: str = "us-east-1"
    raw_spiffe_id: str = ""

    def __post_init__(self) -> None:
        if not self.raw_spiffe_id:
            self.raw_spiffe_id = f"spiffe://{self.trust_domain}/ns/{self.namespace}/sa/{self.service_account}"

    @classmethod
    def parse(cls, spiffe_id: str) -> Optional["SPIFFEIdentity"]:
        """Parse and validate a SPIFFE ID string (e.g. spiffe://docutask.internal/ns/default/sa/worker-01)."""
        pattern = r"^spiffe://([^/]+)/ns/([^/]+)/sa/([^/]+)$"
        match = re.match(pattern, spiffe_id)
        if not match:
            return None
        trust_domain, namespace, service_account = match.groups()
        return cls(
            trust_domain=trust_domain,
            namespace=namespace,
            service_account=service_account,
            workload_name=service_account,
            raw_spiffe_id=spiffe_id,
        )


@dataclass
class WorkloadSVID:
    """SPIFFE Verifiable Identity Document (SVID) cryptographic credential."""
    spiffe_id: SPIFFEIdentity
    token: str
    issued_at: datetime
    expires_at: datetime
    claims: Dict[str, Any] = field(default_factory=dict)

    @property
    def is_expired(self) -> bool:
        """Check if SVID token is expired."""
        return datetime.now(timezone.utc) > self.expires_at


class WorkloadIdentityManager:
    """Issues, parses, and cryptographically signs/validates Workload SVIDs."""

    def __init__(self, trust_domain: str = "docutask.internal", signing_secret: str = "secret-spiffe-signing-key-9f") -> None:
        self.trust_domain = trust_domain
        self.signing_secret = signing_secret.encode("utf-8")

    def create_identity(self, namespace: str, service_account: str, cluster_id: str = "cluster-alpha", region: str = "us-east-1") -> SPIFFEIdentity:
        """Construct a SPIFFE identity."""
        return SPIFFEIdentity(
            trust_domain=self.trust_domain,
            namespace=namespace,
            service_account=service_account,
            workload_name=service_account,
            cluster_id=cluster_id,
            region=region,
        )

    def issue_svid(self, identity: SPIFFEIdentity, ttl_seconds: int = 3600, custom_claims: Optional[Dict[str, Any]] = None) -> WorkloadSVID:
        """Generate and cryptographically sign an SVID."""
        now = datetime.now(timezone.utc)
        expires = now + timedelta(seconds=ttl_seconds)

        claims = {
            "sub": identity.raw_spiffe_id,
            "iss": f"spiffe://{self.trust_domain}",
            "iat": int(now.timestamp()),
            "exp": int(expires.timestamp()),
            "ns": identity.namespace,
            "sa": identity.service_account,
            "cluster": identity.cluster_id,
            "region": identity.region,
            "jti": uuid.uuid4().hex,
        }
        if custom_claims:
            claims.update(custom_claims)

        payload_bytes = json.dumps(claims, sort_keys=True).encode("utf-8")
        signature = hmac.new(self.signing_secret, payload_bytes, hashlib.sha256).hexdigest()
        token = f"{payload_bytes.hex()}.{signature}"

        return WorkloadSVID(
            spiffe_id=identity,
            token=token,
            issued_at=now,
            expires_at=expires,
            claims=claims,
        )

    def verify_svid(self, token: str) -> Optional[WorkloadSVID]:
        """Verify token signature and expiration, returning WorkloadSVID if valid."""
        parts = token.split(".")
        if len(parts) != 2:
            return None

        hex_payload, signature = parts
        try:
            payload_bytes = bytes.fromhex(hex_payload)
            expected_sig = hmac.new(self.signing_secret, payload_bytes, hashlib.sha256).hexdigest()
            if not hmac.compare_digest(signature, expected_sig):
                return None

            claims = json.loads(payload_bytes.decode("utf-8"))
            now_ts = int(datetime.now(timezone.utc).timestamp())
            if claims.get("exp", 0) < now_ts:
                return None

            identity = SPIFFEIdentity.parse(claims.get("sub", ""))
            if not identity:
                return None

            return WorkloadSVID(
                spiffe_id=identity,
                token=token,
                issued_at=datetime.fromtimestamp(claims.get("iat", 0), tz=timezone.utc),
                expires_at=datetime.fromtimestamp(claims.get("exp", 0), tz=timezone.utc),
                claims=claims,
            )
        except Exception:
            return None
