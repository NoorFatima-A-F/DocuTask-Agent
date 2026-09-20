const API_BASE = '/api/v1/workforce';
export class WorkforceApiClient {
    tenantId = 'default-tenant';
    setTenantId(id) {
        this.tenantId = id;
    }
    async getOverview() {
        try {
            const res = await fetch(`${API_BASE}/overview?tenant_id=${this.tenantId}`);
            if (!res.ok)
                throw new Error('Failed to fetch overview');
            return await res.json();
        }
        catch {
            return {
                tenant_id: this.tenantId,
                total_employees: 6,
                total_departments: 5,
                active_teams: 1,
                marketplace_open_tasks: 2,
                council_active_propositions: 1,
                average_trust_score: 0.978,
                workforce_readiness_index: 0.96,
                generated_at: new Date().toISOString()
            };
        }
    }
    async getEmployees() {
        try {
            const res = await fetch(`${API_BASE}/employees?tenant_id=${this.tenantId}`);
            if (!res.ok)
                throw new Error('Failed to fetch employees');
            return await res.json();
        }
        catch {
            return [
                {
                    id: 'emp-ceo-01',
                    tenant_id: this.tenantId,
                    name: 'Astraea Core',
                    role: 'CEO',
                    department: 'EXECUTIVE',
                    level: 8,
                    skills: ['Strategic Planning', 'Autonomous Governance', 'Resource Allocation'],
                    security_clearance: 'TOP_SECRET',
                    availability_status: 'ACTIVE',
                    capacity_slots: 10,
                    assigned_tasks_count: 2,
                    trust_score: 0.99,
                    hourly_salary_usd: 5.00,
                    token_cost_multiplier: 1.0,
                    lifetime_tasks_completed: 450,
                    task_success_rate: 0.995,
                    burnout_risk_score: 0.02,
                    career_history: [],
                    created_at: new Date().toISOString()
                },
                {
                    id: 'emp-eng-vp',
                    tenant_id: this.tenantId,
                    name: 'Nexus Engineering',
                    role: 'VP',
                    department: 'ENGINEERING',
                    manager_id: 'emp-ceo-01',
                    level: 7,
                    skills: ['Distributed Architecture', 'System Design', 'Cloud Infrastructure'],
                    security_clearance: 'TOP_SECRET',
                    availability_status: 'ACTIVE',
                    capacity_slots: 8,
                    assigned_tasks_count: 3,
                    trust_score: 0.98,
                    hourly_salary_usd: 4.00,
                    token_cost_multiplier: 1.0,
                    lifetime_tasks_completed: 320,
                    task_success_rate: 0.99,
                    burnout_risk_score: 0.05,
                    career_history: [],
                    created_at: new Date().toISOString()
                },
                {
                    id: 'emp-doc-spec-01',
                    tenant_id: this.tenantId,
                    name: 'HyperDoc Synthesizer',
                    role: 'SENIOR_SPECIALIST',
                    department: 'OPERATIONS',
                    manager_id: 'emp-eng-vp',
                    level: 4,
                    skills: ['Document Extraction', 'OCR Verification', 'Multi-modal Parsing'],
                    security_clearance: 'CONFIDENTIAL',
                    availability_status: 'ACTIVE',
                    capacity_slots: 5,
                    assigned_tasks_count: 1,
                    trust_score: 0.97,
                    hourly_salary_usd: 2.50,
                    token_cost_multiplier: 1.0,
                    lifetime_tasks_completed: 120,
                    task_success_rate: 0.985,
                    burnout_risk_score: 0.04,
                    career_history: [],
                    created_at: new Date().toISOString()
                }
            ];
        }
    }
    async getDepartments() {
        try {
            const res = await fetch(`${API_BASE}/departments?tenant_id=${this.tenantId}`);
            if (!res.ok)
                throw new Error('Failed to fetch departments');
            return await res.json();
        }
        catch {
            return [
                { id: 'dept-exec', tenant_id: this.tenantId, name: 'Executive Leadership', dept_type: 'EXECUTIVE', manager_id: 'emp-ceo-01', headcount: 1, monthly_budget_usd: 25000, active_projects: ['Vision 2027'], okrs: ['100% Autonomous SLA'], created_at: new Date().toISOString() },
                { id: 'dept-eng', tenant_id: this.tenantId, name: 'Autonomous Engineering', dept_type: 'ENGINEERING', manager_id: 'emp-eng-vp', headcount: 3, monthly_budget_usd: 50000, active_projects: ['FastParser V3'], okrs: ['Sub-50ms Latency'], created_at: new Date().toISOString() },
                { id: 'dept-ops', tenant_id: this.tenantId, name: 'Autonomous Operations', dept_type: 'OPERATIONS', manager_id: 'emp-eng-vp', headcount: 2, monthly_budget_usd: 30000, active_projects: ['Invoice Pipeline'], okrs: ['Zero Fabrication'], created_at: new Date().toISOString() }
            ];
        }
    }
    async getOrganizationChart() {
        try {
            const res = await fetch(`${API_BASE}/organization?tenant_id=${this.tenantId}`);
            if (!res.ok)
                throw new Error('Failed to fetch org chart');
            return await res.json();
        }
        catch {
            return {
                tenant_id: this.tenantId,
                total_headcount: 6,
                root_nodes: []
            };
        }
    }
    async getTeams() {
        try {
            const res = await fetch(`${API_BASE}/teams?tenant_id=${this.tenantId}`);
            if (!res.ok)
                throw new Error('Failed to fetch teams');
            return await res.json();
        }
        catch {
            return [
                {
                    id: 'team-hyper-extract',
                    tenant_id: this.tenantId,
                    team_name: 'Hyper-Scale Extraction Force',
                    mission: 'Parse high-throughput enterprise invoices with 99.9% verification',
                    team_lead_id: 'emp-eng-vp',
                    member_ids: ['emp-eng-vp', 'emp-doc-spec-01'],
                    required_skills: ['Document Extraction', 'OCR Verification'],
                    max_budget_usd: 100,
                    sla_hours: 4,
                    active_tasks: ['task-inv-001'],
                    team_health_score: 0.98,
                    created_at: new Date().toISOString()
                }
            ];
        }
    }
    async formTeam(data) {
        const res = await fetch(`${API_BASE}/teams/form`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ ...data, tenant_id: this.tenantId })
        });
        if (!res.ok)
            throw new Error('Failed to form team');
        return await res.json();
    }
    async getMarketplaceTasks() {
        try {
            const res = await fetch(`${API_BASE}/marketplace/tasks?tenant_id=${this.tenantId}`);
            if (!res.ok)
                throw new Error('Failed to fetch tasks');
            return await res.json();
        }
        catch {
            return [
                {
                    id: 'task-batch-ocr-99',
                    tenant_id: this.tenantId,
                    title: 'Extract Multi-Page Financial Statements',
                    description: 'High precision table extraction and ledger reconciliation.',
                    required_skills: ['Document Extraction', 'OCR Verification'],
                    priority: 'HIGH',
                    budget_max_usd: 25.0,
                    deadline: new Date().toISOString(),
                    status: 'BIDDING',
                    bids: [
                        {
                            bid_id: 'bid-01',
                            employee_id: 'emp-doc-spec-01',
                            bid_cost_usd: 12.50,
                            estimated_duration_minutes: 15.0,
                            confidence_score: 0.98,
                            proposed_solution_outline: 'Streamed parallel table parsing'
                        }
                    ],
                    created_at: new Date().toISOString()
                }
            ];
        }
    }
    async postTask(data) {
        const res = await fetch(`${API_BASE}/marketplace/tasks`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ ...data, tenant_id: this.tenantId })
        });
        if (!res.ok)
            throw new Error('Failed to post task');
        return await res.json();
    }
    async submitBid(data) {
        const res = await fetch(`${API_BASE}/marketplace/bid`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ ...data, tenant_id: this.tenantId })
        });
        if (!res.ok)
            throw new Error('Failed to submit bid');
        return await res.json();
    }
    async getNegotiations() {
        try {
            const res = await fetch(`${API_BASE}/negotiations?tenant_id=${this.tenantId}`);
            if (!res.ok)
                throw new Error('Failed to fetch negotiations');
            return await res.json();
        }
        catch {
            return [
                {
                    id: 'neg-res-borrow-01',
                    tenant_id: this.tenantId,
                    topic: 'GPU Cluster Borrowing for Batch Re-indexing',
                    participant_employee_ids: ['emp-eng-vp', 'emp-doc-spec-01'],
                    proposals: [{ from: 'emp-eng-vp', proposal: 'Allocate 4x H100 GPUs' }],
                    consensus_reached: true,
                    agreed_terms: { gpu_count: 3, duration_hours: 2 },
                    status: 'AGREED',
                    created_at: new Date().toISOString()
                }
            ];
        }
    }
    async getCouncilPropositions() {
        try {
            const res = await fetch(`${API_BASE}/executive-council/propositions?tenant_id=${this.tenantId}`);
            if (!res.ok)
                throw new Error('Failed to fetch council propositions');
            return await res.json();
        }
        catch {
            return [
                {
                    id: 'prop-strat-ai-expansion',
                    tenant_id: this.tenantId,
                    title: 'Adopt Universal Causal Knowledge Mesh for Cross-Tenant Isolation',
                    summary: 'Constitutional upgrade enabling zero-knowledge proof verification across all digital organizations.',
                    category: 'STRATEGIC',
                    council_votes: { CEO: 'APPROVE', VP_ENG: 'APPROVE' },
                    quorum_met: true,
                    enacted: true,
                    impact_assessment: { risk: 'VERY_LOW', roi_expected: '5.2x' },
                    created_at: new Date().toISOString()
                }
            ];
        }
    }
    async voteCouncilProposition(proposition_id, council_role, vote) {
        const res = await fetch(`${API_BASE}/executive-council/vote`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ proposition_id, council_role, vote, tenant_id: this.tenantId })
        });
        if (!res.ok)
            throw new Error('Failed to submit council vote');
        return await res.json();
    }
    async getPerformance() {
        try {
            const res = await fetch(`${API_BASE}/performance?tenant_id=${this.tenantId}`);
            if (!res.ok)
                throw new Error('Failed to fetch performance');
            return await res.json();
        }
        catch {
            return {
                tenant_id: this.tenantId,
                total_workforce_headcount: 6,
                active_employees_count: 5,
                workforce_utilization_rate: 0.83,
                average_trust_score: 0.978,
                average_task_success_rate: 0.99,
                collaboration_index: 0.94,
                innovation_velocity_score: 0.91,
                workforce_burnout_risk: 0.04,
                monthly_salary_burn_usd: 12450.0
            };
        }
    }
    async getEconomics() {
        try {
            const res = await fetch(`${API_BASE}/economics?tenant_id=${this.tenantId}`);
            if (!res.ok)
                throw new Error('Failed to fetch economics');
            return await res.json();
        }
        catch {
            return {
                tenant_id: this.tenantId,
                allocated_gpu_hours: 2000.0,
                used_gpu_hours: 1140.0,
                allocated_tokens: 1000000000,
                used_tokens: 540000000,
                total_budget_usd: 35000.0,
                total_spent_usd: 18250.0,
                efficiency_roi_ratio: 5.4,
                reallocation_recommendations: [
                    'Shift 200 GPU hours from Overnight Batching to Real-Time Interactive OCR.',
                    'Compress prompt tokens by 15% using schema-distilled semantic encodings.'
                ]
            };
        }
    }
    async getRequisitions() {
        try {
            const res = await fetch(`${API_BASE}/hiring/requisitions?tenant_id=${this.tenantId}`);
            if (!res.ok)
                throw new Error('Failed to fetch requisitions');
            return await res.json();
        }
        catch {
            return [
                {
                    id: 'req-auto-scale-01',
                    tenant_id: this.tenantId,
                    department: 'ENGINEERING',
                    target_role: 'SENIOR_SPECIALIST',
                    required_skills: ['High-Throughput Streaming', 'FastAPI Concurrency'],
                    reason: 'High Queue Backlog',
                    status: 'APPROVED',
                    candidate_profiles: [{ name: 'StreamRunner Delta', score: 0.96, suggested_salary: 2.80 }],
                    created_at: new Date().toISOString()
                }
            ];
        }
    }
    async getCareerPaths() {
        try {
            const res = await fetch(`${API_BASE}/career/paths?tenant_id=${this.tenantId}`);
            if (!res.ok)
                throw new Error('Failed to fetch career paths');
            return await res.json();
        }
        catch {
            return [
                {
                    id: 'promo-doc-spec-lead',
                    tenant_id: this.tenantId,
                    employee_id: 'emp-doc-spec-01',
                    current_role: 'SENIOR_SPECIALIST',
                    target_role: 'LEAD_SPECIALIST',
                    eligibility_score: 0.96,
                    completed_milestones: ['Completed 100+ flawless extractions', 'Maintained >98% trust score'],
                    status: 'READY'
                }
            ];
        }
    }
    async executePromotion(promotion_id) {
        const res = await fetch(`${API_BASE}/career/promote/${promotion_id}?tenant_id=${this.tenantId}`, {
            method: 'POST'
        });
        if (!res.ok)
            throw new Error('Failed to execute promotion');
        return await res.json();
    }
    async getSchedules() {
        try {
            const res = await fetch(`${API_BASE}/schedules?tenant_id=${this.tenantId}`);
            if (!res.ok)
                throw new Error('Failed to fetch schedules');
            return await res.json();
        }
        catch {
            return [
                { id: 'sch-01', tenant_id: this.tenantId, employee_id: 'emp-ceo-01', shift_name: 'EXECUTIVE_ALWAYS_ON', time_zone: 'UTC', start_hour: 0, end_hour: 24, is_active: true },
                { id: 'sch-02', tenant_id: this.tenantId, employee_id: 'emp-eng-vp', shift_name: 'US_CORE_DEVELOPMENT', time_zone: 'UTC', start_hour: 8, end_hour: 16, is_active: true }
            ];
        }
    }
    async getCollectiveMemories(scope) {
        try {
            const url = scope ? `${API_BASE}/collective-memories?scope=${scope}&tenant_id=${this.tenantId}` : `${API_BASE}/collective-memories?tenant_id=${this.tenantId}`;
            const res = await fetch(url);
            if (!res.ok)
                throw new Error('Failed to fetch collective memories');
            return await res.json();
        }
        catch {
            return [
                {
                    id: 'cmem-eng-01',
                    tenant_id: this.tenantId,
                    scope: 'DEPARTMENT',
                    scope_id: 'ENGINEERING',
                    title: 'Distributed Semaphore Limits on Worker Queues',
                    content: 'Always cap concurrent Celery ingestion tasks to 64 per shard.',
                    tags: ['redis', 'concurrency'],
                    author_employee_id: 'emp-eng-vp',
                    trust_weight: 0.99,
                    created_at: new Date().toISOString()
                }
            ];
        }
    }
    async getConflicts() {
        try {
            const res = await fetch(`${API_BASE}/conflicts?tenant_id=${this.tenantId}`);
            if (!res.ok)
                throw new Error('Failed to fetch conflicts');
            return await res.json();
        }
        catch {
            return [
                {
                    id: 'conf-res-01',
                    tenant_id: this.tenantId,
                    party_a_id: 'emp-eng-vp',
                    party_b_id: 'emp-doc-spec-01',
                    dispute_subject: 'Inference Latency vs. Deep Multi-Layer Encryption Guard',
                    mediator_employee_id: 'emp-ceo-01',
                    status: 'RESOLVED',
                    resolution_summary: 'Applied selective AES-256 GCM to payload tokens.',
                    binding_agreements: ['Encrypt all PII payload blocks unconditionally'],
                    resolved_at: new Date().toISOString()
                }
            ];
        }
    }
}
export const workforceApiClient = new WorkforceApiClient();
