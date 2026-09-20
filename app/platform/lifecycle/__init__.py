"""
Platform Lifecycle Management Package.
"""

from .component import ILifecycleComponent, BaseLifecycleComponent
from .manager import LifecycleManager

__all__ = [
    "ILifecycleComponent",
    "BaseLifecycleComponent",
    "LifecycleManager",
]
