import React, { useState } from 'react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import {
  HelpCircle,
  TrendingDown,
  TrendingUp,
  Sparkles,
  Lock,
  Search,
} from 'lucide-react';

interface CounterfactualOutcomeItem {
  id: string;
  premise: string;
  latencyDeltaPct: number;
  costDeltaPct: number;
  riskShift: string;
  confidence: number;
  tradeoffs: string;
  hash: string;
}

export const CounterfactualExplorer: React.FC = () => {
  const [customPremise, setCustomPremise] = useState<string>(
    'What if worker concurrency is scaled up to 32 and token caching is enabled?'
  );

  const counterfactuals: CounterfactualOutcomeItem[] = [
    {
      id: 'cfo-101',
      premise: 'What if worker concurrency is scaled up to 16 and token caching is enabled?',
      latencyDeltaPct: -28.5,
      costDeltaPct: 12.0,
      riskShift: 'REDUCED',
      confidence: 0.985,
      tradeoffs: 'Provides 28.5% faster end-to-end mission delivery at the cost of 12% higher burst memory usage.',
      hash: '0x4a9b8c7d...221e',
    },
    {
      id: 'cfo-102',
      premise: 'What if token caching is disabled during high-density financial balance sheet parsing?',
      latencyDeltaPct: 35.0,
      costDeltaPct: 20.0,
      riskShift: 'ELEVATED',
      confidence: 0.990,
      tradeoffs: 'Disabling cache forces cold model inference on repetitive templates with higher latency.',
      hash: '0x1b2c3d4e...990f',
    },
    {
      id: 'cfo-103',
      premise: 'What if OCR extraction worker pool experiences a 50% node crash?',
      latencyDeltaPct: 45.0,
      costDeltaPct: 0.0,
      riskShift: 'ELEVATED',
      confidence: 0.978,
      tradeoffs: 'Fallback to secondary specialist agents preserves 100% zero-fabrication floor while latency increases by 45%.',
      hash: '0x7e8f9a0b...334a',
    },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold tracking-tight">Counterfactual Reasoning Explorer</h1>
            <Badge variant="intelligence" size="sm" hasDot isPulsing>
              "WHAT-IF" REASONING ACTIVE
            </Badge>
            <Badge variant="outline" size="sm">
              AWM-PSDTIP Phase 13.10
            </Badge>
          </div>
          <p className="text-xs text-muted-foreground mt-1">
            Evaluate hypothetical interventions, alternative planner graphs, policy mutations, and recovery trajectories without live system disruption.
          </p>
        </div>
      </div>

      {/* Interactive Query Input */}
      <Card className="p-5 bg-gradient-to-r from-purple-950/30 via-indigo-950/20 to-background border-purple-500/30 space-y-3">
        <div className="flex items-center gap-2">
          <HelpCircle className="w-5 h-5 text-purple-400" />
          <h2 className="text-sm font-bold text-foreground">Hypothetical Intervention Query</h2>
        </div>
        <div className="flex flex-col sm:flex-row gap-3">
          <div className="relative flex-1">
            <Search className="w-4 h-4 absolute left-3 top-3 text-muted-foreground" />
            <input
              type="text"
              value={customPremise}
              onChange={(e) => setCustomPremise(e.target.value)}
              className="w-full bg-secondary/50 text-xs rounded-lg pl-9 pr-3 py-2.5 border border-border/40 focus:outline-none focus:border-primary text-foreground"
              placeholder="Enter hypothetical what-if scenario..."
            />
          </div>
          <Button variant="intelligence" size="sm">
            <Sparkles className="w-3.5 h-3.5 mr-1.5" />
            Evaluate Counterfactual
          </Button>
        </div>
      </Card>

      {/* Outcomes Stream */}
      <div className="space-y-4">
        {counterfactuals.map((cf) => (
          <Card key={cf.id} className="p-5 border-border/40 space-y-4 hover:border-purple-500/30 transition-colors">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
              <div className="space-y-1">
                <span className="text-xs font-mono font-bold text-purple-400">{cf.id}</span>
                <h3 className="text-sm font-semibold text-foreground">{cf.premise}</h3>
              </div>
              <Badge
                variant={
                  cf.riskShift === 'REDUCED'
                    ? 'success'
                    : cf.riskShift === 'ELEVATED'
                    ? 'warning'
                    : 'default'
                }
                size="sm"
              >
                Risk: {cf.riskShift}
              </Badge>
            </div>

            {/* Impact Metric Cards */}
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs font-mono">
              <div className="p-3 rounded bg-secondary/20 border border-border/30 flex items-center justify-between">
                <span className="text-muted-foreground">Latency Delta:</span>
                <span className={`font-bold flex items-center gap-1 ${cf.latencyDeltaPct < 0 ? 'text-emerald-400' : 'text-amber-400'}`}>
                  {cf.latencyDeltaPct < 0 ? <TrendingDown className="w-3.5 h-3.5" /> : <TrendingUp className="w-3.5 h-3.5" />}
                  {cf.latencyDeltaPct > 0 ? `+${cf.latencyDeltaPct}%` : `${cf.latencyDeltaPct}%`}
                </span>
              </div>

              <div className="p-3 rounded bg-secondary/20 border border-border/30 flex items-center justify-between">
                <span className="text-muted-foreground">Compute Cost Delta:</span>
                <span className="font-bold text-foreground">
                  {cf.costDeltaPct > 0 ? `+${cf.costDeltaPct}%` : `${cf.costDeltaPct}%`}
                </span>
              </div>

              <div className="p-3 rounded bg-secondary/20 border border-border/30 flex items-center justify-between">
                <span className="text-muted-foreground">Prediction Confidence:</span>
                <span className="font-bold text-purple-300">{(cf.confidence * 100).toFixed(1)}%</span>
              </div>
            </div>

            {/* Tradeoff Summary */}
            <p className="text-xs text-muted-foreground">{cf.tradeoffs}</p>

            <div className="flex items-center justify-between text-[11px] text-muted-foreground pt-3 border-t border-border/30 font-mono">
              <div className="flex items-center gap-1.5 truncate max-w-md">
                <Lock className="w-3.5 h-3.5 text-purple-400 flex-shrink-0" />
                <span>Proof Hash: {cf.hash}</span>
              </div>
              <Button variant="outline" size="sm">
                Apply as Candidate Policy
              </Button>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};
