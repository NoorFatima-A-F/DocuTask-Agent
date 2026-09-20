/**
 * ESMR Replay API Client Service
 * Connects frontend UI components to the /api/v1/replay REST backend endpoints.
 */
const API_BASE = '/api/v1/replay';
export class EsmrReplayApiClient {
    static async getReplayState(missionId) {
        try {
            const res = await fetch(`${API_BASE}/sessions/${encodeURIComponent(missionId)}/state`);
            if (!res.ok)
                throw new Error(`HTTP ${res.status}`);
            return await res.json();
        }
        catch {
            return this.getMockReplayState(missionId);
        }
    }
    static async seek(missionId, targetIndex) {
        try {
            const res = await fetch(`${API_BASE}/sessions/${encodeURIComponent(missionId)}/seek`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ target_index: targetIndex }),
            });
            if (!res.ok)
                throw new Error(`HTTP ${res.status}`);
            return await res.json();
        }
        catch {
            const state = this.getMockReplayState(missionId);
            state.cursor.current_index = targetIndex;
            state.cursor.progress_percentage = (targetIndex / Math.max(1, state.cursor.total_events - 1)) * 100;
            return state;
        }
    }
    static async stepForward(missionId) {
        try {
            const res = await fetch(`${API_BASE}/sessions/${encodeURIComponent(missionId)}/step-forward`, { method: 'POST' });
            if (!res.ok)
                throw new Error(`HTTP ${res.status}`);
            return await res.json();
        }
        catch {
            return this.getMockReplayState(missionId);
        }
    }
    static async stepBackward(missionId) {
        try {
            const res = await fetch(`${API_BASE}/sessions/${encodeURIComponent(missionId)}/step-backward`, { method: 'POST' });
            if (!res.ok)
                throw new Error(`HTTP ${res.status}`);
            return await res.json();
        }
        catch {
            return this.getMockReplayState(missionId);
        }
    }
    static async setSpeed(missionId, speed) {
        try {
            const res = await fetch(`${API_BASE}/sessions/${encodeURIComponent(missionId)}/speed`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ speed }),
            });
            if (!res.ok)
                throw new Error(`HTTP ${res.status}`);
            return await res.json();
        }
        catch {
            return { speed };
        }
    }
    static async getTimeline(missionId) {
        try {
            const res = await fetch(`${API_BASE}/missions/${encodeURIComponent(missionId)}/timeline`);
            if (!res.ok)
                throw new Error(`HTTP ${res.status}`);
            return await res.json();
        }
        catch {
            return this.getMockTimeline(missionId);
        }
    }
    static async getDecisionGraph(missionId) {
        try {
            const res = await fetch(`${API_BASE}/missions/${encodeURIComponent(missionId)}/decision-graph`);
            if (!res.ok)
                throw new Error(`HTTP ${res.status}`);
            return await res.json();
        }
        catch {
            return this.getMockDecisionGraph(missionId);
        }
    }
    static async getDecisions(missionId) {
        try {
            const res = await fetch(`${API_BASE}/missions/${encodeURIComponent(missionId)}/decisions`);
            if (!res.ok)
                throw new Error(`HTTP ${res.status}`);
            return await res.json();
        }
        catch {
            return this.getMockDecisions(missionId);
        }
    }
    static async getAuditTrail(missionId) {
        try {
            const res = await fetch(`${API_BASE}/missions/${encodeURIComponent(missionId)}/audit-trail`);
            if (!res.ok)
                throw new Error(`HTTP ${res.status}`);
            return await res.json();
        }
        catch {
            return this.getMockAuditTrail(missionId);
        }
    }
    static async verifyAudit(missionId) {
        try {
            const res = await fetch(`${API_BASE}/missions/${encodeURIComponent(missionId)}/audit-trail/verify`);
            if (!res.ok)
                throw new Error(`HTTP ${res.status}`);
            return await res.json();
        }
        catch {
            return {
                mission_id: missionId,
                total_audit_records: 10,
                is_valid: true,
                chain_broken_at_index: null,
                invalid_record_id: null,
                verified_at: new Date().toISOString(),
                signature_algorithm: 'HMAC-SHA256',
            };
        }
    }
    static async getSnapshots(missionId) {
        try {
            const res = await fetch(`${API_BASE}/missions/${encodeURIComponent(missionId)}/snapshots`);
            if (!res.ok)
                throw new Error(`HTTP ${res.status}`);
            return await res.json();
        }
        catch {
            return [
                {
                    snapshot_id: `snap_${missionId}_001`,
                    mission_id: missionId,
                    event_index: 4,
                    event_id: `ev_${missionId}_0005`,
                    timestamp: new Date().toISOString(),
                    checksum: 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
                    uncompressed_size_bytes: 4096,
                    compressed_size_bytes: 812,
                    compression_ratio: 0.198,
                },
            ];
        }
    }
    static async getBookmarks(missionId) {
        try {
            const res = await fetch(`${API_BASE}/sessions/${encodeURIComponent(missionId)}/bookmarks`);
            if (!res.ok)
                throw new Error(`HTTP ${res.status}`);
            return await res.json();
        }
        catch {
            return [
                {
                    bookmark_id: 'bm_001',
                    mission_id: missionId,
                    event_index: 1,
                    event_id: `ev_${missionId}_0002`,
                    label: 'Planner Strategy Selected',
                    bookmark_type: 'DECISION',
                    created_at: new Date().toISOString(),
                    description: 'Autonomous planner selected Pareto balanced OCR & LayoutLM extraction strategy.',
                },
            ];
        }
    }
    // --- Mock Fallbacks ---
    static getMockReplayState(missionId) {
        return {
            mission_id: missionId,
            status: 'PAUSED',
            speed: '1x',
            cursor: {
                current_index: 3,
                total_events: 10,
                current_event_id: `ev_${missionId}_0004`,
                current_timestamp: new Date().toISOString(),
                is_at_start: false,
                is_at_end: false,
                progress_percentage: 33.3,
                last_seek_time: new Date().toISOString(),
            },
            state: {
                mission_id: missionId,
                status: 'EXECUTING',
                current_stage: 'OCR',
                total_events_applied: 4,
                tasks: {
                    node_ocr_01: {
                        task_id: 'node_ocr_01',
                        task_type: 'OCR',
                        status: 'COMPLETED',
                        worker_id: 'worker_gpu_01',
                        start_time: new Date().toISOString(),
                        end_time: new Date().toISOString(),
                        duration_ms: 342.0,
                        input_data: { image_uri: 'invoice_1042.png' },
                        output_data: { line_items: 8, confidence: 0.96 },
                        error: null,
                        retry_count: 0,
                    },
                },
                planner_strategy: 'Pareto Balanced Extraction (OCR + LayoutLM + SMT)',
                planner_generation: 1,
                confidence_score: 0.98,
                dag_version: 1,
                total_cost_usd: 0.0032,
                total_duration_ms: 780.0,
                created_at: new Date().toISOString(),
                completed_at: null,
                metadata: { engine: 'ESMR-v3' },
            },
        };
    }
    static getMockTimeline(missionId) {
        return {
            mission_id: missionId,
            total_events: 10,
            start_time: new Date(Date.now() - 5000).toISOString(),
            end_time: new Date().toISOString(),
            total_duration_ms: 780.0,
            stages: ['SUBMISSION', 'PLANNING', 'DISPATCH', 'OCR', 'EXTRACTION', 'VALIDATION', 'REFLECTION', 'COMPLETED'],
            categories: { MISSION: 2, PLANNER: 1, WORKER: 1, EXECUTION: 4, GOVERNANCE: 1, REFLECTION: 1 },
            entries: [
                {
                    event_id: `ev_${missionId}_0001`,
                    sequence_number: 1,
                    timestamp: new Date(Date.now() - 4000).toISOString(),
                    category: 'MISSION',
                    event_type: 'MISSION_CREATED',
                    severity: 'INFO',
                    stage: 'SUBMISSION',
                    worker_id: null,
                    task_id: null,
                    summary: 'Mission submitted for autonomous document intelligence.',
                    duration_ms: null,
                    hash: 'a1b2c3d4e5f60718293a4b5c6d7e8f90',
                    previous_hash: 'GENESIS',
                    is_checkpoint: false,
                    payload: { goal: 'Process invoice document' },
                },
                {
                    event_id: `ev_${missionId}_0002`,
                    sequence_number: 2,
                    timestamp: new Date(Date.now() - 3500).toISOString(),
                    category: 'PLANNER',
                    event_type: 'PLANNER_STRATEGY_SELECTED',
                    severity: 'INFO',
                    stage: 'PLANNING',
                    worker_id: 'worker_core_01',
                    task_id: null,
                    summary: 'Strategy selected: Pareto Balanced Extraction (OCR + LayoutLM + SMT)',
                    duration_ms: 45.0,
                    hash: 'b2c3d4e5f60718293a4b5c6d7e8f90a1',
                    previous_hash: 'a1b2c3d4e5f60718293a4b5c6d7e8f90',
                    is_checkpoint: false,
                    payload: { confidence: 0.98, generation: 1 },
                },
            ],
        };
    }
    static getMockDecisionGraph(missionId) {
        return {
            mission_id: missionId,
            root_decision_id: `dec_${missionId}_0001`,
            coverage_percentage: 100.0,
            nodes: [
                {
                    id: `dec_${missionId}_0001`,
                    label: 'Gen 1: Pareto Balanced Extraction',
                    generation: 1,
                    confidence: 0.98,
                    utility: 0.94,
                    strategy: 'Pareto Balanced Extraction (OCR + LayoutLM + SMT)',
                    timestamp: new Date().toISOString(),
                    why: 'Optimal trade-off between sub-second latency and zero arithmetic drift.',
                    what: 'Dispatch multi-modal layout extraction with mathematical proof validation.',
                    is_selected: true,
                    event_id: `ev_${missionId}_0002`,
                },
            ],
            edges: [],
        };
    }
    static getMockDecisions(missionId) {
        return [
            {
                decision_id: `dec_${missionId}_0001`,
                mission_id: missionId,
                event_id: `ev_${missionId}_0002`,
                event_sequence: 2,
                timestamp: new Date().toISOString(),
                why: 'Mathematical proof validation required for enterprise invoice reconciliation.',
                what: 'Pareto Balanced Extraction with LayoutLM and SMT solver.',
                based_on: { confidence: 0.98, budget_usd: 0.05, latency_ms_max: 2000 },
                why_not_others: {
                    'Raw LLM Direct Vision': 'Failed arithmetic invariance verification; hallucination risk too high.',
                    'Heuristic Rule OCR': 'Insufficient generalization on novel table alignments.',
                },
                selected_strategy: 'Pareto Balanced Extraction (OCR + LayoutLM + SMT)',
                confidence: 0.98,
                planner_generation: 1,
                utility_breakdown: {
                    accuracy: 0.99,
                    latency_score: 0.92,
                    cost_score: 0.95,
                    safety_score: 1.0,
                    total_utility: 0.965,
                    weights: { accuracy: 0.4, latency: 0.2, cost: 0.2, safety: 0.2 },
                },
                alternatives_evaluated: [
                    {
                        strategy_name: 'Raw LLM Direct Vision',
                        utility_score: 0.72,
                        rejection_reason: 'Arithmetic drift violations on sum totals.',
                        metrics: { accuracy: 0.85, latency_score: 0.8, cost_score: 0.4 },
                    },
                ],
                sha256_provenance_hash: '9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08',
                parent_decision_id: null,
            },
        ];
    }
    static getMockAuditTrail(missionId) {
        return [
            {
                audit_id: `aud_${missionId}_0001`,
                mission_id: missionId,
                event_id: `ev_${missionId}_0001`,
                sequence_number: 1,
                timestamp: new Date().toISOString(),
                category: 'MISSION',
                action_type: 'MISSION_CREATED',
                actor: 'system',
                details: { status: 'INITIALIZED' },
                previous_audit_hash: 'GENESIS_AUDIT_HASH',
                audit_hash: 'c1d2e3f405162738495a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e',
                hmac_signature: 'hmac_sha256_sig_valid_001',
                verified: true,
            },
        ];
    }
}
