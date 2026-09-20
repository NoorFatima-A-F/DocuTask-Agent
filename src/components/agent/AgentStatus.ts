/**
 * AgentStatus Component Contract & Model
 * 
 * Defines the contract for visualizing an autonomous agent's live operational status,
 * cognitive state, heartbeat, active mission, and role capability.
 */

export type AgentRoleType =
  | 'COORDINATOR'
  | 'PLANNER'
  | 'EVIDENCE'
  | 'BENCHMARK'
  | 'STATISTICS'
  | 'PUBLICATION'
  | 'REVIEWER'
  | 'GOVERNANCE'
  | 'MEMORY'
  | 'REFLECTION'
  | 'EXTRACTION'
  | 'RECONCILIATION';

export type AgentOperationalState =
  | 'IDLE'
  | 'THINKING'
  | 'OBSERVING'
  | 'PLANNING'
  | 'EXECUTING'
  | 'VERIFYING'
  | 'LEARNING'
  | 'WAITING_FOR_HITL'
  | 'PAUSED'
  | 'ERROR'
  | 'TERMINATED';

export interface AgentCognitivePhase {
  phaseName: string;
  startedAtUtc: string;
  estimatedDurationMs?: number;
  progressPercent?: number;
  currentThoughtSummary?: string;
}

export interface AgentMetricTelemetry {
  tokensProcessed: number;
  activeMemoryItemsCount: number;
  decisionsCount: number;
  avgLatencyMs: number;
  uncertaintyScore: number; // 0.0 to 1.0
}

export interface AgentStatusModel {
  agentId: string;
  name: string;
  role: AgentRoleType;
  state: AgentOperationalState;
  cognitivePhase?: AgentCognitivePhase;
  activeMissionId?: string;
  activeGoalDescription?: string;
  telemetry: AgentMetricTelemetry;
  lastHeartbeatUtc: string;
  isAutonomous: boolean;
  requiresAttention: boolean;
  avatarUrl?: string;
}

export interface AgentStatusProps {
  agent: AgentStatusModel;
  variant?: 'compact' | 'card' | 'detailed' | 'drawer';
  showTelemetry?: boolean;
  showThoughtStream?: boolean;
  onSelect?: (agentId: string) => void;
  onPauseResume?: (agentId: string, targetState: 'PAUSED' | 'RESUME') => void;
  className?: string;
}
