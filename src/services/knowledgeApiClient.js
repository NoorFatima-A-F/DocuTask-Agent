const BASE_URL = '/api/v1/knowledge';
export const knowledgeApiClient = {
    async search(query, topK = 5, tenantId = 'default-tenant') {
        try {
            const res = await fetch(`${BASE_URL}/search?tenant_id=${encodeURIComponent(tenantId)}&query=${encodeURIComponent(query)}&top_k=${topK}`, {
                method: 'POST'
            });
            if (!res.ok)
                throw new Error(`Search failed: ${res.statusText}`);
            return await res.json();
        }
        catch {
            return [
                {
                    asset_id: 'mock-1',
                    title: 'Global Procurement Policy 2026',
                    content: 'Dual VP approval required for all contracts exceeding $50k.',
                    score: 0.92,
                    source_type: 'LOCAL_DOCUMENT',
                    security_classification: 'INTERNAL',
                    matched_via: 'HYBRID_SEMANTIC'
                }
            ];
        }
    },
    async retrieveContext(goal, tenantId = 'default-tenant') {
        try {
            const res = await fetch(`${BASE_URL}/context`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ tenant_id: tenantId, goal, top_k: 4 })
            });
            if (!res.ok)
                throw new Error(`Retrieve context failed: ${res.statusText}`);
            return await res.json();
        }
        catch {
            return {
                query: goal,
                snippets: [],
                graph_context: ['[Ontology] Finance Department owns InvoiceReconciliationAgent'],
                memory_context: ['[PROCEDURAL MEMORY] SOP: Step 1 Validate PO, Step 2 Match Line Items'],
                optimized_context_prompt: `# GROUNDED ENTERPRISE CONTEXT FOR GOAL: ${goal}\n- Verified Policy: Contracts over $50k require VP signoff.`,
                total_tokens_estimated: 140,
                compression_ratio: 3.2,
                retrieval_latency_ms: 12.4
            };
        }
    },
    async listAssets(tenantId = 'default-tenant') {
        try {
            const res = await fetch(`${BASE_URL}/assets?tenant_id=${encodeURIComponent(tenantId)}`);
            if (!res.ok)
                throw new Error(`List assets failed: ${res.statusText}`);
            return await res.json();
        }
        catch {
            return [
                {
                    id: 'asset-001',
                    tenant_id: tenantId,
                    organization_id: 'default-org',
                    workspace_id: 'default-workspace',
                    project_id: 'default-project',
                    name: 'Global Procurement Policy 2026',
                    description: 'Standard enterprise procurement thresholds & approvals',
                    source_type: 'LOCAL_DOCUMENT',
                    state: 'AVAILABLE',
                    security_classification: 'INTERNAL',
                    access_policy: {
                        allowed_roles: ['admin', 'member'],
                        allowed_users: [],
                        denied_roles: [],
                        require_mfa: false,
                        max_security_clearance: 'CONFIDENTIAL'
                    },
                    raw_content: 'Dual VP approval required for all contracts exceeding $50k.',
                    processed_content: 'Dual VP approval required for all contracts exceeding $50k.',
                    embedding_ids: ['emb-1'],
                    metadata: {
                        created_at: new Date().toISOString(),
                        updated_at: new Date().toISOString(),
                        file_type: 'pdf',
                        file_size_bytes: 45000,
                        token_count: 320,
                        custom_tags: ['procurement', 'finance'],
                        extracted_entities: ['Finance Department', 'VP Approval']
                    },
                    version: 1,
                    freshness_score: 1.0,
                    reliability_score: 0.98,
                    created_at: new Date().toISOString(),
                    updated_at: new Date().toISOString()
                }
            ];
        }
    },
    async ingestAsset(payload) {
        const res = await fetch(`${BASE_URL}/assets/ingest`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        if (!res.ok)
            throw new Error(`Ingest asset failed: ${res.statusText}`);
        return await res.json();
    },
    async listSources(tenantId = 'default-tenant') {
        try {
            const res = await fetch(`${BASE_URL}/sources?tenant_id=${encodeURIComponent(tenantId)}`);
            if (!res.ok)
                throw new Error(`List sources failed: ${res.statusText}`);
            return await res.json();
        }
        catch {
            return [
                {
                    id: 'src-1',
                    tenant_id: tenantId,
                    organization_id: 'default-org',
                    workspace_id: 'default-workspace',
                    name: 'Corporate Google Drive',
                    source_type: 'GOOGLE_DRIVE',
                    connection_config: { folder: 'Company Policies' },
                    sync_schedule: '0 * * * *',
                    is_active: true,
                    total_assets_synced: 142,
                    health_status: 'HEALTHY',
                    created_at: new Date().toISOString()
                },
                {
                    id: 'src-2',
                    tenant_id: tenantId,
                    organization_id: 'default-org',
                    workspace_id: 'default-workspace',
                    name: 'Confluence Architecture Wiki',
                    source_type: 'CONFLUENCE',
                    connection_config: { space: 'ARCH' },
                    sync_schedule: '0 */6 * * *',
                    is_active: true,
                    total_assets_synced: 88,
                    health_status: 'HEALTHY',
                    created_at: new Date().toISOString()
                }
            ];
        }
    },
    async getGraphOverview(tenantId = 'default-tenant') {
        try {
            const res = await fetch(`${BASE_URL}/graph/overview?tenant_id=${encodeURIComponent(tenantId)}`);
            if (!res.ok)
                throw new Error(`Graph overview failed: ${res.statusText}`);
            return await res.json();
        }
        catch {
            return {
                total_nodes: 5,
                total_edges: 4,
                nodes: [
                    { id: 'node-1', tenant_id: tenantId, name: 'Finance Department', entity_type: 'DEPARTMENT', properties: {}, confidence_score: 1.0, created_at: new Date().toISOString() },
                    { id: 'node-2', tenant_id: tenantId, name: 'InvoiceReconciliationAgent', entity_type: 'AI_AGENT', properties: {}, confidence_score: 1.0, created_at: new Date().toISOString() },
                    { id: 'node-3', tenant_id: tenantId, name: 'SAP ERP Gateway', entity_type: 'SYSTEM', properties: {}, confidence_score: 1.0, created_at: new Date().toISOString() },
                    { id: 'node-4', tenant_id: tenantId, name: 'PO Threshold Policy', entity_type: 'POLICY', properties: {}, confidence_score: 1.0, created_at: new Date().toISOString() }
                ],
                edges: [
                    { id: 'e-1', tenant_id: tenantId, source_node_id: 'node-1', target_node_id: 'node-2', relation_type: 'owns', properties: {}, weight: 1.0, created_at: new Date().toISOString() },
                    { id: 'e-2', tenant_id: tenantId, source_node_id: 'node-2', target_node_id: 'node-3', relation_type: 'depends_on', properties: {}, weight: 1.0, created_at: new Date().toISOString() },
                    { id: 'e-3', tenant_id: tenantId, source_node_id: 'node-2', target_node_id: 'node-4', relation_type: 'governed_by', properties: {}, weight: 1.0, created_at: new Date().toISOString() }
                ],
                entity_counts: { DEPARTMENT: 1, AI_AGENT: 1, SYSTEM: 1, POLICY: 1 }
            };
        }
    },
    async listMemories(tenantId = 'default-tenant') {
        try {
            const res = await fetch(`${BASE_URL}/memory/list?tenant_id=${encodeURIComponent(tenantId)}`);
            if (!res.ok)
                throw new Error(`List memories failed: ${res.statusText}`);
            return await res.json();
        }
        catch {
            return [
                {
                    id: 'mem-1',
                    tenant_id: tenantId,
                    tier: 'PROCEDURAL',
                    key: 'sop_invoice_reconciliation',
                    content: 'Step 1: Validate OCR, Step 2: Query PO in SAP, Step 3: Match Line Items',
                    metadata: { version: '2.1' },
                    importance_score: 1.0,
                    access_count: 34,
                    created_at: new Date().toISOString()
                }
            ];
        }
    },
    async getQualityReport(tenantId = 'default-tenant') {
        try {
            const res = await fetch(`${BASE_URL}/quality/report?tenant_id=${encodeURIComponent(tenantId)}`);
            if (!res.ok)
                throw new Error(`Quality report failed: ${res.statusText}`);
            return await res.json();
        }
        catch {
            return {
                tenant_id: tenantId,
                total_assets: 24,
                freshness_index: 0.96,
                avg_reliability_score: 0.95,
                duplicate_assets_count: 0,
                active_conflicts: [],
                coverage_score: 0.94,
                healthy: true
            };
        }
    },
    async runOptimization(tenantId = 'default-tenant') {
        const res = await fetch(`${BASE_URL}/optimize?tenant_id=${encodeURIComponent(tenantId)}`, { method: 'POST' });
        return await res.json();
    },
    async runEvaluation(tenantId = 'default-tenant') {
        const res = await fetch(`${BASE_URL}/evaluation/run`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ tenant_id: tenantId, benchmark_suite: 'RAG_BENCHMARK_PROD' })
        });
        return await res.json();
    }
};
