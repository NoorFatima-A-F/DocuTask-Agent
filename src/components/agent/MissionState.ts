/**
 * MissionState Component Contract & Model
 * 
 * Maps directly to the 14-state deterministic Finite State Machine (FSM):
 * CREATED -> VALIDATING -> VALIDATED -> ANALYZING_CAPABILITIES ->
 * ANALYZING_DEPENDENCIES -> ANALYZING_RISK -> ESTIMATING_BUDGET ->
 * GENERATING_SUCCESS_CRITERIA -> READY_FOR_OBSERVATION -> ACTIVE ->
 * PAUSED -> COMPLETED / FAILED / ABORTED / ARCHIVED.
 */

export type MissionFSMState =
  | 'CREATED'
  | 'VALIDATING'
  | 'VALIDATED'
  | 'ANALYZING_CAPABILITIES'
  | 'ANALYZING_DEPENDENCIES'
  | 'ANALYZING_RISK'
  | 'ESTIMATING_BUDGET'
  | 'GENERATING_SUCCESS_CRITERIA'
  | 'READY_FOR_OBSERVATION'
  | 'ACTIVE'
  | 'PAUSED'
  | 'COMPLETED'
  | 'FAILED'
  | 'ABORTED'
  | 'ARCHIVED';

export interface StateTransitionAuditRecord {
  transitionId: string;
  fromState: MissionFSMState;
  toState: MissionFSMState;
  timestampUtc: string;
  reason: string;
  triggeredBy: string;
  metadata?: Record<string, unknown>;
}

export interface MissionBudgetSummary {
  estimatedHardwareHours: number;
  consumedHardwareHours: number;
  estimatedCostUsd: number;
  consumedCostUsd: number;
  currency: string;
}

export interface MissionStateModel {
  missionId: string;
  goalId: string;
  title: string;
  currentState: MissionFSMState;
  stateHistory: StateTransitionAuditRecord[];
  createdAtUtc: string;
  updatedAtUtc: string;
  budget: MissionBudgetSummary;
  readinessScore: number; // 0.0 to 1.0
  totalNodesCount: number;
  completedNodesCount: number;
  canonicalDigest: string; // SHA-256
  isBlocked: boolean;
  blockReason?: string;
}

export interface MissionStateProps {
  mission: MissionStateModel;
  variant?: 'badge' | 'progress-stepper' | 'hero' | 'summary';
  showAuditTrail?: boolean;
  onTransitionRequest?: (missionId: string, targetState: MissionFSMState) => void;
  className?: string;
}
