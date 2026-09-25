"""
Autonomous Resource Intelligence, Adaptive Optimization & Economic Orchestration Platform (ARIA-EOP).
Phase 13.6: Provides mathematical multi-objective decision optimization, economic and ROI estimation,
resource inventory tracking, policy-driven model and tool routing, Monte-Carlo strategy simulation,
adaptive deadline-aware scheduling, probabilistic latency/cost prediction, and SLA governance.
"""

# Legacy imports preserved for backward compatibility
from app.runtime.optimization.objective_functions import ObjectiveFunctions
from app.runtime.optimization.pareto_optimizer import ParetoPlan, ParetoOptimizer
from app.runtime.optimization.optimization_statistics import OptimizationStatistics
from app.runtime.optimization.optimization_history import OptimizationRunRecord, OptimizationHistoryTracker, optimization_history
from app.runtime.optimization.optimization_serializer import OptimizationSerializer
from app.runtime.optimization.optimizer_validator import OptimizerValidator
from app.runtime.optimization.optimizer import MultiObjectivePlanOptimizer

# Phase 13.6 Domain Events
from app.runtime.optimization.events.optimization_events import (
    OptimizationDomainEvent,
    BaseOptimizationEvent,
    OptimizationStarted,
    OptimizationCompleted,
    StrategyEvaluated,
    ResourceAllocated,
    ModelSelected,
    WorkerSelected,
    BudgetReserved,
    BudgetExceeded,
    ConstraintViolated,
    SimulationCompleted,
    OptimizationRejected,
    OptimizationApplied,
)

# Phase 13.6 Optimization Core
from app.runtime.optimization.optimization.optimization_engine import OptimizationEngine, optimization_engine
from app.runtime.optimization.optimization.optimization_pipeline import OptimizationPipeline, OptimizationReport
from app.runtime.optimization.optimization.strategy_selector import StrategySelector, CandidateExecutionStrategy
from app.runtime.optimization.optimization.constraint_solver import ConstraintSolver, ConstraintCheckResult
from app.runtime.optimization.optimization.decision_optimizer import DecisionOptimizer, OptimizationDecision
from app.runtime.optimization.optimization.execution_optimizer import ExecutionOptimizer, ExecutionDirective

# Phase 13.6 Economic Intelligence
from app.runtime.optimization.economics.economic_engine import EconomicEngine, economic_engine, FullEconomicProfile
from app.runtime.optimization.economics.cost_model import CostModel, UnitCostBreakdown
from app.runtime.optimization.economics.value_estimator import ValueEstimator, ValueEstimation
from app.runtime.optimization.economics.roi_engine import ROIEngine, ROIMetrics
from app.runtime.optimization.economics.business_priority import BusinessPriority, PriorityWeights
from app.runtime.optimization.economics.budget_allocator import BudgetAllocator, budget_allocator, BudgetReservation

# Phase 13.6 Resource Management
from app.runtime.optimization.resource.resource_registry import ResourceRegistry, resource_registry, ResourceNode
from app.runtime.optimization.resource.capacity_manager import CapacityManager, CapacityStatus
from app.runtime.optimization.resource.allocation_engine import AllocationEngine, allocation_engine, AllocationTicket

# Phase 13.6 Policy-Driven Routing
from app.runtime.optimization.routing.model_router import ModelRouter, OCRRouter, ValidationRouter, RouteDecision

# Phase 13.6 Monte-Carlo Simulation
from app.runtime.optimization.simulation.execution_simulator import ExecutionSimulator, ScenarioSimulationResult, WhatIfEngine

# Phase 13.6 Adaptive Scheduling
from app.runtime.optimization.scheduling.adaptive_scheduler import AdaptiveScheduler, SchedulePlan

# Phase 13.6 Predictive Analytics
from app.runtime.optimization.prediction.latency_predictor import LatencyPredictor, PredictionReport

# Phase 13.6 Governance & Policies
from app.runtime.optimization.policies.optimization_policy import OptimizationPolicySpec, PolicyValidator

__all__ = [
    # Legacy
    "ObjectiveFunctions",
    "ParetoPlan",
    "ParetoOptimizer",
    "OptimizationStatistics",
    "OptimizationRunRecord",
    "OptimizationHistoryTracker",
    "optimization_history",
    "OptimizationSerializer",
    "OptimizerValidator",
    "MultiObjectivePlanOptimizer",
    # Events
    "OptimizationDomainEvent",
    "BaseOptimizationEvent",
    "OptimizationStarted",
    "OptimizationCompleted",
    "StrategyEvaluated",
    "ResourceAllocated",
    "ModelSelected",
    "WorkerSelected",
    "BudgetReserved",
    "BudgetExceeded",
    "ConstraintViolated",
    "SimulationCompleted",
    "OptimizationRejected",
    "OptimizationApplied",
    # Optimization Core
    "OptimizationEngine",
    "optimization_engine",
    "OptimizationPipeline",
    "OptimizationReport",
    "StrategySelector",
    "CandidateExecutionStrategy",
    "ConstraintSolver",
    "ConstraintCheckResult",
    "DecisionOptimizer",
    "OptimizationDecision",
    "ExecutionOptimizer",
    "ExecutionDirective",
    # Economics
    "EconomicEngine",
    "economic_engine",
    "FullEconomicProfile",
    "CostModel",
    "UnitCostBreakdown",
    "ValueEstimator",
    "ValueEstimation",
    "ROIEngine",
    "ROIMetrics",
    "BusinessPriority",
    "PriorityWeights",
    "BudgetAllocator",
    "budget_allocator",
    "BudgetReservation",
    # Resource
    "ResourceRegistry",
    "resource_registry",
    "ResourceNode",
    "CapacityManager",
    "CapacityStatus",
    "AllocationEngine",
    "allocation_engine",
    "AllocationTicket",
    # Routing
    "ModelRouter",
    "OCRRouter",
    "ValidationRouter",
    "RouteDecision",
    # Simulation
    "ExecutionSimulator",
    "ScenarioSimulationResult",
    "WhatIfEngine",
    # Scheduling
    "AdaptiveScheduler",
    "SchedulePlan",
    # Prediction
    "LatencyPredictor",
    "PredictionReport",
    # Policies
    "OptimizationPolicySpec",
    "PolicyValidator",
]
