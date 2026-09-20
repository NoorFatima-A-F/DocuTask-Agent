/**
 * WorkflowStep Component Contract & Model
 * 
 * Represents a node in the hierarchical Mission Graph (DAG of Actions/Tasks/Subgoals).
 */

export type StepNodeType =
  | 'ACTION'
  | 'TASK'
  | 'SUBGOAL'
  | 'MILESTONE'
  | 'OBJECTIVE';

export type StepExecutionStatus =
  | 'PENDING'
  | 'QUEUED'
  | 'RUNNING'
  | 'COMPLETED'
  | 'FAILED'
  | 'SKIPPED'
  | 'WAITING_FOR_DEPENDENCY'
  | 'BLOCKED';

export interface StepArtifactReference {
  id: string;
  name: string;
  mimeType: string;
  sizeBytes?: number;
  uri: string;
  sha256Digest: string;
}

export interface WorkflowStepModel {
  stepId: string;
  nodeType: StepNodeType;
  title: string;
  description: string;
  assignedAgentRole: string;
  status: StepExecutionStatus;
  dependencyStepIds: string[];
  startedAtUtc?: string;
  completedAtUtc?: string;
  durationMs?: number;
  retryCount: number;
  maxRetries: number;
  inputArtifacts: StepArtifactReference[];
  outputArtifacts: StepArtifactReference[];
  errorMessage?: string;
  isCriticalPath: boolean;
}

export interface WorkflowStepProps {
  step: WorkflowStepModel;
  variant?: 'node' | 'list-item' | 'card' | 'detail';
  isSelected?: boolean;
  onSelect?: (stepId: string) => void;
  onRetry?: (stepId: string) => void;
  className?: string;
}
