/**
 * Phase 13.16: Autonomous World Modeling, Predictive Intelligence & Causal Reasoning Platform (AWMPICRP)
 * API Client with complete REST endpoints and fallback live simulation mocks.
 */

import {
  WorldModelExecutiveSummary,
  WorldObservation,
  FusedFact,
  WorldEntity,
  WorldRelation,
  WorldGraphSnapshot,
  TemporalPattern,
  CausalGraph,
  Hypothesis,
  ScenarioBranch,
  CounterfactualWorld,
  PredictionTrajectory,
  DecisionOption,
  DecisionPortfolio,
  UncertaintyAssessment,
  VerificationOutcome,
  CognitiveMemoryRecord,
  WorldModelEvent,
  PredictionHorizon,
} from '../types/worldModelPlatform';

const BASE_URL = '/api/v1/world_model';

export class WorldModelApiClient {
  private static async fetchJson<T>(url: string, options?: RequestInit, fallback?: T): Promise<T> {
    try {
      const res = await fetch(url, {
        headers: { 'Content-Type': 'application/json' },
        ...options,
      });
      if (!res.ok) {
        throw new Error(`HTTP ${res.status}: ${res.statusText}`);
      }
      return await res.json();
    } catch (err) {
      if (fallback !== undefined) {
        console.warn(`[WorldModelApiClient] Network error on ${url}, using fallback:`, err);
        return fallback;
      }
      throw err;
    }
  }

  // Executive Summary & Status
  public static async getStatus(): Promise<WorldModelExecutiveSummary> {
    const fallback: WorldModelExecutiveSummary = {
      status: 'online',
      phase: '13.16',
      name: 'Autonomous World Modeling, Predictive Intelligence & Causal Reasoning Platform (AWMPICRP)',
      state: 'modeling',
      summary: {
        runtime_status: {
          intelligence_state: 'modeling',
          total_cycles_executed: 142,
          last_cycle_timestamp: new Date().toISOString(),
          uptime_seconds: 48200,
        },
        world_entities_count: 24,
        world_relations_count: 58,
        fused_facts_count: 184,
        active_hypotheses_count: 16,
        simulated_scenarios_count: 32,
        predictive_trajectories_count: 12,
        decisions_count: 8,
        consolidated_memories_count: 450,
        system_uncertainty: {
          assessment_id: 'unc-init-01',
          target_domain: 'system_runtime',
          observed_entropy: 0.28,
          epistemic_component: 0.16,
          aleatoric_component: 0.12,
          confidence_level: 0.88,
          total_uncertainty: 0.28,
          created_at: new Date().toISOString(),
        },
        recent_events_count: 65,
      },
    };
    return this.fetchJson<WorldModelExecutiveSummary>(`${BASE_URL}/status`, {}, fallback);
  }

  // Trigger Cognitive Cycle
  public static async executeCognitiveCycle(payload: {
    goal?: string;
    raw_observation?: Record<string, any>;
    source?: string;
    target_metric?: string;
    horizon?: PredictionHorizon;
  }): Promise<any> {
    return this.fetchJson(`${BASE_URL}/cycle`, {
      method: 'POST',
      body: JSON.stringify(payload),
    }, { success: true, simulated: true });
  }

  // Observations
  public static async getObservations(limit = 50): Promise<{ count: number; observations: WorldObservation[]; metrics: any }> {
    const fallback = {
      count: 3,
      observations: [
        {
          observation_id: 'obs-mock-1',
          source: 'cluster_telemetry_agent',
          modality: 'metrics',
          raw_payload: { cpu_usage: 62.4, queue_latency_ms: 14.8, memory_pressure: 0.45 },
          signal_strength: 0.92,
          noise_level: 0.08,
          source_reliability: 0.96,
          tags: ['telemetry', 'compute', 'cluster_alpha'],
          snr_ratio: 11.5,
          novelty_score: 0.18,
          is_processed: true,
          timestamp: new Date().toISOString(),
        },
        {
          observation_id: 'obs-mock-2',
          source: 'ocr_pipeline_sentinel',
          modality: 'event_stream',
          raw_payload: { document_throughput: 480, failure_rate: 0.002 },
          signal_strength: 0.95,
          noise_level: 0.05,
          source_reliability: 0.99,
          tags: ['ocr', 'throughput', 'quality'],
          snr_ratio: 19.0,
          novelty_score: 0.12,
          is_processed: true,
          timestamp: new Date(Date.now() - 30000).toISOString(),
        },
      ],
      metrics: { total_observations: 2, mean_snr_ratio: 15.25, mean_novelty: 0.15 },
    };
    return this.fetchJson(`${BASE_URL}/observations?limit=${limit}`, {}, fallback);
  }

  public static async ingestObservation(data: Partial<WorldObservation>): Promise<{ success: boolean; observation: WorldObservation }> {
    return this.fetchJson(`${BASE_URL}/observations`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  // Knowledge Fusion
  public static async getFacts(limit = 50): Promise<{ count: number; facts: FusedFact[]; metrics: any }> {
    const fallback = {
      count: 2,
      facts: [
        {
          fact_id: 'fact-mock-1',
          subject: 'OCRWorkerPool',
          predicate: 'scalesHorizontallyWith',
          object: 'DocumentBatchQueueDepth',
          confidence: 0.96,
          source: 'knowledge_fusion_engine',
          evidence_ids: ['obs-mock-1', 'obs-mock-2'],
          truth_score: 0.98,
          decay_rate: 0.001,
          verification_count: 14,
          created_at: new Date(Date.now() - 86400000).toISOString(),
          last_reinforced_at: new Date().toISOString(),
        },
      ],
      metrics: { total_facts: 1, mean_truth_score: 0.98 },
    };
    return this.fetchJson(`${BASE_URL}/knowledge/facts?limit=${limit}`, {}, fallback);
  }

  public static async fuseFact(data: { subject: string; predicate: string; object: string; confidence?: number; source?: string }): Promise<any> {
    return this.fetchJson(`${BASE_URL}/knowledge/facts`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  // World Graph
  public static async getWorldGraph(): Promise<{
    entities: WorldEntity[];
    relations: WorldRelation[];
    snapshots_count: number;
    metrics: any;
  }> {
    const fallback = {
      entities: [
        {
          entity_id: 'ent-1',
          name: 'Primary Ingest Cluster',
          domain: 'system' as const,
          properties: { region: 'us-central1', capacity: 1000 },
          state: { active_nodes: 8, health: 'OPTIMAL' },
          confidence: 0.99,
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString(),
        },
        {
          entity_id: 'ent-2',
          name: 'Vector Search Index',
          domain: 'database' as const,
          properties: { dimensions: 1536, indexed_docs: 145000 },
          state: { query_p99_ms: 8.2, status: 'READY' },
          confidence: 0.95,
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString(),
        },
      ],
      relations: [
        {
          relation_id: 'rel-1',
          source_id: 'ent-1',
          target_id: 'ent-2',
          relation_type: 'interacts_with' as const,
          weight: 1.0,
          confidence: 0.95,
          properties: { bandwidth_mbps: 450 },
          created_at: new Date().toISOString(),
        },
      ],
      snapshots_count: 12,
      metrics: { total_entities: 2, total_relations: 1, graph_entropy: 0.35 },
    };
    return this.fetchJson(`${BASE_URL}/world/graph`, {}, fallback);
  }

  public static async createSnapshot(reason = 'manual_snapshot'): Promise<{ success: boolean; snapshot: WorldGraphSnapshot }> {
    return this.fetchJson(`${BASE_URL}/world/snapshots?trigger_reason=${encodeURIComponent(reason)}`, {
      method: 'POST',
    });
  }

  // Temporal
  public static async getTemporalPatterns(): Promise<{ count: number; patterns: TemporalPattern[]; metrics: any }> {
    const fallback = {
      count: 2,
      patterns: [
        {
          pattern_id: 'tmp-1',
          target_entity: 'Document Ingestion Rate',
          frequency: 'hourly' as const,
          cycle_duration_seconds: 3600,
          confidence: 0.94,
          description: 'Peak document ingestion burst at beginning of each hour',
          first_observed: new Date(Date.now() - 7 * 86400000).toISOString(),
          last_observed: new Date().toISOString(),
        },
      ],
      metrics: { total_patterns: 1, mean_confidence: 0.94 },
    };
    return this.fetchJson(`${BASE_URL}/temporal/patterns`, {}, fallback);
  }

  // Causal
  public static async getCausalGraph(): Promise<{ graph: CausalGraph | null; metrics: any }> {
    const fallback = {
      graph: {
        graph_id: 'cgraph-main',
        name: 'Enterprise Document Pipeline Causal Model',
        nodes: {
          n1: { node_id: 'n1', name: 'Batch Concurrency', domain: 'system', properties: {} },
          n2: { node_id: 'n2', name: 'Memory Consumption', domain: 'resource', properties: {} },
          n3: { node_id: 'n3', name: 'Page Processing Latency', domain: 'process', properties: {} },
        },
        edges: [
          { source_id: 'n1', target_id: 'n2', strength: 'strong' as const, weight: 0.85, mechanism: 'Linear heap allocation' },
          { source_id: 'n2', target_id: 'n3', strength: 'moderate' as const, weight: 0.65, mechanism: 'GC pause overhead' },
        ],
        updated_at: new Date().toISOString(),
      },
      metrics: { node_count: 3, edge_count: 2 },
    };
    return this.fetchJson(`${BASE_URL}/causal/graph`, {}, fallback);
  }

  public static async executeCausalIntervention(data: {
    target_node: string;
    interventions: Record<string, any>;
    observed_context?: Record<string, any>;
  }): Promise<any> {
    return this.fetchJson(`${BASE_URL}/causal/intervene`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  // Hypotheses
  public static async getHypotheses(): Promise<{ count: number; hypotheses: Hypothesis[]; metrics: any }> {
    const fallback = {
      count: 2,
      hypotheses: [
        {
          hypothesis_id: 'hyp-1',
          statement: 'Enabling quantization reduces inference memory by 45% with <0.5% accuracy impact',
          cause_entity: 'Model Quantization (INT8)',
          effect_entity: 'GPU VRAM Footprint',
          prior_probability: 0.75,
          posterior_probability: 0.94,
          evidence_count: 28,
          status: 'confirmed' as const,
          domain: 'system' as const,
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString(),
        },
      ],
      metrics: { total_hypotheses: 1, confirmed_count: 1 },
    };
    return this.fetchJson(`${BASE_URL}/hypotheses`, {}, fallback);
  }

  // Scenarios
  public static async getScenarios(): Promise<{ count: number; branches: ScenarioBranch[]; metrics: any }> {
    const fallback = {
      count: 3,
      branches: [
        {
          branch_id: 'sc-1',
          base_snapshot_id: 'snap-01',
          branch_type: 'expected' as const,
          probability: 0.65,
          time_horizon_seconds: 86400,
          state_divergence_delta: 0.08,
          projected_state: { estimated_throughput: 12000, error_rate: 0.001 },
          critical_events: ['Diurnal peak at 14:00 UTC', 'Automated nightly index compaction'],
          created_at: new Date().toISOString(),
        },
        {
          branch_id: 'sc-2',
          base_snapshot_id: 'snap-01',
          branch_type: 'black_swan' as const,
          probability: 0.04,
          time_horizon_seconds: 86400,
          state_divergence_delta: 0.82,
          projected_state: { estimated_throughput: 400, error_rate: 0.35 },
          critical_events: ['Upstream cloud region network partition', 'Auth token provider outage'],
          created_at: new Date().toISOString(),
        },
      ],
      metrics: { total_scenarios: 2, mean_divergence: 0.45 },
    };
    return this.fetchJson(`${BASE_URL}/scenarios`, {}, fallback);
  }

  public static async simulateScenarios(data: {
    base_snapshot_id: string;
    time_horizon_seconds?: number;
    monte_carlo_runs?: number;
  }): Promise<any> {
    return this.fetchJson(`${BASE_URL}/scenarios/simulate`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  // Counterfactuals
  public static async getCounterfactuals(): Promise<{ count: number; counterfactuals: CounterfactualWorld[]; metrics: any }> {
    const fallback = {
      count: 1,
      counterfactuals: [
        {
          simulation_id: 'cf-1',
          base_snapshot_id: 'snap-01',
          interventions: { autoscaling_threshold_cpu: 0.6 },
          query_target: 'P99 Document Extraction Latency',
          factual_outcome: '2.4 seconds',
          counterfactual_outcome: '0.85 seconds',
          divergence_score: 0.64,
          causal_attribution: 'Early scale-out prevented thread starvation in OCR worker pool',
          created_at: new Date().toISOString(),
        },
      ],
      metrics: { total_counterfactuals: 1 },
    };
    return this.fetchJson(`${BASE_URL}/counterfactuals`, {}, fallback);
  }

  public static async simulateCounterfactual(data: {
    base_snapshot_id: string;
    interventions: Record<string, any>;
    query_target: string;
    factual_outcome?: any;
  }): Promise<any> {
    return this.fetchJson(`${BASE_URL}/counterfactuals/simulate`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  // Forecasting
  public static async getForecasts(): Promise<{ count: number; trajectories: PredictionTrajectory[]; metrics: any }> {
    const fallback = {
      count: 1,
      trajectories: [
        {
          trajectory_id: 'pred-1',
          target_metric: 'Hourly Document Processing Volume',
          horizon: 'medium_term' as const,
          horizon_seconds: 86400,
          expected_value: 14200,
          lower_bound_95: 12800,
          upper_bound_95: 15600,
          confidence_score: 0.91,
          time_series_points: [
            { timestamp: new Date(Date.now() + 3600000).toISOString(), expected: 13000, lower: 12100, upper: 13900 },
            { timestamp: new Date(Date.now() + 7200000).toISOString(), expected: 13800, lower: 12600, upper: 14900 },
            { timestamp: new Date(Date.now() + 10800000).toISOString(), expected: 14200, lower: 12800, upper: 15600 },
          ],
          causal_drivers: ['Business hours workflow surge', 'Enterprise queue backlog status'],
          created_at: new Date().toISOString(),
        },
      ],
      metrics: { total_trajectories: 1, mean_confidence: 0.91 },
    };
    return this.fetchJson(`${BASE_URL}/forecasts`, {}, fallback);
  }

  public static async generateForecast(data: {
    target_metric: string;
    horizon?: PredictionHorizon;
    horizon_seconds?: number;
    include_causal_factors?: boolean;
    context?: Record<string, any>;
  }): Promise<any> {
    return this.fetchJson(`${BASE_URL}/forecasts/generate`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  // Decisions
  public static async getDecisions(): Promise<{
    options_count: number;
    options: DecisionOption[];
    portfolios_count: number;
    portfolios: DecisionPortfolio[];
    metrics: any;
  }> {
    const fallback = {
      options_count: 2,
      options: [
        {
          option_id: 'opt-1',
          title: 'Scale Out Ingestion Worker Pool',
          description: 'Add 6 temporary spot GPU workers for surge processing',
          actions: [{ type: 'k8s_scale', replicas: 12 }],
          expected_outcomes: { throughput_gain: 0.75, latency_drop: 0.4 },
          expected_utility: 0.88,
          risk_profile: 'balanced' as const,
          cost: 1.2,
          time_horizon_seconds: 14400,
          created_at: new Date().toISOString(),
        },
      ],
      portfolios_count: 1,
      portfolios: [
        {
          portfolio_id: 'port-1',
          objective: 'Maximize Throughput & Minimize P99 Latency',
          selected_options: ['opt-1'],
          total_cost: 1.2,
          aggregate_utility: 0.88,
          risk_profile: 'balanced' as const,
          created_at: new Date().toISOString(),
        },
      ],
      metrics: { total_options: 1, total_portfolios: 1 },
    };
    return this.fetchJson(`${BASE_URL}/decisions/portfolios`, {}, fallback);
  }

  public static async evaluateDecision(data: Partial<DecisionOption>): Promise<any> {
    return this.fetchJson(`${BASE_URL}/decisions/evaluate`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  // Uncertainty
  public static async getUncertainty(): Promise<{ count: number; assessments: UncertaintyAssessment[]; metrics: any }> {
    const fallback = {
      count: 1,
      assessments: [
        {
          assessment_id: 'unc-1',
          target_domain: 'Document Classification Under New Domain Shifts',
          observed_entropy: 0.32,
          epistemic_component: 0.22,
          aleatoric_component: 0.10,
          confidence_level: 0.84,
          total_uncertainty: 0.32,
          created_at: new Date().toISOString(),
        },
      ],
      metrics: { total_assessments: 1, mean_uncertainty: 0.32 },
    };
    return this.fetchJson(`${BASE_URL}/uncertainty`, {}, fallback);
  }

  // Verifications
  public static async getVerifications(): Promise<{ count: number; outcomes: VerificationOutcome[]; calibration: any; metrics: any }> {
    const fallback = {
      count: 2,
      outcomes: [
        {
          verification_id: 'ver-1',
          prediction_id: 'pred-1',
          actual_value: 13950,
          predicted_value: 14200,
          residual_error: 0.017,
          status: 'verified' as const,
          calibration_weight: 0.98,
          recorded_at: new Date().toISOString(),
        },
      ],
      calibration: {
        expected_calibration_error: 0.042,
        brier_score: 0.038,
        sample_count: 42,
      },
      metrics: { total_verified: 40, total_refuted: 2 },
    };
    return this.fetchJson(`${BASE_URL}/verifications`, {}, fallback);
  }

  public static async recordVerification(data: { prediction_id: string; actual_value: any; context?: Record<string, any> }): Promise<any> {
    return this.fetchJson(`${BASE_URL}/verifications/record`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  // Memory
  public static async getMemoryRecords(): Promise<{ count: number; records: CognitiveMemoryRecord[]; metrics: any }> {
    const fallback = {
      count: 2,
      records: [
        {
          record_id: 'mem-1',
          tier: 'semantic' as const,
          content: { concept: 'Document PDF Font Embedding Corruptions trigger fallback Tesseract OCR path' },
          importance_score: 0.92,
          access_count: 84,
          associations: ['pdf', 'fonts', 'tesseract', 'fallback'],
          created_at: new Date(Date.now() - 30 * 86400000).toISOString(),
          last_accessed: new Date().toISOString(),
        },
      ],
      metrics: { total_memories: 1, mean_importance: 0.92 },
    };
    return this.fetchJson(`${BASE_URL}/memory/records`, {}, fallback);
  }

  // Events
  public static async getEvents(limit = 50): Promise<{ count: number; events: WorldModelEvent[] }> {
    const fallback = {
      count: 3,
      events: [
        {
          event_id: 'evt-1',
          event_type: 'WORLD_STATE_UPDATED',
          timestamp: new Date().toISOString(),
          severity: 'info' as const,
          source_subsystem: 'world_engine',
          payload: { entities_updated: 4, relations_updated: 8 },
        },
      ],
    };
    return this.fetchJson(`${BASE_URL}/events?limit=${limit}`, {}, fallback);
  }
}
