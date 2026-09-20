/**
 * MemoryInsight Component Contract & Model
 * 
 * Visualizes autonomous agent episodic memory, retention decay (R = e^(-lambda * dt)),
 * recall frequency, and learned invariants.
 */

export type MemoryStoreType =
  | 'EPISODIC'
  | 'LONG_TERM'
  | 'SUCCESS_PARETO'
  | 'FAILURE_PATTERN'
  | 'REGRESSION_TRACE'
  | 'KNOWLEDGE_GRAPH';

export interface MemoryInsightModel {
  memoryId: string;
  storeType: MemoryStoreType;
  title: string;
  summary: string;
  createdAtUtc: string;
  lastRecalledAtUtc: string;
  recallCount: number;
  decayRetentionScore: number; // 0.0 to 1.0 (R = e^(-lambda * dt))
  relevanceSimilarity: number; // 0.0 to 1.0
  tags: string[];
  associatedMissionId?: string;
  sha256Proof: string;
}

export interface MemoryInsightProps {
  memory: MemoryInsightModel;
  variant?: 'card' | 'compact' | 'graph-node' | 'timeline-item';
  onReinforce?: (memoryId: string) => void;
  onInspect?: (memoryId: string) => void;
  className?: string;
}
