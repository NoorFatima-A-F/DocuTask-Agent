"""
Phase 3H.5.9: Predictive Health Intelligence & Proactive Failure Prevention — Domain Models
"""
from enum import Enum
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime


class PredictionRiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class SystemReliabilityState(str, Enum):
    HEALTHY = "HEALTHY"
    DEGRADED = "DEGRADED"
    RISK_INCREASING = "RISK_INCREASING"
    FAILURE_IMMINENT = "FAILURE_IMMINENT"
    RECOVERING = "RECOVERING"


class RemediationApprovalLevel(str, Enum):
    SAFE_AUTOMATIC = "SAFE_AUTOMATIC"
    APPROVAL_REQUIRED = "APPROVAL_REQUIRED"


class DetectionMethod(str, Enum):
    MOVING_AVERAGE = "MOVING_AVERAGE"
    STANDARD_DEVIATION = "STANDARD_DEVIATION"
    BASELINE_DEVIATION = "BASELINE_DEVIATION"
    TREND_ANALYSIS = "TREND_ANALYSIS"
    BEHAVIORAL_ANALYSIS = "BEHAVIORAL_ANALYSIS"


class PredictiveCertificationTier(str, Enum):
    PREDICTIVE_RELIABILITY_READY = "Predictive Reliability Ready"
    ADVANCED_AIOPS_READY = "Advanced AIOps Ready"
    IMPROVEMENT_REQUIRED = "Improvement Required"
    FAILED = "Failed"


# ─── 3H.5.9.1: Predictive Health Architecture ───────────────────────────────


class PredictiveArchitectureReport(BaseModel):
    report_title: str = "Predictive Health Architecture Report"
    pipeline_stages: List[str] = Field(default_factory=list)
    signal_sources: List[str] = Field(default_factory=list)
    metric_categories: List[str] = Field(default_factory=list)
    application_signals: List[str] = Field(default_factory=list)
    dependency_signals: List[str] = Field(default_factory=list)
    total_signal_sources: int = 0
    architecture_valid: bool = True


# ─── 3H.5.9.2: Feature Engineering ──────────────────────────────────────────


class PredictiveFeature(BaseModel):
    name: str
    value: float
    window: str
    source: str
    category: str  # resource, performance, reliability, ai


class FeatureEngineeringReport(BaseModel):
    report_title: str = "Feature Engineering Report"
    total_features_extracted: int = 0
    features: List[PredictiveFeature] = Field(default_factory=list)
    resource_features_count: int = 0
    performance_features_count: int = 0
    reliability_features_count: int = 0
    ai_features_count: int = 0
    feature_engineering_valid: bool = True


# ─── 3H.5.9.3: Anomaly Detection ────────────────────────────────────────────


class AnomalyItem(BaseModel):
    anomaly_id: str
    metric: str
    component: str
    observed_value: float
    expected_range: str
    severity: str  # INFO, WARNING, CRITICAL
    confidence: float
    detection_method: DetectionMethod
    pattern: str = ""


class AnomalyDetectionReport(BaseModel):
    report_title: str = "Anomaly Detection Report"
    total_anomalies_detected: int = 0
    anomalies: List[AnomalyItem] = Field(default_factory=list)
    statistical_detection_active: bool = True
    trend_detection_active: bool = True
    behavioral_detection_active: bool = True
    anomaly_detection_valid: bool = True


# ─── 3H.5.9.4: Failure Probability Prediction ───────────────────────────────


class FailurePredictionItem(BaseModel):
    prediction_id: str
    component: str
    failure_type: str
    time_window: str
    probability: float = Field(..., ge=0.0, le=1.0)
    confidence: float = Field(..., ge=0.0, le=1.0)
    risk_level: PredictionRiskLevel


class FailurePredictionReport(BaseModel):
    report_title: str = "Failure Prediction Report"
    total_predictions: int = 0
    predictions: List[FailurePredictionItem] = Field(default_factory=list)
    high_risk_predictions: int = 0
    mean_confidence: float = 0.0
    failure_prediction_valid: bool = True


# ─── 3H.5.9.5: Capacity Risk Prediction ─────────────────────────────────────


class CapacityPredictionItem(BaseModel):
    prediction_id: str
    resource: str
    prediction_type: str
    current_utilization_pct: float
    growth_rate: str
    estimated_exhaustion_time: str
    risk_level: PredictionRiskLevel
    confidence: float = Field(..., ge=0.0, le=1.0)


class CapacityPredictionReport(BaseModel):
    report_title: str = "Capacity Prediction Report"
    total_capacity_predictions: int = 0
    predictions: List[CapacityPredictionItem] = Field(default_factory=list)
    critical_resources: int = 0
    capacity_prediction_valid: bool = True


# ─── 3H.5.9.6: Proactive Remediation ────────────────────────────────────────


class ProactiveRemediationItem(BaseModel):
    action_id: str
    trigger_prediction: str
    target_component: str
    preventive_action: str
    approval_level: RemediationApprovalLevel
    validation_result: str
    action_successful: bool = True


class ProactiveRemediationReport(BaseModel):
    report_title: str = "Proactive Remediation Report"
    total_preventive_actions: int = 0
    actions: List[ProactiveRemediationItem] = Field(default_factory=list)
    automatic_actions_count: int = 0
    approval_required_count: int = 0
    all_actions_successful: bool = True
    proactive_remediation_valid: bool = True


# ─── 3H.5.9.7: Prediction Accuracy ──────────────────────────────────────────


class PredictionAccuracyMetrics(BaseModel):
    precision: float = Field(..., ge=0.0, le=1.0)
    recall: float = Field(..., ge=0.0, le=1.0)
    false_positive_rate: float = Field(..., ge=0.0, le=1.0)
    true_positive_count: int = 0
    false_positive_count: int = 0
    false_negative_count: int = 0
    total_predictions: int = 0


class PredictionAccuracyReport(BaseModel):
    report_title: str = "Prediction Accuracy Report"
    metrics: PredictionAccuracyMetrics
    false_alarm_rate_pct: float = 0.0
    accuracy_threshold_met: bool = True
    prediction_accuracy_valid: bool = True


# ─── 3H.5.9.8: Predictive Incident Creation ─────────────────────────────────


class PredictiveIncidentItem(BaseModel):
    incident_id: str
    incident_type: str = "PREDICTIVE"
    risk_component: str
    failure_probability: float = Field(..., ge=0.0, le=1.0)
    recommended_action: str
    risk_level: PredictionRiskLevel
    incident_created: bool = True


class PredictiveIncidentReport(BaseModel):
    report_title: str = "Predictive Incident Report"
    total_predictive_incidents: int = 0
    incidents: List[PredictiveIncidentItem] = Field(default_factory=list)
    all_incidents_actionable: bool = True
    predictive_incident_valid: bool = True


# ─── 3H.5.9.9: Digital Reliability Twin ─────────────────────────────────────


class ComponentReliabilityState(BaseModel):
    component: str
    current_state: SystemReliabilityState
    failure_history_count: int = 0
    current_telemetry_health_pct: float = 100.0
    dependencies: List[str] = Field(default_factory=list)


class ReliabilityTwinReport(BaseModel):
    report_title: str = "Digital Reliability Twin Report"
    overall_system_state: SystemReliabilityState
    component_states: List[ComponentReliabilityState] = Field(default_factory=list)
    total_components_modeled: int = 0
    healthy_components: int = 0
    degraded_components: int = 0
    reliability_twin_valid: bool = True


# ─── 3H.5.9.10: Chaos Prediction Validation ─────────────────────────────────


class ChaosPredictionScenario(BaseModel):
    scenario_name: str
    injected_fault: str
    prediction_triggered: bool = True
    prediction_time_before_failure_seconds: float = 0.0
    prediction_accuracy_pct: float = 100.0
    incidents_prevented: int = 0
    scenario_passed: bool = True


class ChaosPredictionReport(BaseModel):
    report_title: str = "Chaos Prediction Validation Report"
    total_chaos_scenarios: int = 0
    scenarios: List[ChaosPredictionScenario] = Field(default_factory=list)
    mean_prediction_lead_time_seconds: float = 0.0
    all_chaos_predictions_passed: bool = True
    chaos_prediction_valid: bool = True


# ─── 3H.5.9.11: Predictive Reliability Dashboards ───────────────────────────


class PredictiveDashboardItem(BaseModel):
    dashboard_name: str
    active_panels: int
    refresh_rate_seconds: int
    status: str = "ONLINE"


class PredictiveDashboardReport(BaseModel):
    report_title: str = "Predictive Reliability Dashboard Report"
    dashboards: List[PredictiveDashboardItem] = Field(default_factory=list)
    total_dashboards: int = 0
    all_dashboards_active: bool = True
    dashboard_valid: bool = True


# ─── 3H.5.9.12: Predictive Reliability Scorecard ────────────────────────────


class PredictiveHealthScorecard(BaseModel):
    prediction_accuracy_score: float = Field(..., ge=0.0, le=100.0)
    anomaly_detection_score: float = Field(..., ge=0.0, le=100.0)
    preventive_actions_score: float = Field(..., ge=0.0, le=100.0)
    false_alarm_control_score: float = Field(..., ge=0.0, le=100.0)
    reliability_improvement_score: float = Field(..., ge=0.0, le=100.0)
    security_score: float = Field(..., ge=0.0, le=100.0)
    composite_score: float = Field(..., ge=0.0, le=100.0)
    tier: PredictiveCertificationTier
    certified_predictive_ready: bool
