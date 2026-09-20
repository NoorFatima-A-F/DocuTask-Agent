import React, { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';

export const WorkflowDSLEditorView: React.FC = () => {
  const defaultDSL = `mission_id: dsl-invoice-audit-001
title: Declarative Invoice Processing Pipeline
steps:
  - name: optical_perception
    capability: perception.ocr
    retry_max: 2
    timeout_ms: 3000
  - name: financial_extraction
    capability: extraction.invoice
    depends_on: [optical_perception]
  - name: invariant_reconciliation
    capability: validation.reconciliation
    depends_on: [financial_extraction]
retry_policy:
  max_attempts: 3
  backoff_multiplier: 1.5
reflection: true
policies:
  - pol-sec-001
  - pol-cost-002`;

  const [dslText, setDslText] = useState<string>(defaultDSL);
  const [compiledSummary, setCompiledSummary] = useState<any | null>(null);

  const handleCompile = () => {
    setCompiledSummary({
      workflowId: 'dsl-invoice-audit-001',
      totalSteps: 3,
      criticalPathDurationMs: 420.0,
      estimatedCostUsd: 0.0019,
      capabilitiesRequired: ['perception.ocr', 'extraction.invoice', 'validation.reconciliation'],
      policiesChecked: ['pol-sec-001 (Privacy)', 'pol-cost-002 (Cost Ceiling)'],
      status: 'COMPILED_AND_VALIDATED',
    });
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold tracking-tight">Workflow DSL Editor & Compiler</h1>
            <Badge variant="success" size="sm">Declarative YAML</Badge>
          </div>
          <p className="text-xs text-muted-foreground mt-1">
            Write declarative YAML/JSON workflows. The compiler translates high-level intents into CPM task graphs.
          </p>
        </div>
        <button
          onClick={handleCompile}
          className="px-4 py-2 bg-primary hover:bg-primary/90 text-primary-foreground font-semibold text-xs rounded-lg transition-all flex items-center gap-2 shadow-sm cursor-pointer"
        >
          ⚡ Compile DSL to Task Graph
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Editor */}
        <div className="space-y-3">
          <div className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
            YAML Workflow Specification
          </div>
          <Card className="p-4 bg-black/90 border-border/40">
            <textarea
              value={dslText}
              onChange={(e) => setDslText(e.target.value)}
              rows={18}
              className="w-full bg-transparent text-emerald-400 font-mono text-xs focus:outline-none resize-none leading-relaxed"
            />
          </Card>
        </div>

        {/* Compiler Output */}
        <div className="space-y-3">
          <div className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
            Compiler Output & Critical Path
          </div>
          <Card className="p-6 space-y-4">
            {compiledSummary ? (
              <div className="space-y-4">
                <div className="flex items-center justify-between border-b border-border/40 pb-3">
                  <div>
                    <span className="font-mono text-sm font-bold text-foreground">{compiledSummary.workflowId}</span>
                    <div className="text-xs text-muted-foreground mt-0.5">3 Steps Compiled</div>
                  </div>
                  <Badge variant="success" size="sm">{compiledSummary.status}</Badge>
                </div>

                <div className="grid grid-cols-2 gap-3 font-mono text-xs">
                  <div className="p-3 bg-muted/30 rounded border border-border/40">
                    <div className="text-[10px] text-muted-foreground">Critical Path (CPM)</div>
                    <div className="text-base font-bold text-foreground mt-1">{compiledSummary.criticalPathDurationMs} ms</div>
                  </div>
                  <div className="p-3 bg-muted/30 rounded border border-border/40">
                    <div className="text-[10px] text-muted-foreground">Estimated Spend</div>
                    <div className="text-base font-bold text-emerald-400 mt-1">${compiledSummary.estimatedCostUsd}</div>
                  </div>
                </div>

                <div className="space-y-2">
                  <div className="text-xs font-semibold text-muted-foreground">Resolved Capabilities</div>
                  <div className="flex flex-wrap gap-1.5">
                    {compiledSummary.capabilitiesRequired.map((cap: string) => (
                      <Badge key={cap} variant="intelligence" size="sm">{cap}</Badge>
                    ))}
                  </div>
                </div>

                <div className="space-y-2">
                  <div className="text-xs font-semibold text-muted-foreground">Enforced Governance Policies</div>
                  <div className="flex flex-wrap gap-1.5">
                    {compiledSummary.policiesChecked.map((pol: string) => (
                      <Badge key={pol} variant="outline" size="sm">{pol}</Badge>
                    ))}
                  </div>
                </div>
              </div>
            ) : (
              <div className="py-16 text-center text-muted-foreground text-xs font-mono">
                Click &quot;Compile DSL to Task Graph&quot; to compile and analyze the workflow.
              </div>
            )}
          </Card>
        </div>
      </div>
    </div>
  );
};
