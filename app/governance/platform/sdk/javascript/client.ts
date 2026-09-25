/**
 * Enterprise Governance TypeScript / JavaScript Client.
 */

import {
  EvaluateRequest,
  GovernanceDecision,
  GovernancePolicy,
  GovernanceReport,
  WebhookSubscription,
} from "./models";

export interface ClientConfig {
  apiKey: string;
  baseUrl?: string;
  timeoutMs?: number;
  maxRetries?: number;
}

export class GovernanceClient {
  private apiKey: string;
  private baseUrl: string;
  private timeoutMs: number;
  private maxRetries: number;

  constructor(config: ClientConfig) {
    if (!config.apiKey) {
      throw new Error("API Key is required to initialize GovernanceClient.");
    }
    this.apiKey = config.apiKey;
    this.baseUrl = (config.baseUrl || "https://api.governance.doctask.io").replace(/\/$/, "");
    this.timeoutMs = config.timeoutMs || 10000;
    this.maxRetries = config.maxRetries || 3;
  }

  private async request<T>(method: string, path: string, body?: any): Promise<T> {
    const url = `${this.baseUrl}${path}`;
    const headers = {
      "Authorization": `Bearer ${this.apiKey}`,
      "Content-Type": "application/json",
      "User-Agent": "@doctask/governance-sdk/1.0.0",
    };

    let lastError: Error | null = null;
    for (let attempt = 0; attempt <= this.maxRetries; attempt++) {
      try {
        const response = await fetch(url, {
          method,
          headers,
          body: body ? JSON.stringify(body) : undefined,
          signal: AbortSignal.timeout(this.timeoutMs),
        });

        const json = await response.json();
        if (!response.ok || json.error) {
          throw new Error(json.error?.message || `HTTP ${response.status}: Failed to execute request`);
        }
        return json as T;
      } catch (err: any) {
        lastError = err;
        if (attempt < this.maxRetries) {
          const delay = Math.pow(2, attempt) * 500;
          await new Promise((resolve) => setTimeout(resolve, delay));
          continue;
        }
        throw lastError;
      }
    }
    throw lastError || new Error("Failed request execution");
  }

  /**
   * Evaluate an action against tenant governance rules.
   */
  public async evaluate(request: EvaluateRequest): Promise<GovernanceDecision> {
    return this.request<GovernanceDecision>("POST", "/api/v1/governance/evaluate", request);
  }

  /**
   * Retrieve a policy by ID.
   */
  public async getPolicy(policyId: string): Promise<GovernancePolicy> {
    return this.request<GovernancePolicy>("GET", `/api/v1/governance/policies/${policyId}`);
  }

  /**
   * List active governance policies.
   */
  public async listPolicies(): Promise<GovernancePolicy[]> {
    const res = await this.request<{ items: GovernancePolicy[] }>("GET", "/api/v1/governance/policies");
    return res.items || [];
  }

  /**
   * Retrieve compliance and governance intelligence report.
   */
  public async generateReport(reportType: string = "executive"): Promise<GovernanceReport> {
    return this.request<GovernanceReport>("GET", `/api/v1/governance/analytics?type=${reportType}`);
  }

  /**
   * Register a webhook endpoint.
   */
  public async createWebhook(url: string, events: string[] = ["*"]): Promise<WebhookSubscription> {
    return this.request<WebhookSubscription>("POST", "/api/v1/webhooks", { url, events });
  }
}
