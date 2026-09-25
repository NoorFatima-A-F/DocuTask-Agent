"""
Phase 13.16: Autonomous World Modeling, Predictive Intelligence & Causal Reasoning Platform (AWMPICRP).
Defines Enums, 60+ Domain Events, data structures, and typed event bus.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Callable, Dict, List, Optional
import uuid


class WorldState(str, Enum):
    INITIALIZING = "initializing"
    OBSERVING = "observing"
    MODELING = "modeling"
    PREDICTING = "predicting"
    SIMULATING = "simulating"
    OPTIMIZING = "optimizing"
    STABLE = "stable"
    DEGRADED = "degraded"
    RECOVERING = "recovering"


class PredictionState(str, Enum):
    PENDING = "pending"
    ACTIVE = "active"
    VALIDATED = "validated"
    REJECTED = "rejected"
    EXPIRED = "expired"
    DRIFTED = "drifted"


class ForecastConfidence(str, Enum):
    VERY_LOW = "very_low"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"


class HypothesisStatus(str, Enum):
    FORMULATED = "formulated"
    TESTING = "testing"
    SUPPORTED = "supported"
    REFUTED = "refuted"
    INCONCLUSIVE = "inconclusive"


class CausalConfidence(str, Enum):
    SPECULATIVE = "speculative"
    CORRELATED = "correlated"
    PROBABLE_CAUSE = "probable_cause"
    PROVEN_CAUSE = "proven_cause"


class ScenarioStatus(str, Enum):
    GENERATED = "generated"
    SIMULATING = "simulating"
    COMPLETED = "completed"
    EVALUATED = "evaluated"


class KnowledgeFreshness(str, Enum):
    REAL_TIME = "real_time"
    FRESH = "fresh"
    STALE = "stale"
    DECAYED = "decayed"
    ARCHIVED = "archived"


class ObservationQuality(str, Enum):
    HIGH_SIGNAL = "high_signal"
    MODERATE_SIGNAL = "moderate_signal"
    NOISY = "noisy"
    CONFLICTING = "conflicting"
    UNVERIFIED = "unverified"


class TemporalResolution(str, Enum):
    REAL_TIME = "real_time"
    MINUTELY = "minutely"
    HOURLY = "hourly"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"


class ReasoningMode(str, Enum):
    INDUCTIVE = "inductive"
    DEDUCTIVE = "deductive"
    ABDUCTIVE = "abductive"
    COUNTERFACTUAL = "counterfactual"
    BAYESIAN = "bayesian"


class ModelVersion(str, Enum):
    V1_INITIAL = "v1.0.0"
    V1_1_CONTINUOUS = "v1.1.0"
    V1_2_CAUSAL = "v1.2.0"
    V2_DEEP_WORLD = "v2.0.0"


class ObservationSource(str, Enum):
    EXECUTION_RUNTIME = "execution_runtime"
    ORGANIZATION_RUNTIME = "organization_runtime"
    EVOLUTION_RUNTIME = "evolution_runtime"
    SCIENCE_RUNTIME = "science_runtime"
    STRATEGY_RUNTIME = "strategy_runtime"
    EXTERNAL_API = "external_api"
    LOGS_TELEMETRY = "logs_telemetry"
    USER_FEEDBACK = "user_feedback"
    BROWSER_SESSION = "browser_session"
    IOT_SENSOR = "iot_sensor"


class WorldModelEventType(str, Enum):
    # Observation Events
    OBSERVATION_RECEIVED = "observation.received"
    OBSERVATION_CLASSIFIED = "observation.classified"
    OBSERVATION_FILTERED = "observation.filtered"
    NOVELTY_DETECTED = "observation.novelty_detected"
    CONFLICT_DETECTED = "observation.conflict_detected"

    # Knowledge Fusion Events
    KNOWLEDGE_INTEGRATED = "knowledge.integrated"
    KNOWLEDGE_MERGED = "knowledge.merged"
    KNOWLEDGE_CONFLICT_RESOLVED = "knowledge.conflict_resolved"
    ENTITY_LINKED = "knowledge.entity_linked"
    KNOWLEDGE_FRESHNESS_DECAYED = "knowledge.freshness_decayed"

    # World State & Graph Events
    WORLD_STATE_UPDATED = "world.state_updated"
    GRAPH_NODE_ADDED = "world.graph_node_added"
    GRAPH_EDGE_ADDED = "world.graph_edge_added"
    GRAPH_PRUNED = "world.graph_pruned"
    WORLD_CHECKPOINT_CREATED = "world.checkpoint_created"
    WORLD_SNAPSHOT_RESTORED = "world.snapshot_restored"

    # Temporal Events
    TEMPORAL_PATTERN_DISCOVERED = "temporal.pattern_discovered"
    PERIODICITY_IDENTIFIED = "temporal.periodicity_identified"
    CONCEPT_DRIFT_DETECTED = "temporal.concept_drift_detected"
    TREND_EXTRAPOLATED = "temporal.trend_extrapolated"

    # Causal Reasoning Events
    CAUSAL_RELATIONSHIP_DISCOVERED = "causal.relationship_discovered"
    CAUSAL_DAG_UPDATED = "causal.dag_updated"
    ROOT_CAUSE_ISOLATED = "causal.root_cause_isolated"
    INTERVENTION_SIMULATED = "causal.intervention_simulated"

    # Hypothesis Events
    HYPOTHESIS_CREATED = "hypothesis.created"
    HYPOTHESIS_TESTED = "hypothesis.tested"
    HYPOTHESIS_SUPPORTED = "hypothesis.supported"
    HYPOTHESIS_REFUTED = "hypothesis.refuted"

    # Scenario & Counterfactual Events
    SCENARIO_GENERATED = "scenario.generated"
    SCENARIO_EXECUTED = "scenario.executed"
    SCENARIO_COMPARED = "scenario.compared"
    COUNTERFACTUAL_CREATED = "counterfactual.created"
    COUNTERFACTUAL_EVALUATED = "counterfactual.evaluated"
    BLACK_SWAN_DETECTED = "scenario.black_swan_detected"

    # Predictive Intelligence Events
    PREDICTION_GENERATED = "prediction.generated"
    FORECAST_WINDOW_UPDATED = "prediction.forecast_window_updated"
    FUTURE_RISK_DETECTED = "prediction.future_risk_detected"
    OPPORTUNITY_DETECTED = "prediction.opportunity_detected"
    PREDICTION_DRIFT_DETECTED = "prediction.drift_detected"

    # Decision Intelligence Events
    DECISION_EVALUATED = "decision.evaluated"
    EXPECTED_UTILITY_CALCULATED = "decision.expected_utility_calculated"
    PORTFOLIO_OPTIMIZED = "decision.portfolio_optimized"
    DECISION_RECOMMENDED = "decision.recommended"

    # Uncertainty Events
    UNCERTAINTY_DECOMPOSED = "uncertainty.decomposed"
    ENTROPY_CALCULATED = "uncertainty.entropy_calculated"
    CONFIDENCE_ADJUSTED = "uncertainty.confidence_adjusted"
    BELIEF_UPDATED = "uncertainty.belief_updated"
    BAYESIAN_UPDATE_PERFORMED = "uncertainty.bayesian_update_performed"

    # Verification & Learning Events
    PREDICTION_VALIDATED = "verification.prediction_validated"
    PREDICTION_REJECTED = "verification.prediction_rejected"
    CALIBRATION_MEASURED = "verification.calibration_measured"
    MEMORY_CONSOLIDATED = "memory.consolidated"
    MEMORY_REPLAYED = "memory.replayed"
    LEARNING_CYCLE_COMPLETED = "learning.cycle_completed"


@dataclass
class WorldModelEvent:
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    event_type: WorldModelEventType = WorldModelEventType.OBSERVATION_RECEIVED
    source: str = "world_intelligence_runtime"
    payload: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    correlation_id: Optional[str] = None
    confidence: float = 0.95

    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_id": self.event_id,
            "event_type": self.event_type.value if isinstance(self.event_type, WorldModelEventType) else str(self.event_type),
            "source": self.source,
            "payload": self.payload,
            "timestamp": self.timestamp,
            "correlation_id": self.correlation_id,
            "confidence": round(self.confidence, 4),
        }


class WorldModelEventBus:
    """Reactive Event Dispatcher & Historical Event Store for World Model."""

    def __init__(self):
        self._subscribers: Dict[str, List[Callable[[WorldModelEvent], None]]] = {}
        self._history: List[WorldModelEvent] = []
        self._max_history: int = 1500

    def subscribe(self, event_type: str, handler: Callable[[WorldModelEvent], None]) -> None:
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(handler)

    def subscribe_all(self, handler: Callable[[WorldModelEvent], None]) -> None:
        self.subscribe("*", handler)

    def publish(self, event: WorldModelEvent) -> None:
        self._history.append(event)
        if len(self._history) > self._max_history:
            self._history.pop(0)

        event_key = event.event_type.value if isinstance(event.event_type, WorldModelEventType) else str(event.event_type)
        if event_key in self._subscribers:
            for handler in self._subscribers[event_key]:
                try:
                    handler(event)
                except Exception as e:
                    print(f"Error in WorldModel event handler for {event_key}: {e}")

        if "*" in self._subscribers:
            for handler in self._subscribers["*"]:
                try:
                    handler(event)
                except Exception as e:
                    print(f"Error in WorldModel wildcard handler: {e}")

    def get_history(self, limit: int = 100, event_type: Optional[str] = None) -> List[Dict[str, Any]]:
        filtered = self._history
        if event_type:
            filtered = [
                e for e in filtered
                if (e.event_type.value if isinstance(e.event_type, WorldModelEventType) else str(e.event_type)) == event_type
            ]
        return [e.to_dict() for e in filtered[-limit:]]

    def clear(self) -> None:
        self._history.clear()
        self._subscribers.clear()


# Global Singleton
world_model_event_bus = WorldModelEventBus()
