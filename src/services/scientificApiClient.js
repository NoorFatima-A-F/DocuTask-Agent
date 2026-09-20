/**
 * Scientific Metric & Intelligence API Client
 */
const API_BASE = '/api/v1/runtime';
export class ScientificApiClient {
    static instance;
    constructor() { }
    static getInstance() {
        if (!ScientificApiClient.instance) {
            ScientificApiClient.instance = new ScientificApiClient();
        }
        return ScientificApiClient.instance;
    }
    async fetchMetricRegistry() {
        const res = await fetch(`${API_BASE}/metrics/registry`);
        if (!res.ok) {
            throw new Error(`Failed to fetch metric registry: ${res.statusText}`);
        }
        return res.json();
    }
    async fetchMetricProvenance(metricId, missionId) {
        const params = new URLSearchParams();
        if (metricId)
            params.append('metric_id', metricId);
        if (missionId)
            params.append('mission_id', missionId);
        const res = await fetch(`${API_BASE}/metrics/provenance?${params.toString()}`);
        if (!res.ok) {
            throw new Error(`Failed to fetch metric provenance: ${res.statusText}`);
        }
        return res.json();
    }
    async fetchBayesianConfidence(missionId) {
        const params = new URLSearchParams();
        if (missionId)
            params.append('mission_id', missionId);
        const res = await fetch(`${API_BASE}/confidence/decomposition?${params.toString()}`);
        if (!res.ok) {
            throw new Error(`Failed to fetch Bayesian confidence: ${res.statusText}`);
        }
        return res.json();
    }
    async fetchReplayDiff(missionId, stepA, stepB) {
        const params = new URLSearchParams({
            mission_id: missionId,
            step_a: stepA.toString(),
            step_b: stepB.toString(),
        });
        const res = await fetch(`${API_BASE}/replay/diff?${params.toString()}`);
        if (!res.ok) {
            throw new Error(`Failed to fetch replay diff: ${res.statusText}`);
        }
        return res.json();
    }
    async fetchRuntimeTraces(missionId) {
        const params = new URLSearchParams();
        if (missionId)
            params.append('mission_id', missionId);
        const res = await fetch(`${API_BASE}/traces?${params.toString()}`);
        if (!res.ok) {
            throw new Error(`Failed to fetch runtime traces: ${res.statusText}`);
        }
        return res.json();
    }
}
export const scientificApiClient = ScientificApiClient.getInstance();
