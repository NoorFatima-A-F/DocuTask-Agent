import React from 'react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { MetricProvenanceModal } from '../../src/components/telemetry/MetricProvenanceModal';
import { BayesianConfidencePanel } from '../../src/workspace/confidence/BayesianConfidencePanel';
import { ReplayDiffComparator } from '../../src/workspace/replay/ReplayDiffComparator';
import { RuntimeTraceGraph } from '../../src/workspace/timeline/RuntimeTraceGraph';
import { RuntimeStatisticsDashboard } from '../../src/workspace/statistics/RuntimeStatisticsDashboard';
import type { MetricProvenanceRecordData } from '../../src/types/scientificMetrics';

const mockProvenance: MetricProvenanceRecordData = {
  metric_id: 'worker_utilization',
  metric_name: 'Worker Utilization',
  metric_version: '2.0',
  value: 0.9214,
  formatted_value: '92.14%',
  unit: 'PERCENTAGE',
  formula_id: 'FORMULA_WORKER_UTILIZATION',
  formula_expression: 'sum(active_worker_time) / sum(allocated_worker_time)',
  formula_latex: '\\mathcal{U} = \\frac{\\sum t_{\\text{active}}}{\\sum t_{\\text{allocated}}}',
  variables_used: { active_time_ms: 4520.0, allocated_time_ms: 4905.0 },
  raw_event_ids: ['evt_w1', 'evt_w2', 'evt_w3'],
  sample_size: 483,
  observation_window: { duration_seconds: 12.41 },
  statistical_summary: {
    sample_size: 483,
    mean: 0.9214,
    median: 0.9200,
    mode: 0.9200,
    variance: 0.0012,
    standard_deviation: 0.0346,
    standard_error: 0.0015,
    min_value: 0.82,
    max_value: 0.98,
    p50: 0.92,
    p90: 0.96,
    p95: 0.97,
    p99: 0.98,
    confidence_interval_95: [0.9184, 0.9244],
    margin_of_error_95: 0.003,
    distribution_model: 'STANDARD_NORMAL',
  },
  merkle_events_root_sha256: '9a7b3c2d1e0f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b',
  calculated_at_utc: '2026-09-09T12:42:16Z',
  sentinel_state: null,
  tags: ['runtime', 'workers', 'efficiency'],
};

describe('Scientific Metric Provenance & Runtime Intelligence UI Suite', () => {
  beforeEach(() => {
    vi.restoreAllMocks();
  });

  it('renders MetricProvenanceModal with LaTeX formula, variables, and Merkle root', () => {
    const handleClose = vi.fn();
    render(<MetricProvenanceModal provenance={mockProvenance} onClose={handleClose} />);

    expect(screen.getByText('Worker Utilization')).toBeDefined();
    expect(screen.getByText('92.14%')).toBeDefined();
    expect(screen.getByText('n = 483')).toBeDefined();

    // Verify LaTeX expression exists
    expect(screen.getByText(/sum\(active_worker_time\)/i)).toBeDefined();

    // Switch to Statistics Tab
    const statsTab = screen.getByText('Distribution Statistics');
    fireEvent.click(statsTab);
    expect(screen.getByText('STANDARD_NORMAL')).toBeDefined();

    // Switch to Lineage Tab
    const lineageTab = screen.getByText('Merkle Evidence Lineage');
    fireEvent.click(lineageTab);
    expect(screen.getByText(/9a7b3c2d1e0f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b/i)).toBeDefined();

    // Close
    const closeBtn = screen.getByRole('button', { name: /close modal/i });
    fireEvent.click(closeBtn);
    expect(handleClose).toHaveBeenCalledTimes(1);
  });

  it('renders BayesianConfidencePanel with evidence fusion signals', async () => {
    render(<BayesianConfidencePanel />);

    expect(screen.getByText('Explainable Confidence Mathematics & Evidence Fusion')).toBeDefined();
    expect(screen.getByText(/Uninformative Prior P\(θ\)/i)).toBeDefined();
    expect(screen.getByText(/Log-Odds Evidence Gain/i)).toBeDefined();
  });

  it('renders ReplayDiffComparator and calculates state deltas', async () => {
    render(<ReplayDiffComparator />);

    expect(screen.getByText(/Replay Step Diff & Execution State Delta/i)).toBeDefined();
    await waitFor(() => {
      expect(screen.getAllByText(/Snapshot @ Step #/i).length).toBeGreaterThan(0);
    });
  });

  it('renders RuntimeTraceGraph and allows span inspection', async () => {
    render(<RuntimeTraceGraph />);

    expect(screen.getByText(/Runtime Causal Execution & Trace Trees/i)).toBeDefined();
    await waitFor(() => {
      expect(screen.getByText(/Execution Span Hierarchy/i)).toBeDefined();
    });
  });

  it('renders RuntimeStatisticsDashboard with 100% event derived metrics', async () => {
    render(<RuntimeStatisticsDashboard />);

    expect(screen.getByText(/Scientifically Grounded Runtime Statistics/i)).toBeDefined();
    await waitFor(() => {
      expect(screen.getByText(/Worker Utilization/i)).toBeDefined();
      expect(screen.getByText(/Average Event Latency/i)).toBeDefined();
    });
  });
});
