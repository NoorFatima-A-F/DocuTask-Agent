"""
Universal Connector Engine for Phase 13.15.
Manages persistent external system connections, protocols, authentication bindings, and health telemetry.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
import json
import time
from typing import Any, Dict, List, Optional
import uuid

from app.runtime.execution.events.execution_events import (
    ConnectorCategory,
    ConnectorStatus,
    ExecutionEvent,
    ExecutionEventType,
    RiskLevel,
    execution_event_bus,
)


@dataclass
class ConnectorConfig:
    connector_id: str
    name: str
    category: ConnectorCategory
    protocol: str  # https, graphql, grpc, postgresql, aws_sdk, gcp_sdk, slack_web, github_api
    endpoint_url: str
    credential_id: Optional[str] = None
    status: ConnectorStatus = ConnectorStatus.CONNECTED
    health_score: float = 0.98
    latency_ms: float = 32.0
    rate_limit_rpm: int = 120
    rpm_used: int = 12
    max_concurrency: int = 25
    active_connections: int = 2
    metadata: Dict[str, Any] = field(default_factory=dict)
    last_health_check: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "connector_id": self.connector_id,
            "name": self.name,
            "category": self.category.value if isinstance(self.category, ConnectorCategory) else str(self.category),
            "protocol": self.protocol,
            "endpoint_url": self.endpoint_url,
            "credential_id": self.credential_id,
            "status": self.status.value if isinstance(self.status, ConnectorStatus) else str(self.status),
            "health_score": round(self.health_score, 3),
            "latency_ms": round(self.latency_ms, 2),
            "rate_limit_rpm": self.rate_limit_rpm,
            "rpm_used": self.rpm_used,
            "max_concurrency": self.max_concurrency,
            "active_connections": self.active_connections,
            "metadata": self.metadata,
            "last_health_check": self.last_health_check,
            "created_at": self.created_at,
        }


class ConnectorEngine:
    """Manages integration connectors for the external world."""

    def __init__(self):
        self._connectors: Dict[str, ConnectorConfig] = {}
        self._initialize_seed_connectors()

    def _initialize_seed_connectors(self) -> None:
        seed_connectors = [
            ConnectorConfig(
                connector_id="conn_github_enterprise",
                name="GitHub Enterprise Gateway",
                category=ConnectorCategory.CODE_REPOSITORY,
                protocol="github_api",
                endpoint_url="https://api.github.com",
                credential_id="cred_github_pat_org",
                status=ConnectorStatus.CONNECTED,
                health_score=0.99,
                latency_ms=45.2,
                rate_limit_rpm=300,
                rpm_used=24,
                metadata={"org": "enterprise-corp", "api_version": "2022-11-28"},
            ),
            ConnectorConfig(
                connector_id="conn_slack_ops",
                name="Slack Operations Bot",
                category=ConnectorCategory.COMMUNICATION,
                protocol="slack_web",
                endpoint_url="https://slack.com/api",
                credential_id="cred_slack_bot_token",
                status=ConnectorStatus.CONNECTED,
                health_score=1.0,
                latency_ms=28.4,
                rate_limit_rpm=100,
                rpm_used=8,
                metadata={"default_channel": "#autonomous-ops-feed"},
            ),
            ConnectorConfig(
                connector_id="conn_k8s_production",
                name="Kubernetes Production Cluster Control Plane",
                category=ConnectorCategory.INFRASTRUCTURE,
                protocol="k8s_api",
                endpoint_url="https://k8s-prod-control.corp.internal:6443",
                credential_id="cred_k8s_service_account",
                status=ConnectorStatus.CONNECTED,
                health_score=0.97,
                latency_ms=18.6,
                rate_limit_rpm=600,
                rpm_used=52,
                metadata={"cluster_version": "v1.29.2", "nodes_count": 48},
            ),
            ConnectorConfig(
                connector_id="conn_aws_us_east_1",
                name="AWS us-east-1 Regional SDK",
                category=ConnectorCategory.CLOUD,
                protocol="aws_sdk",
                endpoint_url="https://us-east-1.amazonaws.com",
                credential_id="cred_aws_iam_role",
                status=ConnectorStatus.CONNECTED,
                health_score=0.995,
                latency_ms=36.1,
                rate_limit_rpm=1200,
                rpm_used=110,
                metadata={"region": "us-east-1", "account_id": "847291038102"},
            ),
            ConnectorConfig(
                connector_id="conn_postgres_warehouse",
                name="Enterprise Analytics PostgreSQL",
                category=ConnectorCategory.DATABASE,
                protocol="postgresql",
                endpoint_url="postgresql://db.prod.internal:5432/analytics_dw",
                credential_id="cred_db_service_user",
                status=ConnectorStatus.CONNECTED,
                health_score=0.985,
                latency_ms=12.4,
                rate_limit_rpm=2000,
                rpm_used=145,
                metadata={"engine": "PostgreSQL 16.2", "pool_size": 30},
            ),
            ConnectorConfig(
                connector_id="conn_stripe_billing",
                name="Stripe Global Merchant Gateway",
                category=ConnectorCategory.PAYMENT_FINANCE,
                protocol="https",
                endpoint_url="https://api.stripe.com/v1",
                credential_id="cred_stripe_restricted_key",
                status=ConnectorStatus.CONNECTED,
                health_score=0.99,
                latency_ms=54.7,
                rate_limit_rpm=150,
                rpm_used=14,
                metadata={"mode": "live", "webhook_configured": True},
            ),
            ConnectorConfig(
                connector_id="conn_browser_headless_pool",
                name="Playwright Headless Cluster",
                category=ConnectorCategory.BROWSER_VISION,
                protocol="cdp_playwright",
                endpoint_url="ws://browser-cluster.corp.internal:9222",
                status=ConnectorStatus.CONNECTED,
                health_score=0.96,
                latency_ms=68.0,
                rate_limit_rpm=60,
                rpm_used=5,
                metadata={"pool_capacity": 16, "chromium_version": "124.0.0"},
            ),
        ]
        for c in seed_connectors:
            self._connectors[c.connector_id] = c

    def create_connector(self, config: ConnectorConfig) -> ConnectorConfig:
        self._connectors[config.connector_id] = config
        execution_event_bus.publish(
            ExecutionEvent(
                event_type=ExecutionEventType.CONNECTOR_CREATED,
                source="connector_engine",
                payload={"connector_id": config.connector_id, "name": config.name, "category": config.category},
                risk_level=RiskLevel.LOW,
            )
        )
        return config

    def get_connector(self, connector_id: str) -> Optional[ConnectorConfig]:
        return self._connectors.get(connector_id)

    def list_connectors(self, category: Optional[str] = None, status: Optional[str] = None) -> List[ConnectorConfig]:
        items = list(self._connectors.values())
        if category:
            items = [c for c in items if (c.category.value if isinstance(c.category, ConnectorCategory) else str(c.category)).lower() == category.lower()]
        if status:
            items = [c for c in items if (c.status.value if isinstance(c.status, ConnectorStatus) else str(c.status)).lower() == status.lower()]
        return items

    def test_connection(self, connector_id: str) -> Dict[str, Any]:
        connector = self.get_connector(connector_id)
        if not connector:
            return {"success": False, "error": f"Connector {connector_id} not found"}

        # Simulate round-trip network probe & latency check
        start_time = time.time()
        # Simulated check
        latency = (time.time() - start_time) * 1000.0 + 15.0  # ms
        connector.latency_ms = (connector.latency_ms * 0.7) + (latency * 0.3)
        connector.status = ConnectorStatus.CONNECTED
        connector.last_health_check = datetime.now(timezone.utc).isoformat()
        connector.health_score = min(1.0, max(0.8, connector.health_score + 0.01))

        execution_event_bus.publish(
            ExecutionEvent(
                event_type=ExecutionEventType.CONNECTOR_AUTHENTICATED,
                source="connector_engine",
                payload={"connector_id": connector_id, "latency_ms": latency, "status": connector.status.value},
            )
        )

        return {
            "success": True,
            "connector_id": connector_id,
            "status": connector.status.value,
            "latency_ms": round(connector.latency_ms, 2),
            "last_health_check": connector.last_health_check,
            "endpoint": connector.endpoint_url,
        }

    def get_summary(self) -> Dict[str, Any]:
        connectors = list(self._connectors.values())
        total = len(connectors)
        connected = sum(1 for c in connectors if c.status == ConnectorStatus.CONNECTED)
        by_category = {}
        for c in connectors:
            cat = c.category.value if isinstance(c.category, ConnectorCategory) else str(c.category)
            by_category[cat] = by_category.get(cat, 0) + 1

        return {
            "total_connectors": total,
            "connected_count": connected,
            "categories": by_category,
            "average_latency_ms": round(sum(c.latency_ms for c in connectors) / total, 2) if total else 0.0,
        }


# Global Singleton
connector_engine = ConnectorEngine()
