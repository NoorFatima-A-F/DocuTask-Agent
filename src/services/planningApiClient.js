/**
 * Planning API Client for DocuTask Agent.
 * Interacts with /api/v1/planning REST endpoints with local fallback for offline demo capabilities.
 */
const API_BASE = '/api/v1/planning';
export class PlanningApiClient {
    static async planMission(missionId, intent, userConstraints) {
        try {
            const res = await fetch(`${API_BASE}/plan`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ mission_id: missionId, intent, user_constraints: userConstraints }),
            });
            if (res.ok)
                return await res.json();
        }
        catch {
            // Fallback to synthetic client payload
        }
        return this.getFallbackPlan(missionId, intent);
    }
    static async getStrategyMatrix(missionId) {
        try {
            const res = await fetch(`${API_BASE}/strategies/${missionId}`);
            if (res.ok)
                return await res.json();
        }
        catch {
            // Fallback
        }
        return (await this.getFallbackPlan(missionId, '')).selection_record.comparison_matrix;
    }
    static async queryCounterfactual(missionId, queryType, weightOverrides, targetStrategyId) {
        try {
            const res = await fetch(`${API_BASE}/counterfactuals/query`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    mission_id: missionId,
                    query_type: queryType,
                    weight_overrides: weightOverrides,
                    target_strategy_id: targetStrategyId,
                }),
            });
            if (res.ok)
                return await res.json();
        }
        catch {
            // Fallback
        }
        return {
            query_type: queryType,
            target_strategy_id: targetStrategyId,
            summary_explanation: 'Recalculated strategy utility: Strategy Alpha overtakes when latency weight exceeds 0.48.',
            algebraic_proof: 'U = 0.80*Acc - 0.10*Lat - 0.05*Cost - 0.05*Risk',
            tipping_point: {
                parameter: 'w_latency',
                current_value: 0.20,
                tipping_threshold: 0.48,
                condition: 'If latency weight w_latency >= 0.48, Strategy Alpha (Fast) becomes optimal.',
            },
            alternative_ranking: [
                { strategy_id: 'strat_alpha', name: 'Strategy Alpha (Fast Turbo)', archetype: 'ALPHA_FAST', new_utility: 0.82 },
                { strategy_id: 'strat_delta', name: 'Strategy Delta (Pareto)', archetype: 'DELTA_PARETO', new_utility: 0.74 },
                { strategy_id: 'strat_gamma', name: 'Strategy Gamma (Frugal)', archetype: 'GAMMA_COST', new_utility: 0.61 },
                { strategy_id: 'strat_beta', name: 'Strategy Beta (Accurate)', archetype: 'BETA_ACCURATE', new_utility: 0.49 },
            ],
            version: '1.0.0',
        };
    }
    static async getDAG(missionId) {
        try {
            const res = await fetch(`${API_BASE}/dag/${missionId}`);
            if (res.ok)
                return await res.json();
        }
        catch {
            // Fallback
        }
        return (await this.getFallbackPlan(missionId, '')).selected_dag;
    }
    static async mutateDAG(missionId, mutationType, targetNodeId, splitCount = 2) {
        try {
            const res = await fetch(`${API_BASE}/dag/${missionId}/mutate`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    mutation_type: mutationType,
                    target_node_id: targetNodeId,
                    split_count: splitCount,
                    rationale: 'Interactive operator UI optimization',
                }),
            });
            if (res.ok)
                return await res.json();
        }
        catch {
            // Fallback
        }
        return (await this.getFallbackPlan(missionId, '')).selected_dag;
    }
    static async getSchedulerStatus() {
        try {
            const res = await fetch(`${API_BASE}/scheduler/status`);
            if (res.ok)
                return await res.json();
        }
        catch {
            // Fallback
        }
        return {
            total_workers: 8,
            idle_workers: 6,
            busy_workers: 2,
            utilization_pct: 25.0,
            queue_depth: 0,
            active_leases_count: 2,
            active_leases: [
                {
                    lease_id: 'lease_ocr_01',
                    worker_id: 'worker-node-1',
                    mission_id: 'm1',
                    step_id: 'step_1',
                    capability_id: 'ocr_cloud_vision',
                    priority: 2,
                    leased_at: new Date().toISOString(),
                    expires_at_epoch: Date.now() / 1000 + 45,
                    is_active: true,
                    preempted: false,
                },
                {
                    lease_id: 'lease_llm_02',
                    worker_id: 'worker-node-2',
                    mission_id: 'm1',
                    step_id: 'step_2',
                    capability_id: 'llm_flash_lite',
                    priority: 2,
                    leased_at: new Date().toISOString(),
                    expires_at_epoch: Date.now() / 1000 + 30,
                    is_active: true,
                    preempted: false,
                },
            ],
        };
    }
    static async evaluateMission(missionId, actualLatencyMs, actualCostUsd, actualAccuracy) {
        try {
            const res = await fetch(`${API_BASE}/evaluate/${missionId}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    mission_id: missionId,
                    actual_latency_ms: actualLatencyMs,
                    actual_cost_usd: actualCostUsd,
                    actual_accuracy: actualAccuracy,
                }),
            });
            if (res.ok)
                return await res.json();
        }
        catch {
            // Fallback
        }
        return {
            calibration_id: 'calib_demo_01',
            mission_id: missionId,
            strategy_id: 'strat_delta_pareto',
            comparison: {
                predicted_latency_ms: 1850.0,
                actual_latency_ms: actualLatencyMs || 1920.0,
                latency_delta_ms: 70.0,
                latency_error_pct: 3.78,
                predicted_cost_usd: 0.0038,
                actual_cost_usd: actualCostUsd || 0.0039,
                cost_delta_usd: 0.0001,
                cost_error_pct: 2.63,
                predicted_accuracy: 0.985,
                actual_accuracy: actualAccuracy || 0.99,
                accuracy_delta: 0.005,
                predicted_risk_score: 0.06,
                actual_failure_occurred: false,
            },
            overall_calibration_score: 0.968,
            root_causes: ['Plan executed strictly within nominal 95% confidence bounds.'],
            tuning_recommendations: { model_status: 'Calibration optimal. Predictive parameters verified.' },
            timestamp: new Date().toISOString(),
        };
    }
    static getFallbackPlan(missionId, intent) {
        return {
            mission_id: missionId || 'mission_active_001',
            goal_graph: {
                graph_id: 'goal_graph_01',
                mission_id: missionId,
                root_intent: intent || 'Extract multi-page invoice tables and cross-verify totals',
                objectives: {},
                root_objective_ids: ['obj_1'],
                dependencies: {},
                created_at: new Date().toISOString(),
                version: '1.0.0',
            },
            constraint_set: {
                constraint_set_id: 'cset_01',
                mission_id: missionId,
                constraints: [],
                created_at: new Date().toISOString(),
            },
            candidate_strategies: [
                {
                    strategy_id: 'strat_delta_pareto',
                    archetype: 'DELTA_PARETO',
                    name: 'Strategy Delta (Adaptive Pareto-Balanced)',
                    description: 'Hybrid pipeline: Cloud Vision precision for OCR, Flash Lite for high-speed extraction, AST validation, and Pro LLM fallback.',
                    mission_id: missionId,
                    steps: [
                        { step_id: 's1', objective_id: 'o1', name: 'Document Ingestion & Neural OCR', capability_id: 'ocr_cloud_vision', provider: 'google_cloud_vision', estimated_latency_ms: 450, estimated_cost_usd: 0.0015, estimated_accuracy: 0.985, failure_probability: 0.005 },
                        { step_id: 's2', objective_id: 'o2', name: 'Semantic Entity & Table Extraction', capability_id: 'llm_flash_lite', provider: 'gemini_flash_lite', estimated_latency_ms: 600, estimated_cost_usd: 0.0005, estimated_accuracy: 0.965, failure_probability: 0.02, fallback_capability_id: 'llm_pro_reasoner' },
                        { step_id: 's3', objective_id: 'o3', name: 'Deterministic AST Math & Tax Validation', capability_id: 'fast_rule_engine', provider: 'ast_validator', estimated_latency_ms: 25, estimated_cost_usd: 0.00001, estimated_accuracy: 0.9999, failure_probability: 0.0001 },
                        { step_id: 's4', objective_id: 'o4', name: 'Episodic Memory Graph Indexing', capability_id: 'episodic_memory_graph', provider: 'chroma_graph', estimated_latency_ms: 120, estimated_cost_usd: 0.0002, estimated_accuracy: 0.97, failure_probability: 0.005 },
                    ],
                    concurrency_level: 8,
                    estimated_total_latency_ms: 1195,
                    estimated_critical_path_ms: 850,
                    estimated_total_cost_usd: 0.00221,
                    estimated_accuracy: 0.98,
                    estimated_risk_score: 0.06,
                    token_estimate: 18500,
                    is_pareto_optimal: true,
                    constraint_compliance: { is_valid: true, violations: [], soft_penalty: 0 },
                    rationale: 'Maximizes Pareto multi-objective utility by capturing 98% of Pro accuracy at 15% of the cost and 40% of the latency.',
                    created_at: new Date().toISOString(),
                },
                {
                    strategy_id: 'strat_alpha_fast',
                    archetype: 'ALPHA_FAST',
                    name: 'Strategy Alpha (Latency-Optimized Turbo)',
                    description: 'Leverages local fast OCR and Gemini 2.0 Flash Lite with deterministic AST rule verification for maximum throughput.',
                    mission_id: missionId,
                    steps: [],
                    concurrency_level: 8,
                    estimated_total_latency_ms: 650,
                    estimated_critical_path_ms: 480,
                    estimated_total_cost_usd: 0.0008,
                    estimated_accuracy: 0.89,
                    estimated_risk_score: 0.18,
                    token_estimate: 12000,
                    is_pareto_optimal: true,
                    constraint_compliance: { is_valid: true, violations: [], soft_penalty: 0 },
                    rationale: 'Selected when SLA is extremely tight.',
                    created_at: new Date().toISOString(),
                },
                {
                    strategy_id: 'strat_beta_accurate',
                    archetype: 'BETA_ACCURATE',
                    name: 'Strategy Beta (Maximum Accuracy Deep Reasoning)',
                    description: 'Utilizes Cloud Vision Neural OCR, Gemini 2.0 Pro deep extraction, and multi-stage reflective validation.',
                    mission_id: missionId,
                    steps: [],
                    concurrency_level: 4,
                    estimated_total_latency_ms: 3800,
                    estimated_critical_path_ms: 2900,
                    estimated_total_cost_usd: 0.0165,
                    estimated_accuracy: 0.995,
                    estimated_risk_score: 0.03,
                    token_estimate: 48000,
                    is_pareto_optimal: true,
                    constraint_compliance: { is_valid: true, violations: [], soft_penalty: 0 },
                    rationale: 'Selected for mission-critical financial audits.',
                    created_at: new Date().toISOString(),
                },
                {
                    strategy_id: 'strat_gamma_cost',
                    archetype: 'GAMMA_COST',
                    name: 'Strategy Gamma (Budget Frugal & Efficient)',
                    description: 'Minimizes cost footprint through local Tesseract OCR, Flash Lite routing, and batch rule checks.',
                    mission_id: missionId,
                    steps: [],
                    concurrency_level: 6,
                    estimated_total_latency_ms: 820,
                    estimated_critical_path_ms: 620,
                    estimated_total_cost_usd: 0.0005,
                    estimated_accuracy: 0.88,
                    estimated_risk_score: 0.14,
                    token_estimate: 8500,
                    is_pareto_optimal: false,
                    constraint_compliance: { is_valid: true, violations: [], soft_penalty: 0 },
                    rationale: 'Selected for bulk ingestion workloads.',
                    created_at: new Date().toISOString(),
                },
            ],
            selection_record: {
                selected_strategy_id: 'strat_delta_pareto',
                selected_archetype: 'DELTA_PARETO',
                selection_rationale: 'Selected Strategy Delta (Adaptive Pareto-Balanced) with highest multi-objective utility score (0.4392). Provides optimal balance of 98.0% accuracy at $0.0022 cost and 850ms critical path latency.',
                rejection_reasons: {
                    strat_alpha_fast: 'Lower accuracy (89% vs 98%) creates unacceptable extraction risk on financial line items.',
                    strat_beta_accurate: 'Excessive latency (2900ms vs 850ms) and 7.5x cost penalty for marginal +1.5% accuracy gain.',
                    strat_gamma_cost: 'Dominated in Pareto space by Strategy Delta with higher accuracy at negligible cost increment.',
                },
                comparison_matrix: {
                    mission_id: missionId,
                    entries: [
                        { strategy_id: 'strat_delta_pareto', archetype: 'DELTA_PARETO', name: 'Strategy Delta (Adaptive Pareto-Balanced)', rank: 1, utility_score: 0.4392, accuracy: 0.98, critical_path_ms: 850, total_cost_usd: 0.0022, risk_score: 0.06, token_estimate: 18500, is_pareto_optimal: true, is_valid: true, violations: [] },
                        { strategy_id: 'strat_alpha_fast', archetype: 'ALPHA_FAST', name: 'Strategy Alpha (Latency-Optimized Turbo)', rank: 2, utility_score: 0.3850, accuracy: 0.89, critical_path_ms: 480, total_cost_usd: 0.0008, risk_score: 0.18, token_estimate: 12000, is_pareto_optimal: true, is_valid: true, violations: [], rejection_reason: 'Lower accuracy on financial entities.' },
                        { strategy_id: 'strat_beta_accurate', archetype: 'BETA_ACCURATE', name: 'Strategy Beta (Maximum Accuracy Deep Reasoning)', rank: 3, utility_score: 0.3120, accuracy: 0.995, critical_path_ms: 2900, total_cost_usd: 0.0165, risk_score: 0.03, token_estimate: 48000, is_pareto_optimal: true, is_valid: true, violations: [], rejection_reason: 'Latency and cost penalty exceeds budget envelope.' },
                        { strategy_id: 'strat_gamma_cost', archetype: 'GAMMA_COST', name: 'Strategy Gamma (Budget Frugal & Efficient)', rank: 4, utility_score: 0.2980, accuracy: 0.88, critical_path_ms: 620, total_cost_usd: 0.0005, risk_score: 0.14, token_estimate: 8500, is_pareto_optimal: false, is_valid: true, violations: [], rejection_reason: 'Suboptimal utility tradeoff.' },
                    ],
                    pareto_frontier_strategy_ids: ['strat_delta_pareto', 'strat_alpha_fast', 'strat_beta_accurate'],
                    selected_strategy_id: 'strat_delta_pareto',
                    version: '1.0.0',
                },
                utility_breakdown: {
                    strategy_id: 'strat_delta_pareto',
                    total_utility: 0.4392,
                    accuracy_term: 0.3920,
                    latency_penalty_term: 0.0170,
                    cost_penalty_term: 0.0044,
                    risk_penalty_term: 0.0060,
                    memory_bonus_term: 0.0475,
                    satisfaction_bonus_term: 0.0500,
                    soft_constraint_penalty: 0.0,
                    raw_accuracy: 0.98,
                    normalized_latency: 0.085,
                    normalized_cost: 0.022,
                    raw_risk: 0.06,
                    weights: { w_accuracy: 0.4, w_latency: 0.2, w_cost: 0.2, w_risk: 0.1, w_memory: 0.05, w_satisfaction: 0.05 },
                    equation: 'U = 0.40*Acc - 0.20*(L/10000) - 0.20*(C/0.10) - 0.10*R + 0.05*M + 0.05*S',
                    version: '2.0.0',
                },
            },
            selected_dag: {
                dag_id: 'dag_01',
                mission_id: missionId,
                strategy_id: 'strat_delta_pareto',
                nodes: {
                    n1: { node_id: 'n1', name: 'Document Ingestion & Neural OCR', capability_id: 'ocr_cloud_vision', provider: 'google_cloud_vision', status: 'COMPLETED', retry_count: 0, max_retries: 3, timeout_ms: 30000, payload: {}, metadata: {} },
                    n2: { node_id: 'n2', name: 'Semantic Entity & Table Extraction', capability_id: 'llm_flash_lite', provider: 'gemini_flash_lite', status: 'RUNNING', retry_count: 0, max_retries: 3, timeout_ms: 30000, payload: {}, metadata: {} },
                    n3: { node_id: 'n3', name: 'Deterministic AST Math & Tax Validation', capability_id: 'fast_rule_engine', provider: 'ast_validator', status: 'PENDING', retry_count: 0, max_retries: 3, timeout_ms: 30000, payload: {}, metadata: {} },
                    n4: { node_id: 'n4', name: 'Episodic Memory Graph Indexing', capability_id: 'episodic_memory_graph', provider: 'chroma_graph', status: 'PENDING', retry_count: 0, max_retries: 3, timeout_ms: 30000, payload: {}, metadata: {} },
                },
                edges: [
                    { edge_id: 'e1', source_id: 'n1', target_id: 'n2', edge_type: 'DATA' },
                    { edge_id: 'e2', source_id: 'n2', target_id: 'n3', edge_type: 'DATA' },
                    { edge_id: 'e3', source_id: 'n3', target_id: 'n4', edge_type: 'DATA' },
                ],
                mutation_history: [
                    { mutation_id: 'm1', timestamp: new Date().toISOString(), mutation_type: 'NODE_SPLIT', target_node_id: 'n2', rationale: 'Parallelized multi-page chunks', diff_summary: 'Split node n2 into 2 execution shards', applied_by: 'AutonomousPlanner' },
                ],
                version: 2,
                created_at: new Date().toISOString(),
            },
            simulations: {},
            cost_predictions: {},
            latency_predictions: {},
            risk_profiles: {},
            counterfactual_explanations: [
                {
                    query_type: 'WHY_STRATEGY_SELECTED',
                    target_strategy_id: 'strat_delta_pareto',
                    summary_explanation: 'Strategy Delta achieved maximum multi-objective utility (0.4392) by providing near-pro accuracy at a fraction of latency and token cost.',
                    algebraic_proof: 'U(Delta) = 0.4392 > U(Alpha) = 0.3850 > U(Beta) = 0.3120 > U(Gamma) = 0.2980',
                    version: '1.0.0',
                },
            ],
        };
    }
}
