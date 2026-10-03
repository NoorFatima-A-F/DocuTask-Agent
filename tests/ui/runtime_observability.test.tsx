import React from 'react';
import { describe, it, expect } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import { WorkspaceProvider } from '../../src/workspace/context/WorkspaceContext';
import { WorkspacePage } from '../../src/workspace/WorkspacePage';
import {
  LiveRuntimeDashboardView,
  EventSourcedMissionTimeline,
  ExecutionFlameGraphViewer,
  ObservabilityTraceExplorer,
} from '../../src/workspace/observability';

describe('Autonomous Runtime Observability Layer (AROL) UI Suite', () => {
  it('renders LiveRuntimeDashboardView with health scores and resource telemetry', async () => {
    render(
      <WorkspaceProvider>
        <LiveRuntimeDashboardView />
      </WorkspaceProvider>
    );
    await waitFor(() => {
      expect(screen.getByText(/Autonomous Runtime Observability Layer/i)).toBeDefined();
      expect(screen.getByText(/Failure Resilience/i)).toBeDefined();
      expect(screen.getByText(/Node Success Rate/i)).toBeDefined();
    });
  });

  it('renders EventSourcedMissionTimeline with cryptographic integrity proof', async () => {
    render(
      <WorkspaceProvider>
        <EventSourcedMissionTimeline />
      </WorkspaceProvider>
    );
    await waitFor(() => {
      expect(screen.getByText(/Event-Sourced Mission Execution Timeline/i)).toBeDefined();
      expect(screen.getByText(/Event Hash-Chain Status/i)).toBeDefined();
    });
  });

  it('renders ExecutionFlameGraphViewer with critical path profiler', async () => {
    render(
      <WorkspaceProvider>
        <ExecutionFlameGraphViewer />
      </WorkspaceProvider>
    );
    await waitFor(() => {
      expect(screen.getByText(/Execution Flame Graph & Critical Path Profiler/i)).toBeDefined();
      expect(screen.getByText(/Critical Path Latency/i)).toBeDefined();
    });
  });

  it('renders ObservabilityTraceExplorer with trace search and span inspector', async () => {
    render(
      <WorkspaceProvider>
        <ObservabilityTraceExplorer />
      </WorkspaceProvider>
    );
    await waitFor(() => {
      expect(screen.getByText(/Distributed Trace Explorer & Event Sourcing Inspector/i)).toBeDefined();
      expect(screen.getByPlaceholderText(/Search by Trace ID/i)).toBeDefined();
    });
  });

  it('integrates all AROL observability tabs into WorkspacePage', async () => {
    render(
      <WorkspaceProvider>
        <WorkspacePage />
      </WorkspaceProvider>
    );
    await waitFor(() => {
      expect(screen.getByText(/Live Telemetry/i)).toBeDefined();
      expect(screen.getAllByText(/Event Timeline/i).length).toBeGreaterThan(0);
      expect(screen.getByText(/Flame Graph & Profiler/i)).toBeDefined();
      expect(screen.getByText(/Trace Explorer/i)).toBeDefined();
    });
  });
});
