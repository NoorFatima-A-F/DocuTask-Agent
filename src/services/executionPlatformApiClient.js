/**
 * Phase 13.15: Execution Platform API Client.
 */
const BASE_URL = '/api/v1/execution';
async function fetchJson(url, options) {
    const response = await fetch(url, {
        headers: {
            'Content-Type': 'application/json',
            ...options?.headers,
        },
        ...options,
    });
    if (!response.ok) {
        const errorBody = await response.json().catch(() => ({ detail: response.statusText }));
        throw new Error(errorBody.detail || `Request failed with status ${response.status}`);
    }
    return response.json();
}
export const executionPlatformApiClient = {
    // Overview
    async getOverview() {
        return fetchJson(`${BASE_URL}/overview`);
    },
    // Tools
    async listTools(params) {
        const query = new URLSearchParams();
        if (params?.category)
            query.append('category', params.category);
        if (params?.tool_type)
            query.append('tool_type', params.tool_type);
        if (params?.risk_level)
            query.append('risk_level', params.risk_level);
        if (params?.search)
            query.append('search', params.search);
        return fetchJson(`${BASE_URL}/tools?${query.toString()}`);
    },
    async registerTool(payload) {
        return fetchJson(`${BASE_URL}/tools`, {
            method: 'POST',
            body: JSON.stringify(payload),
        });
    },
    async getTool(toolId) {
        return fetchJson(`${BASE_URL}/tools/${toolId}`);
    },
    // Connectors
    async listConnectors(params) {
        const query = new URLSearchParams();
        if (params?.category)
            query.append('category', params.category);
        if (params?.status)
            query.append('status', params.status);
        return fetchJson(`${BASE_URL}/connectors?${query.toString()}`);
    },
    async createConnector(payload) {
        return fetchJson(`${BASE_URL}/connectors`, {
            method: 'POST',
            body: JSON.stringify(payload),
        });
    },
    async testConnector(connectorId) {
        return fetchJson(`${BASE_URL}/connectors/${connectorId}/test`, {
            method: 'POST',
        });
    },
    // Browser
    async listBrowserSessions() {
        return fetchJson(`${BASE_URL}/browser/sessions`);
    },
    async createBrowserSession() {
        return fetchJson(`${BASE_URL}/browser/sessions`, {
            method: 'POST',
        });
    },
    async executeBrowserAction(sessionId, payload) {
        return fetchJson(`${BASE_URL}/browser/sessions/${sessionId}/actions`, {
            method: 'POST',
            body: JSON.stringify(payload),
        });
    },
    // Workflows
    async listWorkflows() {
        return fetchJson(`${BASE_URL}/workflows`);
    },
    async getWorkflow(workflowId) {
        return fetchJson(`${BASE_URL}/workflows/${workflowId}`);
    },
    // Planner
    async planMission(payload) {
        return fetchJson(`${BASE_URL}/planner/plan`, {
            method: 'POST',
            body: JSON.stringify(payload),
        });
    },
    async listPlans() {
        return fetchJson(`${BASE_URL}/planner/plans`);
    },
    // Credentials
    async listCredentials() {
        return fetchJson(`${BASE_URL}/credentials`);
    },
    async addCredential(payload) {
        return fetchJson(`${BASE_URL}/credentials`, {
            method: 'POST',
            body: JSON.stringify(payload),
        });
    },
    // Policy & Governance
    async listPolicyRules() {
        return fetchJson(`${BASE_URL}/policies/rules`);
    },
    async listApprovals(status) {
        const query = status ? `?status=${status}` : '';
        return fetchJson(`${BASE_URL}/policies/approvals${query}`);
    },
    async resolveApproval(approvalId, approved, approver = 'executive_lead') {
        return fetchJson(`${BASE_URL}/policies/approvals/${approvalId}/resolve`, {
            method: 'POST',
            body: JSON.stringify({ approved, approver }),
        });
    },
    // Simulation
    async simulateWorkflow(workflowId) {
        return fetchJson(`${BASE_URL}/simulation/simulate`, {
            method: 'POST',
            body: JSON.stringify({ workflow_id: workflowId }),
        });
    },
    // Missions & Execution
    async executeGoal(payload) {
        return fetchJson(`${BASE_URL}/missions/execute-goal`, {
            method: 'POST',
            body: JSON.stringify(payload),
        });
    },
    async listMissions(status) {
        const query = status ? `?status=${status}` : '';
        return fetchJson(`${BASE_URL}/missions${query}`);
    },
    async getMission(missionId) {
        return fetchJson(`${BASE_URL}/missions/${missionId}`);
    },
    // Verifications & Rollbacks
    async listVerifications(missionId) {
        const query = missionId ? `?mission_id=${missionId}` : '';
        return fetchJson(`${BASE_URL}/verifications${query}`);
    },
    async listRollbacks(missionId) {
        const query = missionId ? `?mission_id=${missionId}` : '';
        return fetchJson(`${BASE_URL}/rollbacks${query}`);
    },
    // Monitoring & Audit
    async getTelemetry() {
        return fetchJson(`${BASE_URL}/monitoring/telemetry`);
    },
    async listAlerts(resolved) {
        const query = resolved !== undefined ? `?resolved=${resolved}` : '';
        return fetchJson(`${BASE_URL}/monitoring/alerts${query}`);
    },
    async resolveAlert(alertId) {
        return fetchJson(`${BASE_URL}/monitoring/alerts/${alertId}/resolve`, {
            method: 'POST',
        });
    },
    async listAuditEntries(params) {
        const query = new URLSearchParams();
        if (params?.mission_id)
            query.append('mission_id', params.mission_id);
        if (params?.limit)
            query.append('limit', params.limit.toString());
        return fetchJson(`${BASE_URL}/audit/entries?${query.toString()}`);
    },
    async verifyAuditLedger() {
        return fetchJson(`${BASE_URL}/audit/verify`);
    },
};
