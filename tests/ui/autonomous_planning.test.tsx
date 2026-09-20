import React from 'react';
import { describe, it, expect } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { StrategyComparisonMatrixView } from '../../src/workspace/planning/StrategyComparisonMatrix';
import { CounterfactualExplorerView } from '../../src/workspace/planning/CounterfactualExplorer';
import { MutableDAGViewerView } from '../../src/workspace/planning/MutableDAGViewer';
import { ResourceSchedulerDashboardView } from '../../src/workspace/planning/ResourceSchedulerDashboard';
import { PlannerCalibrationCardView } from '../../src/workspace/planning/PlannerCalibrationCard';
import { WorkspaceProvider } from '../../src/workspace/context/WorkspaceContext';
import { WorkspacePage } from '../../src/workspace/WorkspacePage';

describe('Autonomous Planning UI Test Suite', () => {
  it('renders StrategyComparisonMatrixView with Pareto badges and utility breakdown', async () => {
    render(<StrategyComparisonMatrixView missionId="mission_test_ui" />);

    await waitFor(() => {
      expect(screen.getByText('Multi-Objective Strategy Comparison Matrix')).toBeDefined();
    });

    expect(screen.getByText('Winning Strategy')).toBeDefined();
    expect(screen.getAllByText(/Strategy Delta/i).length).toBeGreaterThan(0);
    expect(screen.getAllByText(/Pareto Optimal/i).length).toBeGreaterThan(0);
    expect(screen.getByText(/Utility Formulation & Selection Provenance/i)).toBeDefined();
  });

  it('renders CounterfactualExplorerView with interactive sliders and presets', async () => {
    render(<CounterfactualExplorerView missionId="mission_test_ui" />);

    await waitFor(() => {
      expect(screen.getByText('Counterfactual Explainability Explorer')).toBeDefined();
    });

    expect(screen.getByText('Pareto Balanced')).toBeDefined();
    expect(screen.getByText('Deep Audit (Accuracy)')).toBeDefined();
    expect(screen.getByText('Realtime SLA (Turbo)')).toBeDefined();
    expect(screen.getByText('Bulk Frugal (Cost)')).toBeDefined();

    // Click on Turbo preset
    const turboBtn = screen.getByText('Realtime SLA (Turbo)');
    fireEvent.click(turboBtn);

    await waitFor(() => {
      expect(screen.getByText('Recalculated Strategy Order')).toBeDefined();
    });
  });

  it('renders MutableDAGViewerView with dynamic nodes and mutation controls', async () => {
    render(<MutableDAGViewerView missionId="mission_test_ui" />);

    await waitFor(() => {
      expect(screen.getByText('Mutable Execution DAG & Live Mutations')).toBeDefined();
    });

    expect(screen.getByText('Node Inspector:')).toBeDefined();
    expect(screen.getByText('Split into 2 Shards')).toBeDefined();
    expect(screen.getByText('Hot-Swap Capability')).toBeDefined();
    expect(screen.getByText('DAG Mutation Audit Trail')).toBeDefined();
  });

  it('renders ResourceSchedulerDashboardView with worker cluster status and leases', async () => {
    render(<ResourceSchedulerDashboardView />);

    await waitFor(() => {
      expect(screen.getByText('Worker Leasing & Priority Execution Matrix')).toBeDefined();
    });

    expect(screen.getByText('Total Workers')).toBeDefined();
    expect(screen.getByText('Active Leases')).toBeDefined();
    expect(screen.getByText('Idle Capacity')).toBeDefined();
    expect(screen.getByText('Queue Depth')).toBeDefined();
  });

  it('renders PlannerCalibrationCardView with expected vs actual telemetry comparisons', async () => {
    render(<PlannerCalibrationCardView missionId="mission_test_ui" />);

    await waitFor(() => {
      expect(screen.getByText('Planner Calibration & Drift Analysis')).toBeDefined();
    });

    expect(screen.getByText('Model Calibration')).toBeDefined();
    expect(screen.getByText('Execution Latency')).toBeDefined();
    expect(screen.getByText('Cost Consumption')).toBeDefined();
    expect(screen.getByText('Validation Accuracy')).toBeDefined();
  });

  it('integrates planning tabs seamlessly inside WorkspacePage', async () => {
    render(
      <WorkspaceProvider>
        <WorkspacePage />
      </WorkspaceProvider>
    );

    // Verify planning tab buttons exist in workspace header
    expect(screen.getByText('Strategy Matrix')).toBeDefined();
    expect(screen.getByText('Counterfactuals')).toBeDefined();
    expect(screen.getByText('Mutable DAG')).toBeDefined();
    expect(screen.getByText('Worker Scheduler')).toBeDefined();
    expect(screen.getByText('Self-Calibration')).toBeDefined();

    // Click on Strategy Matrix tab
    const matrixTab = screen.getByText('Strategy Matrix');
    fireEvent.click(matrixTab);

    await waitFor(() => {
      expect(screen.getByText('Multi-Objective Strategy Comparison Matrix')).toBeDefined();
    });
  });
});
