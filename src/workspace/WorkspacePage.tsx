import React from 'react';
import { useWorkspace } from './context/WorkspaceContext';
import { DemoController } from './demo/DemoController';
import { ConversationPanel } from './conversation/ConversationPanel';
import { AgentInboxPanel } from './agent-inbox/AgentInboxPanel';
import { TaskBoardPanel } from './TaskBoardPanel';
import { ThoughtStreamPanel } from './thought-stream/ThoughtStreamPanel';
import { HumanFeedbackPanel } from './feedback/HumanFeedbackPanel';
import { LiveTimelinePanel } from './timeline/LiveTimelinePanel';
import { RuntimeTraceGraph } from './timeline/RuntimeTraceGraph';
import { MemoryGraphPanel } from './memory-graph/MemoryGraphPanel';
import {
  MissionConfidenceDashboard,
  ConfidenceDimensionMatrix,
  ScientificFormulaExplorer,
  FeatureContributionWaterfall,
  RuntimeEvidenceExplorer,
  ConfidenceTimeline,
  ConfidenceTrendAnalysis,
  CalibrationDashboard,
  ReliabilityDiagramViewer,
  ConfidenceLineageExplorer,
  UncertaintyIntervalViewer,
  FormulaGovernanceInspector,
  ConfidenceExplorerPanel,
  BayesianConfidencePanel,
} from './confidence';
import { RuntimeStatisticsDashboard } from './statistics/RuntimeStatisticsDashboard';
import {
  MissionReplayStudio,
  ReplayTimelineExplorer,
  RuntimeStateInspector,
  ReplayForensicsCenter,
  EvidenceEvolutionExplorer,
  ConfidenceEvolutionViewer,
  PlannerDAGReplay,
  ReplayDiffStudio,
  AuditReportGenerator,
  ReplayStatisticsDashboard,
  ReplayVerificationCenter,
  MissionTimeTravelExplorer,
  ReplayDiffComparator,
  MissionReplayPlayer,
  CinematicReplayMovie,
} from './replay';
import { MissionStoryPanel } from './story/MissionStoryPanel';
import {
  StrategyComparisonMatrixView,
  CounterfactualExplorerView,
  MutableDAGViewerView,
  ResourceSchedulerDashboardView,
  PlannerCalibrationCardView,
} from './planning';
import {
  PlannerGraphView,
  ExecutionDAG,
  CriticalPathView,
  WorkerAllocationView,
  DependencyExplorer,
  DependencyExplorerView,
  GraphMutationTimeline,
  PlannerSimulationDashboard,
  RecoveryGraphViewer,
  PlannerLifecycleView,
  GoalAnalysisView,
  TaskDecompositionView,
  LiveDAGView,
  SchedulerView,
  WorkerAssignmentView,
  PlannerTimelineView,
  PlannerDecisionExplorerView,
  QueueMonitorView,
  PlannerReplayView,
} from './planner';
import {
  BeliefExplorerPanel,
  WorldPredictionDashboard,
  EVOIExplorerPanel,
  MetaReasoningInspector,
  GovernanceAssuranceMatrix,
} from './intelligence';
import {
  StrategySynthesisExplorer,
  PlannerEvolutionTimeline,
  DigitalTwinSimulatorView,
  StructuralCausalGraphView,
  MultiAgentCouncilPanel,
  EvolutionExecutiveDashboard,
  ArchitectureProfilerCenter,
  CapabilityGapExplorer,
  ArchitectureOptimizerStudio,
  MutationWorkbench,
  BenchmarkAnalyticsCenter,
  EvolutionSimulationStudio,
  GovernanceApprovalCenter as EvolutionGovernanceApprovalCenter,
  DeploymentControlCenter,
  RecursiveEvolutionTimeline,
  PlatformGenomeExplorer,
  ContinuousImprovementCenter,
} from './evolution';
import {
  LiveRuntimeDashboardView,
  EventSourcedMissionTimeline,
  ExecutionFlameGraphViewer,
  ObservabilityTraceExplorer,
} from './observability';
import {
  MissionReplayController,
  TimelineExplorerView,
  DecisionGraphView,
  PlannerEvolutionHistoryView,
  EvidenceExplorerView,
  HumanReviewReplayView,
  SnapshotBrowserView,
  EnterpriseAuditExplorerView,
  IntegrityVerificationPanel,
  EnterpriseExportCenterView,
} from './replay';
import {
  ResourceIntelligenceDashboard,
  EconomicIntelligenceCenter,
  OptimizationDecisionExplorer,
  StrategyComparisonStudio,
  ResourceAllocationMonitor,
  ModelToolRoutingExplorer,
  ScenarioSimulationLab,
  MultiObjectiveOptimizationViewer,
  SLABudgetGovernanceCenter,
  PredictionAnalyticsDashboard,
  OptimizationLineageExplorer,
  ResourceHealthCapacityDashboard,
  FeatureStoreInspectorView,
  ScientificConfidenceView,
  OptimizerExplorerView,
  ParetoFrontierView,
  ConstraintInspectorView,
  RiskExplorerView,
  CalibrationLabView,
  PolicyComparisonView,
  BenchmarkCenterView,
  ModelRoutingExplorerView,
  RetryOptimizerView,
  ScientificMetricsDashboardView,
} from './optimization';
import {
  OutcomeVerificationView,
  PredictionAccuracyView,
  CounterfactualReplayLabView,
  DigitalTwinMonitorView,
  DriftDetectionCenterView,
  ExperimentDashboardView,
  CausalAnalysisView,
  PolicyEvolutionTimelineView,
  GovernanceApprovalCenterView,
  ScientificCertificationReportView,
} from './validation';
import {
  LiveDAGExecutionView,
  RuntimeCostIntelligenceView,
  MathematicalConfidenceProofView,
  ResourceSchedulerMonitorView,
  FailureChaosRecoveryLabView,
  AutomatedBenchmarkStudioView,
  ForensicProvenanceAuditView,
  HackathonDemoControlCenter,
} from './transparency';
import {
  OrganizationOverviewView,
  ExecutiveControlCenter,
  DepartmentMonitorView,
  NegotiationStudioView,
  OrganizationHealthView,
  IncidentCommandCenter,
  LearningEvolutionView,
  SLAIntelligenceView,
  CommunicationBusView,
  OrganizationSimulationView,
  OrganizationExecutiveDashboard,
  MissionControlCenter,
  StrategyGenerationStudio,
  OrganizationDesigner,
  WorkforceManagementCenter,
  AutonomousProjectManager,
  ResourceOptimizationCenter,
  PerformanceIntelligenceDashboard,
  FinanceOptimizationCenter,
  NegotiationArena,
  OrganizationSimulationStudio,
  OrganizationalEvolutionTimeline,
} from './organization';
import {
  EvidenceExplorerView as Phase8EvidenceExplorerView,
  PlannerDecisionLedgerView,
  ToolCallInspectorView,
  RuntimeProvenanceGraphView,
  ReproducibilityStudioView,
  BenchmarkCertificateCenterView,
  JudgeVerificationConsoleView,
  IndependentAuditExportView,
  ExecutionEvidenceTimelineView,
  RuntimeTruthDashboardView,
} from './evidence';
import {
  PlatformDashboardView,
  SDKExplorerView,
  CapabilityRegistryView,
  PluginMarketplaceView,
  WorkflowComposerView,
  WorkflowDSLEditorView,
  DynamicToolRegistryView,
  OrganizationTemplatesView,
  PolicyManagerView,
  ExtensionLifecycleView,
  PluginCertificationView,
  SandboxInspectorView,
  APIContractExplorerView,
  PlatformDiagnosticsView,
} from './platform';
import {
  AdaptiveIntelligenceOverviewView,
  ExperienceExplorerView,
  StrategyLibraryView,
  HypothesisLaboratoryView,
  ExperimentCenterView,
  PlannerEvolutionView as Phase10PlannerEvolutionView,
  PredictionAnalyticsView,
  ConsensusAnalyzerView,
  KnowledgeGraphExplorerView,
  OrganizationalLearningView,
  ContinuousOptimizationTimelineView,
  ScientificImprovementDashboardView,
} from './intelligence';
import {
  TruthLedgerExplorerView,
  DecisionProofExplorerView,
  MetricProvenanceView,
  ScientificBenchmarksView,
  ReplayCertificationView,
  TrustDashboardView,
  DriftAnalyticsView,
  VerificationCenterView,
  MissionCertificationView,
  ScientificReportsView,
} from './trust';
import {
  DigitalTwinView,
  ChaosLabView,
  IncidentCommanderView,
  DependencyGraphView,
  RecoveryTimelineView,
  InvariantExplorerView,
  ReliabilityMathematicsView,
  ProductionReadinessView,
  MissionTimeMachineView,
  StressArenaView,
  OperationalAnalyticsView,
  CertificationCenterView,
} from './resilience';
import {
  MissionTimelineView,
  PlannerEventsView,
  WorkerEventsView,
  RuntimeEventExplorerView,
  LiveEventStreamView,
  CorrelationExplorerView,
  EventGraphView,
  MissionTraceView,
  TelemetryStreamView,
  ProjectionInspectorView,
} from './events';
import {
  ReflectionCenter,
  OrganizationalLearningDashboard,
  PatternMiningExplorer,
  KnowledgeGraphExplorer as LearningKnowledgeGraphExplorer,
  KnowledgeRegistryView,
  StrategyLibraryView as Phase135StrategyLibraryView,
  PolicyEvolutionCenter,
  GovernanceApprovalWorkflow,
  LearningTimeline,
  KnowledgeLineageExplorer,
  RecommendationReviewStudio,
  LearningAnalyticsDashboard,
} from './learning';
import {
  OperationalCommandCenter,
  HealthIntelligenceDashboard,
  IncidentManagementCenter,
  DiagnosisExplorer,
  SelfHealingStudio,
  RecoveryOrchestrationCenter,
  PredictiveFailureAnalytics,
  ChaosEngineeringLab,
  ResilienceScorecard,
  OperationalGovernanceCenter,
  OperationalEventTimeline,
  OperationsAnalyticsDashboard,
} from './operations';
import {
  SwarmCommandCenter,
  AgentRegistryExplorer,
  CommunicationMonitor,
  NegotiationStudio,
  ConsensusDashboard,
  CoalitionManagerView,
  TaskMarketplaceView,
  ReputationAnalytics,
  TrustNetworkExplorer,
  CoordinationTimeline,
  SwarmGovernanceCenter,
  SwarmLearningDashboard,
} from './swarm';
import {
  MetaReasoningCenter,
  StrategicPlanningStudio,
  RecursiveReflectionExplorer,
  ExperimentationLab,
  CapabilityDiscoveryDashboard,
  PolicyEvolutionCenter as MetaPolicyEvolutionCenter,
  ArchitectureOptimizerView,
  SelfImprovementTimeline,
  StrategyComparisonWorkbench,
  GovernanceApprovalCenter as MetaGovernanceApprovalCenter,
  StrategicKnowledgeGraph,
  ExecutiveDecisionDashboard,
} from './meta';
import {
  DigitalTwinCenter,
  WorldModelExplorer,
  PredictiveSimulationStudio,
  ScenarioComparisonWorkbench,
  CounterfactualExplorer,
  CausalGraphVisualizer,
  ForecastAnalytics,
  RiskPredictionDashboard,
  OpportunityDiscoveryCenter,
  TemporalKnowledgeGraph,
  PredictiveGovernanceCenter,
  ExecutiveFutureDashboard,
} from './world';
import {
  GoalEvolutionCenter,
  MissionPortfolioCenter,
  StrategicRoadmapStudio,
  ExecutiveDecisionCenter,
  OrganizationalMemoryExplorer,
  ResourceNegotiationCenter,
  StrategySimulationStudio,
  DecisionWorkbench,
  ExecutiveStrategyDashboard,
  StrategicInsightsCenter,
  GoalDependencyExplorer,
  LongTermPlanningCenter,
} from './strategy';
import {
  ScientificDiscoveryDashboard,
  HypothesisGenerationCenter,
  ExperimentDesignStudio,
  EvidenceExplorer as ScienceEvidenceExplorer,
  ValidationWorkbench,
  KnowledgeGraphExplorer as ScienceKnowledgeGraphExplorer,
  ResearchPlanningCenter,
  PublicationCenter,
  ConsensusReviewCenter,
  OntologyExplorer,
  DiscoveryTimeline,
  ExecutiveResearchDashboard,
} from './science';
import {
  ExecutionExecutiveDashboard,
  MissionExecutionCenter,
  WorkflowDesigner,
  ToolRegistryExplorer,
  ConnectorManagementCenter,
  BrowserAutomationStudio,
  ExecutionPlannerStudio,
  PolicyGovernanceCenter,
  SimulationControlCenter,
  VerificationWorkbench,
  RollbackRecoveryCenter,
  AuditTimelineExplorer,
} from './execution';
import {
  WorldExecutiveDashboard as WorldModelExecutiveDashboard,
  KnowledgeFusionCenter as WorldModelKnowledgeFusionCenter,
  WorldGraphExplorer as WorldModelGraphExplorer,
  TemporalReasoningStudio as WorldModelTemporalReasoningStudio,
  CausalAnalysisWorkbench as WorldModelCausalAnalysisWorkbench,
  HypothesisLaboratory as WorldModelHypothesisLaboratory,
  ScenarioSimulationCenter as WorldModelScenarioSimulationCenter,
  CounterfactualStudio as WorldModelCounterfactualStudio,
  PredictiveIntelligenceDashboard as WorldModelPredictiveIntelligenceDashboard,
  DecisionIntelligenceCenter as WorldModelDecisionIntelligenceCenter,
  UncertaintyExplorer as WorldModelUncertaintyExplorer,
  WorldEvolutionTimeline as WorldModelEvolutionTimeline,
} from './world_model';
import {
  AIOperationsExecutiveDashboard,
  AgentObservatory,
  ExecutionTraceExplorer,
  EvaluationCenter,
  PromptLaboratory,
  ModelRoutingCenter,
  CostIntelligenceView,
  FailureAnalysisStudio,
  ImprovementStudio,
  ExperimentManager,
  GovernanceDashboard,
  AIEvolutionTimeline,
} from './ai_operations';
import {
  ClusterOverviewDashboard,
  WorkerFleetManager,
  DistributedQueueMonitor,
  SchedulerTimelineView,
  DurableWorkflowInspector,
  CheckpointExplorer,
  DistributedEventStreamView,
  AutoscalingControlCenter,
  MultiRegionFabricMap,
  InfrastructureHealthStudio,
  DeploymentCenter,
  DisasterRecoveryConsole,
} from './distributed';
import {
  ExecutiveCommandCenter as BusinessExecutiveCommandCenter,
  ProcessDesigner,
  ProcessExplorer,
  OrganizationGraphViewer,
  GoalManagerStudio,
  KPIDashboard,
  SLAIntelligenceCenter,
  DecisionRulesStudio,
  HumanApprovalCenter,
  ProcessDiscoveryExplorer,
  DigitalTwinOrgViewer,
  ProcessROISimulator,
} from './business';
import {
  PlatformExecutiveDashboard,
  TenantManagementCenter,
  OrganizationManager,
  WorkspaceExplorer,
  IdentitySSOCenter,
  SubscriptionBillingConsole,
  UsageAnalyticsDashboard,
  MarketplaceManager,
  IntegrationHub,
  PolicyAdministrationCenter,
  WhiteLabelStudio,
  EnterpriseAuditExplorer,
} from './platform_saas';
import {
  AIApplicationDashboard,
  AgentRegistry,
  AgentBuilder,
  VersionExplorer,
  TestingCenter,
  SecurityReviewCenter,
  ApprovalWorkflowCenter,
  DeploymentCenter as AILifecycleDeploymentCenter,
  DependencyGraphViewer,
  MarketplaceStudio,
  LifecycleAnalyticsDashboard,
  RetirementCenter,
} from './ai_lifecycle';
import {
  KnowledgeDashboard,
  KnowledgeExplorer,
  SemanticSearchStudio,
  KnowledgeGraphExplorer as Phase21KnowledgeGraphExplorer,
  KnowledgeSourceManager,
  ContextDebugger,
  MemoryObservatory,
  KnowledgeQualityCenter,
  KnowledgeSecurityCenter,
  KnowledgeEvolution,
  OntologyBuilder,
  RetrievalEvaluation,
} from './knowledge';
import {
  ExecutiveIntelligenceDashboard,
  OrganizationalLearningCenter,
  DecisionIntelligenceExplorer,
  BusinessSimulationStudio,
  AutonomousOptimizationCenter,
  EnterpriseCognitiveGraph,
  ProcessDiscoveryStudio,
  ExperienceMemoryExplorer,
  GoalAlignmentCenter,
  StrategicRecommendationCenter,
  ContinuousLearningMonitor,
  EnterpriseIntelligenceTimeline,
} from './cognitive';
import {
  ExecutiveOrganizationDashboard,
  DigitalWorkforceExplorer,
  OrganizationChartStudio,
  TeamFormationCenter,
  TaskMarketplace,
  AgentCareerCenter,
  ManagerConsole,
  ExecutiveCouncil,
  PerformanceAnalytics,
  HiringPromotionStudio,
  ResourceEconomyDashboard,
  CollectiveIntelligenceMonitor,
} from './workforce';
import { VerificationPlatformStudio } from './verification';
import type { WorkspaceTabType } from './types/workspace';

export const WorkspacePage: React.FC = () => {
  const { activeTab, setActiveTab } = useWorkspace();

  const tabs: { id: WorkspaceTabType; label: string; icon: string }[] = [
    { id: 'CONVERSATION', label: 'Conversation', icon: '💬' },
    { id: 'VERIFICATION_PLATFORM_STUDIO', label: 'Verification Platform (FVPA)', icon: '🛡️' },
    { id: 'WORKFORCE_EXECUTIVE_DASHBOARD', label: 'Workforce Organization (13.23)', icon: '🏢' },
    { id: 'WORKFORCE_DIGITAL_EXPLORER', label: 'Digital Workforce Explorer', icon: '🤖' },
    { id: 'WORKFORCE_ORG_CHART', label: 'Organization Chart Studio', icon: '🌳' },
    { id: 'WORKFORCE_TEAM_FORMATION', label: 'Dynamic Team Formation', icon: '⚡' },
    { id: 'WORKFORCE_TASK_MARKETPLACE', label: 'Task Marketplace & Economy', icon: '🛒' },
    { id: 'WORKFORCE_CAREER_CENTER', label: 'Agent Career Center', icon: '🎓' },
    { id: 'WORKFORCE_MANAGER_CONSOLE', label: 'Manager Console & Reviews', icon: '👔' },
    { id: 'WORKFORCE_EXECUTIVE_COUNCIL', label: 'Executive AI Council', icon: '🏛️' },
    { id: 'WORKFORCE_PERFORMANCE_ANALYTICS', label: 'Workforce Performance', icon: '📊' },
    { id: 'WORKFORCE_HIRING_STUDIO', label: 'Autonomous Hiring Studio', icon: '🎯' },
    { id: 'WORKFORCE_RESOURCE_ECONOMY', label: 'Resource Economy Dashboard', icon: '💰' },
    { id: 'WORKFORCE_COLLECTIVE_INTELLIGENCE', label: 'Collective Intelligence & Conflict', icon: '🧠' },
    { id: 'COGNITIVE_EXECUTIVE_DASHBOARD', label: 'Executive Intelligence (13.22)', icon: '🧠' },
    { id: 'COGNITIVE_ORGANIZATIONAL_LEARNING', label: 'Organizational Learning Center', icon: '📚' },
    { id: 'COGNITIVE_DECISION_INTELLIGENCE', label: 'Decision Intelligence Explorer', icon: '🎯' },
    { id: 'COGNITIVE_SIMULATION_STUDIO', label: 'Business Simulation Studio', icon: '📈' },
    { id: 'COGNITIVE_AUTONOMOUS_OPTIMIZATION', label: 'Autonomous Optimization Center', icon: '⚡' },
    { id: 'COGNITIVE_REASONING_GRAPH', label: 'Cognitive Reasoning Graph', icon: '🕸️' },
    { id: 'COGNITIVE_PROCESS_DISCOVERY', label: 'Process Discovery & Mining', icon: '🔍' },
    { id: 'COGNITIVE_EXPERIENCE_MEMORY', label: 'Experience Memory Pool', icon: '💾' },
    { id: 'COGNITIVE_GOAL_ALIGNMENT', label: 'Goal Alignment & KPI Matrix', icon: '🎯' },
    { id: 'COGNITIVE_STRATEGIC_RECOMMENDATIONS', label: 'Strategic Executive Guidance', icon: '✨' },
    { id: 'COGNITIVE_CONTINUOUS_LEARNING', label: 'Continuous Learning Monitor', icon: '🔄' },
    { id: 'COGNITIVE_INTELLIGENCE_TIMELINE', label: 'Intelligence Event Timeline', icon: '⏳' },
    { id: 'KNOWLEDGE_DASHBOARD', label: 'Knowledge Command Center (13.21)', icon: '📖' },
    { id: 'KNOWLEDGE_EXPLORER', label: 'Knowledge Explorer', icon: '📖' },
    { id: 'KNOWLEDGE_SEMANTIC_SEARCH', label: 'Semantic Search Studio', icon: '🔍' },
    { id: 'KNOWLEDGE_GRAPH', label: 'Ontology Graph Explorer', icon: '🕸️' },
    { id: 'KNOWLEDGE_SOURCES', label: 'Data Source Connectors', icon: '🔌' },
    { id: 'KNOWLEDGE_CONTEXT_DEBUGGER', label: 'Context Budget Debugger', icon: '🔬' },
    { id: 'KNOWLEDGE_MEMORY_OBSERVATORY', label: 'Agent Memory Observatory', icon: '💾' },
    { id: 'KNOWLEDGE_QUALITY', label: 'Knowledge Quality & Conflicts', icon: '🛡️' },
    { id: 'KNOWLEDGE_SECURITY', label: 'Security & Classification', icon: '🔒' },
    { id: 'KNOWLEDGE_EVOLUTION', label: 'Knowledge Evolution Timeline', icon: '⏳' },
    { id: 'KNOWLEDGE_ONTOLOGY_BUILDER', label: 'Ontology & Concept Builder', icon: '📐' },
    { id: 'KNOWLEDGE_RETRIEVAL_EVAL', label: 'RAG Retrieval Evaluation', icon: '📊' },
    { id: 'AI_LIFECYCLE_DASHBOARD', label: 'AI Lifecycle Control (13.20)', icon: '📦' },
    { id: 'AI_LIFECYCLE_REGISTRY', label: 'Enterprise Agent Registry', icon: '🗂️' },
    { id: 'AI_LIFECYCLE_BUILDER', label: 'Agent Builder & Scaffolding', icon: '🛠️' },
    { id: 'AI_LIFECYCLE_VERSION_EXPLORER', label: 'Version Control & Rollback', icon: '🧬' },
    { id: 'AI_LIFECYCLE_TESTING', label: 'AI Quality & Security Testing', icon: '🧪' },
    { id: 'AI_LIFECYCLE_SECURITY_REVIEW', label: 'Security Scanner & Review', icon: '🛡️' },
    { id: 'AI_LIFECYCLE_APPROVALS', label: 'Multi-Stage Approvals', icon: '✍️' },
    { id: 'AI_LIFECYCLE_DEPLOYMENT', label: 'Canary Deployment Control', icon: '🚀' },
    { id: 'AI_LIFECYCLE_DEPENDENCY_GRAPH', label: 'Dependency DAG & Breaking Changes', icon: '🕸️' },
    { id: 'AI_LIFECYCLE_MARKETPLACE', label: 'AI Marketplace Studio', icon: '🏪' },
    { id: 'AI_LIFECYCLE_ANALYTICS', label: 'ROI & Adoption Analytics', icon: '📊' },
    { id: 'AI_LIFECYCLE_RETIREMENT', label: 'Sunset & Retirement Center', icon: '⏳' },
    { id: 'SAAS_EXECUTIVE_DASHBOARD', label: 'SaaS Control Plane (13.19)', icon: '🏢' },
    { id: 'SAAS_TENANT_MANAGEMENT', label: 'Tenant Fleet Manager', icon: '👥' },
    { id: 'SAAS_ORGANIZATION_HIERARCHY', label: 'Organization Hierarchy', icon: '🏛️' },
    { id: 'SAAS_WORKSPACE_EXPLORER', label: 'Workspaces & Projects', icon: '📁' },
    { id: 'SAAS_IDENTITY_SSO', label: 'Identity & SSO Control', icon: '🔑' },
    { id: 'SAAS_SUBSCRIPTION_BILLING', label: 'Subscription & Billing', icon: '💳' },
    { id: 'SAAS_USAGE_ANALYTICS', label: 'Usage & Quota Metering', icon: '⚡' },
    { id: 'SAAS_AI_MARKETPLACE', label: 'Enterprise AI Marketplace', icon: '🏪' },
    { id: 'SAAS_INTEGRATION_HUB', label: 'Integration Hub', icon: '🔌' },
    { id: 'SAAS_POLICY_ADMIN', label: 'Policy & RBAC/ABAC', icon: '⚖️' },
    { id: 'SAAS_WHITE_LABEL_STUDIO', label: 'White-Label & Branding', icon: '🎨' },
    { id: 'SAAS_AUDIT_EXPLORER', label: 'Immutable Audit Ledger', icon: '📜' },
    { id: 'BUSINESS_EXECUTIVE', label: 'Business Command Center (13.19)', icon: '💼' },
    { id: 'BUSINESS_PROCESS_DESIGNER', label: 'BPMN Process Designer', icon: '📐' },
    { id: 'BUSINESS_PROCESS_EXPLORER', label: 'Business Process Explorer', icon: '🗺️' },
    { id: 'BUSINESS_ORG_GRAPH', label: 'Enterprise Knowledge Graph', icon: '🏢' },
    { id: 'BUSINESS_GOALS', label: 'Business Goals & OKRs', icon: '🎯' },
    { id: 'BUSINESS_KPIS', label: 'Enterprise KPI Scorecard', icon: '📊' },
    { id: 'BUSINESS_SLA_CENTER', label: 'SLA Intelligence & Hazard', icon: '🛡️' },
    { id: 'BUSINESS_DECISION_RULES', label: 'Decision Rules Studio', icon: '📜' },
    { id: 'BUSINESS_APPROVAL_CENTER', label: 'Human Approval Center', icon: '✍️' },
    { id: 'BUSINESS_PROCESS_DISCOVERY', label: 'Process Mining & Discovery', icon: '🧭' },
    { id: 'BUSINESS_DIGITAL_TWIN', label: 'Digital Twin of Organization', icon: '🌐' },
    { id: 'BUSINESS_ROI_SIMULATOR', label: 'Process ROI Simulator', icon: '💰' },
    { id: 'DISTRIBUTED_OVERVIEW', label: 'Distributed Fabric (13.18)', icon: '⚡' },
    { id: 'DISTRIBUTED_WORKERS', label: 'Worker Fleet Manager', icon: '🖥️' },
    { id: 'DISTRIBUTED_QUEUES', label: 'Priority Queues & DLQ', icon: '📦' },
    { id: 'DISTRIBUTED_SCHEDULER', label: 'Fair-Share Scheduler', icon: '⏱️' },
    { id: 'DISTRIBUTED_WORKFLOWS', label: 'Durable Workflows', icon: '🔄' },
    { id: 'DISTRIBUTED_CHECKPOINTS', label: 'Checkpoint Explorer', icon: '🛡️' },
    { id: 'DISTRIBUTED_EVENTS', label: 'Distributed Event Stream', icon: '📡' },
    { id: 'DISTRIBUTED_AUTOSCALING', label: 'Autoscaling Engine', icon: '📈' },
    { id: 'DISTRIBUTED_MULTI_REGION', label: 'Multi-Region Topology', icon: '🌐' },
    { id: 'DISTRIBUTED_HEALTH_CHAOS', label: 'Chaos & Failover Studio', icon: '🔥' },
    { id: 'DISTRIBUTED_DEPLOYMENT', label: 'Multi-Cloud Deployment', icon: '🚀' },
    { id: 'DISTRIBUTED_DISASTER_RECOVERY', label: 'Disaster Recovery Console', icon: '🏛️' },
    { id: 'AI_OPS_EXECUTIVE_DASHBOARD', label: 'AI Operations Center (13.17)', icon: '🛡️' },
    { id: 'AI_OPS_AGENT_OBSERVATORY', label: 'Agent Fleet Observatory', icon: '🔭' },
    { id: 'AI_OPS_EXECUTION_TRACES', label: 'Execution Trace Explorer', icon: '🌲' },
    { id: 'AI_OPS_EVALUATION_CENTER', label: 'Evaluation & LLM Judge', icon: '🎯' },
    { id: 'AI_OPS_PROMPT_LAB', label: 'Prompt Laboratory', icon: '🧪' },
    { id: 'AI_OPS_MODEL_ROUTING', label: 'Pareto Model Router', icon: '🔀' },
    { id: 'AI_OPS_COST_INTELLIGENCE', label: 'Cost & Token Intelligence', icon: '💰' },
    { id: 'AI_OPS_FAILURE_ANALYSIS', label: 'Failure Root-Cause Studio', icon: '🪲' },
    { id: 'AI_OPS_IMPROVEMENT_STUDIO', label: 'Controlled Self-Improvement', icon: '✨' },
    { id: 'AI_OPS_EXPERIMENT_MANAGER', label: 'A/B Canary Experiments', icon: '🔬' },
    { id: 'AI_OPS_GOVERNANCE_DASHBOARD', label: 'AI Governance & Compliance', icon: '⚖️' },
    { id: 'AI_OPS_EVOLUTION_TIMELINE', label: 'AI Operations Timeline', icon: '📜' },
    { id: 'AWMPICRP_EXECUTIVE_DASHBOARD', label: 'Autonomous World Model (13.16)', icon: '🔮' },
    { id: 'AWMPICRP_KNOWLEDGE_FUSION', label: 'Knowledge Fusion Center', icon: '🧠' },
    { id: 'AWMPICRP_WORLD_GRAPH', label: 'World Graph Explorer', icon: '🌐' },
    { id: 'AWMPICRP_TEMPORAL_STUDIO', label: 'Temporal Reasoning Studio', icon: '⏳' },
    { id: 'AWMPICRP_CAUSAL_WORKBENCH', label: 'Causal Analysis Workbench', icon: '🔗' },
    { id: 'AWMPICRP_HYPOTHESIS_LAB', label: 'Hypothesis Laboratory', icon: '🧭' },
    { id: 'AWMPICRP_SCENARIO_SIMULATION', label: 'Scenario Simulation Center', icon: '🎲' },
    { id: 'AWMPICRP_COUNTERFACTUAL_STUDIO', label: 'Counterfactual Studio (What-If)', icon: '🪞' },
    { id: 'AWMPICRP_PREDICTIVE_INTELLIGENCE', label: 'Predictive Intelligence Dashboard', icon: '📈' },
    { id: 'AWMPICRP_DECISION_INTELLIGENCE', label: 'Decision Intelligence Center', icon: '🎯' },
    { id: 'AWMPICRP_UNCERTAINTY_EXPLORER', label: 'Uncertainty Explorer & ECE', icon: '🔬' },
    { id: 'AWMPICRP_EVOLUTION_TIMELINE', label: 'World Evolution Timeline', icon: '📜' },
    { id: 'EXECUTION_DASHBOARD', label: 'Autonomous Real-World Operations (13.15)', icon: '⚡' },
    { id: 'EXECUTION_MISSIONS', label: 'Mission Execution Center', icon: '🚀' },
    { id: 'EXECUTION_WORKFLOWS', label: 'Workflow DAG & Saga Designer', icon: '🗺️' },
    { id: 'EXECUTION_TOOLS', label: 'Universal Tool Registry', icon: '🛠️' },
    { id: 'EXECUTION_CONNECTORS', label: 'Connector Gateway Hub', icon: '🔌' },
    { id: 'EXECUTION_BROWSER', label: 'Browser Automation Studio', icon: '🌐' },
    { id: 'EXECUTION_PLANNER', label: 'Critical Path CPM Planner', icon: '📐' },
    { id: 'EXECUTION_POLICY', label: 'Governance & HITL Gates', icon: '🛡️' },
    { id: 'EXECUTION_SIMULATION', label: 'Digital Twin Sandbox', icon: '✨' },
    { id: 'EXECUTION_VERIFICATION', label: 'Verification & State Proofs', icon: '📜' },
    { id: 'EXECUTION_ROLLBACK', label: 'Saga Rollback Recovery', icon: '🔄' },
    { id: 'EXECUTION_AUDIT', label: 'Cryptographic Audit Ledger', icon: '💎' },
    { id: 'EVOLUTION_DASHBOARD', label: 'AI Chief Architect Cockpit (13.13)', icon: '🧬' },
    { id: 'EVOLUTION_CONTINUOUS', label: 'Continuous Self-Evolution Studio', icon: '⚡' },
    { id: 'EVOLUTION_PROFILER', label: 'Runtime Telemetry & Profiler', icon: '⏱️' },
    { id: 'EVOLUTION_CAPABILITY', label: 'Capability Gap Discovery', icon: '🔍' },
    { id: 'EVOLUTION_OPTIMIZER', label: 'Multi-Objective Pareto Studio', icon: '🎛️' },
    { id: 'EVOLUTION_MUTATION', label: 'Self-Modification Workbench', icon: '🛠️' },
    { id: 'EVOLUTION_BENCHMARK', label: 'Empirical Benchmark Analytics', icon: '📊' },
    { id: 'EVOLUTION_SIMULATION', label: 'Digital Twin Replay Sandbox', icon: '🌐' },
    { id: 'EVOLUTION_GOVERNANCE', label: 'Governance & Rollback Center', icon: '🛡️' },
    { id: 'EVOLUTION_DEPLOYMENT', label: 'Canary & Blue/Green Deployer', icon: '🚀' },
    { id: 'EVOLUTION_TIMELINE', label: 'Recursive Evolution Timeline', icon: '⏳' },
    { id: 'EVOLUTION_GENOME', label: 'Platform Architecture Genome', icon: '🧬' },
    { id: 'SCIENCE_EXECUTIVE_DASHBOARD', label: 'Executive Research Cockpit (13.12)', icon: '🔬' },
    { id: 'SCIENCE_DISCOVERY_DASHBOARD', label: 'Scientific Discovery Studio', icon: '✨' },
    { id: 'SCIENCE_HYPOTHESIS_CENTER', label: 'Hypothesis Generation Center (EIG)', icon: '🧭' },
    { id: 'SCIENCE_EXPERIMENT_STUDIO', label: 'Empirical Experiment Studio (A/B)', icon: '🧪' },
    { id: 'SCIENCE_EVIDENCE_EXPLORER', label: 'Evidence & Provenance Ledger', icon: '📜' },
    { id: 'SCIENCE_VALIDATION_WORKBENCH', label: 'Statistical Validation Workbench', icon: '📊' },
    { id: 'SCIENCE_KNOWLEDGE_GRAPH', label: 'Scientific Knowledge Base & Laws', icon: '📖' },
    { id: 'SCIENCE_RESEARCH_PLANNING', label: 'Strategic Research Roadmap Center', icon: '🗺️' },
    { id: 'SCIENCE_PUBLICATION_CENTER', label: 'Publication & DOI Registry Center', icon: '📄' },
    { id: 'SCIENCE_CONSENSUS_REVIEW', label: 'Multi-Agent Consensus Tribunal', icon: '⚖️' },
    { id: 'SCIENCE_ONTOLOGY_EXPLORER', label: 'Semantic Ontology Explorer', icon: '🕸️' },
    { id: 'SCIENCE_DISCOVERY_TIMELINE', label: 'Scientific Discovery Timeline', icon: '⏳' },
    { id: 'STRATEGY_EXECUTIVE_DASHBOARD', label: 'Executive Strategy Cockpit (13.11)', icon: '👑' },

    { id: 'STRATEGY_GOAL_EVOLUTION', label: 'Goal Evolution Center (HTN)', icon: '🎯' },
    { id: 'STRATEGY_MISSION_PORTFOLIO', label: 'Mission Portfolio & Pareto Center', icon: '💼' },
    { id: 'STRATEGY_ROADMAP_STUDIO', label: 'Strategic Roadmap Studio (30-365d)', icon: '🗺️' },
    { id: 'STRATEGY_EXECUTIVE_DECISION', label: 'Executive Decision Center (CSO)', icon: '🏛️' },
    { id: 'STRATEGY_ORGANIZATIONAL_MEMORY', label: 'Organizational Memory & Playbooks', icon: '📚' },
    { id: 'STRATEGY_RESOURCE_NEGOTIATION', label: 'Multi-Swarm Resource Auction', icon: '⚖️' },
    { id: 'STRATEGY_SIMULATION_STUDIO', label: 'Strategy Simulation Studio', icon: '🧪' },
    { id: 'STRATEGY_DECISION_WORKBENCH', label: 'MCDA Decision Workbench (AHP)', icon: '🎛️' },
    { id: 'STRATEGY_INSIGHTS_CENTER', label: 'Strategic Insights & ROI Directives', icon: '💡' },
    { id: 'STRATEGY_GOAL_DEPENDENCY', label: 'Goal Dependency & Conflict Graph', icon: '🕸️' },
    { id: 'STRATEGY_LONG_TERM_PLANNING', label: 'Long-Term Enterprise OKR Center', icon: '🔭' },
    { id: 'WORLD_EXECUTIVE_DASHBOARD', label: 'Executive Future Cockpit (13.10)', icon: '🔮' },
    { id: 'WORLD_DIGITAL_TWIN', label: 'Digital Twin Center', icon: '🌐' },
    { id: 'WORLD_MODEL_EXPLORER', label: 'World Model Explorer', icon: '🌍' },
    { id: 'WORLD_PREDICTIVE_SIMULATION', label: 'Predictive Simulation Studio', icon: '🎲' },
    { id: 'WORLD_SCENARIO_COMPARISON', label: 'Scenario Comparison Workbench', icon: '⚖️' },
    { id: 'WORLD_COUNTERFACTUAL_EXPLORER', label: 'Counterfactual Explorer (What-If)', icon: '🪞' },
    { id: 'WORLD_CAUSAL_GRAPH', label: 'Causal Graph Visualizer (Do-Intervention)', icon: '🔗' },
    { id: 'WORLD_FORECAST_ANALYTICS', label: 'Multi-Horizon Forecast Analytics', icon: '📈' },
    { id: 'WORLD_RISK_PREDICTION', label: 'Predictive Risk Radar', icon: '🛡️' },
    { id: 'WORLD_OPPORTUNITY_DISCOVERY', label: 'Opportunity Discovery Center', icon: '✨' },
    { id: 'WORLD_TEMPORAL_GRAPH', label: 'Temporal Knowledge Graph', icon: '⏳' },
    { id: 'WORLD_PREDICTIVE_GOVERNANCE', label: 'Predictive Governance Center', icon: '📜' },
    { id: 'META_REASONING_CENTER', label: 'Meta-Reasoning Center (13.9)', icon: '🧠' },
    { id: 'META_STRATEGIC_PLANNING', label: 'Strategic Planning Studio', icon: '🧭' },
    { id: 'META_RECURSIVE_REFLECTION', label: 'Recursive Reflection Explorer', icon: '🪞' },
    { id: 'META_EXPERIMENTATION_LAB', label: 'Experimentation Lab (Replay A/B)', icon: '🧪' },
    { id: 'META_CAPABILITY_DISCOVERY', label: 'Capability Discovery Dashboard', icon: '📦' },
    { id: 'META_POLICY_EVOLUTION', label: 'Policy Evolution Center', icon: '📜' },
    { id: 'META_ARCHITECTURE_OPTIMIZER', label: 'Architecture Optimizer', icon: '🏗️' },
    { id: 'META_SELF_IMPROVEMENT', label: 'Self-Improvement Timeline', icon: '🔄' },
    { id: 'META_STRATEGY_WORKBENCH', label: 'Strategy Comparison Workbench', icon: '⚖️' },
    { id: 'META_GOVERNANCE_APPROVAL', label: 'Governance Approval Center', icon: '🛡️' },
    { id: 'META_KNOWLEDGE_GRAPH', label: 'Strategic Knowledge Graph', icon: '🕸️' },
    { id: 'META_EXECUTIVE_DASHBOARD', label: 'Executive Decision Dashboard', icon: '👑' },
    { id: 'SWARM_COMMAND_CENTER', label: 'Swarm Command Center (13.8)', icon: '🐝' },

    { id: 'SWARM_AGENT_REGISTRY', label: 'Agent Registry Explorer', icon: '👥' },
    { id: 'SWARM_COMMUNICATION_BUS', label: 'Communication Bus Monitor', icon: '📡' },
    { id: 'SWARM_NEGOTIATION_STUDIO', label: 'Autonomous Negotiation Studio', icon: '⚖️' },
    { id: 'SWARM_CONSENSUS_DASHBOARD', label: 'Consensus & Voting Engine', icon: '🗳️' },
    { id: 'SWARM_COALITION_MANAGER', label: 'Dynamic Coalition Manager', icon: '🛡️' },
    { id: 'SWARM_TASK_MARKETPLACE', label: 'Task Auction Marketplace', icon: '🛍️' },
    { id: 'SWARM_REPUTATION_ANALYTICS', label: 'Reputation & Trust Analytics', icon: '🎖️' },
    { id: 'SWARM_TRUST_NETWORK', label: 'Trust Network Explorer', icon: '🕸️' },
    { id: 'SWARM_COORDINATION_TIMELINE', label: 'Coordination Replay Timeline', icon: '⏱️' },
    { id: 'SWARM_GOVERNANCE_CENTER', label: 'Swarm Governance Center', icon: '📜' },
    { id: 'SWARM_LEARNING_DASHBOARD', label: 'Swarm Collective Learning', icon: '✨' },
    { id: 'OPERATIONS_COMMAND_CENTER', label: 'Operations Command Center (13.7)', icon: '🩺' },
    { id: 'OPERATIONS_HEALTH_INTELLIGENCE', label: 'Health Intelligence & Topology', icon: '❤️' },
    { id: 'OPERATIONS_INCIDENT_MANAGEMENT', label: 'Incident Management Center', icon: '🚨' },
    { id: 'OPERATIONS_DIAGNOSIS_EXPLORER', label: 'Diagnosis & Root-Cause Explorer', icon: '🧭' },
    { id: 'OPERATIONS_SELF_HEALING', label: 'Self-Healing Studio', icon: '⚡' },
    { id: 'OPERATIONS_RECOVERY_ORCHESTRATION', label: 'Recovery Orchestration', icon: '🔄' },
    { id: 'OPERATIONS_PREDICTIVE_FAILURE', label: 'Predictive Failure Analytics', icon: '🔮' },
    { id: 'OPERATIONS_CHAOS_LAB', label: 'Chaos Engineering Lab', icon: '🔥' },
    { id: 'OPERATIONS_RESILIENCE_SCORECARD', label: 'Resilience Scorecard', icon: '🛡️' },
    { id: 'OPERATIONS_GOVERNANCE_CENTER', label: 'Operational Governance', icon: '📜' },
    { id: 'OPERATIONS_EVENT_TIMELINE', label: 'Operational Event Timeline', icon: '⏱️' },
    { id: 'OPERATIONS_ANALYTICS_DASHBOARD', label: 'Operations Analytics', icon: '📊' },
    { id: 'OPTIMIZATION_RESOURCE_INTELLIGENCE', label: 'Resource Intelligence (13.6)', icon: '⚡' },
    { id: 'OPTIMIZATION_ECONOMIC_CENTER', label: 'Economic Intelligence Center', icon: '💰' },
    { id: 'OPTIMIZATION_DECISION_EXPLORER', label: 'Optimization Decisions', icon: '🧭' },
    { id: 'OPTIMIZATION_STRATEGY_STUDIO', label: 'Strategy Comparison Studio', icon: '⚖️' },
    { id: 'OPTIMIZATION_RESOURCE_ALLOCATION', label: 'Resource Allocation Monitor', icon: '🎫' },
    { id: 'OPTIMIZATION_MODEL_ROUTING', label: 'Model & Tool Routing', icon: '🔀' },
    { id: 'OPTIMIZATION_SCENARIO_LAB', label: 'Scenario Simulation Lab', icon: '🧪' },
    { id: 'OPTIMIZATION_MULTI_OBJECTIVE', label: 'Multi-Objective Pareto Studio', icon: '🎛️' },
    { id: 'OPTIMIZATION_SLA_BUDGET_GOVERNANCE', label: 'SLA & Budget Governance', icon: '🛡️' },
    { id: 'OPTIMIZATION_PREDICTION_ANALYTICS', label: 'Prediction Analytics', icon: '📈' },
    { id: 'OPTIMIZATION_LINEAGE_EXPLORER', label: 'Optimization Lineage (SHA256)', icon: '🔒' },
    { id: 'OPTIMIZATION_RESOURCE_HEALTH', label: 'Resource Health & Capacity', icon: '🩺' },
    { id: 'LEARNING_REFLECTION_CENTER', label: 'Reflection Center (13.5)', icon: '🧠' },
    { id: 'LEARNING_ORGANIZATIONAL_DASHBOARD', label: 'Org Learning Dashboard', icon: '📖' },
    { id: 'LEARNING_PATTERN_MINING', label: 'Pattern Mining Explorer', icon: '🌿' },
    { id: 'LEARNING_KNOWLEDGE_GRAPH', label: 'Knowledge Graph (13.5)', icon: '🕸️' },
    { id: 'LEARNING_KNOWLEDGE_REGISTRY', label: 'Knowledge Registry', icon: '🗄️' },
    { id: 'LEARNING_STRATEGY_LIBRARY', label: 'Strategy Library (13.5)', icon: '📑' },
    { id: 'LEARNING_POLICY_EVOLUTION', label: 'Policy Evolution Center', icon: '🎛️' },
    { id: 'LEARNING_GOVERNANCE_APPROVAL', label: 'Governance Approvals', icon: '🛡️' },
    { id: 'LEARNING_TIMELINE', label: 'Learning Timeline', icon: '⏳' },
    { id: 'LEARNING_KNOWLEDGE_LINEAGE', label: 'Knowledge Lineage (SHA256)', icon: '🔒' },
    { id: 'LEARNING_RECOMMENDATION_STUDIO', label: 'Recommendation Studio', icon: '✨' },
    { id: 'LEARNING_ANALYTICS_DASHBOARD', label: 'Learning Analytics', icon: '📊' },
    { id: 'CONFIDENCE_MISSION_DASHBOARD', label: 'Mission Confidence (13.3)', icon: '🛡️' },
    { id: 'CONFIDENCE_DIMENSION_MATRIX', label: '13-Dimension Matrix', icon: '🎯' },
    { id: 'CONFIDENCE_FORMULA_EXPLORER', label: 'Scientific Formulas', icon: '📐' },
    { id: 'CONFIDENCE_WATERFALL', label: 'Feature Waterfall', icon: '🌊' },
    { id: 'CONFIDENCE_EVIDENCE_EXPLORER', label: 'Runtime Evidence', icon: '🔍' },
    { id: 'CONFIDENCE_TIMELINE', label: 'Confidence Timeline', icon: '⏱️' },
    { id: 'CONFIDENCE_TRENDS', label: 'Confidence Trends', icon: '📈' },
    { id: 'CONFIDENCE_CALIBRATION_DASHBOARD', label: 'Calibration (ECE)', icon: '🎯' },
    { id: 'CONFIDENCE_RELIABILITY_DIAGRAM', label: 'Reliability Diagram', icon: '📊' },
    { id: 'CONFIDENCE_LINEAGE', label: 'Confidence Lineage', icon: '⛓️' },
    { id: 'CONFIDENCE_UNCERTAINTY_INTERVAL', label: 'Uncertainty Intervals', icon: '🔬' },
    { id: 'CONFIDENCE_GOVERNANCE_INSPECTOR', label: 'Formula Governance', icon: '⚖️' },
    { id: 'REPLAY_MISSION_STUDIO', label: 'Mission Replay (13.4)', icon: '▶️' },
    { id: 'REPLAY_TIMELINE_EXPLORER', label: 'Replay Timeline', icon: '⏱️' },
    { id: 'REPLAY_STATE_INSPECTOR', label: 'Runtime State Inspector', icon: '👁️' },
    { id: 'REPLAY_FORENSICS_CENTER', label: 'Replay Forensics', icon: '🔍' },
    { id: 'REPLAY_EVIDENCE_EVOLUTION', label: 'Evidence Evolution', icon: '💎' },
    { id: 'REPLAY_CONFIDENCE_EVOLUTION', label: 'Confidence Evolution', icon: '📈' },
    { id: 'REPLAY_PLANNER_DAG', label: 'Planner DAG Replay', icon: '🗺️' },
    { id: 'REPLAY_DIFF_STUDIO', label: 'Replay Diff Studio', icon: '⚖️' },
    { id: 'REPLAY_AUDIT_GENERATOR', label: 'Audit Package Generator', icon: '📜' },
    { id: 'REPLAY_STATISTICS_DASHBOARD', label: 'Replay Statistics', icon: '📊' },
    { id: 'REPLAY_VERIFICATION_CENTER', label: 'Replay Verification', icon: '🛡️' },
    { id: 'REPLAY_TIME_TRAVEL', label: 'Time Travel & Checkpoints', icon: '🧭' },

    { id: 'EVENT_MISSION_TIMELINE', label: 'Domain Event Timeline', icon: '⏱️' },
    { id: 'EVENT_PLANNER_EVENTS', label: 'Planner Domain Events', icon: '🧠' },
    { id: 'EVENT_WORKER_EVENTS', label: 'Worker Domain Events', icon: '⚙️' },
    { id: 'EVENT_EXPLORER', label: 'Runtime Event Explorer', icon: '🔍' },
    { id: 'EVENT_LIVE_STREAM', label: 'Live SSE Event Stream', icon: '📡' },
    { id: 'EVENT_CORRELATION_EXPLORER', label: 'Correlation & Trace', icon: '🔗' },
    { id: 'EVENT_GRAPH', label: 'Causal Event Graph', icon: '🕸️' },
    { id: 'EVENT_MISSION_TRACE', label: 'Mission Flame Trace', icon: '🔥' },
    { id: 'EVENT_TELEMETRY_STREAM', label: 'Event-Driven Telemetry', icon: '📊' },
    { id: 'EVENT_PROJECTION_INSPECTOR', label: 'Projection Inspector', icon: '🔬' },
    { id: 'PLANNER_LIFECYCLE', label: 'Planner 14-State Lifecycle', icon: '🔄' },
    { id: 'PLANNER_GOAL_ANALYSIS', label: 'Goal Analysis & Constraints', icon: '🎯' },
    { id: 'PLANNER_TASK_DECOMPOSITION', label: 'Task Decomposition', icon: '📑' },
    { id: 'PLANNER_LIVE_DAG', label: 'Live DAG Mutation & Flow', icon: '🕸️' },
    { id: 'PLANNER_SCHEDULER', label: 'DAG Wavefront Scheduler', icon: '⚡' },
    { id: 'PLANNER_WORKER_ASSIGNMENT', label: 'Worker Allocation Proofs', icon: '👥' },
    { id: 'PLANNER_TIMELINE', label: 'Planner Action Timeline', icon: '⏱️' },
    { id: 'PLANNER_DECISION_EXPLORER', label: 'Planner Decision Cards', icon: '📜' },
    { id: 'PLANNER_CRITICAL_PATH', label: 'CPM Critical Path', icon: '📐' },
    { id: 'PLANNER_QUEUE_MONITOR', label: '7-State Runtime Queues', icon: '📋' },
    { id: 'PLANNER_DEPENDENCY_EXPLORER', label: 'DAG Dependency Topology', icon: '🔗' },
    { id: 'PLANNER_REPLAY', label: 'Planner Replay Studio', icon: '🎬' },
    { id: 'RESILIENCE_DIGITAL_TWIN', label: 'Operational Digital Twin', icon: '👥' },
    { id: 'RESILIENCE_CHAOS_LAB', label: 'Autonomous Chaos Lab', icon: '🔥' },
    { id: 'RESILIENCE_INCIDENT_COMMANDER', label: 'Incident Commander', icon: '🚨' },
    { id: 'RESILIENCE_DEPENDENCY_GRAPH', label: 'Blast Radius & Topology', icon: '🕸️' },
    { id: 'RESILIENCE_RECOVERY_TIMELINE', label: 'Recovery Marketplace', icon: '⚡' },
    { id: 'RESILIENCE_INVARIANT_EXPLORER', label: 'Runtime Invariant Monitor', icon: '🛡️' },
    { id: 'RESILIENCE_RELIABILITY_MATH', label: 'Reliability Mathematics', icon: '📐' },
    { id: 'RESILIENCE_PRODUCTION_READINESS', label: 'Production Readiness Score', icon: '🚀' },
    { id: 'RESILIENCE_TIME_MACHINE', label: 'Mission Time Machine', icon: '⏱️' },
    { id: 'RESILIENCE_STRESS_ARENA', label: 'Multi-Mission Stress Arena', icon: '🏟️' },
    { id: 'RESILIENCE_OPERATIONAL_ANALYTICS', label: 'Operational Analytics', icon: '📊' },
    { id: 'RESILIENCE_CERTIFICATION_CENTER', label: 'Enterprise Resilience Dossier', icon: '📜' },
    { id: 'TRUTH_LEDGER_EXPLORER', label: 'Runtime Truth Ledger', icon: '💎' },

    { id: 'DECISION_PROOF_EXPLORER', label: 'Decision Proofs', icon: '📐' },
    { id: 'METRIC_PROVENANCE', label: 'Metric Provenance', icon: '🔬' },
    { id: 'SCIENTIFIC_BENCHMARKS', label: 'Scientific Benchmarks', icon: '🏆' },
    { id: 'REPLAY_CERTIFICATION', label: 'Replay Certification', icon: '🎯' },
    { id: 'TRUST_DASHBOARD', label: 'Trust Scorecard', icon: '🛡️' },
    { id: 'DRIFT_ANALYTICS', label: 'Runtime Drift Analytics', icon: '🌊' },
    { id: 'VERIFICATION_CENTER', label: 'Independent Verification', icon: '⚡' },
    { id: 'MISSION_CERTIFICATION', label: 'Mission Certification', icon: '🎖️' },
    { id: 'SCIENTIFIC_REPORTS', label: 'Scientific Reports', icon: '📜' },
    { id: 'ADAPTIVE_INTELLIGENCE_OVERVIEW', label: 'Adaptive Intelligence', icon: '🧠' },
    { id: 'SCIENTIFIC_IMPROVEMENT_DASHBOARD', label: 'Self-Improvement Proofs', icon: '🏆' },
    { id: 'EXPERIENCE_EXPLORER', label: 'Experience Explorer', icon: '💎' },
    { id: 'STRATEGY_LIBRARY', label: 'Mined Strategy Library', icon: '🧬' },
    { id: 'HYPOTHESIS_LABORATORY', label: 'Hypothesis Lab', icon: '🧪' },
    { id: 'EXPERIMENT_CENTER', label: 'A/B Experiment Center', icon: '📊' },
    { id: 'PREDICTION_ANALYTICS', label: 'Prediction Analytics', icon: '📈' },
    { id: 'CONSENSUS_ANALYZER', label: 'Consensus Intelligence', icon: '🏛️' },
    { id: 'KNOWLEDGE_GRAPH_EXPLORER', label: 'Adaptive Knowledge Graph', icon: '🕸️' },
    { id: 'ORGANIZATIONAL_LEARNING', label: 'Org Learning Curves', icon: '👥' },
    { id: 'CONTINUOUS_OPTIMIZATION_TIMELINE', label: 'Continuous Lifecycle', icon: '⏱️' },
    { id: 'PLATFORM_DASHBOARD', label: 'Agent Platform OS', icon: '🖥️' },
    { id: 'PLUGIN_MARKETPLACE', label: 'Agent Marketplace', icon: '🏪' },
    { id: 'ORGANIZATION_TEMPLATES', label: 'Org Blueprints', icon: '🏛️' },
    { id: 'WORKFLOW_COMPOSER', label: 'Visual Workflow Composer', icon: '🧩' },
    { id: 'WORKFLOW_DSL_EDITOR', label: 'Workflow DSL Editor', icon: '📝' },
    { id: 'CAPABILITY_REGISTRY', label: 'Dynamic Capabilities', icon: '⚙️' },
    { id: 'DYNAMIC_TOOL_REGISTRY', label: 'Dynamic Tools', icon: '🔧' },
    { id: 'POLICY_MANAGER', label: 'Enterprise Policies', icon: '🛡️' },
    { id: 'PLUGIN_CERTIFICATION', label: 'Plugin Certification', icon: '🎖️' },
    { id: 'SANDBOX_INSPECTOR', label: 'Sandbox Isolation', icon: '📦' },
    { id: 'SDK_EXPLORER', label: 'Enterprise Agent SDK', icon: '📚' },
    { id: 'API_CONTRACT_EXPLORER', label: 'API & Contract Explorer', icon: '📜' },
    { id: 'EXTENSION_LIFECYCLE', label: 'Extension Lifecycle', icon: '🔄' },
    { id: 'PLATFORM_DIAGNOSTICS', label: 'Platform Diagnostics', icon: '🩺' },
    { id: 'JUDGE_VERIFICATION_CONSOLE', label: '1-Click Judge Verification', icon: '⚡' },
    { id: 'RUNTIME_TRUTH_DASHBOARD', label: 'Runtime Truth Reality', icon: '💎' },
    { id: 'EVIDENCE_EXPLORER', label: 'Merkle Evidence Explorer', icon: '🔒' },
    { id: 'PLANNER_DECISION_LEDGER', label: 'Planner Decision Ledger', icon: '📜' },
    { id: 'TOOL_CALL_INSPECTOR', label: 'Tool Execution Ledger', icon: '🔬' },
    { id: 'RUNTIME_PROVENANCE_GRAPH', label: 'Lineage Provenance DAG', icon: '🕸️' },
    { id: 'REPRODUCIBILITY_STUDIO', label: 'Deterministic Replay Studio', icon: '🎯' },
    { id: 'BENCHMARK_CERTIFICATE_CENTER', label: 'Certified Benchmarks', icon: '🏆' },
    { id: 'INDEPENDENT_AUDIT_EXPORT', label: 'Independent Audit Export', icon: '📦' },
    { id: 'EXECUTION_EVIDENCE_TIMELINE', label: 'Execution Evidence Timeline', icon: '⏱️' },
    { id: 'ORGANIZATION_OVERVIEW', label: 'Digital Enterprise Org', icon: '🏛️' },
    { id: 'EXECUTIVE_CONTROL_CENTER', label: 'Executive Strategy', icon: '👔' },
    { id: 'DEPARTMENT_MONITOR', label: 'Department Workload', icon: '⚙️' },
    { id: 'NEGOTIATION_STUDIO', label: 'Resource Negotiation', icon: '⚖️' },
    { id: 'ORGANIZATION_HEALTH', label: 'Org Health Index', icon: '🩺' },
    { id: 'INCIDENT_COMMAND_CENTER', label: 'Incident War Room', icon: '🚨' },
    { id: 'LEARNING_EVOLUTION', label: 'Org Learning & Memory', icon: '🧠' },
    { id: 'SLA_INTELLIGENCE', label: 'SLA & Error Budgets', icon: '⏱️' },
    { id: 'ORGANIZATION_SIMULATION', label: '100-Org Digital Twin', icon: '🌐' },
    { id: 'ORGANIZATION_EXECUTIVE_DASHBOARD', label: 'AI CEO Cockpit', icon: '🏛️' },
    { id: 'ORGANIZATION_MISSION_CONTROL', label: 'Mission Control', icon: '🎯' },
    { id: 'ORGANIZATION_STRATEGY_STUDIO', label: 'Strategy Studio', icon: '🧭' },
    { id: 'ORGANIZATION_DESIGNER', label: 'Organization Designer', icon: '🕸️' },
    { id: 'ORGANIZATION_WORKFORCE_CENTER', label: 'Workforce Manager', icon: '👥' },
    { id: 'ORGANIZATION_PROJECT_MANAGER', label: 'Autonomous Project Manager', icon: '📁' },
    { id: 'ORGANIZATION_RESOURCE_OPTIMIZATION', label: 'Resource Intelligence', icon: '⚡' },
    { id: 'ORGANIZATION_PERFORMANCE_DASHBOARD', label: 'Performance Scorecard', icon: '🏆' },
    { id: 'ORGANIZATION_FINANCE_CENTER', label: 'Finance & ROI Center', icon: '💰' },
    { id: 'ORGANIZATION_NEGOTIATION_ARENA', label: 'Negotiation Arena', icon: '⚖️' },
    { id: 'ORGANIZATION_SIMULATION_STUDIO', label: 'Org Digital Twin Sim', icon: '📦' },
    { id: 'ORGANIZATION_EVOLUTION_TIMELINE', label: 'Org Evolution Timeline', icon: '📜' },
    { id: 'HACKATHON_DEMO_CONTROLLER', label: '1-Click Demo Controller', icon: '🎬' },
    { id: 'LIVE_DAG_EXECUTION', label: 'Live Dynamic DAG (CPM)', icon: '🗺️' },
    { id: 'RUNTIME_COST_INTELLIGENCE', label: 'Cost & Energy Matrix', icon: '💰' },
    { id: 'MATHEMATICAL_CONFIDENCE_PROOF', label: 'Confidence Math Proof', icon: '📐' },
    { id: 'RESOURCE_SCHEDULER_MONITOR', label: 'Resource Scheduler', icon: '⚙️' },
    { id: 'CHAOS_RECOVERY_LAB', label: 'Failure Recovery Lab', icon: '⚡' },
    { id: 'AUTOMATED_BENCHMARK_STUDIO', label: '1-Click Benchmark Studio', icon: '🏆' },
    { id: 'FORENSIC_PROVENANCE_AUDIT', label: 'Field Provenance Lineage', icon: '🔬' },
    { id: 'OUTCOME_VERIFICATION', label: 'Outcome Verification', icon: '🎯' },
    { id: 'PREDICTION_ACCURACY', label: 'Prediction Precision', icon: '📈' },
    { id: 'COUNTERFACTUAL_REPLAY', label: 'Counterfactual Lab', icon: '🔀' },
    { id: 'DIGITAL_TWIN_MONITOR', label: 'Digital Twin Sandbox', icon: '👥' },
    { id: 'DRIFT_DETECTION', label: 'Online Drift Center', icon: '🌊' },
    { id: 'EXPERIMENT_DASHBOARD', label: 'A/B Experiment Lab', icon: '🧪' },
    { id: 'CAUSAL_ANALYSIS', label: 'Causal SCM & Interventions', icon: '🕸️' },
    { id: 'POLICY_EVOLUTION', label: 'Policy Evolution & Rollback', icon: '🧬' },
    { id: 'GOVERNANCE_APPROVAL', label: 'Governance Gatekeeper', icon: '🛡️' },
    { id: 'SCIENTIFIC_CERTIFICATION', label: 'Certification Dossier', icon: '📜' },
    { id: 'FEATURE_STORE', label: 'Feature Store Inspector', icon: '🗄️' },
    { id: 'SCIENTIFIC_CONFIDENCE', label: 'Confidence & Evidence Lab', icon: '🎯' },
    { id: 'OPTIMIZER_EXPLORER', label: 'Multi-Objective Optimizer', icon: '⚡' },
    { id: 'PARETO_FRONTIER', label: 'Pareto Frontier', icon: '📈' },
    { id: 'CONSTRAINT_INSPECTOR', label: 'Constraint Inspector', icon: '🛡️' },
    { id: 'RISK_EXPLORER', label: 'Risk & Hazard Model', icon: '⚠️' },
    { id: 'CALIBRATION_LAB', label: 'Calibration Lab (ECE)', icon: '📊' },
    { id: 'POLICY_COMPARISON', label: 'Policy Regret & Drift', icon: '⚖️' },
    { id: 'BENCHMARK_CENTER', label: 'Benchmark Center', icon: '🏆' },
    { id: 'MODEL_ROUTING', label: 'Model Router', icon: '🔀' },
    { id: 'RETRY_OPTIMIZER', label: 'Retry Optimizer', icon: '🔄' },
    { id: 'SCIENTIFIC_METRICS', label: 'Scientific Telemetry', icon: '📐' },
    { id: 'ESMR_REPLAY', label: 'ESMR Replay Runtime', icon: '⏪' },
    { id: 'ESMR_TIMELINE', label: 'ESMR Event Timeline', icon: '⏱️' },
    { id: 'ESMR_DECISIONS', label: 'Decision Provenance DAG', icon: '🧠' },
    { id: 'ESMR_EVOLUTION', label: 'Planner Evolution History', icon: '🧬' },
    { id: 'ESMR_EVIDENCE', label: 'Evidence & Invariants', icon: '🔬' },
    { id: 'ESMR_HUMAN_REVIEW', label: 'Human Review Playback', icon: '👤' },
    { id: 'ESMR_SNAPSHOTS', label: 'Snapshot Manager', icon: '💾' },
    { id: 'ESMR_AUDIT', label: 'Signed Audit Explorer', icon: '🛡️' },
    { id: 'ESMR_INTEGRITY', label: 'Hash Chain Verifier', icon: '🔒' },
    { id: 'ESMR_EXPORTS', label: 'Forensic Export Center', icon: '📦' },
    { id: 'APDLE_GRAPH', label: 'Planner Graph (APDLE)', icon: '🗺️' },
    { id: 'APDLE_EXECUTION_DAG', label: 'Execution Wavefronts', icon: '🌊' },
    { id: 'APDLE_CRITICAL_PATH', label: 'Critical Path (CPM)', icon: '⚡' },
    { id: 'APDLE_WORKERS', label: 'Worker Allocator', icon: '🤖' },
    { id: 'APDLE_DEPENDENCIES', label: 'Dependency Explorer', icon: '🔗' },
    { id: 'APDLE_MUTATIONS', label: 'DAG Mutation Log', icon: '🔄' },
    { id: 'APDLE_SIMULATION', label: 'Monte Carlo Planner Sim', icon: '🎲' },
    { id: 'APDLE_RECOVERY', label: 'Recovery Subgraphs', icon: '🩹' },
    { id: 'AROL_DASHBOARD', label: 'Live Telemetry', icon: '📊' },
    { id: 'AROL_TIMELINE', label: 'Event Timeline', icon: '⏱️' },
    { id: 'AROL_FLAMEGRAPH', label: 'Flame Graph & Profiler', icon: '🔥' },
    { id: 'AROL_TRACES', label: 'Trace Explorer', icon: '🔍' },
    { id: 'STRATEGY_SYNTHESIS', label: 'Strategy Synthesis', icon: '🧬' },
    { id: 'PLANNER_EVOLUTION', label: 'Planner Evolution', icon: '🚀' },
    { id: 'DIGITAL_TWIN', label: 'Digital Twin Sim', icon: '🖥️' },
    { id: 'CAUSAL_REASONING', label: 'Causal Do-Calculus', icon: '🔮' },
    { id: 'COUNCIL_DELIBERATION', label: 'Council Deliberation', icon: '🏛️' },
    { id: 'BELIEF_EXPLORER', label: 'Belief Explorer', icon: '🧠' },
    { id: 'WORLD_FORECAST', label: 'World Simulator', icon: '🌐' },
    { id: 'EVOI_EXPLORER', label: 'EVOI & Sensing', icon: '✨' },
    { id: 'META_REASONING', label: 'Meta Reasoning', icon: '🧭' },
    { id: 'GOVERNANCE_ASSURANCE', label: 'SMT Governance', icon: '🛡️' },
    { id: 'STRATEGY_MATRIX', label: 'Strategy Matrix', icon: '🎯' },
    { id: 'COUNTERFACTUALS', label: 'Counterfactuals', icon: '🔮' },
    { id: 'MUTABLE_DAG', label: 'Mutable DAG', icon: '🔀' },
    { id: 'SCHEDULER', label: 'Worker Scheduler', icon: '⚙️' },
    { id: 'PLANNER_CALIBRATION', label: 'Self-Calibration', icon: '📈' },
    { id: 'RUNTIME_STATS', label: 'Scientific Metrics', icon: '📐' },
    { id: 'BAYESIAN_CONFIDENCE', label: 'Bayesian Fusion', icon: '🎯' },
    { id: 'TRACE_GRAPH', label: 'Trace DAG', icon: '⚡' },
    { id: 'REPLAY_DIFF', label: 'Replay Diff', icon: '⚖️' },
    { id: 'AGENT_INBOX', label: 'Agent Inbox', icon: '📥' },
    { id: 'TASK_BOARD', label: 'Task Board', icon: '📋' },
    { id: 'THOUGHT_STREAM', label: 'Live Thoughts', icon: '💭' },
    { id: 'FEEDBACK_LOOP', label: 'Feedback Loop', icon: '✍️' },
    { id: 'TIMELINE', label: 'Timeline', icon: '⏱️' },
    { id: 'MEMORY_GRAPH', label: 'Memory Graph', icon: '🕸️' },
    { id: 'CONFIDENCE_EXPLORER', label: 'Confidence Breakdown', icon: '📊' },
    { id: 'MISSION_STORY', label: 'Mission Story', icon: '📖' },
    { id: 'CINEMATIC_REPLAY', label: 'Cinematic Movie', icon: '🎬' },
    { id: 'MISSION_REPLAY', label: 'Time Machine Replay', icon: '⏪' },
  ];

  return (
    <div className="w-full space-y-6">
      {/* 1. One-Click Autonomous Demo Controller */}
      <DemoController />

      {/* 2. Workspace Navigation Tabs */}
      <div className="flex items-center overflow-x-auto gap-2 p-1.5 rounded-2xl bg-[#0F172A] border border-[#1E293B] shadow-inner">
        {tabs.map((tab) => {
          const isActive = activeTab === tab.id;

          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`px-4 py-2.5 rounded-xl text-xs font-semibold font-mono flex items-center gap-2 transition-all whitespace-nowrap ${
                isActive
                  ? 'bg-gradient-to-r from-[#0066FF] to-[#00D2FF] text-white shadow-[0_0_15px_rgba(0,210,255,0.35)]'
                  : 'text-[#94A3B8] hover:text-[#F8FAFC] hover:bg-[#131D35]'
              }`}
            >
              <span>{tab.icon}</span>
              <span>{tab.label}</span>
            </button>
          );
        })}
      </div>

      {/* 3. Active Workspace Panel */}
      <div className="w-full">
        {activeTab === 'CONVERSATION' && <ConversationPanel />}
        {activeTab === 'CONFIDENCE_MISSION_DASHBOARD' && <MissionConfidenceDashboard />}
        {activeTab === 'CONFIDENCE_DIMENSION_MATRIX' && <ConfidenceDimensionMatrix />}
        {activeTab === 'CONFIDENCE_FORMULA_EXPLORER' && <ScientificFormulaExplorer />}
        {activeTab === 'CONFIDENCE_WATERFALL' && <FeatureContributionWaterfall />}
        {activeTab === 'CONFIDENCE_EVIDENCE_EXPLORER' && <RuntimeEvidenceExplorer />}
        {activeTab === 'CONFIDENCE_TIMELINE' && <ConfidenceTimeline />}
        {activeTab === 'CONFIDENCE_TRENDS' && <ConfidenceTrendAnalysis />}
        {activeTab === 'CONFIDENCE_CALIBRATION_DASHBOARD' && <CalibrationDashboard />}
        {activeTab === 'CONFIDENCE_RELIABILITY_DIAGRAM' && <ReliabilityDiagramViewer />}
        {activeTab === 'CONFIDENCE_LINEAGE' && <ConfidenceLineageExplorer />}
        {activeTab === 'CONFIDENCE_UNCERTAINTY_INTERVAL' && <UncertaintyIntervalViewer />}
        {activeTab === 'CONFIDENCE_GOVERNANCE_INSPECTOR' && <FormulaGovernanceInspector />}
        {activeTab === 'REPLAY_MISSION_STUDIO' && <MissionReplayStudio />}
        {activeTab === 'REPLAY_TIMELINE_EXPLORER' && <ReplayTimelineExplorer />}
        {activeTab === 'REPLAY_STATE_INSPECTOR' && <RuntimeStateInspector />}
        {activeTab === 'REPLAY_FORENSICS_CENTER' && <ReplayForensicsCenter />}
        {activeTab === 'REPLAY_EVIDENCE_EVOLUTION' && <EvidenceEvolutionExplorer />}
        {activeTab === 'REPLAY_CONFIDENCE_EVOLUTION' && <ConfidenceEvolutionViewer />}
        {activeTab === 'REPLAY_PLANNER_DAG' && <PlannerDAGReplay />}
        {activeTab === 'REPLAY_DIFF_STUDIO' && <ReplayDiffStudio />}
        {activeTab === 'REPLAY_AUDIT_GENERATOR' && <AuditReportGenerator />}
        {activeTab === 'REPLAY_STATISTICS_DASHBOARD' && <ReplayStatisticsDashboard />}
        {activeTab === 'REPLAY_VERIFICATION_CENTER' && <ReplayVerificationCenter />}
        {activeTab === 'REPLAY_TIME_TRAVEL' && <MissionTimeTravelExplorer />}
        {activeTab === 'EVENT_MISSION_TIMELINE' && <MissionTimelineView />}
        {activeTab === 'EVENT_PLANNER_EVENTS' && <PlannerEventsView />}
        {activeTab === 'EVENT_WORKER_EVENTS' && <WorkerEventsView />}
        {activeTab === 'EVENT_EXPLORER' && <RuntimeEventExplorerView />}
        {activeTab === 'EVENT_LIVE_STREAM' && <LiveEventStreamView />}
        {activeTab === 'EVENT_CORRELATION_EXPLORER' && <CorrelationExplorerView />}
        {activeTab === 'EVENT_GRAPH' && <EventGraphView />}
        {activeTab === 'EVENT_MISSION_TRACE' && <MissionTraceView />}
        {activeTab === 'EVENT_TELEMETRY_STREAM' && <TelemetryStreamView />}
        {activeTab === 'EVENT_PROJECTION_INSPECTOR' && <ProjectionInspectorView />}
        {activeTab === 'PLANNER_LIFECYCLE' && <PlannerLifecycleView />}
        {activeTab === 'PLANNER_GOAL_ANALYSIS' && <GoalAnalysisView />}
        {activeTab === 'PLANNER_TASK_DECOMPOSITION' && <TaskDecompositionView />}
        {activeTab === 'PLANNER_LIVE_DAG' && <LiveDAGView />}
        {activeTab === 'PLANNER_SCHEDULER' && <SchedulerView />}
        {activeTab === 'PLANNER_WORKER_ASSIGNMENT' && <WorkerAssignmentView />}
        {activeTab === 'PLANNER_TIMELINE' && <PlannerTimelineView />}
        {activeTab === 'PLANNER_DECISION_EXPLORER' && <PlannerDecisionExplorerView />}
        {activeTab === 'PLANNER_CRITICAL_PATH' && <CriticalPathView />}
        {activeTab === 'PLANNER_QUEUE_MONITOR' && <QueueMonitorView />}
        {activeTab === 'PLANNER_DEPENDENCY_EXPLORER' && <DependencyExplorerView />}
        {activeTab === 'PLANNER_REPLAY' && <PlannerReplayView />}
        {activeTab === 'RESILIENCE_DIGITAL_TWIN' && <DigitalTwinView />}
        {activeTab === 'RESILIENCE_CHAOS_LAB' && <ChaosLabView />}
        {activeTab === 'RESILIENCE_INCIDENT_COMMANDER' && <IncidentCommanderView />}
        {activeTab === 'RESILIENCE_DEPENDENCY_GRAPH' && <DependencyGraphView />}
        {activeTab === 'RESILIENCE_RECOVERY_TIMELINE' && <RecoveryTimelineView />}
        {activeTab === 'RESILIENCE_INVARIANT_EXPLORER' && <InvariantExplorerView />}
        {activeTab === 'RESILIENCE_RELIABILITY_MATH' && <ReliabilityMathematicsView />}
        {activeTab === 'RESILIENCE_PRODUCTION_READINESS' && <ProductionReadinessView />}
        {activeTab === 'RESILIENCE_TIME_MACHINE' && <MissionTimeMachineView />}
        {activeTab === 'RESILIENCE_STRESS_ARENA' && <StressArenaView />}
        {activeTab === 'RESILIENCE_OPERATIONAL_ANALYTICS' && <OperationalAnalyticsView />}
        {activeTab === 'RESILIENCE_CERTIFICATION_CENTER' && <CertificationCenterView />}
        {activeTab === 'TRUTH_LEDGER_EXPLORER' && <TruthLedgerExplorerView />}

        {activeTab === 'DECISION_PROOF_EXPLORER' && <DecisionProofExplorerView />}
        {activeTab === 'METRIC_PROVENANCE' && <MetricProvenanceView />}
        {activeTab === 'SCIENTIFIC_BENCHMARKS' && <ScientificBenchmarksView />}
        {activeTab === 'REPLAY_CERTIFICATION' && <ReplayCertificationView />}
        {activeTab === 'TRUST_DASHBOARD' && <TrustDashboardView />}
        {activeTab === 'DRIFT_ANALYTICS' && <DriftAnalyticsView />}
        {activeTab === 'VERIFICATION_CENTER' && <VerificationCenterView />}
        {activeTab === 'MISSION_CERTIFICATION' && <MissionCertificationView />}
        {activeTab === 'SCIENTIFIC_REPORTS' && <ScientificReportsView />}
        {activeTab === 'ADAPTIVE_INTELLIGENCE_OVERVIEW' && <AdaptiveIntelligenceOverviewView />}
        {activeTab === 'SCIENTIFIC_IMPROVEMENT_DASHBOARD' && <ScientificImprovementDashboardView />}
        {activeTab === 'EXPERIENCE_EXPLORER' && <ExperienceExplorerView />}
        {activeTab === 'STRATEGY_LIBRARY' && <StrategyLibraryView />}
        {activeTab === 'HYPOTHESIS_LABORATORY' && <HypothesisLaboratoryView />}
        {activeTab === 'EXPERIMENT_CENTER' && <ExperimentCenterView />}
        {activeTab === 'PLANNER_EVOLUTION' && <Phase10PlannerEvolutionView />}
        {activeTab === 'PREDICTION_ANALYTICS' && <PredictionAnalyticsView />}
        {activeTab === 'CONSENSUS_ANALYZER' && <ConsensusAnalyzerView />}
        {activeTab === 'KNOWLEDGE_GRAPH_EXPLORER' && <KnowledgeGraphExplorerView />}
        {activeTab === 'ORGANIZATIONAL_LEARNING' && <OrganizationalLearningView />}
        {activeTab === 'CONTINUOUS_OPTIMIZATION_TIMELINE' && <ContinuousOptimizationTimelineView />}
        {activeTab === 'PLATFORM_DASHBOARD' && <PlatformDashboardView />}
        {activeTab === 'PLUGIN_MARKETPLACE' && <PluginMarketplaceView />}
        {activeTab === 'ORGANIZATION_TEMPLATES' && <OrganizationTemplatesView />}
        {activeTab === 'WORKFLOW_COMPOSER' && <WorkflowComposerView />}
        {activeTab === 'WORKFLOW_DSL_EDITOR' && <WorkflowDSLEditorView />}
        {activeTab === 'CAPABILITY_REGISTRY' && <CapabilityRegistryView />}
        {activeTab === 'DYNAMIC_TOOL_REGISTRY' && <DynamicToolRegistryView />}
        {activeTab === 'POLICY_MANAGER' && <PolicyManagerView />}
        {activeTab === 'PLUGIN_CERTIFICATION' && <PluginCertificationView />}
        {activeTab === 'SANDBOX_INSPECTOR' && <SandboxInspectorView />}
        {activeTab === 'SDK_EXPLORER' && <SDKExplorerView />}
        {activeTab === 'API_CONTRACT_EXPLORER' && <APIContractExplorerView />}
        {activeTab === 'EXTENSION_LIFECYCLE' && <ExtensionLifecycleView />}
        {activeTab === 'PLATFORM_DIAGNOSTICS' && <PlatformDiagnosticsView />}
        {activeTab === 'JUDGE_VERIFICATION_CONSOLE' && <JudgeVerificationConsoleView />}
        {activeTab === 'RUNTIME_TRUTH_DASHBOARD' && <RuntimeTruthDashboardView />}
        {activeTab === 'EVIDENCE_EXPLORER' && <Phase8EvidenceExplorerView />}
        {activeTab === 'PLANNER_DECISION_LEDGER' && <PlannerDecisionLedgerView />}
        {activeTab === 'TOOL_CALL_INSPECTOR' && <ToolCallInspectorView />}
        {activeTab === 'RUNTIME_PROVENANCE_GRAPH' && <RuntimeProvenanceGraphView />}
        {activeTab === 'REPRODUCIBILITY_STUDIO' && <ReproducibilityStudioView />}
        {activeTab === 'BENCHMARK_CERTIFICATE_CENTER' && <BenchmarkCertificateCenterView />}
        {activeTab === 'INDEPENDENT_AUDIT_EXPORT' && <IndependentAuditExportView />}
        {activeTab === 'EXECUTION_EVIDENCE_TIMELINE' && <ExecutionEvidenceTimelineView />}
        {activeTab === 'ORGANIZATION_OVERVIEW' && <OrganizationOverviewView />}
        {activeTab === 'EXECUTIVE_CONTROL_CENTER' && <ExecutiveControlCenter />}
        {activeTab === 'DEPARTMENT_MONITOR' && <DepartmentMonitorView />}
        {activeTab === 'NEGOTIATION_STUDIO' && <NegotiationStudioView />}
        {activeTab === 'ORGANIZATION_HEALTH' && <OrganizationHealthView />}
        {activeTab === 'INCIDENT_COMMAND_CENTER' && <IncidentCommandCenter />}
        {activeTab === 'LEARNING_EVOLUTION' && <LearningEvolutionView />}
        {activeTab === 'SLA_INTELLIGENCE' && <SLAIntelligenceView />}
        {activeTab === 'COMMUNICATION_BUS' && <CommunicationBusView />}
        {activeTab === 'ORGANIZATION_SIMULATION' && <OrganizationSimulationView />}
        {activeTab === 'HACKATHON_DEMO_CONTROLLER' && <HackathonDemoControlCenter />}
        {activeTab === 'LIVE_DAG_EXECUTION' && <LiveDAGExecutionView />}
        {activeTab === 'RUNTIME_COST_INTELLIGENCE' && <RuntimeCostIntelligenceView />}
        {activeTab === 'MATHEMATICAL_CONFIDENCE_PROOF' && <MathematicalConfidenceProofView />}
        {activeTab === 'RESOURCE_SCHEDULER_MONITOR' && <ResourceSchedulerMonitorView />}
        {activeTab === 'CHAOS_RECOVERY_LAB' && <FailureChaosRecoveryLabView />}
        {activeTab === 'AUTOMATED_BENCHMARK_STUDIO' && <AutomatedBenchmarkStudioView />}
        {activeTab === 'FORENSIC_PROVENANCE_AUDIT' && <ForensicProvenanceAuditView />}
        {activeTab === 'OUTCOME_VERIFICATION' && <OutcomeVerificationView />}
        {activeTab === 'PREDICTION_ACCURACY' && <PredictionAccuracyView />}
        {activeTab === 'COUNTERFACTUAL_REPLAY' && <CounterfactualReplayLabView />}
        {activeTab === 'DIGITAL_TWIN_MONITOR' && <DigitalTwinMonitorView />}
        {activeTab === 'DRIFT_DETECTION' && <DriftDetectionCenterView />}
        {activeTab === 'EXPERIMENT_DASHBOARD' && <ExperimentDashboardView />}
        {activeTab === 'CAUSAL_ANALYSIS' && <CausalAnalysisView />}
        {activeTab === 'POLICY_EVOLUTION' && <PolicyEvolutionTimelineView />}
        {activeTab === 'GOVERNANCE_APPROVAL' && <GovernanceApprovalCenterView />}
        {activeTab === 'SCIENTIFIC_CERTIFICATION' && <ScientificCertificationReportView />}
        {activeTab === 'FEATURE_STORE' && <FeatureStoreInspectorView />}
        {activeTab === 'SCIENTIFIC_CONFIDENCE' && <ScientificConfidenceView />}
        {activeTab === 'OPTIMIZER_EXPLORER' && <OptimizerExplorerView />}
        {activeTab === 'PARETO_FRONTIER' && <ParetoFrontierView />}
        {activeTab === 'CONSTRAINT_INSPECTOR' && <ConstraintInspectorView />}
        {activeTab === 'RISK_EXPLORER' && <RiskExplorerView />}
        {activeTab === 'CALIBRATION_LAB' && <CalibrationLabView />}
        {activeTab === 'POLICY_COMPARISON' && <PolicyComparisonView />}
        {activeTab === 'BENCHMARK_CENTER' && <BenchmarkCenterView />}
        {activeTab === 'MODEL_ROUTING' && <ModelRoutingExplorerView />}
        {activeTab === 'RETRY_OPTIMIZER' && <RetryOptimizerView />}
        {activeTab === 'SCIENTIFIC_METRICS' && <ScientificMetricsDashboardView />}
        {activeTab === 'ESMR_REPLAY' && <MissionReplayController missionId="mission_demo_001" />}
        {activeTab === 'ESMR_TIMELINE' && <TimelineExplorerView missionId="mission_demo_001" />}
        {activeTab === 'ESMR_DECISIONS' && <DecisionGraphView missionId="mission_demo_001" />}
        {activeTab === 'ESMR_EVOLUTION' && <PlannerEvolutionHistoryView missionId="mission_demo_001" />}
        {activeTab === 'ESMR_EVIDENCE' && <EvidenceExplorerView missionId="mission_demo_001" />}
        {activeTab === 'ESMR_HUMAN_REVIEW' && <HumanReviewReplayView missionId="mission_demo_001" />}
        {activeTab === 'ESMR_SNAPSHOTS' && <SnapshotBrowserView missionId="mission_demo_001" />}
        {activeTab === 'ESMR_AUDIT' && <EnterpriseAuditExplorerView missionId="mission_demo_001" />}
        {activeTab === 'ESMR_INTEGRITY' && <IntegrityVerificationPanel missionId="mission_demo_001" />}
        {activeTab === 'ESMR_EXPORTS' && <EnterpriseExportCenterView missionId="mission_demo_001" />}
        {activeTab === 'APDLE_GRAPH' && <PlannerGraphView />}
        {activeTab === 'APDLE_EXECUTION_DAG' && <ExecutionDAG />}
        {activeTab === 'APDLE_CRITICAL_PATH' && <CriticalPathView />}
        {activeTab === 'APDLE_WORKERS' && <WorkerAllocationView />}
        {activeTab === 'APDLE_DEPENDENCIES' && <DependencyExplorer />}
        {activeTab === 'APDLE_MUTATIONS' && <GraphMutationTimeline />}
        {activeTab === 'APDLE_SIMULATION' && <PlannerSimulationDashboard />}
        {activeTab === 'APDLE_RECOVERY' && <RecoveryGraphViewer />}
        {activeTab === 'AROL_DASHBOARD' && <LiveRuntimeDashboardView />}
        {activeTab === 'AROL_TIMELINE' && <EventSourcedMissionTimeline />}
        {activeTab === 'AROL_FLAMEGRAPH' && <ExecutionFlameGraphViewer />}
        {activeTab === 'AROL_TRACES' && <ObservabilityTraceExplorer />}
        {activeTab === 'STRATEGY_SYNTHESIS' && <StrategySynthesisExplorer />}
        {activeTab === 'PLANNER_EVOLUTION' && <PlannerEvolutionTimeline />}
        {activeTab === 'DIGITAL_TWIN' && <DigitalTwinSimulatorView />}
        {activeTab === 'CAUSAL_REASONING' && <StructuralCausalGraphView />}
        {activeTab === 'COUNCIL_DELIBERATION' && <MultiAgentCouncilPanel />}
        {activeTab === 'BELIEF_EXPLORER' && <BeliefExplorerPanel />}
        {activeTab === 'WORLD_FORECAST' && <WorldPredictionDashboard />}
        {activeTab === 'EVOI_EXPLORER' && <EVOIExplorerPanel />}
        {activeTab === 'META_REASONING' && <MetaReasoningInspector />}
        {activeTab === 'GOVERNANCE_ASSURANCE' && <GovernanceAssuranceMatrix />}
        {activeTab === 'STRATEGY_MATRIX' && <StrategyComparisonMatrixView />}
        {activeTab === 'COUNTERFACTUALS' && <CounterfactualExplorerView />}
        {activeTab === 'MUTABLE_DAG' && <MutableDAGViewerView />}
        {activeTab === 'SCHEDULER' && <ResourceSchedulerDashboardView />}
        {activeTab === 'PLANNER_CALIBRATION' && <PlannerCalibrationCardView />}
        {activeTab === 'RUNTIME_STATS' && <RuntimeStatisticsDashboard />}
        {activeTab === 'BAYESIAN_CONFIDENCE' && <BayesianConfidencePanel />}
        {activeTab === 'TRACE_GRAPH' && <RuntimeTraceGraph />}
        {activeTab === 'REPLAY_DIFF' && <ReplayDiffComparator />}
        {activeTab === 'MISSION_STORY' && <MissionStoryPanel />}
        {activeTab === 'AGENT_INBOX' && <AgentInboxPanel />}
        {activeTab === 'TASK_BOARD' && <TaskBoardPanel />}
        {activeTab === 'THOUGHT_STREAM' && <ThoughtStreamPanel />}
        {activeTab === 'FEEDBACK_LOOP' && <HumanFeedbackPanel />}
        {activeTab === 'TIMELINE' && <LiveTimelinePanel />}
        {activeTab === 'MEMORY_GRAPH' && <MemoryGraphPanel />}
        {activeTab === 'CONFIDENCE_EXPLORER' && <ConfidenceExplorerPanel />}
        {activeTab === 'CINEMATIC_REPLAY' && <CinematicReplayMovie />}
        {activeTab === 'MISSION_REPLAY' && <MissionReplayPlayer />}
        {activeTab === 'LEARNING_REFLECTION_CENTER' && <ReflectionCenter />}
        {activeTab === 'LEARNING_ORGANIZATIONAL_DASHBOARD' && <OrganizationalLearningDashboard />}
        {activeTab === 'LEARNING_PATTERN_MINING' && <PatternMiningExplorer />}
        {activeTab === 'LEARNING_KNOWLEDGE_GRAPH' && <LearningKnowledgeGraphExplorer />}
        {activeTab === 'LEARNING_KNOWLEDGE_REGISTRY' && <KnowledgeRegistryView />}
        {activeTab === 'LEARNING_STRATEGY_LIBRARY' && <Phase135StrategyLibraryView />}
        {activeTab === 'LEARNING_POLICY_EVOLUTION' && <PolicyEvolutionCenter />}
        {activeTab === 'LEARNING_GOVERNANCE_APPROVAL' && <GovernanceApprovalWorkflow />}
        {activeTab === 'LEARNING_TIMELINE' && <LearningTimeline />}
        {activeTab === 'LEARNING_KNOWLEDGE_LINEAGE' && <KnowledgeLineageExplorer />}
        {activeTab === 'LEARNING_RECOMMENDATION_STUDIO' && <RecommendationReviewStudio />}
        {activeTab === 'LEARNING_ANALYTICS_DASHBOARD' && <LearningAnalyticsDashboard />}
        {activeTab === 'OPTIMIZATION_RESOURCE_INTELLIGENCE' && <ResourceIntelligenceDashboard />}
        {activeTab === 'OPTIMIZATION_ECONOMIC_CENTER' && <EconomicIntelligenceCenter />}
        {activeTab === 'OPTIMIZATION_DECISION_EXPLORER' && <OptimizationDecisionExplorer />}
        {activeTab === 'OPTIMIZATION_STRATEGY_STUDIO' && <StrategyComparisonStudio />}
        {activeTab === 'OPTIMIZATION_RESOURCE_ALLOCATION' && <ResourceAllocationMonitor />}
        {activeTab === 'OPTIMIZATION_MODEL_ROUTING' && <ModelToolRoutingExplorer />}
        {activeTab === 'OPTIMIZATION_SCENARIO_LAB' && <ScenarioSimulationLab />}
        {activeTab === 'OPTIMIZATION_MULTI_OBJECTIVE' && <MultiObjectiveOptimizationViewer />}
        {activeTab === 'OPTIMIZATION_SLA_BUDGET_GOVERNANCE' && <SLABudgetGovernanceCenter />}
        {activeTab === 'OPTIMIZATION_PREDICTION_ANALYTICS' && <PredictionAnalyticsDashboard />}
        {activeTab === 'OPTIMIZATION_LINEAGE_EXPLORER' && <OptimizationLineageExplorer />}
        {activeTab === 'OPTIMIZATION_RESOURCE_HEALTH' && <ResourceHealthCapacityDashboard />}
        {activeTab === 'OPERATIONS_COMMAND_CENTER' && <OperationalCommandCenter />}
        {activeTab === 'OPERATIONS_HEALTH_INTELLIGENCE' && <HealthIntelligenceDashboard />}
        {activeTab === 'OPERATIONS_INCIDENT_MANAGEMENT' && <IncidentManagementCenter />}
        {activeTab === 'OPERATIONS_DIAGNOSIS_EXPLORER' && <DiagnosisExplorer />}
        {activeTab === 'OPERATIONS_SELF_HEALING' && <SelfHealingStudio />}
        {activeTab === 'OPERATIONS_RECOVERY_ORCHESTRATION' && <RecoveryOrchestrationCenter />}
        {activeTab === 'OPERATIONS_PREDICTIVE_FAILURE' && <PredictiveFailureAnalytics />}
        {activeTab === 'OPERATIONS_CHAOS_LAB' && <ChaosEngineeringLab />}
        {activeTab === 'OPERATIONS_RESILIENCE_SCORECARD' && <ResilienceScorecard />}
        {activeTab === 'OPERATIONS_GOVERNANCE_CENTER' && <OperationalGovernanceCenter />}
        {activeTab === 'OPERATIONS_EVENT_TIMELINE' && <OperationalEventTimeline />}
        {activeTab === 'OPERATIONS_ANALYTICS_DASHBOARD' && <OperationsAnalyticsDashboard />}
        {activeTab === 'SWARM_COMMAND_CENTER' && <SwarmCommandCenter />}
        {activeTab === 'SWARM_AGENT_REGISTRY' && <AgentRegistryExplorer />}
        {activeTab === 'SWARM_COMMUNICATION_BUS' && <CommunicationMonitor />}
        {activeTab === 'SWARM_NEGOTIATION_STUDIO' && <NegotiationStudio />}
        {activeTab === 'SWARM_CONSENSUS_DASHBOARD' && <ConsensusDashboard />}
        {activeTab === 'SWARM_COALITION_MANAGER' && <CoalitionManagerView />}
        {activeTab === 'SWARM_TASK_MARKETPLACE' && <TaskMarketplaceView />}
        {activeTab === 'SWARM_REPUTATION_ANALYTICS' && <ReputationAnalytics />}
        {activeTab === 'SWARM_TRUST_NETWORK' && <TrustNetworkExplorer />}
        {activeTab === 'SWARM_COORDINATION_TIMELINE' && <CoordinationTimeline />}
        {activeTab === 'SWARM_GOVERNANCE_CENTER' && <SwarmGovernanceCenter />}
        {activeTab === 'SWARM_LEARNING_DASHBOARD' && <SwarmLearningDashboard />}
        {activeTab === 'META_REASONING_CENTER' && <MetaReasoningCenter />}
        {activeTab === 'META_STRATEGIC_PLANNING' && <StrategicPlanningStudio />}
        {activeTab === 'META_RECURSIVE_REFLECTION' && <RecursiveReflectionExplorer />}
        {activeTab === 'META_EXPERIMENTATION_LAB' && <ExperimentationLab />}
        {activeTab === 'META_CAPABILITY_DISCOVERY' && <CapabilityDiscoveryDashboard />}
        {activeTab === 'META_POLICY_EVOLUTION' && <MetaPolicyEvolutionCenter />}
        {activeTab === 'META_ARCHITECTURE_OPTIMIZER' && <ArchitectureOptimizerView />}
        {activeTab === 'META_SELF_IMPROVEMENT' && <SelfImprovementTimeline />}
        {activeTab === 'META_STRATEGY_WORKBENCH' && <StrategyComparisonWorkbench />}
        {activeTab === 'META_GOVERNANCE_APPROVAL' && <MetaGovernanceApprovalCenter />}
        {activeTab === 'META_KNOWLEDGE_GRAPH' && <StrategicKnowledgeGraph />}
        {activeTab === 'META_EXECUTIVE_DASHBOARD' && <ExecutiveDecisionDashboard />}
        {activeTab === 'WORLD_EXECUTIVE_DASHBOARD' && <ExecutiveFutureDashboard />}
        {activeTab === 'WORLD_DIGITAL_TWIN' && <DigitalTwinCenter />}
        {activeTab === 'WORLD_MODEL_EXPLORER' && <WorldModelExplorer />}
        {activeTab === 'WORLD_PREDICTIVE_SIMULATION' && <PredictiveSimulationStudio />}
        {activeTab === 'WORLD_SCENARIO_COMPARISON' && <ScenarioComparisonWorkbench />}
        {activeTab === 'WORLD_COUNTERFACTUAL_EXPLORER' && <CounterfactualExplorer />}
        {activeTab === 'WORLD_CAUSAL_GRAPH' && <CausalGraphVisualizer />}
        {activeTab === 'WORLD_FORECAST_ANALYTICS' && <ForecastAnalytics />}
        {activeTab === 'WORLD_RISK_PREDICTION' && <RiskPredictionDashboard />}
        {activeTab === 'WORLD_OPPORTUNITY_DISCOVERY' && <OpportunityDiscoveryCenter />}
        {activeTab === 'WORLD_TEMPORAL_GRAPH' && <TemporalKnowledgeGraph />}
        {activeTab === 'WORLD_PREDICTIVE_GOVERNANCE' && <PredictiveGovernanceCenter />}
        {activeTab === 'STRATEGY_EXECUTIVE_DASHBOARD' && <ExecutiveStrategyDashboard />}
        {activeTab === 'STRATEGY_GOAL_EVOLUTION' && <GoalEvolutionCenter />}
        {activeTab === 'STRATEGY_MISSION_PORTFOLIO' && <MissionPortfolioCenter />}
        {activeTab === 'STRATEGY_ROADMAP_STUDIO' && <StrategicRoadmapStudio />}
        {activeTab === 'STRATEGY_EXECUTIVE_DECISION' && <ExecutiveDecisionCenter />}
        {activeTab === 'STRATEGY_ORGANIZATIONAL_MEMORY' && <OrganizationalMemoryExplorer />}
        {activeTab === 'STRATEGY_RESOURCE_NEGOTIATION' && <ResourceNegotiationCenter />}
        {activeTab === 'STRATEGY_SIMULATION_STUDIO' && <StrategySimulationStudio />}
        {activeTab === 'STRATEGY_DECISION_WORKBENCH' && <DecisionWorkbench />}
        {activeTab === 'STRATEGY_INSIGHTS_CENTER' && <StrategicInsightsCenter />}
        {activeTab === 'STRATEGY_GOAL_DEPENDENCY' && <GoalDependencyExplorer />}
        {activeTab === 'STRATEGY_LONG_TERM_PLANNING' && <LongTermPlanningCenter />}
        {activeTab === 'SCIENCE_EXECUTIVE_DASHBOARD' && <ExecutiveResearchDashboard />}
        {activeTab === 'SCIENCE_DISCOVERY_DASHBOARD' && <ScientificDiscoveryDashboard />}
        {activeTab === 'SCIENCE_HYPOTHESIS_CENTER' && <HypothesisGenerationCenter />}
        {activeTab === 'SCIENCE_EXPERIMENT_STUDIO' && <ExperimentDesignStudio />}
        {activeTab === 'SCIENCE_EVIDENCE_EXPLORER' && <ScienceEvidenceExplorer />}
        {activeTab === 'SCIENCE_VALIDATION_WORKBENCH' && <ValidationWorkbench />}
        {activeTab === 'SCIENCE_KNOWLEDGE_GRAPH' && <ScienceKnowledgeGraphExplorer />}
        {activeTab === 'SCIENCE_RESEARCH_PLANNING' && <ResearchPlanningCenter />}
        {activeTab === 'SCIENCE_PUBLICATION_CENTER' && <PublicationCenter />}
        {activeTab === 'SCIENCE_CONSENSUS_REVIEW' && <ConsensusReviewCenter />}
        {activeTab === 'SCIENCE_ONTOLOGY_EXPLORER' && <OntologyExplorer />}
        {activeTab === 'SCIENCE_DISCOVERY_TIMELINE' && <DiscoveryTimeline />}
        {activeTab === 'EVOLUTION_DASHBOARD' && <EvolutionExecutiveDashboard />}
        {activeTab === 'EVOLUTION_CONTINUOUS' && <ContinuousImprovementCenter />}
        {activeTab === 'EVOLUTION_PROFILER' && <ArchitectureProfilerCenter />}
        {activeTab === 'EVOLUTION_CAPABILITY' && <CapabilityGapExplorer />}
        {activeTab === 'EVOLUTION_OPTIMIZER' && <ArchitectureOptimizerStudio />}
        {activeTab === 'EVOLUTION_MUTATION' && <MutationWorkbench />}
        {activeTab === 'EVOLUTION_BENCHMARK' && <BenchmarkAnalyticsCenter />}
        {activeTab === 'EVOLUTION_SIMULATION' && <EvolutionSimulationStudio />}
        {activeTab === 'EVOLUTION_GOVERNANCE' && <EvolutionGovernanceApprovalCenter />}
        {activeTab === 'EVOLUTION_DEPLOYMENT' && <DeploymentControlCenter />}
        {activeTab === 'EVOLUTION_TIMELINE' && <RecursiveEvolutionTimeline />}
        {activeTab === 'EVOLUTION_GENOME' && <PlatformGenomeExplorer />}
        {activeTab === 'ORGANIZATION_EXECUTIVE_DASHBOARD' && <OrganizationExecutiveDashboard />}
        {activeTab === 'ORGANIZATION_MISSION_CONTROL' && <MissionControlCenter />}
        {activeTab === 'ORGANIZATION_STRATEGY_STUDIO' && <StrategyGenerationStudio />}
        {activeTab === 'ORGANIZATION_DESIGNER' && <OrganizationDesigner />}
        {activeTab === 'ORGANIZATION_WORKFORCE_CENTER' && <WorkforceManagementCenter />}
        {activeTab === 'ORGANIZATION_PROJECT_MANAGER' && <AutonomousProjectManager />}
        {activeTab === 'ORGANIZATION_RESOURCE_OPTIMIZATION' && <ResourceOptimizationCenter />}
        {activeTab === 'ORGANIZATION_PERFORMANCE_DASHBOARD' && <PerformanceIntelligenceDashboard />}
        {activeTab === 'ORGANIZATION_FINANCE_CENTER' && <FinanceOptimizationCenter />}
        {activeTab === 'ORGANIZATION_NEGOTIATION_ARENA' && <NegotiationArena />}
        {activeTab === 'ORGANIZATION_SIMULATION_STUDIO' && <OrganizationSimulationStudio />}
        {activeTab === 'ORGANIZATION_EVOLUTION_TIMELINE' && <OrganizationalEvolutionTimeline />}
        {activeTab === 'EXECUTION_DASHBOARD' && <ExecutionExecutiveDashboard />}
        {activeTab === 'EXECUTION_MISSIONS' && <MissionExecutionCenter />}
        {activeTab === 'EXECUTION_WORKFLOWS' && <WorkflowDesigner />}
        {activeTab === 'EXECUTION_TOOLS' && <ToolRegistryExplorer />}
        {activeTab === 'EXECUTION_CONNECTORS' && <ConnectorManagementCenter />}
        {activeTab === 'EXECUTION_BROWSER' && <BrowserAutomationStudio />}
        {activeTab === 'EXECUTION_PLANNER' && <ExecutionPlannerStudio />}
        {activeTab === 'EXECUTION_POLICY' && <PolicyGovernanceCenter />}
        {activeTab === 'EXECUTION_SIMULATION' && <SimulationControlCenter />}
        {activeTab === 'EXECUTION_VERIFICATION' && <VerificationWorkbench />}
        {activeTab === 'EXECUTION_ROLLBACK' && <RollbackRecoveryCenter />}
        {activeTab === 'EXECUTION_AUDIT' && <AuditTimelineExplorer />}
        {activeTab === 'AWMPICRP_EXECUTIVE_DASHBOARD' && <WorldModelExecutiveDashboard />}
        {activeTab === 'AWMPICRP_KNOWLEDGE_FUSION' && <WorldModelKnowledgeFusionCenter />}
        {activeTab === 'AWMPICRP_WORLD_GRAPH' && <WorldModelGraphExplorer />}
        {activeTab === 'AWMPICRP_TEMPORAL_STUDIO' && <WorldModelTemporalReasoningStudio />}
        {activeTab === 'AWMPICRP_CAUSAL_WORKBENCH' && <WorldModelCausalAnalysisWorkbench />}
        {activeTab === 'AWMPICRP_HYPOTHESIS_LAB' && <WorldModelHypothesisLaboratory />}
        {activeTab === 'AWMPICRP_SCENARIO_SIMULATION' && <WorldModelScenarioSimulationCenter />}
        {activeTab === 'AWMPICRP_COUNTERFACTUAL_STUDIO' && <WorldModelCounterfactualStudio />}
        {activeTab === 'AWMPICRP_PREDICTIVE_INTELLIGENCE' && <WorldModelPredictiveIntelligenceDashboard />}
        {activeTab === 'AWMPICRP_DECISION_INTELLIGENCE' && <WorldModelDecisionIntelligenceCenter />}
        {activeTab === 'AWMPICRP_UNCERTAINTY_EXPLORER' && <WorldModelUncertaintyExplorer />}
        {activeTab === 'AWMPICRP_EVOLUTION_TIMELINE' && <WorldModelEvolutionTimeline />}
        {activeTab === 'AI_OPS_EXECUTIVE_DASHBOARD' && <AIOperationsExecutiveDashboard />}
        {activeTab === 'AI_OPS_AGENT_OBSERVATORY' && <AgentObservatory />}
        {activeTab === 'AI_OPS_EXECUTION_TRACES' && <ExecutionTraceExplorer />}
        {activeTab === 'AI_OPS_EVALUATION_CENTER' && <EvaluationCenter />}
        {activeTab === 'AI_OPS_PROMPT_LAB' && <PromptLaboratory />}
        {activeTab === 'AI_OPS_MODEL_ROUTING' && <ModelRoutingCenter />}
        {activeTab === 'AI_OPS_COST_INTELLIGENCE' && <CostIntelligenceView />}
        {activeTab === 'AI_OPS_FAILURE_ANALYSIS' && <FailureAnalysisStudio />}
        {activeTab === 'AI_OPS_IMPROVEMENT_STUDIO' && <ImprovementStudio />}
        {activeTab === 'AI_OPS_EXPERIMENT_MANAGER' && <ExperimentManager />}
        {activeTab === 'AI_OPS_GOVERNANCE_DASHBOARD' && <GovernanceDashboard />}
        {activeTab === 'AI_OPS_EVOLUTION_TIMELINE' && <AIEvolutionTimeline />}
        {activeTab === 'DISTRIBUTED_OVERVIEW' && <ClusterOverviewDashboard />}
        {activeTab === 'DISTRIBUTED_WORKERS' && <WorkerFleetManager />}
        {activeTab === 'DISTRIBUTED_QUEUES' && <DistributedQueueMonitor />}
        {activeTab === 'DISTRIBUTED_SCHEDULER' && <SchedulerTimelineView />}
        {activeTab === 'DISTRIBUTED_WORKFLOWS' && <DurableWorkflowInspector />}
        {activeTab === 'DISTRIBUTED_CHECKPOINTS' && <CheckpointExplorer />}
        {activeTab === 'DISTRIBUTED_EVENTS' && <DistributedEventStreamView />}
        {activeTab === 'DISTRIBUTED_AUTOSCALING' && <AutoscalingControlCenter />}
        {activeTab === 'DISTRIBUTED_MULTI_REGION' && <MultiRegionFabricMap />}
        {activeTab === 'DISTRIBUTED_HEALTH_CHAOS' && <InfrastructureHealthStudio />}
        {activeTab === 'DISTRIBUTED_DEPLOYMENT' && <DeploymentCenter />}
        {activeTab === 'DISTRIBUTED_DISASTER_RECOVERY' && <DisasterRecoveryConsole />}
        {activeTab === 'BUSINESS_EXECUTIVE' && <BusinessExecutiveCommandCenter />}
        {activeTab === 'BUSINESS_PROCESS_DESIGNER' && <ProcessDesigner />}
        {activeTab === 'BUSINESS_PROCESS_EXPLORER' && <ProcessExplorer />}
        {activeTab === 'BUSINESS_ORG_GRAPH' && <OrganizationGraphViewer />}
        {activeTab === 'BUSINESS_GOALS' && <GoalManagerStudio />}
        {activeTab === 'BUSINESS_KPIS' && <KPIDashboard />}
        {activeTab === 'BUSINESS_SLA_CENTER' && <SLAIntelligenceCenter />}
        {activeTab === 'BUSINESS_DECISION_RULES' && <DecisionRulesStudio />}
        {activeTab === 'BUSINESS_APPROVAL_CENTER' && <HumanApprovalCenter />}
        {activeTab === 'BUSINESS_PROCESS_DISCOVERY' && <ProcessDiscoveryExplorer />}
        {activeTab === 'BUSINESS_DIGITAL_TWIN' && <DigitalTwinOrgViewer />}
        {activeTab === 'BUSINESS_ROI_SIMULATOR' && <ProcessROISimulator />}
        {activeTab === 'SAAS_EXECUTIVE_DASHBOARD' && <PlatformExecutiveDashboard />}
        {activeTab === 'SAAS_TENANT_MANAGEMENT' && <TenantManagementCenter />}
        {activeTab === 'SAAS_ORGANIZATION_HIERARCHY' && <OrganizationManager />}
        {activeTab === 'SAAS_WORKSPACE_EXPLORER' && <WorkspaceExplorer />}
        {activeTab === 'SAAS_IDENTITY_SSO' && <IdentitySSOCenter />}
        {activeTab === 'SAAS_SUBSCRIPTION_BILLING' && <SubscriptionBillingConsole />}
        {activeTab === 'SAAS_USAGE_ANALYTICS' && <UsageAnalyticsDashboard />}
        {activeTab === 'SAAS_AI_MARKETPLACE' && <MarketplaceManager />}
        {activeTab === 'SAAS_INTEGRATION_HUB' && <IntegrationHub />}
        {activeTab === 'SAAS_POLICY_ADMIN' && <PolicyAdministrationCenter />}
        {activeTab === 'SAAS_WHITE_LABEL_STUDIO' && <WhiteLabelStudio />}
        {activeTab === 'SAAS_AUDIT_EXPLORER' && <EnterpriseAuditExplorer />}
        {activeTab === 'AI_LIFECYCLE_DASHBOARD' && <AIApplicationDashboard />}
        {activeTab === 'AI_LIFECYCLE_REGISTRY' && <AgentRegistry />}
        {activeTab === 'AI_LIFECYCLE_BUILDER' && <AgentBuilder />}
        {activeTab === 'AI_LIFECYCLE_VERSION_EXPLORER' && <VersionExplorer />}
        {activeTab === 'AI_LIFECYCLE_TESTING' && <TestingCenter />}
        {activeTab === 'AI_LIFECYCLE_SECURITY_REVIEW' && <SecurityReviewCenter />}
        {activeTab === 'AI_LIFECYCLE_APPROVALS' && <ApprovalWorkflowCenter />}
        {activeTab === 'AI_LIFECYCLE_DEPLOYMENT' && <AILifecycleDeploymentCenter />}
        {activeTab === 'AI_LIFECYCLE_DEPENDENCY_GRAPH' && <DependencyGraphViewer />}
        {activeTab === 'AI_LIFECYCLE_MARKETPLACE' && <MarketplaceStudio />}
        {activeTab === 'AI_LIFECYCLE_ANALYTICS' && <LifecycleAnalyticsDashboard />}
        {activeTab === 'AI_LIFECYCLE_RETIREMENT' && <RetirementCenter />}
        {activeTab === 'KNOWLEDGE_DASHBOARD' && <KnowledgeDashboard />}
        {activeTab === 'KNOWLEDGE_EXPLORER' && <KnowledgeExplorer />}
        {activeTab === 'KNOWLEDGE_SEMANTIC_SEARCH' && <SemanticSearchStudio />}
        {activeTab === 'KNOWLEDGE_GRAPH' && <Phase21KnowledgeGraphExplorer />}
        {activeTab === 'KNOWLEDGE_SOURCES' && <KnowledgeSourceManager />}
        {activeTab === 'KNOWLEDGE_CONTEXT_DEBUGGER' && <ContextDebugger />}
        {activeTab === 'KNOWLEDGE_MEMORY_OBSERVATORY' && <MemoryObservatory />}
        {activeTab === 'KNOWLEDGE_QUALITY' && <KnowledgeQualityCenter />}
        {activeTab === 'KNOWLEDGE_SECURITY' && <KnowledgeSecurityCenter />}
        {activeTab === 'KNOWLEDGE_EVOLUTION' && <KnowledgeEvolution />}
        {activeTab === 'KNOWLEDGE_ONTOLOGY_BUILDER' && <OntologyBuilder />}
        {activeTab === 'KNOWLEDGE_RETRIEVAL_EVAL' && <RetrievalEvaluation />}
        {activeTab === 'COGNITIVE_EXECUTIVE_DASHBOARD' && <ExecutiveIntelligenceDashboard />}
        {activeTab === 'COGNITIVE_ORGANIZATIONAL_LEARNING' && <OrganizationalLearningCenter />}
        {activeTab === 'COGNITIVE_DECISION_INTELLIGENCE' && <DecisionIntelligenceExplorer />}
        {activeTab === 'COGNITIVE_SIMULATION_STUDIO' && <BusinessSimulationStudio />}
        {activeTab === 'COGNITIVE_AUTONOMOUS_OPTIMIZATION' && <AutonomousOptimizationCenter />}
        {activeTab === 'COGNITIVE_REASONING_GRAPH' && <EnterpriseCognitiveGraph />}
        {activeTab === 'COGNITIVE_PROCESS_DISCOVERY' && <ProcessDiscoveryStudio />}
        {activeTab === 'COGNITIVE_EXPERIENCE_MEMORY' && <ExperienceMemoryExplorer />}
        {activeTab === 'COGNITIVE_GOAL_ALIGNMENT' && <GoalAlignmentCenter />}
        {activeTab === 'COGNITIVE_STRATEGIC_RECOMMENDATIONS' && <StrategicRecommendationCenter />}
        {activeTab === 'COGNITIVE_CONTINUOUS_LEARNING' && <ContinuousLearningMonitor />}
        {activeTab === 'COGNITIVE_INTELLIGENCE_TIMELINE' && <EnterpriseIntelligenceTimeline />}
        {activeTab === 'WORKFORCE_EXECUTIVE_DASHBOARD' && <ExecutiveOrganizationDashboard />}
        {activeTab === 'WORKFORCE_DIGITAL_EXPLORER' && <DigitalWorkforceExplorer />}
        {activeTab === 'WORKFORCE_ORG_CHART' && <OrganizationChartStudio />}
        {activeTab === 'WORKFORCE_TEAM_FORMATION' && <TeamFormationCenter />}
        {activeTab === 'WORKFORCE_TASK_MARKETPLACE' && <TaskMarketplace />}
        {activeTab === 'WORKFORCE_CAREER_CENTER' && <AgentCareerCenter />}
        {activeTab === 'WORKFORCE_MANAGER_CONSOLE' && <ManagerConsole />}
        {activeTab === 'WORKFORCE_EXECUTIVE_COUNCIL' && <ExecutiveCouncil />}
        {activeTab === 'WORKFORCE_PERFORMANCE_ANALYTICS' && <PerformanceAnalytics />}
        {activeTab === 'WORKFORCE_HIRING_STUDIO' && <HiringPromotionStudio />}
        {activeTab === 'WORKFORCE_RESOURCE_ECONOMY' && <ResourceEconomyDashboard />}
        {activeTab === 'WORKFORCE_COLLECTIVE_INTELLIGENCE' && <CollectiveIntelligenceMonitor />}
        {activeTab === 'VERIFICATION_PLATFORM_STUDIO' && <VerificationPlatformStudio />}
      </div>
    </div>
  );
};



