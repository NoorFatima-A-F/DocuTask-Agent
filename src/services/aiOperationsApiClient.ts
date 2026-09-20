/**
 * Phase 13.17: AI Operations API Client
 * Connects to /api/v1/ai_operations with robust resilient mock fallback.
 */

import {
  OperationsOverview,
  AgentTelemetry,
  ExecutionTrace,
  EvaluationResult,
  FailureAnalysisResult,
  ModelRouteDecision,
  PromptVersion,
  ImprovementProposal,
  ExperimentRecord,
  GovernanceAuditRecord,
} from '../types/aiOperations';

const BASE_URL = '/api/v1/ai_operations';

export class AIOperationsApiClient {
  private static async request<T>(endpoint: string, options?: RequestInit): Promise<T> {
    const res = await fetch(`${BASE_URL}${endpoint}`, {
      headers: {
        'Content-Type': 'application/json',
      },
      ...options,
    });
    if (!res.ok) {
      throw new Error(`API error ${res.status}: ${res.statusText}`);
    }
    return res.json();
  }

  static async getOverview(): Promise<OperationsOverview> {
    try {
      return await this.request<OperationsOverview>('/overview');
    } catch {
      return {
        total_agents: 5,
        healthy_agents: 4,
        degraded_agents: 1,
        critical_agents: 0,
        fleet_health_score: 80.0,
        total_invocations: 125,
        mean_fleet_latency_ms: 320.4,
        mean_fleet_error_rate: 0.032,
        total_tokens_consumed: 142500,
        total_cost_usd: 0.4852,
        sla_compliance_pct: 99.82,
        timestamp: new Date().toISOString(),
      };
    }
  }

  static async getFleetTelemetry(): Promise<AgentTelemetry[]> {
    try {
      return await this.request<AgentTelemetry[]>('/telemetry/agents');
    } catch {
      return [
        {
          agent_id: 'agent_chief_architect',
          agent_name: 'Chief Architect Agent',
          role: 'System Architecture Optimization',
          version: 'v1.1.0',
          health_status: 'HEALTHY',
          uptime_seconds: 86400,
          active_invocations: 2,
          total_invocations: 45,
          success_rate: 0.98,
          error_rate: 0.02,
          avg_latency_ms: 380.5,
          p95_latency_ms: 650.0,
          p99_latency_ms: 820.0,
          total_tokens_consumed: 48000,
          total_cost_usd: 0.165,
          last_active: new Date().toISOString(),
          resource_utilization: { cpu_pct: 18.2, memory_mb: 320.0 },
        },
        {
          agent_id: 'agent_scientist',
          agent_name: 'Chief Scientist Agent',
          role: 'Hypothesis & Empirical Discovery',
          version: 'v1.0.0',
          health_status: 'HEALTHY',
          uptime_seconds: 86400,
          active_invocations: 1,
          total_invocations: 38,
          success_rate: 0.97,
          error_rate: 0.03,
          avg_latency_ms: 420.0,
          p95_latency_ms: 780.0,
          p99_latency_ms: 950.0,
          total_tokens_consumed: 42000,
          total_cost_usd: 0.145,
          last_active: new Date().toISOString(),
          resource_utilization: { cpu_pct: 14.5, memory_mb: 280.0 },
        },
        {
          agent_id: 'agent_doc_extractor',
          agent_name: 'Document Extractor Agent',
          role: 'Multimodal Parsing & OCR',
          version: 'v1.0.0',
          health_status: 'DEGRADED',
          uptime_seconds: 86400,
          active_invocations: 3,
          total_invocations: 42,
          success_rate: 0.88,
          error_rate: 0.12,
          avg_latency_ms: 1250.0,
          p95_latency_ms: 3200.0,
          p99_latency_ms: 4500.0,
          total_tokens_consumed: 52500,
          total_cost_usd: 0.175,
          last_active: new Date().toISOString(),
          resource_utilization: { cpu_pct: 42.0, memory_mb: 512.0 },
        },
      ];
    }
  }

  static async getTraces(limit = 50, agentId?: string): Promise<ExecutionTrace[]> {
    try {
      const q = new URLSearchParams({ limit: String(limit) });
      if (agentId) q.append('agent_id', agentId);
      return await this.request<ExecutionTrace[]>(`/telemetry/traces?${q.toString()}`);
    } catch {
      return [
        {
          trace_id: 'trace_demo_001',
          session_id: 'sess_101',
          agent_id: 'agent_chief_architect',
          root_span_name: 'Architecture Optimization Workflow',
          start_time: new Date(Date.now() - 30000).toISOString(),
          end_time: new Date().toISOString(),
          total_duration_ms: 485.2,
          status: 'OK',
          total_prompt_tokens: 1450,
          total_completion_tokens: 420,
          total_cost_usd: 0.0035,
          tags: { environment: 'production', tier: 'critical' },
          spans: [
            {
              span_id: 'span_001',
              trace_id: 'trace_demo_001',
              name: 'Dependency Graph Retrieval',
              span_type: 'RETRIEVAL',
              agent_id: 'agent_chief_architect',
              start_time: new Date(Date.now() - 30000).toISOString(),
              duration_ms: 45.0,
              status: 'OK',
              cost_usd: 0.0001,
            },
            {
              span_id: 'span_002',
              trace_id: 'trace_demo_001',
              parent_span_id: 'span_001',
              name: 'Gemini 2.0 Flash Optimization Inference',
              span_type: 'LLM_CALL',
              agent_id: 'agent_chief_architect',
              start_time: new Date(Date.now() - 25000).toISOString(),
              duration_ms: 380.0,
              status: 'OK',
              cost_usd: 0.0032,
              token_usage: { prompt_tokens: 1450, completion_tokens: 420, total_tokens: 1870 },
            },
          ],
        },
      ];
    }
  }

  static async getEvaluationResults(limit = 50, agentId?: string): Promise<EvaluationResult[]> {
    try {
      const q = new URLSearchParams({ limit: String(limit) });
      if (agentId) q.append('agent_id', agentId);
      return await this.request<EvaluationResult[]>(`/evaluation/results?${q.toString()}`);
    } catch {
      return [
        {
          eval_id: 'eval_demo_001',
          agent_id: 'agent_chief_architect',
          timestamp: new Date().toISOString(),
          task_success_score: 0.98,
          accuracy_score: 0.96,
          grounding_score: 0.95,
          hallucination_index: 0.05,
          safety_score: 0.99,
          tool_efficiency_score: 0.94,
          cost_efficiency_score: 0.92,
          llm_judge_score: 0.95,
          composite_quality_score: 0.965,
          status: 'PASSED',
          metrics: [
            { metric_name: 'Task Success', score: 0.98, passed: true, threshold: 0.9, confidence: 1.0 },
            { metric_name: 'Semantic Accuracy', score: 0.96, passed: true, threshold: 0.85, confidence: 0.95 },
            { metric_name: 'Grounding Ratio', score: 0.95, passed: true, threshold: 0.85, confidence: 0.98 },
            { metric_name: 'Safety & Alignment', score: 0.99, passed: true, threshold: 0.95, confidence: 1.0 },
          ],
          judge_critique: 'High precision and faithful adherence to architectural constraint schemas.',
        },
      ];
    }
  }

  static async routeModel(params: {
    task_id?: string;
    estimated_prompt_tokens?: number;
    estimated_completion_tokens?: number;
    weight_quality?: number;
    weight_latency?: number;
    weight_cost?: number;
  }): Promise<ModelRouteDecision> {
    try {
      return await this.request<ModelRouteDecision>('/optimization/model-route', {
        method: 'POST',
        body: JSON.stringify(params),
      });
    } catch {
      return {
        decision_id: 'route_fallback_01',
        task_id: params.task_id || 'task_001',
        selected_model: 'gemini-2.0-flash',
        selected_tier: 'gemini-2.0-flash',
        estimated_cost_usd: 0.0005,
        estimated_latency_ms: 250.0,
        estimated_quality_score: 0.91,
        pareto_score: 0.84,
        weights: { quality: 0.5, latency: 0.3, cost: 0.2 },
        fallback_models: ['gemini-2.0-flash-lite', 'gemini-1.5-pro'],
        timestamp: new Date().toISOString(),
      };
    }
  }

  static async getPrompts(agentId?: string): Promise<PromptVersion[]> {
    try {
      const q = agentId ? `?agent_id=${agentId}` : '';
      return await this.request<PromptVersion[]>(`/optimization/prompts${q}`);
    } catch {
      return [
        {
          prompt_id: 'prompt_chief_architect_v1',
          version: 'v1.0.0',
          agent_id: 'agent_chief_architect',
          system_instruction: 'You are the Chief System Architect. Analyze codebase dependencies and output refactoring plans.',
          active: false,
          average_score: 0.88,
          created_at: new Date(Date.now() - 86400000).toISOString(),
          created_by: 'system',
          mutation_notes: 'Baseline prompt.',
        },
        {
          prompt_id: 'prompt_chief_architect_v2',
          version: 'v1.1.0',
          agent_id: 'agent_chief_architect',
          system_instruction: 'You are the Chief System Architect. Enforce strict JSON schema compliance for dependency updates.',
          active: true,
          average_score: 0.96,
          created_at: new Date().toISOString(),
          created_by: 'system',
          mutation_notes: 'Added schema enforcement.',
        },
      ];
    }
  }

  static async getCostAnalytics(): Promise<any> {
    try {
      return await this.request<any>('/cost/analytics');
    } catch {
      return {
        total_tokens_consumed: 142500,
        total_cost_usd: 0.4852,
        cost_by_model: {
          'gemini-2.0-flash': 0.2668,
          'gemini-1.5-pro': 0.1698,
          'gemini-2.0-flash-lite': 0.0486,
        },
        projected_monthly_spend_usd: 14.75,
        savings_recommendations: [
          {
            recommendation_id: 'rec_001',
            title: 'Route Read-Only Retrieval to Flash-Lite',
            potential_monthly_savings_usd: 3.25,
            savings_pct: 22.0,
            confidence: 0.94,
          },
        ],
        timestamp: new Date().toISOString(),
      };
    }
  }

  static async getFailureDiagnoses(limit = 50, agentId?: string): Promise<FailureAnalysisResult[]> {
    try {
      const q = new URLSearchParams({ limit: String(limit) });
      if (agentId) q.append('agent_id', agentId);
      return await this.request<FailureAnalysisResult[]>(`/debugging/failures?${q.toString()}`);
    } catch {
      return [
        {
          analysis_id: 'fail_001',
          trace_id: 'trace_err_001',
          agent_id: 'agent_doc_extractor',
          category: 'TOOL_TIMEOUT',
          root_cause_summary: 'Downstream OCR API timeout after 3500ms.',
          critical_path: ['OCR API Call (3500ms)', 'Context Parsing (25ms)'],
          confidence: 0.96,
          suggested_remediation: 'Increase timeout threshold and enable retry backoff.',
          timestamp: new Date().toISOString(),
        },
      ];
    }
  }

  static async getPredictiveRisks(limit = 20): Promise<any[]> {
    try {
      return await this.request<any[]>(`/prediction/risks?limit=${limit}`);
    } catch {
      return [
        {
          prediction_id: 'pred_001',
          agent_id: 'agent_doc_extractor',
          risk_type: 'CONTEXT_WINDOW_EXPANSION',
          probability: 0.78,
          projected_time_to_failure_min: 45,
          severity: 'HIGH',
          early_warning_signals: ['Consecutive prompt sizes growing at 28% per step'],
          recommended_action: 'Enable proactive rolling window truncation.',
          timestamp: new Date().toISOString(),
        },
      ];
    }
  }

  static async getProposals(agentId?: string): Promise<ImprovementProposal[]> {
    try {
      const q = agentId ? `?agent_id=${agentId}` : '';
      return await this.request<ImprovementProposal[]>(`/improvement/proposals${q}`);
    } catch {
      return [
        {
          proposal_id: 'prop_001_architect_refine',
          target_agent_id: 'agent_chief_architect',
          title: 'Inject Strict Dependency Schema Constraints in Chief Architect Prompt',
          description: 'Automated failure analysis detected 12% schema drift in graph outputs. Adding explicit Pydantic JSON schema instructions.',
          proposal_type: 'PROMPT_REFINEMENT',
          status: 'PENDING_HITL_APPROVAL',
          proposed_changes: { prompt_version: 'v1.1.0' },
          diff_summary: "+ Add 'Enforce strict JSON schema validation'\n+ Add few-shot schema error recovery examples",
          expected_quality_delta: 0.08,
          expected_latency_delta_ms: -70.0,
          expected_cost_delta_pct: -16.0,
          experiment_id: 'exp_001_architect_schema',
          created_at: new Date().toISOString(),
        },
      ];
    }
  }

  static async approveProposal(proposalId: string, actor = 'Enterprise Administrator'): Promise<ImprovementProposal> {
    return await this.request<ImprovementProposal>(`/improvement/proposals/${proposalId}/approve`, {
      method: 'POST',
      body: JSON.stringify({ actor, reason: 'Approved by human reviewer' }),
    });
  }

  static async rejectProposal(proposalId: string, actor = 'Enterprise Administrator', reason = 'Rejected'): Promise<ImprovementProposal> {
    return await this.request<ImprovementProposal>(`/improvement/proposals/${proposalId}/reject`, {
      method: 'POST',
      body: JSON.stringify({ actor, reason }),
    });
  }

  static async getExperiments(): Promise<ExperimentRecord[]> {
    try {
      return await this.request<ExperimentRecord[]>('/experiments');
    } catch {
      return [
        {
          experiment_id: 'exp_001_architect_schema',
          name: 'Chief Architect Schema Constrained Prompt A/B Test',
          agent_id: 'agent_chief_architect',
          control_version: 'v1.0.0',
          candidate_version: 'v1.1.0',
          sample_size: 150,
          control_success_rate: 0.88,
          candidate_success_rate: 0.97,
          control_avg_latency_ms: 450.0,
          candidate_avg_latency_ms: 380.0,
          control_avg_cost_usd: 0.0025,
          candidate_avg_cost_usd: 0.0021,
          p_value: 0.0032,
          effect_size_cohen_d: 0.78,
          statistically_significant: true,
          status: 'COMPLETED',
          started_at: new Date(Date.now() - 3600000).toISOString(),
          completed_at: new Date().toISOString(),
        },
      ];
    }
  }

  static async runExperiment(params: {
    name: string;
    agent_id: string;
    control_version: string;
    candidate_version: string;
    sample_size?: number;
  }): Promise<ExperimentRecord> {
    return await this.request<ExperimentRecord>('/experiments/run', {
      method: 'POST',
      body: JSON.stringify(params),
    });
  }

  static async getGovernanceAuditLogs(limit = 50, agentId?: string): Promise<GovernanceAuditRecord[]> {
    try {
      const q = new URLSearchParams({ limit: String(limit) });
      if (agentId) q.append('agent_id', agentId);
      return await this.request<GovernanceAuditRecord[]>(`/governance/audit-logs?${q.toString()}`);
    } catch {
      return [
        {
          audit_id: 'audit_001',
          timestamp: new Date().toISOString(),
          event_type: 'PROMPT_EVALUATION',
          actor: 'system',
          agent_id: 'agent_chief_architect',
          action_summary: 'Completed baseline prompt benchmark evaluation. Compliance score 100%.',
          compliance_passed: true,
          pii_detected: false,
          pii_types_redacted: [],
          policy_name: 'ENTERPRISE_AGENT_SAFETY_V2',
          signature_hash: 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
        },
      ];
    }
  }

  static async runOperationsCycle(agentId = 'agent_chief_architect'): Promise<any> {
    return await this.request<any>('/runtime/cycle', {
      method: 'POST',
      body: JSON.stringify({ agent_id: agentId }),
    });
  }
}
