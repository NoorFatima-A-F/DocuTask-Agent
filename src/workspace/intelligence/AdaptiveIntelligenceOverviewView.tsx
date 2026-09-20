import React, { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';

export const AdaptiveIntelligenceOverviewView: React.FC = () => {
  const [activeCycle, setActiveCycle] = useState<string | null>(null);

  const metrics = {
    totalExperiences: 1420,
    minedStrategies: 8,
    activeHypotheses: 5,
    abExperimentsCompleted: 14,
    statisticallyPromoted: 6,
    meanImprovementPct: '18.4%',
    predictionMAE: '42.1 ms',
    currentPlannerVersion: 'v2.1.0',
    evidenceLinkageRate: '100.0%',
    scientificPValue: 'p < 0.001',
  };

  const activeImprovements = [
    {
      id: 'pipe_inv_opt_01',
      title: 'Invoice Fan-Out Parallelization',
      domain: 'Invoice',
      stage: 'DEPLOYED',
      pVal: 'p = 0.0004',
      improvement: '+22.4% Latency Reduction',
      version: 'v2.1.0',
    },
    {
      id: 'pipe_legal_02',
      title: 'Legal Contract Pre-validation Invariant Guard',
      domain: 'Contract',
      stage: 'MONITORING',
      pVal: 'p = 0.0012',
      improvement: '-85.0% Downstream Retries',
      version: 'v2.0.4',
    },
    {
      id: 'pipe_med_03',
      title: 'Medical Clinical Trial Vision Tiering',
      domain: 'Medical',
      stage: 'EXPERIMENT_RUNNING',
      pVal: 'p = 0.0210',
      improvement: '+14.2% Cost Savings',
      version: 'CANDIDATE',
    },
  ];

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold tracking-tight">Adaptive Intelligence & Scientific Learning</h1>
            <Badge variant="intelligence" size="sm">AISLCOP v10.0</Badge>
          </div>
          <p className="text-xs text-muted-foreground mt-1">
            Closed-loop self-improving platform: Experience &rarr; Hypothesis &rarr; A/B Experimentation &rarr; Statistical Verification &rarr; Versioned Deployment.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Badge variant="success" size="md">
            Scientific Attestation: Validated
          </Badge>
          <Badge variant="outline" size="md">
            Active: {metrics.currentPlannerVersion}
          </Badge>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <Card className="p-4 border-primary/20">
          <div className="text-xs text-muted-foreground">Experiences Logged</div>
          <div className="text-2xl font-bold font-mono text-foreground mt-1">{metrics.totalExperiences}</div>
          <div className="text-[11px] text-emerald-400 mt-1">100% Cryptographically Hashed</div>
        </Card>
        <Card className="p-4">
          <div className="text-xs text-muted-foreground">Mined Strategies</div>
          <div className="text-2xl font-bold font-mono text-foreground mt-1">{metrics.minedStrategies}</div>
          <div className="text-[11px] text-muted-foreground mt-1">{metrics.statisticallyPromoted} Promoted</div>
        </Card>
        <Card className="p-4">
          <div className="text-xs text-muted-foreground">A/B Experiments</div>
          <div className="text-2xl font-bold font-mono text-foreground mt-1">{metrics.abExperimentsCompleted}</div>
          <div className="text-[11px] text-emerald-400 mt-1">Welch's t-test (p &lt; 0.05)</div>
        </Card>
        <Card className="p-4">
          <div className="text-xs text-muted-foreground">Mean System Gain</div>
          <div className="text-2xl font-bold font-mono text-foreground mt-1">{metrics.meanImprovementPct}</div>
          <div className="text-[11px] text-primary mt-1">Prediction MAE: {metrics.predictionMAE}</div>
        </Card>
      </div>

      {/* Decision Loop Architecture Visualizer */}
      <Card className="p-5 border-border/60 bg-muted/10">
        <div className="flex items-center justify-between border-b border-border/40 pb-3 mb-4">
          <h2 className="text-sm font-semibold tracking-wide">Scientific Decision Loop & Optimization Pipeline</h2>
          <Badge variant="outline" size="sm">Deterministic & Reversible</Badge>
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-7 gap-2 text-center text-xs">
          <div className="p-3 rounded-lg border border-border/60 bg-background flex flex-col items-center justify-center">
            <span className="font-semibold text-foreground">1. Execution</span>
            <span className="text-[10px] text-muted-foreground mt-1">DAG Telemetry</span>
          </div>
          <div className="p-3 rounded-lg border border-border/60 bg-background flex flex-col items-center justify-center">
            <span className="font-semibold text-foreground">2. Experience</span>
            <span className="text-[10px] text-muted-foreground mt-1">Evidence Merkle</span>
          </div>
          <div className="p-3 rounded-lg border border-border/60 bg-background flex flex-col items-center justify-center">
            <span className="font-semibold text-foreground">3. Mining</span>
            <span className="text-[10px] text-muted-foreground mt-1">Candidate Strat</span>
          </div>
          <div className="p-3 rounded-lg border border-border/60 bg-background flex flex-col items-center justify-center">
            <span className="font-semibold text-foreground">4. Hypothesis</span>
            <span className="text-[10px] text-muted-foreground mt-1">Bottleneck Delta</span>
          </div>
          <div className="p-3 rounded-lg border border-border/60 bg-background flex flex-col items-center justify-center">
            <span className="font-semibold text-foreground">5. A/B Trials</span>
            <span className="text-[10px] text-muted-foreground mt-1">Control vs Cand</span>
          </div>
          <div className="p-3 rounded-lg border border-border/60 bg-background flex flex-col items-center justify-center">
            <span className="font-semibold text-foreground">6. Verification</span>
            <span className="text-[10px] text-emerald-400 mt-1">p &lt; 0.05</span>
          </div>
          <div className="p-3 rounded-lg border border-emerald-500/40 bg-emerald-950/20 flex flex-col items-center justify-center">
            <span className="font-semibold text-emerald-400">7. Deploy & Rollback</span>
            <span className="text-[10px] text-emerald-300 mt-1">Versioned Kernel</span>
          </div>
        </div>
      </Card>

      {/* Active Improvement Pipelines */}
      <Card className="p-5">
        <div className="flex items-center justify-between border-b border-border/40 pb-3 mb-4">
          <h2 className="text-sm font-semibold tracking-wide">Active Continuous Improvement Pipelines</h2>
          <button 
            onClick={() => setActiveCycle('Triggered autonomous learning loop for invoice domain')}
            className="text-xs px-3 py-1.5 rounded bg-primary text-primary-foreground hover:bg-primary/90 transition-colors font-medium"
          >
            Trigger Optimization Cycle
          </button>
        </div>

        {activeCycle && (
          <div className="mb-4 p-3 rounded bg-emerald-950/30 border border-emerald-500/30 text-xs text-emerald-300">
            {activeCycle} &mdash; A/B validation concluded with p &lt; 0.001. Promoted to planner version.
          </div>
        )}

        <div className="space-y-3">
          {activeImprovements.map((pipe) => (
            <div key={pipe.id} className="p-3 rounded-lg border border-border/60 bg-muted/5 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
              <div>
                <div className="flex items-center gap-2">
                  <span className="font-semibold text-xs text-foreground">{pipe.title}</span>
                  <Badge variant={pipe.stage === 'DEPLOYED' ? 'success' : pipe.stage === 'MONITORING' ? 'intelligence' : 'warning'} size="sm">
                    {pipe.stage}
                  </Badge>
                  <span className="text-[11px] text-muted-foreground font-mono">[{pipe.domain}]</span>
                </div>
                <div className="text-xs text-muted-foreground mt-1 flex items-center gap-3">
                  <span>Significance: <strong className="text-emerald-400">{pipe.pVal}</strong></span>
                  <span>Measured Delta: <strong className="text-foreground">{pipe.improvement}</strong></span>
                </div>
              </div>
              <div className="flex items-center gap-2">
                <Badge variant="outline" size="sm" className="font-mono">
                  Target: {pipe.version}
                </Badge>
              </div>
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
};
