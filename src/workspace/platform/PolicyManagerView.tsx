import React from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';

export const PolicyManagerView: React.FC = () => {
  const policies = [
    {
      id: 'pol-sec-001',
      name: 'Strict PII / PHI Redaction Rule',
      category: 'PRIVACY',
      severity: 'BLOCKING',
      description: 'Blocks unredacted Social Security Numbers, Medical Record Numbers, or Credit Cards from leaving secure enclave.',
      expression: 'phi_redacted == true',
      status: 'ENFORCED',
    },
    {
      id: 'pol-cost-002',
      name: 'Mission Budget Guardrail ($0.05 Max / Doc)',
      category: 'COST',
      severity: 'BLOCKING',
      description: 'Automatically throttles or aborts mission sub-graphs exceeding $0.05 per document page.',
      expression: 'cost_usd <= 0.05',
      status: 'ENFORCED',
    },
    {
      id: 'pol-model-003',
      name: 'Approved Enterprise Foundation Models Only',
      category: 'MODEL_RESTRICTION',
      severity: 'BLOCKING',
      description: 'Ensures only zero-data-retention enterprise tier LLM endpoints (Gemini 2.5) are invoked.',
      expression: "model in ['gemini-2.5-flash', 'gemini-2.5-pro']",
      status: 'ENFORCED',
    },
    {
      id: 'pol-gov-004',
      name: 'Four-Eyes Human Approval for High-Value Wire Transits (> $10k)',
      category: 'COMPLIANCE',
      severity: 'BLOCKING',
      description: 'Requires cryptographic human supervisor signature for invoices exceeding $10,000.',
      expression: 'amount <= 10000 or human_signed == true',
      status: 'ENFORCED',
    },
  ];

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold tracking-tight">Enterprise Policy Manager</h1>
            <Badge variant="success" size="sm">Zero Governance Bypass</Badge>
          </div>
          <p className="text-xs text-muted-foreground mt-1">
            Global governance rules across Security, Compliance, Privacy, Cost Ceilings, and Model Allow-lists enforced before execution.
          </p>
        </div>
        <Badge variant="outline" size="md">
          {policies.length} Active Guardrails
        </Badge>
      </div>

      <div className="space-y-4">
        {policies.map((p) => (
          <Card key={p.id} className="p-5 space-y-3">
            <div className="flex items-start justify-between">
              <div>
                <div className="flex items-center gap-2">
                  <span className="font-bold text-sm text-foreground">{p.name}</span>
                  <Badge variant="intelligence" size="sm">{p.category}</Badge>
                  <Badge variant={p.severity === 'BLOCKING' ? 'error' : 'warning'} size="sm">{p.severity}</Badge>
                </div>
                <div className="font-mono text-xs text-muted-foreground mt-0.5">{p.id}</div>
              </div>
              <Badge variant="success" size="sm">✓ {p.status}</Badge>
            </div>

            <p className="text-xs text-muted-foreground">{p.description}</p>

            <div className="p-2.5 bg-black/80 rounded border border-border/40 font-mono text-xs text-emerald-400">
              Condition: {p.expression}
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};
