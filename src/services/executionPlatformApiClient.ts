/**
 * Phase 13.15: Execution Platform API Client.
 */

import {
  ApprovalRequest,
  AuditEntry,
  BrowserAction,
  BrowserSession,
  ConnectorConfig,
  CredentialRecord,
  ExecutionPlan,
  ExecutionPlatformOverview,
  MissionExecution,
  PolicyRule,
  RollbackSession,
  SimulationReport,
  SystemTelemetrySnapshot,
  ToolDefinition,
  WorkflowDefinition,
  AnomalyAlert,
  VerificationCertificate,
} from '../types/executionPlatform';

const BASE_URL = '/api/v1/execution';

async function fetchJson<T>(url: string, options?: RequestInit): Promise<T> {
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
  async getOverview(): Promise<ExecutionPlatformOverview> {
    return fetchJson<ExecutionPlatformOverview>(`${BASE_URL}/overview`);
  },

  // Tools
  async listTools(params?: { category?: string; tool_type?: string; risk_level?: string; search?: string }): Promise<{ tools: ToolDefinition[]; total: number }> {
    const query = new URLSearchParams();
    if (params?.category) query.append('category', params.category);
    if (params?.tool_type) query.append('tool_type', params.tool_type);
    if (params?.risk_level) query.append('risk_level', params.risk_level);
    if (params?.search) query.append('search', params.search);
    return fetchJson<{ tools: ToolDefinition[]; total: number }>(`${BASE_URL}/tools?${query.toString()}`);
  },

  async registerTool(payload: Partial<ToolDefinition>): Promise<{ success: boolean; tool: ToolDefinition }> {
    return fetchJson<{ success: boolean; tool: ToolDefinition }>(`${BASE_URL}/tools`, {
      method: 'POST',
      body: JSON.stringify(payload),
    });
  },

  async getTool(toolId: string): Promise<{ tool: ToolDefinition }> {
    return fetchJson<{ tool: ToolDefinition }>(`${BASE_URL}/tools/${toolId}`);
  },

  // Connectors
  async listConnectors(params?: { category?: string; status?: string }): Promise<{ connectors: ConnectorConfig[]; total: number }> {
    const query = new URLSearchParams();
    if (params?.category) query.append('category', params.category);
    if (params?.status) query.append('status', params.status);
    return fetchJson<{ connectors: ConnectorConfig[]; total: number }>(`${BASE_URL}/connectors?${query.toString()}`);
  },

  async createConnector(payload: Partial<ConnectorConfig>): Promise<{ success: boolean; connector: ConnectorConfig }> {
    return fetchJson<{ success: boolean; connector: ConnectorConfig }>(`${BASE_URL}/connectors`, {
      method: 'POST',
      body: JSON.stringify(payload),
    });
  },

  async testConnector(connectorId: string): Promise<{ success: boolean; status: string; latency_ms: number }> {
    return fetchJson<{ success: boolean; status: string; latency_ms: number }>(`${BASE_URL}/connectors/${connectorId}/test`, {
      method: 'POST',
    });
  },

  // Browser
  async listBrowserSessions(): Promise<{ sessions: BrowserSession[]; total: number }> {
    return fetchJson<{ sessions: BrowserSession[]; total: number }>(`${BASE_URL}/browser/sessions`);
  },

  async createBrowserSession(): Promise<{ session: BrowserSession }> {
    return fetchJson<{ session: BrowserSession }>(`${BASE_URL}/browser/sessions`, {
      method: 'POST',
    });
  },

  async executeBrowserAction(sessionId: string, payload: { action_type: string; selector?: string; value?: string }): Promise<{ success: boolean; action: BrowserAction; current_url: string; page_title: string }> {
    return fetchJson<{ success: boolean; action: BrowserAction; current_url: string; page_title: string }>(`${BASE_URL}/browser/sessions/${sessionId}/actions`, {
      method: 'POST',
      body: JSON.stringify(payload),
    });
  },

  // Workflows
  async listWorkflows(): Promise<{ workflows: WorkflowDefinition[]; total: number }> {
    return fetchJson<{ workflows: WorkflowDefinition[]; total: number }>(`${BASE_URL}/workflows`);
  },

  async getWorkflow(workflowId: string): Promise<{ workflow: WorkflowDefinition; tiers: string[][] }> {
    return fetchJson<{ workflow: WorkflowDefinition; tiers: string[][] }>(`${BASE_URL}/workflows/${workflowId}`);
  },

  // Planner
  async planMission(payload: { mission_goal: string; target_tools?: string[] }): Promise<{ workflow: WorkflowDefinition; plan: ExecutionPlan }> {
    return fetchJson<{ workflow: WorkflowDefinition; plan: ExecutionPlan }>(`${BASE_URL}/planner/plan`, {
      method: 'POST',
      body: JSON.stringify(payload),
    });
  },

  async listPlans(): Promise<{ plans: ExecutionPlan[]; total: number }> {
    return fetchJson<{ plans: ExecutionPlan[]; total: number }>(`${BASE_URL}/planner/plans`);
  },

  // Credentials
  async listCredentials(): Promise<{ credentials: CredentialRecord[]; total: number }> {
    return fetchJson<{ credentials: CredentialRecord[]; total: number }>(`${BASE_URL}/credentials`);
  },

  async addCredential(payload: { name: string; cred_type: string; target_system: string; raw_secret: string; scopes?: string[] }): Promise<{ success: boolean; credential: CredentialRecord }> {
    return fetchJson<{ success: boolean; credential: CredentialRecord }>(`${BASE_URL}/credentials`, {
      method: 'POST',
      body: JSON.stringify(payload),
    });
  },

  // Policy & Governance
  async listPolicyRules(): Promise<{ rules: PolicyRule[]; total: number }> {
    return fetchJson<{ rules: PolicyRule[]; total: number }>(`${BASE_URL}/policies/rules`);
  },

  async listApprovals(status?: string): Promise<{ approvals: ApprovalRequest[]; total: number }> {
    const query = status ? `?status=${status}` : '';
    return fetchJson<{ approvals: ApprovalRequest[]; total: number }>(`${BASE_URL}/policies/approvals${query}`);
  },

  async resolveApproval(approvalId: string, approved: boolean, approver = 'executive_lead'): Promise<{ success: boolean; approval: ApprovalRequest }> {
    return fetchJson<{ success: boolean; approval: ApprovalRequest }>(`${BASE_URL}/policies/approvals/${approvalId}/resolve`, {
      method: 'POST',
      body: JSON.stringify({ approved, approver }),
    });
  },

  // Simulation
  async simulateWorkflow(workflowId: string): Promise<{ simulation: SimulationReport }> {
    return fetchJson<{ simulation: SimulationReport }>(`${BASE_URL}/simulation/simulate`, {
      method: 'POST',
      body: JSON.stringify({ workflow_id: workflowId }),
    });
  },

  // Missions & Execution
  async executeGoal(payload: { goal: string; dry_run?: boolean; initiated_by?: string }): Promise<{
    mission_id: string;
    goal: string;
    status: string;
    plan_id: string;
    simulation_id: string;
    critical_path_steps: string[];
    total_execution_time_ms: number;
    steps_executed: number;
    audit_trail_valid: boolean;
    mission: MissionExecution;
  }> {
    return fetchJson<{
      mission_id: string;
      goal: string;
      status: string;
      plan_id: string;
      simulation_id: string;
      critical_path_steps: string[];
      total_execution_time_ms: number;
      steps_executed: number;
      audit_trail_valid: boolean;
      mission: MissionExecution;
    }>(`${BASE_URL}/missions/execute-goal`, {
      method: 'POST',
      body: JSON.stringify(payload),
    });
  },

  async listMissions(status?: string): Promise<{ missions: MissionExecution[]; total: number }> {
    const query = status ? `?status=${status}` : '';
    return fetchJson<{ missions: MissionExecution[]; total: number }>(`${BASE_URL}/missions${query}`);
  },

  async getMission(missionId: string): Promise<{ mission: MissionExecution }> {
    return fetchJson<{ mission: MissionExecution }>(`${BASE_URL}/missions/${missionId}`);
  },

  // Verifications & Rollbacks
  async listVerifications(missionId?: string): Promise<{ certificates: VerificationCertificate[]; total: number }> {
    const query = missionId ? `?mission_id=${missionId}` : '';
    return fetchJson<{ certificates: VerificationCertificate[]; total: number }>(`${BASE_URL}/verifications${query}`);
  },

  async listRollbacks(missionId?: string): Promise<{ rollbacks: RollbackSession[]; total: number }> {
    const query = missionId ? `?mission_id=${missionId}` : '';
    return fetchJson<{ rollbacks: RollbackSession[]; total: number }>(`${BASE_URL}/rollbacks${query}`);
  },

  // Monitoring & Audit
  async getTelemetry(): Promise<{ telemetry: SystemTelemetrySnapshot }> {
    return fetchJson<{ telemetry: SystemTelemetrySnapshot }>(`${BASE_URL}/monitoring/telemetry`);
  },

  async listAlerts(resolved?: boolean): Promise<{ alerts: AnomalyAlert[]; total: number }> {
    const query = resolved !== undefined ? `?resolved=${resolved}` : '';
    return fetchJson<{ alerts: AnomalyAlert[]; total: number }>(`${BASE_URL}/monitoring/alerts${query}`);
  },

  async resolveAlert(alertId: string): Promise<{ success: boolean; alert_id: string }> {
    return fetchJson<{ success: boolean; alert_id: string }>(`${BASE_URL}/monitoring/alerts/${alertId}/resolve`, {
      method: 'POST',
    });
  },

  async listAuditEntries(params?: { mission_id?: string; limit?: number }): Promise<{ entries: AuditEntry[]; total: number }> {
    const query = new URLSearchParams();
    if (params?.mission_id) query.append('mission_id', params.mission_id);
    if (params?.limit) query.append('limit', params.limit.toString());
    return fetchJson<{ entries: AuditEntry[]; total: number }>(`${BASE_URL}/audit/entries?${query.toString()}`);
  },

  async verifyAuditLedger(): Promise<{ ledger_valid: boolean; error?: string }> {
    return fetchJson<{ ledger_valid: boolean; error?: string }>(`${BASE_URL}/audit/verify`);
  },
};
