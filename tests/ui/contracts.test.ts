import { describe, it, expect } from 'vitest';
import { designTokens, colors, typography, spacing, shadows, borders, animations } from '../../src/design-system';
import type {
  AgentStatusModel,
  MissionStateModel,
  WorkflowStepModel,
  DecisionExplanationModel,
  ConfidenceScoreModel,
  MemoryInsightModel,
} from '../../src/components/agent';

describe('DocuTask Agent Design System Tokens', () => {
  it('should export all brand and agent state colors', () => {
    expect(colors.brand.primary).toBe('#0066FF');
    expect(colors.brand.secondary).toBe('#00D2FF');
    expect(colors.agent.thinking).toBe('#00D2FF');
    expect(colors.agent.completed).toBe('#10B981');
    expect(colors.agent.verifying).toBe('#8B5CF6');
  });

  it('should export zero-fabrication sentinels', () => {
    expect(colors.sentinel.unknown).toBeDefined();
    expect(colors.sentinel.notCollected).toBeDefined();
    expect(colors.sentinel.insufficientEvidence).toBeDefined();
  });

  it('should contain valid typography, spacing, shadows, and borders', () => {
    expect(typography.fontFamily.sans).toContain('Inter');
    expect(typography.fontFamily.mono).toContain('JetBrains Mono');
    expect(spacing[4]).toBe('1rem');
    expect(shadows.glowCobalt).toContain('rgba(0, 102, 255');
    expect(borders.radius.lg).toBe('12px');
    expect(animations.duration.normal).toBe('250ms');
    expect(designTokens.layout.sidebarWidth).toBe('280px');
  });
});

describe('Agent Component Contract Typings', () => {
  it('should validate AgentStatusModel contract', () => {
    const agent: AgentStatusModel = {
      agentId: 'agent_ocr_001',
      name: 'DocuTask Invoice Specialist',
      role: 'EXTRACTION',
      state: 'THINKING',
      cognitivePhase: {
        phaseName: 'OBSERVING',
        startedAtUtc: '2026-09-08T18:00:00Z',
        currentThoughtSummary: 'Analyzing table bounding boxes in invoice scan #44',
      },
      telemetry: {
        tokensProcessed: 14200,
        activeMemoryItemsCount: 42,
        decisionsCount: 9,
        avgLatencyMs: 145,
        uncertaintyScore: 0.04,
      },
      lastHeartbeatUtc: '2026-09-08T18:01:00Z',
      isAutonomous: true,
      requiresAttention: false,
    };

    expect(agent.state).toBe('THINKING');
    expect(agent.isAutonomous).toBe(true);
  });

  it('should validate 14-state MissionStateModel contract', () => {
    const mission: MissionStateModel = {
      missionId: 'mission_9941',
      goalId: 'goal_invoice_f1_95',
      title: 'Optimize Invoice Extraction F1',
      currentState: 'READY_FOR_OBSERVATION',
      stateHistory: [
        {
          transitionId: 'tr_01',
          fromState: 'CREATED',
          toState: 'VALIDATING',
          timestampUtc: '2026-09-08T18:00:00Z',
          reason: 'Initial submission',
          triggeredBy: 'System',
        },
        {
          transitionId: 'tr_02',
          fromState: 'VALIDATING',
          toState: 'READY_FOR_OBSERVATION',
          timestampUtc: '2026-09-08T18:00:05Z',
          reason: 'All checks passed',
          triggeredBy: 'MissionBuilder',
        },
      ],
      createdAtUtc: '2026-09-08T18:00:00Z',
      updatedAtUtc: '2026-09-08T18:00:05Z',
      budget: {
        estimatedHardwareHours: 1.5,
        consumedHardwareHours: 0.0,
        estimatedCostUsd: 2.4,
        consumedCostUsd: 0.0,
        currency: 'USD',
      },
      readinessScore: 0.94,
      totalNodesCount: 5,
      completedNodesCount: 0,
      canonicalDigest: 'a1b2c3d4e5f6',
      isBlocked: false,
    };

    expect(mission.currentState).toBe('READY_FOR_OBSERVATION');
    expect(mission.stateHistory.length).toBe(2);
  });

  it('should validate DecisionExplanationModel and risk vectors', () => {
    const decision: DecisionExplanationModel = {
      decisionId: 'dec_001',
      agentId: 'agent_ocr_001',
      timestampUtc: '2026-09-08T18:05:00Z',
      primaryAction: 'APPLY_ADAPTIVE_THRESHOLDING',
      rationale: 'Image contrast in region (120, 450) is below 0.35 threshold.',
      confidenceScore: 0.965,
      confidenceInterval: [0.94, 0.98],
      riskVectors: [
        { dimension: 'ACCURACY', score: 0.05, severity: 'LOW' },
        { dimension: 'LATENCY', score: 0.12, severity: 'LOW' },
      ],
      overallRiskScore: 0.085,
      alternativesConsidered: [
        {
          id: 'alt_01',
          actionName: 'GLOBAL_OTSU_BINARIZATION',
          expectedScore: 0.82,
          rejectedReason: 'High degradation on bottom-left watermark.',
        },
      ],
      requiresHumanReview: false,
      evidenceSha256: 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
    };

    expect(decision.primaryAction).toBe('APPLY_ADAPTIVE_THRESHOLDING');
    expect(decision.confidenceScore).toBeGreaterThan(0.9);
  });

  it('should validate ConfidenceScoreModel with zero-fabrication sentinels', () => {
    const sentinelScore: ConfidenceScoreModel = {
      metricName: 'Character Recognition Accuracy',
      sentinelState: 'NOT_COLLECTED',
      methodology: 'Ground-truth Levenshtein distance',
    };

    expect(sentinelScore.sentinelState).toBe('NOT_COLLECTED');
    expect(sentinelScore.value).toBeUndefined();
  });

  it('should validate MemoryInsightModel with retention decay', () => {
    const memory: MemoryInsightModel = {
      memoryId: 'mem_inv_04',
      storeType: 'SUCCESS_PARETO',
      title: 'Optimal Binarization Parameter for Thermal Scans',
      summary: 'Threshold scale 1.25 yields 99.1% precision on receipt dates.',
      createdAtUtc: '2026-09-08T12:00:00Z',
      lastRecalledAtUtc: '2026-09-08T18:00:00Z',
      recallCount: 8,
      decayRetentionScore: 0.92,
      relevanceSimilarity: 0.88,
      tags: ['thermal_receipts', 'binarization', 'dates'],
      sha256Proof: 'f6e0a4b2c1d3...',
    };

    expect(memory.decayRetentionScore).toBe(0.92);
    expect(memory.tags).toContain('thermal_receipts');
  });
});
