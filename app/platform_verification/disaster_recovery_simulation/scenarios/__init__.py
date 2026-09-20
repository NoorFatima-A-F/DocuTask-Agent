"""
Scenarios module for Disaster Recovery Simulation Framework.
"""
from app.platform_verification.disaster_recovery_simulation.scenarios.database_loss_scenario import (
    DatabaseLossScenario,
)
from app.platform_verification.disaster_recovery_simulation.scenarios.database_corruption_scenario import (
    DatabaseCorruptionScenario,
)
from app.platform_verification.disaster_recovery_simulation.scenarios.storage_failure_scenario import (
    StorageFailureScenario,
)
from app.platform_verification.disaster_recovery_simulation.scenarios.complete_destruction_scenario import (
    CompleteDestructionScenario,
)
from app.platform_verification.disaster_recovery_simulation.scenarios.cascade_failure_scenario import (
    CascadeFailureScenario,
)

__all__ = [
    "DatabaseLossScenario",
    "DatabaseCorruptionScenario",
    "StorageFailureScenario",
    "CompleteDestructionScenario",
    "CascadeFailureScenario",
]
