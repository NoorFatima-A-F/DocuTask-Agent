/**
 * Mission Control Domain Types & State Models
 * 
 * Supports the complete autonomous AI coworker experience:
 * 11-stage Cognition Loop, 10-agent multi-agent collaboration, 6-phase goal intelligence,
 * explainable decision center, cryptographic evidence ledger, memory decay inspector,
 * and Zero-Fabrication sentinels.
 */

import type {
  AgentRoleType,
  AgentOperationalState,
  MissionFSMState,
  ZeroFabricationSentinel,
  RiskVectorItem,
} from '../components/agent';

export type CognitionLoopStage =
  | 'GOAL'
  | 'OBSERVE'
  | 'PLAN'
  | 'EXECUTE'
  | 'REFLECT'
  | 'CRITIQUE'
  | 'LEARN'
  | 'UPDATE_MEMORY'
  | 'IMPROVE_PLAN'
  | 'CONTINUE'
  | 'STOP';

export interface CognitionStageDetails {
  stage: CognitionLoopStage;
  label: string;
  status: 'PENDING' | 'ACTIVE' | 'COMPLETED' | 'FAILED' | 'SKIPPED';
  startedAtUtc?: string;
  completedAtUtc?: string;
  durationMs?: number;
  confidenceScore?: number;
  sentinel?: ZeroFabricationSentinel;
  summary: string;
  artifactsProduced: string[];
  evidenceCount: number;
}

export interface GoalUnderstandingData {
  intent: string;
  extractedEntities: Record<string, string>;
  constraints: string[];
  allocatedResources: {
    maxHours: number;
    maxBudgetUsd: number;
  };
  deadlineUtc?: string;
  requiredCapabilities: string[];
  riskSummary: string;
  missingInformation: string[];
}

export interface GoalReasoningData {
  derivedRequirements: string[];
  requiredDatasets: string[];
  requiredBenchmarks: string[];
  evaluationMetrics: string[];
  groundTruthAvailability: string;
  expectedDeliverables: string[];
  publicationStandards: string[];
}

export interface AgentNegotiationParticipant {
  agentRole: AgentRoleType;
  stance: 'APPROVE' | 'REJECT' | 'REQUEST_MORE_EVIDENCE' | 'ADAPT_PLAN';
  rationale: string;
  confidence: number;
  timestampUtc: string;
}

export interface GoalNegotiationData {
  participants: AgentNegotiationParticipant[];
  consensusScore: number; // 0.0 to 1.0
  remainingDisagreements: string[];
  isConsensusAchieved: boolean;
}

export interface GoalUtilityAnalysisData {
  expectedBenefit: number; // 0.0 to 1.0
  probabilityOfSuccess: number; // 0.0 to 1.0
  strategicValue: number;
  noveltyScore: number;
  researchImpact: number;
  estimatedCostUsd: number;
  riskScore: number;
  overallUtilityScore: number;
}

export interface GoalIntelligenceData {
  goalId: string;
  rawGoalStatement: string;
  currentPhase:
    | 'UNDERSTANDING'
    | 'REASONING'
    | 'NEGOTIATION'
    | 'UTILITY_ANALYSIS'
    | 'COMPILATION'
    | 'READY';
  phaseStatus: {
    understanding: 'COMPLETED' | 'ACTIVE' | 'PENDING';
    reasoning: 'COMPLETED' | 'ACTIVE' | 'PENDING';
    negotiation: 'COMPLETED' | 'ACTIVE' | 'PENDING';
    utilityAnalysis: 'COMPLETED' | 'ACTIVE' | 'PENDING';
    compilation: 'COMPLETED' | 'ACTIVE' | 'PENDING';
  };
  understanding: GoalUnderstandingData;
  reasoning: GoalReasoningData;
  negotiation: GoalNegotiationData;
  utility: GoalUtilityAnalysisData;
  missionCompilation: {
    generatedDagNodesCount: number;
    milestonesCount: number;
    tasksCount: number;
    estimatedRuntimeMinutes: number;
    stoppingThresholdConfidence: number;
  };
}

export interface AgentThoughtMessage {
  id: string;
  agentRole: AgentRoleType;
  agentName: string;
  timestampUtc: string;
  thoughtType: 'DELIBERATION' | 'EVIDENCE_DISCOVERY' | 'MEMORY_RECALL' | 'DECISION' | 'CONSENSUS' | 'WARNING';
  content: string;
  confidence?: number;
  parentMessageId?: string;
  referencedArtifactId?: string;
  targetAgentRole?: AgentRoleType;
}

export interface AgentTeamMember {
  agentId: string;
  name: string;
  role: AgentRoleType;
  state: AgentOperationalState;
  currentGoal: string;
  thinkingDurationMs: number;
  lastDecisionSummary: string;
  confidence: number;
  sentinel?: ZeroFabricationSentinel;
  tokensProcessed: number;
  queueSize: number;
  heartbeatUtc: string;
}

export interface MissionDagNode {
  id: string;
  label: string;
  nodeType: 'GOAL' | 'SUBGOAL' | 'TASK' | 'EXECUTION_UNIT' | 'EVIDENCE' | 'PUBLICATION';
  status: 'PENDING' | 'IN_PROGRESS' | 'COMPLETED' | 'FAILED' | 'SKIPPED';
  assignedAgent: AgentRoleType;
  dependencies: string[];
  inputs: string[];
  outputs: string[];
  runtimeSeconds?: number;
  retryCount: number;
  artifactsProduced: string[];
  sha256Digest?: string;
}

export interface DecisionRecord {
  id: string;
  timestampUtc: string;
  decisionTitle: string;
  reasoning: string;
  selectedAction: string;
  confidenceScore: number;
  sentinelState?: ZeroFabricationSentinel;
  supportingEvidenceSummary: string;
  evidenceCount: number;
  alternativesConsidered: {
    actionName: string;
    score: number;
    rejectedReason: string;
  }[];
  tradeoffs: string;
  expectedOutcome: string;
  riskVectors: RiskVectorItem[];
  overallRisk: number;
  estimatedBenefitUsd: number;
  estimatedCostUsd: number;
  estimatedRuntimeMs: number;
  requiresHumanReview: boolean;
  isHumanOverridden: boolean;
  humanOverrideAction?: string;
}

export interface EvidenceItem {
  id: string;
  title: string;
  sourceType: 'DATASET' | 'BENCHMARK' | 'EXPERIMENT' | 'OBSERVATION' | 'REGRESSION_TEST' | 'PUBLICATION';
  origin: string;
  timestampUtc: string;
  sha256Digest: string;
  verificationStatus: 'CRYPTOGRAPHICALLY_VERIFIED' | 'SELF_CONSISTENT' | 'UNVERIFIED' | 'PENDING';
  confidenceContribution: number; // e.g. +0.14
  sampleCount: number;
  slsaLevel: 'SLSA_LEVEL_1' | 'SLSA_LEVEL_2' | 'SLSA_LEVEL_3' | 'SLSA_LEVEL_4';
  lineageParentDigest?: string;
}

export interface MemoryStoreEntry {
  id: string;
  store: 'EPISODIC' | 'LONG_TERM' | 'FAILURE_PATTERN' | 'SUCCESS_PARETO' | 'REGRESSION_TRACE' | 'REFLECTION';
  title: string;
  summary: string;
  createdAtUtc: string;
  lastRecalledUtc: string;
  recallCount: number;
  retentionWeight: number; // R = e^(-lambda * dt) (0.0 to 1.0)
  similarityScore: number; // 0.0 to 1.0
  decayHalfLifeDays: number;
  importanceRating: number; // 1 to 5
  linkedMissionIds: string[];
  sha256Proof: string;
}

export interface ConfidenceCenterData {
  currentConfidence: number; // 0.0 to 1.0
  targetConfidence: number; // e.g. 0.95
  stoppingThreshold: number; // e.g. 0.95
  sampleSize: number;
  marginOfError: number; // e.g. 0.023 (+/- 2.3%)
  confidenceInterval: [number, number]; // [0.949, 0.995]
  statisticalPower: number; // e.g. 0.84
  pValue: number; // e.g. 0.0012
  evidenceCount: number;
  missingEvidenceCount: number;
  uncertaintySources: {
    source: string;
    impactPercentage: number;
    mitigationStatus: string;
  }[];
  whyConfidenceChanged: string;
  trendHistory: {
    timestamp: string;
    confidence: number;
    sampleSize: number;
  }[];
}

export interface HumanControlAuditEntry {
  id: string;
  timestampUtc: string;
  action: 'PAUSE' | 'RESUME' | 'APPROVE' | 'REJECT' | 'REQUEST_EXPLANATION' | 'OVERRIDE' | 'ABORT';
  triggeredBy: string;
  reason: string;
  resultingMissionState: MissionFSMState;
  auditSha256Receipt: string;
}

export interface MissionOverviewData {
  missionId: string;
  title: string;
  goalStatement: string;
  currentState: MissionFSMState;
  owner: string;
  startedAtUtc: string;
  elapsedSeconds: number;
  priority: 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW';
  missionType: 'BENCHMARK_OPTIMIZATION' | 'DOCUMENT_RECONCILIATION' | 'EXTRACTION_PIPELINE' | 'COMPLIANCE_AUDIT';
  confidenceScore: number;
  budgetAllocatedUsd: number;
  budgetConsumedUsd: number;
  hardwareHoursUsed: number;
  readinessScore: number;
  canonicalDigestSha256: string;
}

export interface MissionControlState {
  mission: MissionOverviewData;
  goalIntelligence: GoalIntelligenceData;
  cognitionLoop: CognitionStageDetails[];
  currentCognitionStage: CognitionLoopStage;
  agentTeam: AgentTeamMember[];
  thoughtStream: AgentThoughtMessage[];
  dagNodes: MissionDagNode[];
  selectedDagNodeId?: string;
  decisions: DecisionRecord[];
  selectedDecisionId?: string;
  evidenceItems: EvidenceItem[];
  memoryEntries: MemoryStoreEntry[];
  confidenceData: ConfidenceCenterData;
  humanAuditLogs: HumanControlAuditEntry[];
  isPaused: boolean;
  isSimulatingLive: boolean;
}
