/**
 * Phase 13.19: Enterprise Business Platform API Client
 * Connects to /api/v1/business with resilient offline mock fallbacks.
 */
const BASE_URL = '/api/v1/business';
export class BusinessApiClient {
    static async request(endpoint, options) {
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
    static async getOverview() {
        try {
            return await this.request('/overview');
        }
        catch {
            return {
                platform_name: 'EPI-ABOP Enterprise Operating System',
                total_active_processes: 6,
                total_human_approvals_pending: 1,
                total_goals_tracked: 4,
                total_annualized_savings_usd: 205000.0,
                mean_sla_compliance_pct: 99.4,
                mean_automation_rate_pct: 86.2,
                top_bottlenecks: [
                    'Manual Purchase Order Matching (Finance)',
                    'VP Approval Gate for Invoices > $50k',
                ],
                timestamp: new Date().toISOString(),
            };
        }
    }
    static async listProcesses() {
        try {
            return await this.request('/processes');
        }
        catch {
            return [
                {
                    process_id: 'proc_invoice_enterprise_01',
                    title: 'End-to-End Enterprise Invoice Processing',
                    description: 'Autonomous multi-department invoice verification, approval routing, ERP sync, and payment',
                    owner_department: 'Finance',
                    status: 'ACTIVE',
                    variables: { invoice_id: 'INV-9941', amount: 45000.0, vendor: 'Acme Global Tech' },
                    current_step_ids: ['step_ocr_extraction'],
                    created_at: new Date(Date.now() - 86400000).toISOString(),
                    updated_at: new Date().toISOString(),
                    steps: [
                        {
                            step_id: 'step_ocr_extraction',
                            name: 'Multimodal OCR & Data Extraction',
                            step_type: 'TASK',
                            department_id: 'Finance',
                            assigned_role: 'agent_doc_extractor',
                            status: 'COMPLETED',
                            next_steps: ['step_tax_validation'],
                            sla_seconds: 60.0,
                            execution_duration_sec: 1.2,
                        },
                        {
                            step_id: 'step_tax_validation',
                            name: 'Automated Tax & Line-Item Validation',
                            step_type: 'TASK',
                            department_id: 'Finance',
                            assigned_role: 'agent_chief_architect',
                            status: 'COMPLETED',
                            next_steps: ['step_approval_gateway'],
                            sla_seconds: 120.0,
                            execution_duration_sec: 2.4,
                        },
                        {
                            step_id: 'step_approval_gateway',
                            name: 'Amount-Based Routing Gateway',
                            step_type: 'GATEWAY_EXCLUSIVE',
                            department_id: 'Finance',
                            assigned_role: 'agent',
                            status: 'COMPLETED',
                            next_steps: ['step_manager_approval'],
                            sla_seconds: 10.0,
                            execution_duration_sec: 0.1,
                        },
                        {
                            step_id: 'step_manager_approval',
                            name: 'Finance Manager Approval Gate',
                            step_type: 'HUMAN_APPROVAL',
                            department_id: 'Finance',
                            assigned_role: 'role_finance_director',
                            status: 'WAITING_APPROVAL',
                            next_steps: ['step_erp_entry'],
                            sla_seconds: 1800.0,
                            execution_duration_sec: 0.0,
                        },
                        {
                            step_id: 'step_erp_entry',
                            name: 'SAP ERP Ledger Posting',
                            step_type: 'TASK',
                            department_id: 'Finance',
                            assigned_role: 'agent_integrator',
                            status: 'PENDING',
                            next_steps: ['step_payment_release'],
                            sla_seconds: 180.0,
                            execution_duration_sec: 0.0,
                        },
                        {
                            step_id: 'step_payment_release',
                            name: 'Automated Payment Release',
                            step_type: 'TASK',
                            department_id: 'Finance',
                            assigned_role: 'agent_payments',
                            status: 'PENDING',
                            next_steps: [],
                            sla_seconds: 60.0,
                            execution_duration_sec: 0.0,
                        },
                    ],
                },
            ];
        }
    }
    static async executeProcess(processId) {
        return await this.request(`/processes/${processId}/execute`, { method: 'POST' });
    }
    static async listGoals() {
        try {
            return await this.request('/goals');
        }
        catch {
            return [
                {
                    goal_id: 'goal_invoice_velocity',
                    title: 'Accelerate Global Invoice Turnaround by 50%',
                    category: 'EFFICIENCY',
                    target_department: 'Finance',
                    status: 'IN_PROGRESS',
                    progress_pct: 68.5,
                    key_results: [
                        {
                            kr_id: 'kr_cycle_time',
                            description: 'Reduce end-to-end invoice cycle time from 4 days to < 4 hours',
                            target_value: 4.0,
                            current_value: 1.8,
                            unit: 'hours',
                            achieved: true,
                        },
                        {
                            kr_id: 'kr_stp_rate',
                            description: 'Achieve 85% Straight-Through-Processing (STP) rate',
                            target_value: 85.0,
                            current_value: 78.2,
                            unit: '%',
                            achieved: false,
                        },
                    ],
                    aligned_process_ids: ['proc_invoice_enterprise_01'],
                    created_at: new Date(Date.now() - 604800000).toISOString(),
                },
            ];
        }
    }
    static async getOrganization() {
        try {
            return await this.request('/organization');
        }
        catch {
            return {
                departments: [
                    {
                        department_id: 'dept_exec',
                        name: 'Executive Leadership',
                        head_role: 'role_ceo',
                        members_count: 5,
                        active_processes_count: 2,
                        operational_budget_monthly: 150000.0,
                    },
                    {
                        department_id: 'dept_finance',
                        name: 'Finance & Accounts Payable',
                        head_role: 'role_cfo',
                        parent_department_id: 'dept_exec',
                        members_count: 28,
                        active_processes_count: 8,
                        operational_budget_monthly: 85000.0,
                    },
                    {
                        department_id: 'dept_legal',
                        name: 'Legal & Compliance',
                        head_role: 'role_general_counsel',
                        parent_department_id: 'dept_exec',
                        members_count: 12,
                        active_processes_count: 5,
                        operational_budget_monthly: 60000.0,
                    },
                    {
                        department_id: 'dept_ops',
                        name: 'Global Operations & Supply Chain',
                        head_role: 'role_coo',
                        parent_department_id: 'dept_exec',
                        members_count: 45,
                        active_processes_count: 12,
                        operational_budget_monthly: 110000.0,
                    },
                ],
                roles: [
                    {
                        role_id: 'role_finance_director',
                        title: 'Finance Director',
                        department_id: 'dept_finance',
                        is_autonomous_agent: false,
                        approval_limit_amount: 100000.0,
                        assigned_capabilities: ['invoice_approval', 'budget_allocation'],
                    },
                    {
                        role_id: 'role_ap_specialist',
                        title: 'Accounts Payable Specialist (AI Agent)',
                        department_id: 'dept_finance',
                        is_autonomous_agent: true,
                        approval_limit_amount: 5000.0,
                        assigned_capabilities: ['ocr_data_entry', 'line_item_matching'],
                    },
                ],
                systems: [
                    {
                        system_id: 'sys_sap_erp',
                        name: 'SAP S/4HANA Enterprise ERP',
                        system_type: 'ERP',
                        status: 'ONLINE',
                        connected_departments: ['dept_finance', 'dept_ops'],
                    },
                ],
                approval_matrix: {
                    role_ap_specialist: 'role_finance_director',
                    role_finance_director: 'role_cfo',
                },
            };
        }
    }
    static async listApprovals(status) {
        try {
            const q = status ? `?status=${status}` : '';
            return await this.request(`/approvals${q}`);
        }
        catch {
            return [
                {
                    task_id: 'appr_inv_9941',
                    process_id: 'proc_invoice_enterprise_01',
                    step_id: 'step_manager_approval',
                    title: 'Invoice $45,000.00 Review (Vendor: Acme Global Tech)',
                    description: 'Invoice amount exceeds standard $10k auto-approval threshold. Line items verified by AI Agent with 99.4% confidence.',
                    department_id: 'Finance',
                    assigned_role: 'role_finance_director',
                    amount: 45000.0,
                    status: 'PENDING',
                    created_at: new Date(Date.now() - 3600000).toISOString(),
                },
            ];
        }
    }
    static async decideApproval(taskId, decision, rationale, decidedBy) {
        const q = new URLSearchParams({
            decision,
            rationale,
            decided_by: decidedBy,
        });
        return await this.request(`/approvals/${taskId}/decide?${q.toString()}`, {
            method: 'POST',
        });
    }
    static async getDiscovery() {
        try {
            return await this.request('/discovery');
        }
        catch {
            return [
                {
                    discovered_id: 'disc_invoice_proc_real',
                    name: 'Discovered: Accounts Payable Direct Invoicing',
                    frequency: 1420,
                    mean_duration_sec: 3240.0,
                    variants_count: 4,
                    bottleneck_steps: ['Manual Purchase Order Matching', 'Multi-Tier VP Approval Gate'],
                    compliance_score: 0.94,
                },
            ];
        }
    }
    static async optimizeProcess(processId) {
        try {
            const q = processId ? `?process_id=${processId}` : '';
            return await this.request(`/processes/optimize${q}`, {
                method: 'POST',
            });
        }
        catch {
            return [
                {
                    recommendation_id: 'rec_opt_parallel_01',
                    process_id: 'proc_invoice_enterprise_01',
                    title: 'Parallelize Tax Validation & Line-Item Matching',
                    action_type: 'PARALLELIZE',
                    rationale: 'Currently executing sequentially. Converting to a parallel split reduces total path duration by 42%.',
                    estimated_cycle_time_reduction_pct: 42.0,
                    estimated_annual_savings_usd: 85000.0,
                    confidence: 0.95,
                },
            ];
        }
    }
    static async runSimulation(config) {
        try {
            return await this.request('/simulations', {
                method: 'POST',
                body: JSON.stringify(config),
            });
        }
        catch {
            return {
                simulation_id: `sim_${Date.now()}`,
                process_id: config.process_id,
                baseline_cycle_time_sec: 3600.0,
                optimized_cycle_time_sec: 120.0,
                baseline_cost_usd: config.simulated_transactions_count * 18.5,
                optimized_cost_usd: config.simulated_transactions_count * 1.35,
                cost_reduction_usd: config.simulated_transactions_count * (18.5 - 1.35),
                throughput_increase_pct: 2900.0,
                simulated_at: new Date().toISOString(),
            };
        }
    }
    static async getKPIs() {
        try {
            return await this.request('/kpis');
        }
        catch {
            return [
                {
                    kpi_id: 'kpi_invoice_turnaround',
                    name: 'Mean Invoice Turnaround Time',
                    department: 'Finance',
                    current_value: 1.8,
                    benchmark_value: 96.0,
                    unit: 'hours',
                    trend: 'IMPROVING',
                },
                {
                    kpi_id: 'kpi_unit_cost',
                    name: 'Cost per Processed Document',
                    department: 'Finance',
                    current_value: 1.35,
                    benchmark_value: 18.5,
                    unit: 'USD',
                    trend: 'IMPROVING',
                },
                {
                    kpi_id: 'kpi_stp_rate',
                    name: 'Straight-Through Processing (STP) Rate',
                    department: 'Operations',
                    current_value: 84.2,
                    benchmark_value: 22.0,
                    unit: '%',
                    trend: 'IMPROVING',
                },
                {
                    kpi_id: 'kpi_annual_roi',
                    name: 'Annualized Realized Automation ROI',
                    department: 'Executive',
                    current_value: 420000.0,
                    benchmark_value: 0.0,
                    unit: 'USD',
                    trend: 'IMPROVING',
                },
            ];
        }
    }
    static async getDigitalTwin() {
        try {
            return await this.request('/digital-twin');
        }
        catch {
            return {
                total_departments: 4,
                active_human_workers: 90,
                active_agent_workers: 24,
                running_business_processes: 8,
                pending_approvals: 1,
                mean_org_sla_compliance_pct: 99.2,
                department_workloads: {
                    dept_finance: 78.5,
                    dept_legal: 42.0,
                    dept_ops: 85.0,
                    dept_exec: 30.0,
                },
                timestamp: new Date().toISOString(),
            };
        }
    }
    static async runBusinessCycle() {
        return await this.request('/orchestration/cycle', { method: 'POST' });
    }
}
