"""CQRS Query Models and Filter Providers for Platform Delivery Control Plane."""
from dataclasses import dataclass
from typing import Optional


@dataclass
class GetDeploymentQuery:
    """Query to retrieve a deployment record by ID."""
    deployment_id: str


@dataclass
class ListDeploymentsQuery:
    """Query to list deployments matching criteria."""
    environment_id: Optional[str] = None
    status: Optional[str] = None
    application: Optional[str] = None
    limit: int = 50


@dataclass
class GetReleaseQuery:
    """Query to retrieve a release by version or ID."""
    release_id: Optional[str] = None
    version: Optional[str] = None


@dataclass
class GetArtifactQuery:
    """Query to retrieve artifact details and supply chain evidence."""
    digest: str
