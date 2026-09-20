/**
 * Runtime Telemetry API Client
 * 
 * Provides strongly-typed HTTP API methods and Server-Sent Events (SSE) streaming
 * to connect the UI directly to the real execution engine backend.
 */

import type {
  RuntimeEvent,
  MissionMetricsSummary,
  RuntimeAgentStatus,
  RuntimeMissionState,
  ReplaySnapshotState,
} from '../types/runtimeTelemetry';

const API_BASE = '/api/v1/runtime';

export interface StartMissionPayload {
  goal: string;
  missionId?: string;
  scenarioType?: string;
  parameters?: Record<string, any>;
}

export interface SendCommandPayload {
  missionId: string;
  commandText: string;
  targetAgent?: string;
}

export interface HumanFeedbackPayload {
  missionId: string;
  documentId: string;
  fieldName: string;
  originalValue: string;
  correctedValue: string;
  distillationType: 'INVARIANT_RULE' | 'FEW_SHOT_BENCHMARK' | 'SCHEMA_PATCH' | 'CONFIDENCE_PRIOR';
  operatorNotes?: string;
}

export class RuntimeApiClient {
  private static instance: RuntimeApiClient;

  private constructor() {}

  public static getInstance(): RuntimeApiClient {
    if (!RuntimeApiClient.instance) {
      RuntimeApiClient.instance = new RuntimeApiClient();
    }
    return RuntimeApiClient.instance;
  }

  /**
   * Fetch historical runtime events from the append-only store.
   */
  async fetchEvents(missionId?: string, limit: number = 200): Promise<RuntimeEvent[]> {
    const params = new URLSearchParams();
    if (missionId) params.append('mission_id', missionId);
    params.append('limit', limit.toString());

    const res = await fetch(`${API_BASE}/events?${params.toString()}`);
    if (!res.ok) {
      throw new Error(`Failed to fetch runtime events: ${res.statusText}`);
    }
    return res.json();
  }

  /**
   * Fetch mathematical derived metrics with formula provenance.
   */
  async fetchMetrics(missionId?: string): Promise<MissionMetricsSummary> {
    const params = new URLSearchParams();
    if (missionId) params.append('mission_id', missionId);

    const res = await fetch(`${API_BASE}/metrics?${params.toString()}`);
    if (!res.ok) {
      throw new Error(`Failed to fetch derived metrics: ${res.statusText}`);
    }
    return res.json();
  }

  /**
   * Fetch real-time operational status and dynamic heartbeats of all agents.
   */
  async fetchAgents(): Promise<RuntimeAgentStatus[]> {
    const res = await fetch(`${API_BASE}/agents`);
    if (!res.ok) {
      throw new Error(`Failed to fetch agents status: ${res.statusText}`);
    }
    return res.json();
  }

  /**
   * Fetch active mission state and DAG execution progress.
   */
  async fetchMission(missionId?: string): Promise<RuntimeMissionState> {
    const params = new URLSearchParams();
    if (missionId) params.append('mission_id', missionId);

    const res = await fetch(`${API_BASE}/mission?${params.toString()}`);
    if (!res.ok) {
      throw new Error(`Failed to fetch mission state: ${res.statusText}`);
    }
    return res.json();
  }

  /**
   * Fetch deterministic state reconstructed at sequence step N.
   */
  async fetchReplay(missionId: string, step: number): Promise<ReplaySnapshotState> {
    const params = new URLSearchParams({
      mission_id: missionId,
      step: step.toString(),
    });

    const res = await fetch(`${API_BASE}/replay?${params.toString()}`);
    if (!res.ok) {
      throw new Error(`Failed to fetch replay snapshot at step ${step}: ${res.statusText}`);
    }
    return res.json();
  }

  /**
   * Start a real multi-agent mission pipeline.
   */
  async startMission(payload: StartMissionPayload): Promise<{ status: string; mission_id: string; goal: string }> {
    const res = await fetch(`${API_BASE}/mission/start`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        goal: payload.goal,
        mission_id: payload.missionId,
        scenario_type: payload.scenarioType || 'THERMAL_INVOICE_AUDIT',
        parameters: payload.parameters || {},
      }),
    });

    if (!res.ok) {
      throw new Error(`Failed to start mission: ${res.statusText}`);
    }
    return res.json();
  }

  /**
   * Send a conversational command to the active mission or target agent.
   */
  async sendCommand(payload: SendCommandPayload): Promise<any> {
    const res = await fetch(`${API_BASE}/mission/command`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        mission_id: payload.missionId,
        command_text: payload.commandText,
        target_agent: payload.targetAgent,
      }),
    });

    if (!res.ok) {
      throw new Error(`Failed to send command: ${res.statusText}`);
    }
    return res.json();
  }

  /**
   * Submit human feedback for memory distillation and invariant rule synthesis.
   */
  async submitFeedback(payload: HumanFeedbackPayload): Promise<any> {
    const res = await fetch(`${API_BASE}/feedback`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        mission_id: payload.missionId,
        document_id: payload.documentId,
        field_name: payload.fieldName,
        original_value: payload.originalValue,
        corrected_value: payload.correctedValue,
        distillation_type: payload.distillationType,
        operator_notes: payload.operatorNotes,
      }),
    });

    if (!res.ok) {
      throw new Error(`Failed to submit human feedback: ${res.statusText}`);
    }
    return res.json();
  }

  /**
   * Subscribe to live Server-Sent Events (SSE) stream.
   * Returns a cleanup function that closes the connection.
   */
  subscribeEventStream(
    onEvent: (event: RuntimeEvent) => void,
    onError?: (err: any) => void,
    missionId?: string
  ): () => void {
    const params = new URLSearchParams();
    if (missionId) params.append('mission_id', missionId);

    const streamUrl = `${API_BASE}/stream?${params.toString()}`;
    const eventSource = new EventSource(streamUrl);

    eventSource.onmessage = (e) => {
      try {
        const parsed = JSON.parse(e.data);
        if (parsed && parsed.event_id) {
          onEvent(parsed as RuntimeEvent);
        }
      } catch (err) {
        // Ignored keep-alives or formatting issues
      }
    };

    eventSource.onerror = (err) => {
      if (onError) onError(err);
    };

    return () => {
      eventSource.close();
    };
  }
}

export const runtimeApiClient = RuntimeApiClient.getInstance();
