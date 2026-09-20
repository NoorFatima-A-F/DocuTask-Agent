/**
 * Runtime Telemetry API Client
 *
 * Provides strongly-typed HTTP API methods and Server-Sent Events (SSE) streaming
 * to connect the UI directly to the real execution engine backend.
 */
const API_BASE = '/api/v1/runtime';
export class RuntimeApiClient {
    static instance;
    constructor() { }
    static getInstance() {
        if (!RuntimeApiClient.instance) {
            RuntimeApiClient.instance = new RuntimeApiClient();
        }
        return RuntimeApiClient.instance;
    }
    /**
     * Fetch historical runtime events from the append-only store.
     */
    async fetchEvents(missionId, limit = 200) {
        const params = new URLSearchParams();
        if (missionId)
            params.append('mission_id', missionId);
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
    async fetchMetrics(missionId) {
        const params = new URLSearchParams();
        if (missionId)
            params.append('mission_id', missionId);
        const res = await fetch(`${API_BASE}/metrics?${params.toString()}`);
        if (!res.ok) {
            throw new Error(`Failed to fetch derived metrics: ${res.statusText}`);
        }
        return res.json();
    }
    /**
     * Fetch real-time operational status and dynamic heartbeats of all agents.
     */
    async fetchAgents() {
        const res = await fetch(`${API_BASE}/agents`);
        if (!res.ok) {
            throw new Error(`Failed to fetch agents status: ${res.statusText}`);
        }
        return res.json();
    }
    /**
     * Fetch active mission state and DAG execution progress.
     */
    async fetchMission(missionId) {
        const params = new URLSearchParams();
        if (missionId)
            params.append('mission_id', missionId);
        const res = await fetch(`${API_BASE}/mission?${params.toString()}`);
        if (!res.ok) {
            throw new Error(`Failed to fetch mission state: ${res.statusText}`);
        }
        return res.json();
    }
    /**
     * Fetch deterministic state reconstructed at sequence step N.
     */
    async fetchReplay(missionId, step) {
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
    async startMission(payload) {
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
    async sendCommand(payload) {
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
    async submitFeedback(payload) {
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
    subscribeEventStream(onEvent, onError, missionId) {
        const params = new URLSearchParams();
        if (missionId)
            params.append('mission_id', missionId);
        const streamUrl = `${API_BASE}/stream?${params.toString()}`;
        const eventSource = new EventSource(streamUrl);
        eventSource.onmessage = (e) => {
            try {
                const parsed = JSON.parse(e.data);
                if (parsed && parsed.event_id) {
                    onEvent(parsed);
                }
            }
            catch (err) {
                // Ignored keep-alives or formatting issues
            }
        };
        eventSource.onerror = (err) => {
            if (onError)
                onError(err);
        };
        return () => {
            eventSource.close();
        };
    }
}
export const runtimeApiClient = RuntimeApiClient.getInstance();
