import React, { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';

export const PlannerDecisionLedgerView: React.FC = () => {
  const [selectedEntry, setSelectedEntry] = useState<string>('pde-0001');

  const ledgerEntries = [
    {
      id: 'pde-0001',
      decisionId: 'dec-opt-8891',
      missionId: 'mission-alpha-889',
      timestamp: '2026-09-10T18:22:10Z',
      selectedPlan: {
        candidateId: 'cand-flash-p3',
        model: 'gemini-2.5-flash',
        dagDepth: 3,
        parallelism: 3,
        predictedCost: 0.0018,
        predictedLatency: 380,
        predictedAccuracy: 0.985,
        estimatedUtility: 0.892,
      },
      candidatePlans: [
        {
          candidateId: 'cand-flash-p3',
          model: 'gemini-2.5-flash',
          dagDepth: 3,
          parallelism: 3,
          predictedCost: 0.0018,
          predictedLatency: 380,
          predictedAccuracy: 0.985,
          estimatedUtility: 0.892,
          isOptimal: true,
        },
        {
          candidateId: 'cand-pro-p1',
          model: 'gemini-2.5-pro',
          dagDepth: 2,
          parallelism: 1,
          predictedCost: 0.012,
          predictedLatency: 1150,
          predictedAccuracy: 0.994,
          estimatedUtility: 0.741,
          isOptimal: false,
        },
        {
          candidateId: 'cand-hybrid-p2',
          model: 'gemini-2.5-flash+heuristics',
          dagDepth: 4,
          parallelism: 2,
          predictedCost: 0.0009,
          predictedLatency: 420,
          predictedAccuracy: 0.962,
          estimatedUtility: 0.824,
          isOptimal: false,
        },
      ],
      regretReport: {
        optimalCandidateId: 'cand-flash-p3',
        predictedUtility: 0.892,
        realizedUtility: 0.904,
        empiricalRegret: 0.0,
        counterfactualGap: 0.012,
        isBoundedOptimal: true,
      },
      previousHash: 'genesis_decision_block_00000000000000000000000000000000',
      entryHash: 'b7c891e45da092a83c7482910fae12089bb3c17820aedfa9102bc45a8f3b20c9',
      rationale: 'Flash with parallelism=3 provides optimal utility with 98.5% accuracy under 400ms latency envelope.',
    },
    {
      id: 'pde-0002',
      decisionId: 'dec-opt-8892',
      missionId: 'mission-alpha-889',
      timestamp: '2026-09-10T18:22:11Z',
      selectedPlan: {
        candidateId: 'cand-dense-ocr-v2',
        model: 'tesseract-v5-enhanced',
        dagDepth: 2,
        parallelism: 4,
        predictedCost: 0.0004,
        predictedLatency: 125,
        predictedAccuracy: 0.991,
        estimatedUtility: 0.945,
      },
      candidatePlans: [
        {
          candidateId: 'cand-dense-ocr-v2',
          model: 'tesseract-v5-enhanced',
          dagDepth: 2,
          parallelism: 4,
          predictedCost: 0.0004,
          predictedLatency: 125,
          predictedAccuracy: 0.991,
          estimatedUtility: 0.945,
          isOptimal: true,
        },
        {
          candidateId: 'cand-cloud-vision',
          model: 'google-cloud-vision-v1',
          dagDepth: 1,
          parallelism: 1,
          predictedCost: 0.0025,
          predictedLatency: 650,
          predictedAccuracy: 0.993,
          estimatedUtility: 0.812,
          isOptimal: false,
        },
      ],
      regretReport: {
        optimalCandidateId: 'cand-dense-ocr-v2',
        predictedUtility: 0.945,
        realizedUtility: 0.948,
        empiricalRegret: 0.0,
        counterfactualGap: 0.003,
        isBoundedOptimal: true,
      },
      previousHash: 'b7c891e45da092a83c7482910fae12089bb3c17820aedfa9102bc45a8f3b20c9',
      entryHash: 'f4102bc45a8f3b20c9b7c891e45da092a83c7482910fae12089bb3c17820aedf',
      rationale: 'Local enhanced OCR satisfies 99% accuracy constraint at 1/6th cost and 5x lower latency than cloud API.',
    },
  ];

  const activeEntry = ledgerEntries.find((e) => e.id === selectedEntry) || ledgerEntries[0]!;

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold tracking-tight">Planner Decision Ledger</h1>
            <Badge variant="success" size="sm">Hash-Chained & Immutable</Badge>
          </div>
          <p className="text-xs text-muted-foreground mt-1">
            Complete audit trail of all candidate plans considered, Pareto frontiers evaluated, and empirical regret calculations.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Badge variant="intelligence" size="md">
            Max Regret: 0.0000
          </Badge>
          <Badge variant="outline" size="md">
            Chain Valid: TRUE
          </Badge>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Entry Selector */}
        <div className="space-y-3">
          <div className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
            Decision Ledger Entries ({ledgerEntries.length})
          </div>
          {ledgerEntries.map((entry) => {
            const isSelected = entry.id === selectedEntry;
            return (
              <Card
                key={entry.id}
                className={`p-4 cursor-pointer transition-all ${
                  isSelected ? 'border-primary ring-1 ring-primary/40 bg-primary/5' : 'hover:border-border/80'
                }`}
                onClick={() => setSelectedEntry(entry.id)}
              >
                <div className="flex items-start justify-between">
                  <div>
                    <span className="font-mono text-xs font-bold text-foreground">{entry.id}</span>
                    <div className="text-xs font-medium text-muted-foreground mt-0.5">{entry.decisionId}</div>
                  </div>
                  <Badge variant="success" size="sm">Bounded Optimal</Badge>
                </div>
                <div className="mt-2 text-xs font-mono text-foreground/80">
                  Selected: <span className="text-primary font-bold">{entry.selectedPlan.model}</span>
                </div>
                <div className="mt-2 font-mono text-[10px] text-muted-foreground truncate">
                  Hash: {entry.entryHash.slice(0, 18)}...
                </div>
              </Card>
            );
          })}
        </div>

        {/* Selected Decision Detail */}
        <div className="lg:col-span-2 space-y-6">
          <Card className="p-6 space-y-6">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-border/40 pb-4">
              <div>
                <h2 className="text-lg font-bold">{activeEntry.decisionId}</h2>
                <div className="text-xs text-muted-foreground mt-0.5">
                  Mission: <span className="font-mono text-foreground">{activeEntry.missionId}</span> | Timestamp: <span className="font-mono text-foreground">{activeEntry.timestamp}</span>
                </div>
              </div>
              <Badge variant="intelligence" size="md">
                Selected: {activeEntry.selectedPlan.candidateId}
              </Badge>
            </div>

            {/* Rationale & Regret */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="p-4 bg-muted/30 border border-border/40 rounded-lg space-y-2">
                <div className="text-xs font-semibold text-foreground">Selection Rationale</div>
                <p className="text-xs text-muted-foreground leading-relaxed">
                  {activeEntry.rationale}
                </p>
              </div>
              <div className="p-4 bg-muted/30 border border-border/40 rounded-lg space-y-2">
                <div className="text-xs font-semibold text-foreground flex items-center justify-between">
                  <span>Empirical Regret Analysis</span>
                  <Badge variant="success" size="sm">Regret: {activeEntry.regretReport.empiricalRegret.toFixed(4)}</Badge>
                </div>
                <div className="text-xs font-mono space-y-1 text-muted-foreground">
                  <div>Predicted Utility: <span className="text-foreground">{activeEntry.regretReport.predictedUtility}</span></div>
                  <div>Realized Utility: <span className="text-emerald-400 font-bold">{activeEntry.regretReport.realizedUtility}</span></div>
                  <div>Counterfactual Gap: <span className="text-foreground">{activeEntry.regretReport.counterfactualGap}</span></div>
                </div>
              </div>
            </div>

            {/* Candidate Matrix Table */}
            <div className="space-y-2">
              <div className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                Evaluated Candidate Plans ({activeEntry.candidatePlans.length})
              </div>
              <div className="border border-border/40 rounded-lg overflow-hidden">
                <table className="w-full text-left text-xs font-mono">
                  <thead className="bg-muted/50 border-b border-border/40 text-muted-foreground">
                    <tr>
                      <th className="p-2.5">Candidate ID</th>
                      <th className="p-2.5">Model</th>
                      <th className="p-2.5">Cost</th>
                      <th className="p-2.5">Latency</th>
                      <th className="p-2.5">Accuracy</th>
                      <th className="p-2.5">Utility</th>
                      <th className="p-2.5">Status</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-border/40">
                    {activeEntry.candidatePlans.map((cand) => (
                      <tr key={cand.candidateId} className={cand.isOptimal ? 'bg-primary/10 font-bold' : ''}>
                        <td className="p-2.5">{cand.candidateId}</td>
                        <td className="p-2.5 text-foreground">{cand.model}</td>
                        <td className="p-2.5">${cand.predictedCost.toFixed(4)}</td>
                        <td className="p-2.5">{cand.predictedLatency} ms</td>
                        <td className="p-2.5">{(cand.predictedAccuracy * 100).toFixed(1)}%</td>
                        <td className="p-2.5 text-primary">{cand.estimatedUtility.toFixed(3)}</td>
                        <td className="p-2.5">
                          <Badge variant={cand.isOptimal ? 'success' : 'outline'} size="sm">
                            {cand.isOptimal ? 'SELECTED' : 'REJECTED'}
                          </Badge>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>

            {/* Hash Linkage */}
            <div className="p-3 bg-card border border-border/40 rounded font-mono text-[11px] text-muted-foreground space-y-1">
              <div><span className="text-foreground">Previous Entry Hash: </span>{activeEntry.previousHash}</div>
              <div><span className="text-foreground">Current Entry Hash: </span><span className="text-emerald-400 font-bold">{activeEntry.entryHash}</span></div>
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
};
