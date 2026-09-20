import React, { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';

export const DecisionProofExplorerView: React.FC = () => {
  const [selectedProof, setSelectedProof] = useState<string>('prf_001_inv');

  const proofs = [
    {
      proofId: 'prf_001_inv',
      missionId: 'msn_1001',
      domain: 'Invoice',
      plannerVer: 'v2.1.0',
      formula: 'U(s) = 0.50 * Acc(s) - 0.30 * (Lat(s)/1000) - 0.20 * (Cost(s)/0.01)',
      selectedStrategy: 'Invoice Parallel Fan-Out Strategy',
      selectedStrategyId: 'strat_inv_fanout',
      winningScore: 0.1245,
      evidenceHash: '0x8f2ac31b4e5d6a7b',
      candidates: [
        {
          name: 'Invoice Parallel Fan-Out Strategy',
          acc: 0.994,
          lat: 730.0,
          cost: 0.0078,
          utility: 0.1245,
          feasible: true,
          rejection: null,
        },
        {
          name: 'Sequential Single-Pass Baseline',
          acc: 0.978,
          lat: 940.0,
          cost: 0.0084,
          utility: 0.0390,
          feasible: true,
          rejection: null,
        },
        {
          name: 'Heavy Vision Multi-Pass OCR',
          acc: 0.996,
          lat: 2800.0,
          cost: 0.0450,
          utility: -1.2420,
          feasible: false,
          rejection: 'Exceeded cost SLA ceiling ($0.0450 > $0.0200)',
        },
      ],
    },
  ];

  const current = proofs.find((p) => p.proofId === selectedProof) || proofs[0];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold tracking-tight">Decision Proof Explorer</h1>
            <Badge variant="intelligence" size="sm">Pillar 2</Badge>
          </div>
          <p className="text-xs text-muted-foreground mt-1">
            Formal mathematical decision proofs capturing evaluated alternatives, utility scores, constraints, and rejection justifications.
          </p>
        </div>
        <div className="flex items-center gap-2">
          {proofs.map((p) => (
            <button
              key={p.proofId}
              onClick={() => setSelectedProof(p.proofId)}
              className={`text-xs px-2.5 py-1 rounded transition-colors font-mono font-medium ${
                selectedProof === p.proofId ? 'bg-primary text-primary-foreground' : 'bg-muted text-muted-foreground hover:bg-muted/80'
              }`}
            >
              {p.proofId}
            </button>
          ))}
          <Badge variant="success" size="md">
            Proof Status: Cryptographically Bound
          </Badge>
        </div>
      </div>

      {current && (
        <div className="space-y-4">
          {/* Main Card */}
          <Card className="p-5 border-border/60">
            <div className="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-2 border-b border-border/40 pb-3 mb-4">
              <div>
                <span className="font-mono text-xs text-primary font-semibold">{current.proofId}</span>
                <h2 className="text-sm font-semibold text-foreground mt-0.5">
                  Planner Strategy Selection for Mission <strong className="font-mono text-primary">{current.missionId}</strong>
                </h2>
                <div className="text-xs text-muted-foreground mt-1 font-mono">
                  Objective Function: <strong className="text-foreground">{current.formula}</strong>
                </div>
              </div>
              <div className="text-right">
                <Badge variant="success" size="sm">WINNER: {current.selectedStrategyId}</Badge>
                <div className="text-[11px] font-mono text-emerald-400 mt-1">Score: +{current.winningScore.toFixed(4)}</div>
              </div>
            </div>

            {/* Candidate Alternatives Table */}
            <h3 className="text-xs font-semibold text-muted-foreground mb-2">Evaluated Alternatives & Objective Scores</h3>
            <div className="overflow-x-auto border border-border/40 rounded-lg">
              <table className="w-full text-left text-xs border-collapse">
                <thead>
                  <tr className="border-b border-border/40 bg-muted/20 font-semibold text-muted-foreground">
                    <th className="p-3">Candidate Strategy</th>
                    <th className="p-3">Accuracy</th>
                    <th className="p-3">Latency (ms)</th>
                    <th className="p-3">Cost ($)</th>
                    <th className="p-3">Utility Score</th>
                    <th className="p-3">Feasibility</th>
                    <th className="p-3">Rejection / Selection Rationale</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-border/20">
                  {current.candidates.map((c, idx) => (
                    <tr key={idx} className={c.name === current.selectedStrategy ? 'bg-primary/5' : 'hover:bg-muted/10'}>
                      <td className="p-3 font-semibold text-foreground">
                        {c.name}
                        {c.name === current.selectedStrategy && (
                          <span className="ml-2 text-[10px] text-emerald-400 font-mono font-bold">&larr; SELECTED</span>
                        )}
                      </td>
                      <td className="p-3 font-mono text-emerald-400">{(c.acc * 100).toFixed(1)}%</td>
                      <td className="p-3 font-mono">{c.lat.toFixed(0)} ms</td>
                      <td className="p-3 font-mono">${c.cost.toFixed(4)}</td>
                      <td className="p-3 font-mono font-bold text-foreground">{c.utility.toFixed(4)}</td>
                      <td className="p-3">
                        <Badge variant={c.feasible ? 'success' : 'error'} size="sm">
                          {c.feasible ? 'FEASIBLE' : 'REJECTED'}
                        </Badge>
                      </td>
                      <td className="p-3 text-[11px] text-muted-foreground">
                        {c.rejection || 'Selected: Global Maximum Utility Score'}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </Card>
        </div>
      )}
    </div>
  );
};
