/**
 * Scientific Metric & Intelligence API Client
 */

import type {
  MetricDefinitionData,
  MetricProvenanceRecordData,
  BayesianConfidenceResultData,
  ReplayStepDiffData,
  TraceTreeData,
} from '../types/scientificMetrics';

const API_BASE = '/api/v1/runtime';

export class ScientificApiClient {
  private static instance: ScientificApiClient;

  private constructor() {}

  public static getInstance(): ScientificApiClient {
    if (!ScientificApiClient.instance) {
      ScientificApiClient.instance = new ScientificApiClient();
    }
    return ScientificApiClient.instance;
  }

  async fetchMetricRegistry(): Promise<MetricDefinitionData[]> {
    const res = await fetch(`${API_BASE}/metrics/registry`);
    if (!res.ok) {
      throw new Error(`Failed to fetch metric registry: ${res.statusText}`);
    }
    return res.json();
  }

  async fetchMetricProvenance(metricId?: string, missionId?: string): Promise<MetricProvenanceRecordData | Record<string, MetricProvenanceRecordData>> {
    const params = new URLSearchParams();
    if (metricId) params.append('metric_id', metricId);
    if (missionId) params.append('mission_id', missionId);

    const res = await fetch(`${API_BASE}/metrics/provenance?${params.toString()}`);
    if (!res.ok) {
      throw new Error(`Failed to fetch metric provenance: ${res.statusText}`);
    }
    return res.json();
  }

  async fetchBayesianConfidence(missionId?: string): Promise<BayesianConfidenceResultData> {
    const params = new URLSearchParams();
    if (missionId) params.append('mission_id', missionId);

    const res = await fetch(`${API_BASE}/confidence/decomposition?${params.toString()}`);
    if (!res.ok) {
      throw new Error(`Failed to fetch Bayesian confidence: ${res.statusText}`);
    }
    return res.json();
  }

  async fetchReplayDiff(missionId: string, stepA: number, stepB: number): Promise<ReplayStepDiffData> {
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

  async fetchRuntimeTraces(missionId?: string): Promise<TraceTreeData[]> {
    const params = new URLSearchParams();
    if (missionId) params.append('mission_id', missionId);

    const res = await fetch(`${API_BASE}/traces?${params.toString()}`);
    if (!res.ok) {
      throw new Error(`Failed to fetch runtime traces: ${res.statusText}`);
    }
    return res.json();
  }
}

export const scientificApiClient = ScientificApiClient.getInstance();
