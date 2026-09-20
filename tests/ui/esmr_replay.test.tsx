import React from 'react';
import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import { WorkspaceProvider } from '../../src/workspace/context/WorkspaceContext';
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
} from '../../src/workspace/replay';

describe('Phase 3 — Event-Sourced Mission Replay, Decision Provenance & Enterprise Audit (ESMR) UI Suite', () => {
  beforeEach(() => {
    vi.spyOn(globalThis, 'fetch').mockImplementation(() => {
      return Promise.reject(new Error('Network offline in unit test'));
    });
  });

  it('renders MissionReplayController with deterministic status and transport controls', async () => {
    render(
      <WorkspaceProvider>
        <MissionReplayController missionId="test_mission_001" />
      </WorkspaceProvider>
    );

    await waitFor(() => {
      expect(screen.getAllByText(/Event-Sourced Mission Replay Runtime/i).length).toBeGreaterThan(0);
      expect(screen.getAllByText(/DETERMINISTIC/i).length).toBeGreaterThan(0);
      expect(screen.getAllByText(/Speed:/i).length).toBeGreaterThan(0);
      expect(screen.getAllByText(/Genesis/i).length).toBeGreaterThan(0);
      expect(screen.getAllByText(/Live Head/i).length).toBeGreaterThan(0);
    });
  });

  it('renders TimelineExplorerView with chronological event stream and category filters', async () => {
    render(
      <WorkspaceProvider>
        <TimelineExplorerView missionId="test_mission_001" />
      </WorkspaceProvider>
    );

    await waitFor(() => {
      expect(screen.getAllByText(/Event-Sourced Mission Timeline Explorer/i).length).toBeGreaterThan(0);
      expect(screen.getAllByText(/Total Events:/i).length).toBeGreaterThan(0);
    });
  });

  it('renders DecisionGraphView with 4 explainability pillars and utility metrics', async () => {
    render(
      <WorkspaceProvider>
        <DecisionGraphView missionId="test_mission_001" />
      </WorkspaceProvider>
    );

    await waitFor(() => {
      expect(screen.getAllByText(/Decision Provenance & Explainability Graph/i).length).toBeGreaterThan(0);
      expect(screen.getAllByText(/1. Why \(Rationale\)/i).length).toBeGreaterThan(0);
      expect(screen.getAllByText(/2. What \(Action Executed\)/i).length).toBeGreaterThan(0);
      expect(screen.getAllByText(/3. Based On \(Evidence\)/i).length).toBeGreaterThan(0);
      expect(screen.getAllByText(/4. Why Not Others \(Counterfactuals\)/i).length).toBeGreaterThan(0);
    });
  });

  it('renders PlannerEvolutionHistoryView with generational mutations and rejected alternatives', async () => {
    render(
      <WorkspaceProvider>
        <PlannerEvolutionHistoryView missionId="test_mission_001" />
      </WorkspaceProvider>
    );

    await waitFor(() => {
      expect(screen.getAllByText(/Autonomous Planner Evolution & Mutation History/i).length).toBeGreaterThan(0);
      expect(screen.getAllByText(/Generation 1/i).length).toBeGreaterThan(0);
    });
  });

  it('renders EvidenceExplorerView with SMT Invariants, Spatial BBoxes and artifacts', async () => {
    render(
      <WorkspaceProvider>
        <EvidenceExplorerView missionId="test_mission_001" />
      </WorkspaceProvider>
    );

    await waitFor(() => {
      expect(screen.getAllByText(/Forensic Evidence & Invariant Proof Explorer/i).length).toBeGreaterThan(0);
      expect(screen.getAllByText(/SMT FORMAL PROOF: SATISFIABLE \(SAT\)/i).length).toBeGreaterThan(0);
    });
  });

  it('renders HumanReviewReplayView with human-in-the-loop gate status', async () => {
    render(
      <WorkspaceProvider>
        <HumanReviewReplayView missionId="test_mission_001" />
      </WorkspaceProvider>
    );

    await waitFor(() => {
      expect(screen.getAllByText(/Human Review & Intervention Playback/i).length).toBeGreaterThan(0);
      expect(screen.getAllByText(/HUMAN_APPROVAL_GATE/i).length).toBeGreaterThan(0);
    });
  });

  it('renders SnapshotBrowserView with compressed state checkpoints and size ratios', async () => {
    render(
      <WorkspaceProvider>
        <SnapshotBrowserView missionId="test_mission_001" />
      </WorkspaceProvider>
    );

    await waitFor(() => {
      expect(screen.getAllByText(/Snapshot Manager & Checkpoint Browser/i).length).toBeGreaterThan(0);
      expect(screen.getAllByText(/Ratio:/i).length).toBeGreaterThan(0);
    });
  });

  it('renders EnterpriseAuditExplorerView with HMAC-SHA256 signature chain verification', async () => {
    render(
      <WorkspaceProvider>
        <EnterpriseAuditExplorerView missionId="test_mission_001" />
      </WorkspaceProvider>
    );

    await waitFor(() => {
      expect(screen.getAllByText(/Cryptographically Signed Enterprise Audit Trail/i).length).toBeGreaterThan(0);
      expect(screen.getAllByText(/HMAC-SHA256 AUDIT CHAIN VALID/i).length).toBeGreaterThan(0);
    });
  });

  it('renders IntegrityVerificationPanel with unbroken SHA-256 hash-chain status', async () => {
    render(
      <WorkspaceProvider>
        <IntegrityVerificationPanel missionId="test_mission_001" />
      </WorkspaceProvider>
    );

    await waitFor(() => {
      expect(screen.getAllByText(/Cryptographic SHA-256 Hash Chain Integrity Verifier/i).length).toBeGreaterThan(0);
      expect(screen.getAllByText(/SHA-256 HASH CHAIN INTEGRITY: 100% UNBROKEN/i).length).toBeGreaterThan(0);
    });
  });

  it('renders EnterpriseExportCenterView with JSON, CSV, and SOC2 compliance export buttons', async () => {
    render(
      <WorkspaceProvider>
        <EnterpriseExportCenterView missionId="test_mission_001" />
      </WorkspaceProvider>
    );

    await waitFor(() => {
      expect(screen.getAllByText(/Enterprise Forensic Export Center/i).length).toBeGreaterThan(0);
      expect(screen.getAllByText(/Download JSON Package/i).length).toBeGreaterThan(0);
      expect(screen.getAllByText(/Download CSV Log/i).length).toBeGreaterThan(0);
      expect(screen.getAllByText(/Export Compliance Report/i).length).toBeGreaterThan(0);
    });
  });
});
