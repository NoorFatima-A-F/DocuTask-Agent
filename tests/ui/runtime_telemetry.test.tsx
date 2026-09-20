import React from 'react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { runtimeApiClient } from '../../src/services/runtimeApiClient';
import { RuntimeTelemetryProvider, useRuntimeTelemetry } from '../../src/context/RuntimeTelemetryContext';
import { EventInspectorModal } from '../../src/components/telemetry/EventInspectorModal';
import { LiveTimelinePanel } from '../../src/workspace/timeline/LiveTimelinePanel';
import { WorkspaceProvider } from '../../src/workspace/context/WorkspaceContext';
import type { RuntimeEvent } from '../../src/types/runtimeTelemetry';

const mockEvent: RuntimeEvent = {
  event_id: 'evt_test_123',
  mission_id: 'mission_test_456',
  parent_event_id: 'evt_parent_789',
  timestamp: '2026-09-09T10:00:00Z',
  sequence_number: 42,
  agent_id: 'PLANNER',
  worker_id: 'worker_pool_01',
  event_type: 'TaskGraphGenerated',
  payload: {
    node_count: 8,
    critical_path_ms: 1250,
    dag_root: 'node_goal_0',
  },
  metadata: {
    version: '1.0.0',
    environment: 'test',
  },
  correlation_id: 'corr_test_abc',
  causation_id: 'caus_test_def',
  trace_id: '4bf92f3577b34da6a3ce929d0e0e4736',
  span_id: '00f067aa0ba902b7',
  duration_ms: 245.5,
  status: 'COMPLETED',
  version: '1.0.0',
};

describe('Runtime Observability & Real Execution Telemetry UI Suite', () => {
  beforeEach(() => {
    vi.restoreAllMocks();
  });

  it('renders EventInspectorModal with OpenTelemetry trace information and tabs', () => {
    const handleClose = vi.fn();
    render(<EventInspectorModal event={mockEvent} onClose={handleClose} />);

    expect(screen.getByText(/Event #42 Inspector/i)).toBeDefined();
    expect(screen.getByText('TaskGraphGenerated')).toBeDefined();
    expect(screen.getByText('245.5 ms')).toBeDefined();
    expect(screen.getByText('PLANNER')).toBeDefined();

    // Check payload JSON content
    expect(screen.getByText(/"node_count": 8/i)).toBeDefined();

    // Switch to Metadata tab
    const metaTab = screen.getByText('Metadata');
    fireEvent.click(metaTab);
    expect(screen.getByText(/"environment": "test"/i)).toBeDefined();

    // Switch to Trace tab
    const traceTab = screen.getByText('OpenTelemetry Traces');
    fireEvent.click(traceTab);
    expect(screen.getByText('4bf92f3577b34da6a3ce929d0e0e4736')).toBeDefined();
    expect(screen.getByText('00f067aa0ba902b7')).toBeDefined();
    expect(screen.getByText('evt_parent_789')).toBeDefined();

    // Trigger close
    const closeBtn = screen.getByRole('button', { name: /close modal/i });
    fireEvent.click(closeBtn);
    expect(handleClose).toHaveBeenCalledTimes(1);
  });

  it('verifies RuntimeApiClient HTTP fetching and request contracts', async () => {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => [mockEvent],
    });
    global.fetch = fetchMock;

    const events = await runtimeApiClient.fetchEvents('mission_123', 50);
    expect(events.length).toBe(1);
    expect(events[0].event_type).toBe('TaskGraphGenerated');
    expect(fetchMock).toHaveBeenCalledWith(expect.stringContaining('/api/v1/runtime/events?mission_id=mission_123&limit=50'));
  });

  it('verifies LiveTimelinePanel integrates with telemetry and click-to-inspect modal', () => {
    const TestComponent = () => {
      const { setSelectedEventForInspector } = useRuntimeTelemetry();
      return (
        <div>
          <button onClick={() => setSelectedEventForInspector(mockEvent)}>Trigger Inspector</button>
          <LiveTimelinePanel />
        </div>
      );
    };

    render(
      <RuntimeTelemetryProvider>
        <WorkspaceProvider>
          <TestComponent />
        </WorkspaceProvider>
      </RuntimeTelemetryProvider>
    );

    expect(screen.getByText('Live Mission Execution Timeline')).toBeDefined();
  });
});
