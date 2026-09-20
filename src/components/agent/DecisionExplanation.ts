/**
 * DecisionExplanation Component Contract & Model
 * 
 * Provides explainable AI interfaces: rationale, alternatives considered,
 * multi-vector risk evaluation, uncertainty margins, and human-in-the-loop triggers.
 */

export type RiskSeverity = 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';

export interface RiskVectorItem {
  dimension:
    | 'ACCURACY'
    | 'LATENCY'
    | 'SAFETY'
    | 'SECURITY'
    | 'BIAS'
    | 'COST'
    | 'OVERFITTING'
    | 'INFRASTRUCTURE'
    | 'DATASET_SHIFT';
  score: number; // 0.0 to 1.0
  severity: RiskSeverity;
  mitigationStrategy?: string;
}

export interface DecisionAlternative {
  id: string;
  actionName: string;
  expectedScore: number;
  rejectedReason: string;
}

export interface DecisionExplanationModel {
  decisionId: string;
  agentId: string;
  timestampUtc: string;
  primaryAction: string;
  rationale: string;
  confidenceScore: number; // 0.0 to 1.0
  confidenceInterval: [number, number]; // e.g. [0.91, 0.97]
  riskVectors: RiskVectorItem[];
  overallRiskScore: number;
  alternativesConsidered: DecisionAlternative[];
  requiresHumanReview: boolean;
  humanReviewReason?: string;
  evidenceSha256: string;
}

export interface DecisionExplanationProps {
  decision: DecisionExplanationModel;
  variant?: 'inline' | 'drawer' | 'card' | 'modal';
  showRiskRadar?: boolean;
  showAlternatives?: boolean;
  onApprove?: (decisionId: string) => void;
  onReject?: (decisionId: string, reason: string) => void;
  className?: string;
}
