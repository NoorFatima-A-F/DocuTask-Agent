"""Enterprise Deployment Platform Exceptions."""

class DeploymentException(Exception):
    """Base exception for all deployment platform operations."""
    pass


class ReleaseException(DeploymentException):
    """Raised when release creation, validation, or lifecycle fails."""
    pass


class PromotionBlockedException(DeploymentException):
    """Raised when promotion policy criteria or approval gates are not met."""
    pass


class RollbackException(DeploymentException):
    """Raised when rollback execution or automated recovery fails."""
    pass


class MigrationException(DeploymentException):
    """Raised when database schema migration or validation fails."""
    pass


class FlagException(DeploymentException):
    """Raised when feature flag evaluation or configuration fails."""
    pass


class ArtifactValidationException(DeploymentException):
    """Raised when artifact checksum, signature, or SBOM fails validation."""
    pass


class ApprovalGateException(DeploymentException):
    """Raised when an approval gate is rejected, timed out, or unfulfilled."""
    pass


class StrategyExecutionException(DeploymentException):
    """Raised when a deployment strategy fails during execution."""
    pass
