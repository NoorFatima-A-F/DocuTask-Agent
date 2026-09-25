"""
Credential & Secrets Engine for Phase 13.15.
Manages enterprise vaults, scoped credentials, OAuth tokens, and lease rotation.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional
import uuid

from app.runtime.execution.events.execution_events import CredentialType


@dataclass
class CredentialRecord:
    credential_id: str
    name: str
    cred_type: CredentialType
    target_system: str
    scopes: List[str] = field(default_factory=list)
    masked_value: str = "••••••••••••"
    _secret_encrypted: str = ""
    is_active: bool = True
    expires_at: Optional[str] = None
    last_rotated: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "credential_id": self.credential_id,
            "name": self.name,
            "cred_type": self.cred_type.value if isinstance(self.cred_type, CredentialType) else str(self.cred_type),
            "target_system": self.target_system,
            "scopes": self.scopes,
            "masked_value": self.masked_value,
            "is_active": self.is_active,
            "expires_at": self.expires_at,
            "last_rotated": self.last_rotated,
            "created_at": self.created_at,
        }


class CredentialEngine:
    """Manages vault secrets and credential lifecycle."""

    def __init__(self):
        self._credentials: Dict[str, CredentialRecord] = {}
        self._initialize_seed_credentials()

    def _initialize_seed_credentials(self) -> None:
        expiry_future = (datetime.now(timezone.utc) + timedelta(days=90)).isoformat()
        seeds = [
            CredentialRecord(
                credential_id="cred_github_pat_org",
                name="GitHub Enterprise Personal Access Token",
                cred_type=CredentialType.BEARER_TOKEN,
                target_system="api.github.com",
                scopes=["repo", "workflow", "read:org", "admin:repo_hook"],
                masked_value="ghp_••••••••••••x819",
                _secret_encrypted="ghp_mockSecretTokenForGithubRepoAutomation12345",
                expires_at=expiry_future,
            ),
            CredentialRecord(
                credential_id="cred_slack_bot_token",
                name="Slack Bot OAuth Token",
                cred_type=CredentialType.OAUTH2,
                target_system="slack.com",
                scopes=["chat:write", "channels:read", "files:write"],
                masked_value="xoxb-••••••••••••-9012",
                _secret_encrypted="xoxb-mockSlackBotTokenWithOperationsPrivileges",
                expires_at=expiry_future,
            ),
            CredentialRecord(
                credential_id="cred_k8s_service_account",
                name="Kubernetes Cluster Operator SA Token",
                cred_type=CredentialType.BEARER_TOKEN,
                target_system="k8s-prod-control.corp.internal",
                scopes=["deployments:update", "pods:get", "services:list"],
                masked_value="eyJh••••••••••••K91a",
                _secret_encrypted="mockK8sServiceAccountJwtToken1234567890",
                expires_at=expiry_future,
            ),
            CredentialRecord(
                credential_id="cred_aws_iam_role",
                name="AWS IAM Role Execution Credentials",
                cred_type=CredentialType.AWS_IAM,
                target_system="aws.amazon.com",
                scopes=["s3:PutObject", "s3:GetObject", "s3:DeleteObject", "cloudwatch:PutMetricData"],
                masked_value="ASIA••••••••••••7F8E",
                _secret_encrypted="AKIAIOSFODNN7EXAMPLEMOCKAWSKEY",
                expires_at=expiry_future,
            ),
            CredentialRecord(
                credential_id="cred_db_service_user",
                name="Postgres DW Database User",
                cred_type=CredentialType.API_KEY,
                target_system="db.prod.internal",
                scopes=["select", "insert", "update", "analytics_schema"],
                masked_value="pg_user_••••••••••••a31d",
                _secret_encrypted="superSecurePostgresServiceUserPassPhrase2026",
                expires_at=expiry_future,
            ),
            CredentialRecord(
                credential_id="cred_stripe_restricted_key",
                name="Stripe Restricted Invoicing Key",
                cred_type=CredentialType.API_KEY,
                target_system="api.stripe.com",
                scopes=["invoices:write", "customers:read"],
                masked_value="rk_live_••••••••••••94b2",
                _secret_encrypted="rk_live_mockStripeKeyForAutonomousInvoicing",
                expires_at=expiry_future,
            ),
        ]
        for c in seeds:
            self._credentials[c.credential_id] = c

    def add_credential(
        self,
        name: str,
        cred_type: CredentialType,
        target_system: str,
        raw_secret: str,
        scopes: Optional[List[str]] = None,
    ) -> CredentialRecord:
        cid = f"cred_{uuid.uuid4().hex[:8]}"
        masked = raw_secret[:4] + "••••••••••••" + raw_secret[-4:] if len(raw_secret) > 8 else "••••••••••••"
        rec = CredentialRecord(
            credential_id=cid,
            name=name,
            cred_type=cred_type,
            target_system=target_system,
            scopes=scopes or [],
            masked_value=masked,
            _secret_encrypted=raw_secret,
            expires_at=(datetime.now(timezone.utc) + timedelta(days=90)).isoformat(),
        )
        self._credentials[cid] = rec
        return rec

    def get_credential(self, credential_id: str) -> Optional[CredentialRecord]:
        return self._credentials.get(credential_id)

    def list_credentials(self) -> List[CredentialRecord]:
        return list(self._credentials.values())

    def rotate_credential(self, credential_id: str, new_secret: str) -> bool:
        rec = self.get_credential(credential_id)
        if not rec:
            return False
        rec._secret_encrypted = new_secret
        rec.masked_value = new_secret[:4] + "••••••••••••" + new_secret[-4:] if len(new_secret) > 8 else "••••••••••••"
        rec.last_rotated = datetime.now(timezone.utc).isoformat()
        rec.expires_at = (datetime.now(timezone.utc) + timedelta(days=90)).isoformat()
        return True

    def validate_credential(self, credential_id: str) -> Dict[str, Any]:
        rec = self.get_credential(credential_id)
        if not rec:
            return {"valid": False, "error": f"Credential {credential_id} not found."}
        if not rec.is_active:
            return {"valid": False, "error": "Credential has been deactivated."}
        return {"valid": True, "credential_id": rec.credential_id, "scopes": rec.scopes, "expires_at": rec.expires_at}


# Global Singleton
credential_engine = CredentialEngine()
