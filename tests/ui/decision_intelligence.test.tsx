import React from 'react';
import { describe, it, expect } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { BeliefExplorerPanel } from '../../src/workspace/intelligence/BeliefExplorerPanel';
import { WorldPredictionDashboard } from '../../src/workspace/intelligence/WorldPredictionDashboard';
import { EVOIExplorerPanel } from '../../src/workspace/intelligence/EVOIExplorerPanel';
import { MetaReasoningInspector } from '../../src/workspace/intelligence/MetaReasoningInspector';
import { GovernanceAssuranceMatrix } from '../../src/workspace/intelligence/GovernanceAssuranceMatrix';
import { WorkspaceProvider } from '../../src/workspace/context/WorkspaceContext';
import { WorkspacePage } from '../../src/workspace/WorkspacePage';

describe('Autonomous Decision Intelligence Platform (ADIP) UI Suite', () => {
  it('renders BeliefExplorerPanel with Shannon Entropy gauge and Bayesian conjugate update triggers', async () => {
    render(<BeliefExplorerPanel />);

    await waitFor(() => {
      expect(screen.getByText('System Shannon Entropy')).toBeDefined();
    });

    expect(screen.getByText(/Probabilistic Belief State/i)).toBeDefined();
    expect(screen.getByText(/Beta Distribution/i)).toBeDefined();
    expect(screen.getByText('Observe Success (+2 α)')).toBeDefined();
    expect(screen.getByText('Observe Failure (+2 β)')).toBeDefined();

    // Trigger Bayesian observation
    const successBtn = screen.getByText('Observe Success (+2 α)');
    fireEvent.click(successBtn);

    await waitFor(() => {
      expect(screen.getByText(/Bayesian update for/i)).toBeDefined();
    });
  });

  it('renders WorldPredictionDashboard with multi-horizon forward forecasts and physics simulation sliders', async () => {
    render(<WorldPredictionDashboard />);

    await waitFor(() => {
      expect(screen.getByText('World Model Forward Simulator')).toBeDefined();
    });

    await waitFor(() => {
      expect(screen.getByText('T + 5m Horizon')).toBeDefined();
      expect(screen.getByText('T + 10m Horizon')).toBeDefined();
      expect(screen.getByText('T + 30m Horizon')).toBeDefined();
    });

    expect(screen.getByText('Re-simulate Physics')).toBeDefined();
  });

  it('renders EVOIExplorerPanel with information gain and sensing action recommendations', async () => {
    render(<EVOIExplorerPanel />);

    await waitFor(() => {
      expect(
        screen.getByText('Active Information Gathering & Expected Value of Information (EVOI)')
      ).toBeDefined();
    });

    await waitFor(() => {
      expect(screen.getByText(/probe_worker_heartbeats/i)).toBeDefined();
      expect(screen.getByText(/deep_ocr_preflight_scan/i)).toBeDefined();
    });

    expect(screen.getByText('RECOMMENDED')).toBeDefined();
    expect(screen.getByText('REJECTED (COST EXCESS)')).toBeDefined();
  });

  it('renders MetaReasoningInspector with Metacognitive Critic and Scientific Benchmark Suite', async () => {
    render(<MetaReasoningInspector />);

    await waitFor(() => {
      expect(screen.getByText('Metacognitive Self-Critic')).toBeDefined();
    });

    expect(screen.getByText('Counterfactual Regret & Autonomous Adaptation')).toBeDefined();
    expect(screen.getByText(/Empirical Scientific Planner Benchmark Suite/i)).toBeDefined();

    await waitFor(() => {
      expect(screen.getByText(/ADIP AAOS Probabilistic Core/i)).toBeDefined();
    });

    expect(screen.getByText('Re-run Scientific Benchmark')).toBeDefined();
  });

  it('renders GovernanceAssuranceMatrix with SMT proofs and cryptographic Merkle provenance', async () => {
    render(<GovernanceAssuranceMatrix />);

    await waitFor(() => {
      expect(screen.getByText('Formal SMT Constraint Verification Proof')).toBeDefined();
    });

    expect(screen.getByText('Z3 SMT SOLVER: SATISFIABLE')).toBeDefined();

    await waitFor(() => {
      expect(screen.getByText('Cryptographic Merkle Decision Provenance Trail')).toBeDefined();
      expect(screen.getByText('Enterprise Regulatory & Compliance Attestation Matrix')).toBeDefined();
    });
  });

  it('integrates all ADIP intelligence tabs into WorkspacePage', async () => {
    render(
      <WorkspaceProvider>
        <WorkspacePage />
      </WorkspaceProvider>
    );

    expect(screen.getByText('Belief Explorer')).toBeDefined();
    expect(screen.getByText('World Simulator')).toBeDefined();
    expect(screen.getByText('EVOI & Sensing')).toBeDefined();
    expect(screen.getByText('Meta Reasoning')).toBeDefined();
    expect(screen.getByText('SMT Governance')).toBeDefined();

    // Switch to Belief Explorer tab
    fireEvent.click(screen.getByText('Belief Explorer'));
    await waitFor(() => {
      expect(screen.getByText('System Shannon Entropy')).toBeDefined();
    });

    // Switch to World Simulator tab
    fireEvent.click(screen.getByText('World Simulator'));
    await waitFor(() => {
      expect(screen.getByText('World Model Forward Simulator')).toBeDefined();
    });

    // Switch to EVOI & Sensing tab
    fireEvent.click(screen.getByText('EVOI & Sensing'));
    await waitFor(() => {
      expect(
        screen.getByText('Active Information Gathering & Expected Value of Information (EVOI)')
      ).toBeDefined();
    });

    // Switch to Meta Reasoning tab
    fireEvent.click(screen.getByText('Meta Reasoning'));
    await waitFor(() => {
      expect(screen.getByText('Metacognitive Self-Critic')).toBeDefined();
    });

    // Switch to SMT Governance tab
    fireEvent.click(screen.getByText('SMT Governance'));
    await waitFor(() => {
      expect(screen.getByText('Formal SMT Constraint Verification Proof')).toBeDefined();
    });
  });
});
