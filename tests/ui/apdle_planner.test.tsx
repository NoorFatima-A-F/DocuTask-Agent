import React from 'react';
import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import { WorkspaceProvider } from '../../src/workspace/context/WorkspaceContext';
import { WorkspacePage } from '../../src/workspace/WorkspacePage';
import {
  PlannerGraphView,
  ExecutionDAG,
  CriticalPathView,
  WorkerAllocationView,
  DependencyExplorer,
  GraphMutationTimeline,
  PlannerSimulationDashboard,
  RecoveryGraphViewer,
} from '../../src/workspace/planner';

describe('Autonomous Planner Visualization, Dynamic DAG Execution & Live Replanning (APDLE) UI Suite', () => {
  beforeEach(() => {
    vi.spyOn(globalThis, 'fetch').mockImplementation(() => {
      return Promise.reject(new Error('Network offline in unit test'));
    });
  });

  it('renders PlannerGraphView with topological nodes, critical duration metric and generation badge', async () => {
    render(
      <WorkspaceProvider>
        <PlannerGraphView />
      </WorkspaceProvider>
    );
    await waitFor(() => {
      expect(screen.getAllByText(/Critical Path Duration/i).length).toBeGreaterThan(0);
      expect(screen.getAllByText(/DAG Generation/i).length).toBeGreaterThan(0);
      expect(screen.getAllByText(/Structural Depth/i).length).toBeGreaterThan(0);
      expect(screen.getAllByText(/Dependency Edges/i).length).toBeGreaterThan(0);
    });
  });

  it('renders ExecutionDAG with parallel wavefront layers and concurrency badges', async () => {
    render(
      <WorkspaceProvider>
        <ExecutionDAG />
      </WorkspaceProvider>
    );
    await waitFor(() => {
      expect(screen.getAllByText(/Visualizes concurrent execution wavefronts/i).length).toBeGreaterThan(0);
      expect(screen.getAllByText(/PARALLEL CONCURRENCY/i).length).toBeGreaterThan(0);
    });
  });

  it('renders CriticalPathView with CPM analytics table, early/late start and total slack', async () => {
    render(
      <WorkspaceProvider>
        <CriticalPathView />
      </WorkspaceProvider>
    );
    await waitFor(() => {
      expect(screen.getAllByText(/Node-Level Schedule Bounds/i).length).toBeGreaterThan(0);
      expect(screen.getAllByText(/Total Slack/i).length).toBeGreaterThan(0);
      expect(screen.getAllByText(/Parallel Branch Headroom/i).length).toBeGreaterThan(0);
    });
  });

  it('renders WorkerAllocationView with capability matching and concurrency load', async () => {
    render(
      <WorkspaceProvider>
        <WorkerAllocationView />
      </WorkspaceProvider>
    );
    await waitFor(() => {
      expect(screen.getAllByText(/Concurrency Load/i).length).toBeGreaterThan(0);
      expect(screen.getAllByText(/Avg Latency:/i).length).toBeGreaterThan(0);
    });
  });

  it('renders DependencyExplorer with multi-typed dependency breakdown', async () => {
    render(
      <WorkspaceProvider>
        <DependencyExplorer />
      </WorkspaceProvider>
    );
    await waitFor(() => {
      expect(screen.getAllByText('DATA_FLOW').length).toBeGreaterThan(0);
      expect(screen.getAllByText(/Inspects typed dependency edges/i).length).toBeGreaterThan(0);
    });
  });

  it('renders GraphMutationTimeline with in-flight mutation logs and diffs', async () => {
    render(
      <WorkspaceProvider>
        <GraphMutationTimeline />
      </WorkspaceProvider>
    );
    await waitFor(() => {
      expect(screen.getAllByText(/Audit log of in-flight structural DAG alterations/i).length).toBeGreaterThan(0);
      expect(screen.getAllByText(/No runtime mutations applied yet/i).length).toBeGreaterThan(0);
    });
  });

  it('renders PlannerSimulationDashboard with Monte Carlo stochastic simulations', async () => {
    render(
      <WorkspaceProvider>
        <PlannerSimulationDashboard />
      </WorkspaceProvider>
    );
    await waitFor(() => {
      expect(screen.getAllByText(/Stochastic simulation over DAG variance/i).length).toBeGreaterThan(0);
      expect(screen.getAllByText(/Expected Cost/i).length).toBeGreaterThan(0);
    });
  });

  it('renders RecoveryGraphViewer with autonomous recovery subgraphs and strategy switchers', async () => {
    render(
      <WorkspaceProvider>
        <RecoveryGraphViewer />
      </WorkspaceProvider>
    );
    await waitFor(() => {
      expect(screen.getAllByText(/Failure Point/i).length).toBeGreaterThan(0);
      expect(screen.getAllByText(/Injected Recovery Branch/i).length).toBeGreaterThan(0);
      expect(screen.getAllByText(/Resume Target/i).length).toBeGreaterThan(0);
    });
  });

  it('integrates all APDLE planner tabs into WorkspacePage', async () => {
    render(
      <WorkspaceProvider>
        <WorkspacePage />
      </WorkspaceProvider>
    );
    await waitFor(() => {
      expect(screen.getByText(/Planner Graph \(APDLE\)/i)).toBeDefined();
      expect(screen.getByText(/Execution Wavefronts/i)).toBeDefined();
      expect(screen.getByText(/Critical Path \(CPM\)/i)).toBeDefined();
      expect(screen.getByText(/Worker Allocator/i)).toBeDefined();
      expect(screen.getByText(/Dependency Explorer/i)).toBeDefined();
      expect(screen.getByText(/DAG Mutation Log/i)).toBeDefined();
      expect(screen.getByText(/Monte Carlo Planner Sim/i)).toBeDefined();
      expect(screen.getByText(/Recovery Subgraphs/i)).toBeDefined();
    });
  });
});
