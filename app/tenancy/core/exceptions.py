"""Enterprise SaaS Multi-Tenancy Structured Exceptions Hierarchy."""


class TenancyError(Exception):
    """Base exception for all SaaS multi-tenancy errors."""

    def __init__(self, message: str, details: dict | None = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}


class TenantNotFoundError(TenancyError):
    """Raised when an organization or tenant cannot be found."""
    pass


class WorkspaceNotFoundError(TenancyError):
    """Raised when a workspace cannot be located."""
    pass


class EnvironmentNotFoundError(TenancyError):
    """Raised when an environment cannot be found."""
    pass


class ProjectNotFoundError(TenancyError):
    """Raised when a project is not found."""
    pass


class CrossTenantViolationError(TenancyError):
    """Raised when an operation attempts unauthorized cross-tenant resource access."""
    pass


class QuotaExceededError(TenancyError):
    """Raised when a resource usage limit is exceeded."""
    pass


class SubscriptionExpiredError(TenancyError):
    """Raised when a subscription is suspended, inactive, or expired."""
    pass


class InvalidTenantStateError(TenancyError):
    """Raised when an invalid tenant lifecycle state transition is attempted."""
    pass


class DomainVerificationError(TenancyError):
    """Raised when custom domain DNS verification fails."""
    pass


class ComplianceViolationError(TenancyError):
    """Raised when an action violates the tenant's active compliance profile."""
    pass


class FeatureNotEntitledError(TenancyError):
    """Raised when a tenant attempts to access a feature not in their plan."""
    pass


class ProvisioningError(TenancyError):
    """Raised when automated tenant onboarding fails."""
    pass
