import React, { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';

export const ExperimentCenterView: React.FC = () => {
  const [selectedRun, setSelectedRun] = useState<string>('exp_run_01');

  const experiments = [
    {
      id: 'exp_run_01',
      title: 'A/B Trial: Parallel vs Sequential DAG on Invoices',
      hypothesisId: 'hyp_inv_parallel',
      sampleSize: 20,
      status: 'CONCLUDED',
      promotesCandidate: true,
      verdict: 'Statistically significant latency reduction of 22.4% (p = 0.0004, Welch t-test).',
      metrics: {
        controlLatency: 940.5,
        candidateLatency: 730.0,
        controlCost: 0.0084,
        candidateCost: 0.0086,
        controlConfidence: 0.978,
        candidateConfidence: 0.982,
        pValue: 0.0004,
        tStat: -4.82,
        cohensD: -1.45,
      },
    },
    {
      id: 'exp_run_02',
      title: 'A/B Trial: Pre-validation Invariant Guard on Contracts',
      hypothesisId: 'hyp_con_preval',
      sampleSize: 15,
      status: 'CONCLUDED',
      promotesCandidate: true,
      verdict: 'Statistically significant retry reduction from 18% to 2% (p = 0.0012).',
      metrics: {
        controlLatency: 2150.0,
        candidateLatency: 1980.0,
        controlCost: 0.0342,
        candidateCost: 0.0315,
        controlConfidence: 0.942,
        candidateConfidence: 0.965,
        pValue: 0.0012,
        tStat: -3.94,
        cohensD: -1.12,
      },
    },
  ];

  const current = experiments.find((e) => e.id === selectedRun) || experiments[0];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold tracking-tight">A/B Experimentation & Statistical Center</h1>
            <Badge variant="intelligence" size="sm">Pillar 5</Badge>
          </div>
          <p className="text-xs text-muted-foreground mt-1">
            Randomized trials and shadow replays evaluated using Welch's t-test, Cohen's d effect sizes, and p-value significance filters.
          </p>
        </div>
        <div className="flex items-center gap-2">
          {experiments.map((exp) => (
            <button
              key={exp.id}
              onClick={() => setSelectedRun(exp.id)}
              className={`text-xs px-2.5 py-1 rounded transition-colors font-mono font-medium ${
                selectedRun === exp.id ? 'bg-primary text-primary-foreground' : 'bg-muted text-muted-foreground'
              }`}
            >
              {exp.id}
            </button>
          ))}
        </div>
      </div>

      {current && (
        <div className="space-y-4">
          {/* Main Experiment Card */}
          <Card className="p-5 border-border/60">
            <div className="flex items-center justify-between border-b border-border/40 pb-3 mb-4">
              <div>
                <span className="font-mono text-xs text-primary font-semibold">{current.id}</span>
                <h2 className="text-sm font-semibold text-foreground mt-0.5">{current.title}</h2>
              </div>
              <div className="flex items-center gap-2">
                <Badge variant={current.promotesCandidate ? 'success' : 'error'} size="sm">
                  {current.promotesCandidate ? 'PROMOTION GRANTED' : 'REJECTED'}
                </Badge>
              </div>
            </div>

            <div className="p-3 rounded bg-emerald-950/30 border border-emerald-500/30 text-xs text-emerald-300 mb-4">
              <strong>Verdict:</strong> {current.verdict}
            </div>

            {/* Statistical Grid */}
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-center mb-4">
              <div className="p-3 rounded bg-muted/20 border border-border/40">
                <div className="text-[10px] text-muted-foreground">Control Latency</div>
                <div className="text-sm font-mono font-bold text-foreground mt-1">{current.metrics.controlLatency} ms</div>
                <div className="text-[10px] text-muted-foreground mt-0.5">Baseline</div>
              </div>
              <div className="p-3 rounded bg-emerald-950/20 border border-emerald-500/30">
                <div className="text-[10px] text-emerald-400">Candidate Latency</div>
                <div className="text-sm font-mono font-bold text-emerald-400 mt-1">{current.metrics.candidateLatency} ms</div>
                <div className="text-[10px] text-emerald-300 mt-0.5">
                  -{(((current.metrics.controlLatency - current.metrics.candidateLatency) / current.metrics.controlLatency) * 100).toFixed(1)}%
                </div>
              </div>
              <div className="p-3 rounded bg-muted/20 border border-border/40">
                <div className="text-[10px] text-muted-foreground">Welch's t-Statistic</div>
                <div className="text-sm font-mono font-bold text-primary mt-1">{current.metrics.tStat}</div>
                <div className="text-[10px] text-muted-foreground mt-0.5">d = {current.metrics.cohensD}</div>
              </div>
              <div className="p-3 rounded bg-muted/20 border border-border/40">
                <div className="text-[10px] text-muted-foreground">Significance (p-value)</div>
                <div className="text-sm font-mono font-bold text-emerald-400 mt-1">{current.metrics.pValue}</div>
                <div className="text-[10px] text-emerald-300 mt-0.5">&alpha; = 0.05 Passed</div>
              </div>
            </div>
          </Card>
        </div>
      )}
    </div>
  );
};
