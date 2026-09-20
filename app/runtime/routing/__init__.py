"""
Scientific Model Routing Package.
Provides multi-attribute utility optimization for model selection and provenance recording.
"""

from app.runtime.routing.routing_statistics import ModelRoutingStatistics, routing_statistics
from app.runtime.routing.routing_history import ModelRoutingDecisionRecord, ModelRoutingHistory, routing_history
from app.runtime.routing.routing_validator import RoutingValidator
from app.runtime.routing.routing_optimizer import ModelProfile, AVAILABLE_MODELS, RoutingOptimizer
from app.runtime.routing.model_router import ScientificModelRouter

__all__ = [
    "ModelRoutingStatistics",
    "routing_statistics",
    "ModelRoutingDecisionRecord",
    "ModelRoutingHistory",
    "routing_history",
    "RoutingValidator",
    "ModelProfile",
    "AVAILABLE_MODELS",
    "RoutingOptimizer",
    "ScientificModelRouter",
]
