import React from 'react';
import { describe, it, expect } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { StrategySynthesisExplorer } from '../../src/workspace/evolution/StrategySynthesisExplorer';
import { PlannerEvolutionTimeline } from '../../src/workspace/evolution/PlannerEvolutionTimeline';
import { DigitalTwinSimulatorView } from '../../src/workspace/evolution/DigitalTwinSimulatorView';
import { StructuralCausalGraphView } from '../../src/workspace/evolution/StructuralCausalGraphView';
import { MultiAgentCouncilPanel } from '../../src/workspace/evolution/MultiAgentCouncilPanel';
import { WorkspaceProvider } from '../../src/workspace/context/WorkspaceContext';
import { WorkspacePage } from '../../src/workspace/WorkspacePage';

describe('Autonomous Cognitive Evolution (ACOS) UI Suite', () => {
  it('renders StrategySynthesisExplorer with HTN graph nodes and novelty score', async () => {
    render(<StrategySynthesisExplorer />);

    await waitFor(() => {
      expect(screen.getByText('Novelty Score (k-NN)')).toBeDefined();
    });

    expect(screen.getByText(/Synthesized Hierarchical Task DAG/i)).toBeDefined();
    expect(screen.getByText('Constrained Operator AST')).toBeDefined();
    expect(screen.getByText('Mutate Topology')).toBeDefined();

    // Trigger mutation
    const mutateBtn = screen.getByText('Mutate Topology');
    fireEvent.click(mutateBtn);

    await waitFor(() => {
      expect(screen.getByText(/Applied Evolutionary Mutation/i)).toBeDefined();
    });
  });

  it('renders PlannerEvolutionTimeline with generation genealogy and self-evolution trigger', async () => {
    render(<PlannerEvolutionTimeline />);

    await waitFor(() => {
      expect(screen.getByText('Planner Self-Evolution & Continuous Rewriting Engine')).toBeDefined();
    });

    await waitFor(() => {
      expect(screen.getByText('v1.0.0')).toBeDefined();
      expect(screen.getByText('v2.0.0')).toBeDefined();
      expect(screen.getByText('v3.0.0')).toBeDefined();
    });

    expect(screen.getByText('Evolve Next Planner Generation')).toBeDefined();

    // Trigger evolution
    const evolveBtn = screen.getByText('Evolve Next Planner Generation');
    fireEvent.click(evolveBtn);

    await waitFor(() => {
      expect(screen.getByText(/Evolution Cycle Success/i)).toBeDefined();
    });
  });

  it('renders DigitalTwinSimulatorView with 1000-worker cluster physics and latency percentiles', async () => {
    render(<DigitalTwinSimulatorView />);

    await waitFor(() => {
      expect(
        screen.getByText('Digital Twin Distributed Cluster Simulator (1,000+ Workers)')
      ).toBeDefined();
    });

    await waitFor(() => {
      expect(screen.getByText('Tail Latency Breakdown')).toBeDefined();
      expect(screen.getByText('Cluster Hardware Headroom')).toBeDefined();
      expect(screen.getByText('Run 500-Mission Simulation')).toBeDefined();
    });
  });

  it('renders StructuralCausalGraphView with Pearl Do-Calculus intervention sliders and SCM nodes', async () => {
    render(<StructuralCausalGraphView />);

    await waitFor(() => {
      expect(
        screen.getByText("Structural Causal Models & Pearl's Do-Calculus Interventions")
      ).toBeDefined();
    });

    await waitFor(() => {
      expect(screen.getByText('Interventional Effect Calculation')).toBeDefined();
      expect(screen.getByText('SCM Variable Nodes')).toBeDefined();
    });
  });

  it('renders MultiAgentCouncilPanel with 8 specialized agent arguments and Borda tally', async () => {
    render(<MultiAgentCouncilPanel />);

    await waitFor(() => {
      expect(
        screen.getByText('Autonomous Multi-Agent Deliberation Council (8 Specialized Agents)')
      ).toBeDefined();
    });

    await waitFor(() => {
      expect(screen.getByText('Borda Point Standings')).toBeDefined();
      expect(screen.getByText('Vickrey Second-Price Auction Ledger')).toBeDefined();
      expect(screen.getByText(/Council Consensus/i)).toBeDefined();
    });
  });

  it('integrates all ACOS evolution tabs into WorkspacePage', async () => {
    render(
      <WorkspaceProvider>
        <WorkspacePage />
      </WorkspaceProvider>
    );

    expect(screen.getByText('Strategy Synthesis')).toBeDefined();
    expect(screen.getByText('Planner Evolution')).toBeDefined();
    expect(screen.getByText('Digital Twin Sim')).toBeDefined();
    expect(screen.getByText('Causal Do-Calculus')).toBeDefined();
    expect(screen.getByText('Council Deliberation')).toBeDefined();

    // Click Strategy Synthesis tab
    fireEvent.click(screen.getByText('Strategy Synthesis'));
    await waitFor(() => {
      expect(screen.getByText('Novelty Score (k-NN)')).toBeDefined();
    });

    // Click Planner Evolution tab
    fireEvent.click(screen.getByText('Planner Evolution'));
    await waitFor(() => {
      expect(screen.getByText('Planner Self-Evolution & Continuous Rewriting Engine')).toBeDefined();
    });

    // Click Digital Twin Sim tab
    fireEvent.click(screen.getByText('Digital Twin Sim'));
    await waitFor(() => {
      expect(
        screen.getByText('Digital Twin Distributed Cluster Simulator (1,000+ Workers)')
      ).toBeDefined();
    });

    // Click Causal Do-Calculus tab
    fireEvent.click(screen.getByText('Causal Do-Calculus'));
    await waitFor(() => {
      expect(
        screen.getByText("Structural Causal Models & Pearl's Do-Calculus Interventions")
      ).toBeDefined();
    });

    // Click Council Deliberation tab
    fireEvent.click(screen.getByText('Council Deliberation'));
    await waitFor(() => {
      expect(
        screen.getByText('Autonomous Multi-Agent Deliberation Council (8 Specialized Agents)')
      ).toBeDefined();
    });
  });
});
