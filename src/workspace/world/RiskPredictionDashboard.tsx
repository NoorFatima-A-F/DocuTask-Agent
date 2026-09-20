import React from 'react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import {
  AlertTriangle,
  ShieldAlert,
  ArrowRight,
  PlusCircle,
} from 'lucide-react';

interface PredictedRiskItem {
  id: string;
  type: string;
  severity: 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW';
  probability: number;
  impactScore: number;
  description: string;
  affected: string[];
  mitigation: string;
}

export const RiskPredictionDashboard: React.FC = () => {
  const risks: PredictedRiskItem[] = [
    {
      id: 'risk-01',
      type: 'DEADLOCK_CASCADE',
      severity: 'MEDIUM',
      probability: 0.035,
      impactScore: 0.65,
      description: 'High burst ingestion (> 50 simultaneous PDF tasks) could saturate OCR worker thread pool.',
      affected: ['OCR_WORKER_POOL', 'APDLE_DAG_SCHEDULER'],
      mitigation: 'Enable dynamic DAG chunk fan-out and worker auto-scaling.',
    },
    {
      id: 'risk-02',
      type: 'RESOURCE_STARVATION',
      severity: 'LOW',
      probability: 0.012,
      impactScore: 0.40,
      description: 'Shared token cache memory limit reached after 10,000 unique document layouts.',
      affected: ['RUNTIME_MEMORY_CACHE'],
      mitigation: 'Activate LRU memory eviction policy on token embeddings.',
    },
    {
      id: 'risk-03',
      type: 'POLICY_BREACH_DRIFT',
      severity: 'LOW',
      probability: 0.005,
      impactScore: 0.20,
      description: 'Budget SLA threshold near limit during heavy multi-page financial ledger audits.',
      affected: ['BUDGET_GOVERNOR'],
      mitigation: 'Dynamic budget headroom allocation for verified enterprise tier users.',
    },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold tracking-tight">Risk Prediction Dashboard</h1>
            <Badge variant="intelligence" size="sm" hasDot isPulsing>
              FAILURE FORECASTING ACTIVE
            </Badge>
            <Badge variant="outline" size="sm">
              AWM-PSDTIP Phase 13.10
            </Badge>
          </div>
          <p className="text-xs text-muted-foreground mt-1">
            Predictive modeling of deadlock cascades, resource starvation, policy breaches, and failure heatmaps before execution begins.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Button variant="intelligence" size="sm">
            <PlusCircle className="w-3.5 h-3.5 mr-1.5" />
            Analyze New Risk
          </Button>
        </div>
      </div>

      {/* Composite Risk Scorecard Banner */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card className="p-4 bg-emerald-950/10 border-emerald-500/20">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Overall Platform Status</span>
            <ShieldAlert className="w-4 h-4 text-emerald-400" />
          </div>
          <div className="text-2xl font-bold font-mono text-emerald-400 mt-2">STABLE</div>
          <div className="text-[11px] text-muted-foreground mt-1">Composite Risk Index: 0.045</div>
        </Card>

        <Card className="p-4 bg-amber-950/10 border-amber-500/20">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Active Forecasted Risks</span>
            <AlertTriangle className="w-4 h-4 text-amber-400" />
          </div>
          <div className="text-2xl font-bold font-mono text-amber-400 mt-2">{risks.length} Monitored</div>
          <div className="text-[11px] text-muted-foreground mt-1">0 Critical risks identified</div>
        </Card>

        <Card className="p-4 bg-purple-950/10 border-purple-500/20">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Max Failure Probability</span>
            <AlertTriangle className="w-4 h-4 text-purple-400" />
          </div>
          <div className="text-2xl font-bold font-mono text-purple-400 mt-2">3.5%</div>
          <div className="text-[11px] text-muted-foreground mt-1">OCR pool burst load</div>
        </Card>

        <Card className="p-4 bg-blue-950/10 border-blue-500/20">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Automated Mitigations</span>
            <ShieldAlert className="w-4 h-4 text-blue-400" />
          </div>
          <div className="text-2xl font-bold font-mono text-blue-400 mt-2">100% Ready</div>
          <div className="text-[11px] text-muted-foreground mt-1">Pre-computed recovery paths</div>
        </Card>
      </div>

      {/* Risks Stream */}
      <div className="space-y-4">
        {risks.map((r) => (
          <Card key={r.id} className="p-5 border-border/40 space-y-3 hover:border-purple-500/30 transition-colors">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
              <div className="space-y-1">
                <div className="flex items-center gap-2">
                  <span className="text-xs font-mono font-bold text-foreground">{r.id}</span>
                  <Badge variant={r.severity === 'MEDIUM' ? 'warning' : 'default'} size="sm">
                    {r.severity}
                  </Badge>
                  <span className="text-xs font-semibold text-purple-300">{r.type.replace(/_/g, ' ')}</span>
                </div>
                <p className="text-xs text-muted-foreground">{r.description}</p>
              </div>
              <div className="flex items-center gap-2 text-xs font-mono">
                <span className="text-muted-foreground">Probability: <strong className="text-foreground">{(r.probability * 100).toFixed(1)}%</strong></span>
              </div>
            </div>

            {/* Mitigation Directive */}
            <div className="flex items-center gap-2 text-xs text-emerald-400 bg-emerald-950/20 p-2.5 rounded border border-emerald-500/30">
              <ArrowRight className="w-3.5 h-3.5 flex-shrink-0" />
              <span>Mitigation Directive: {r.mitigation}</span>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};
