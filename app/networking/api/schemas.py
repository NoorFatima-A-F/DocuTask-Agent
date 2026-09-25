"""Pydantic Request & Response Schemas for Service Mesh APIs."""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class ServiceRegistrationRequest(BaseModel):
    service_name: str
    namespace: str = "default"
    display_name: str = ""
    description: str = ""
    mtls_required: bool = True
    timeout_ms: int = 5000
    tags: Dict[str, str] = Field(default_factory=dict)


class ServiceResponseSchema(BaseModel):
    service_name: str
    namespace: str
    display_name: str
    mtls_required: bool
    timeout_ms: int
    tags: Dict[str, str]


class EndpointRegistrationRequest(BaseModel):
    endpoint_id: str
    service_name: str
    host: str
    port: int
    namespace: str = "default"
    region: str = "us-central1"
    zone: str = "us-central1-a"
    weight: int = 100


class EndpointResponseSchema(BaseModel):
    endpoint_id: str
    service_name: str
    host: str
    port: int
    namespace: str
    region: str
    zone: str
    weight: int
    health: str


class PolicyCreateRequest(BaseModel):
    policy_id: str
    name: str
    namespace: str = "default"
    default_action: str = "DENY"
    source_service: str = "*"
    source_namespace: str = "*"
    target_service: str = "*"
    target_namespace: str = "default"
    allowed_methods: List[str] = Field(default_factory=lambda: ["*"])
    allowed_paths: List[str] = Field(default_factory=lambda: ["*"])
    action: str = "ALLOW"
    priority: int = 100


class RouteRuleCreateRequest(BaseModel):
    rule_id: str
    name: str
    target_service: str
    namespace: str = "default"
    path_prefix: str = "/"
    version: str = "v1"
    weight: int = 100
    priority: int = 100


class TrafficSplitRequest(BaseModel):
    split_id: str
    service_name: str
    namespace: str = "default"
    split_type: str = "WEIGHTED"
    splits: List[Dict[str, Any]] = Field(default_factory=list)
    shadow_version: Optional[str] = None
    shadow_percentage: float = 0.0


class CertificateIssueRequest(BaseModel):
    subject: str
    san_uris: List[str]
    validity_days: int = 30


class MeshCallRequest(BaseModel):
    target_service: str
    action: str
    payload: Dict[str, Any] = Field(default_factory=dict)
    target_namespace: str = "default"
    timeout_ms: float = 5000.0


class MeshCallResponse(BaseModel):
    status_code: int
    request_id: str
    duration_ms: float
    payload: Optional[Any] = None
    error_message: Optional[str] = None
