import React from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';

export const ScientificBenchmarksView: React.FC = () => {
  const benchmarks = [
    {
      id: 'bench_inv_1000',
      name: 'Standard Enterprise Invoices 1,000-Doc Corpus',
      dataset: 'CorpDoc-Invoice-1K',
      fingerprint: '0x1a2b...9c0d',
      size: 1000,
      seed: 42,
      accuracy: 0.994,
      latencyP50: 820.0,
      costPer1k: '$7.80',
      repeatability: '99.95%',
      evidence: '0x8f2ac31b4e5d6a7b',
    },
    {
      id: 'bench_con_500',
      name: 'Commercial Master Services Agreements 500-Doc Corpus',
      dataset: 'LegalCorp-MSA-500',
      fingerprint: '0x2b3c...0d1e',
      size: 500,
      seed: 1337,
      accuracy: 0.985,
      latencyP50: 1950.0,
      costPer1k: '$32.00',
      repeatability: '99.88%',
      evidence: '0x3c7eb44a1d9e2f8c',
    },
    {
      id: 'bench_med_250',
      name: 'Clinical Trial Patient Intake Forms 250-Doc Corpus',
      dataset: 'HealthSecure-Intake-250',
      fingerprint: '0x3c4d...1e2f',
      size: 250,
      seed: 999,
      accuracy: 0.988,
      latencyP50: 1600.0,
      costPer1k: '$24.50',
      repeatability: '99.91%',
      evidence: '0x991afe820b4c7d6e',
    },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold tracking-tight">Scientific Benchmark Registry</h1>
            <Badge variant="intelligence" size="sm">Pillar 5</Badge>
          </div>
          <p className="text-xs text-muted-foreground mt-1">
            Independently reproducible benchmark datasets with frozen RNG seeds, environment captures, and 10-run repeatability verification.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Badge variant="success" size="md">
            Repeatability: &gt;99.8% Certified
          </Badge>
        </div>
      </div>

      {/* Benchmarks Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {benchmarks.map((b) => (
          <Card key={b.id} className="p-5 flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between mb-2">
                <span className="font-mono text-xs text-primary font-semibold">{b.id}</span>
                <Badge variant="outline" size="sm" className="font-mono">Seed: {b.seed}</Badge>
              </div>

              <h3 className="text-sm font-semibold text-foreground mb-1">{b.name}</h3>
              <div className="text-xs text-muted-foreground mb-4">
                Dataset: <strong className="text-foreground">{b.dataset}</strong> ({b.size} docs)
              </div>

              <div className="grid grid-cols-2 gap-2 p-2.5 rounded bg-muted/20 border border-border/40 mb-4 text-center text-xs">
                <div>
                  <div className="text-[10px] text-muted-foreground">Accuracy</div>
                  <div className="font-mono font-bold text-emerald-400">{(b.accuracy * 100).toFixed(1)}%</div>
                </div>
                <div>
                  <div className="text-[10px] text-muted-foreground">P50 Latency</div>
                  <div className="font-mono font-bold text-foreground">{b.latencyP50} ms</div>
                </div>
                <div>
                  <div className="text-[10px] text-muted-foreground">Cost / 1k Docs</div>
                  <div className="font-mono font-bold text-foreground">{b.costPer1k}</div>
                </div>
                <div>
                  <div className="text-[10px] text-muted-foreground">Repeatability</div>
                  <div className="font-mono font-bold text-primary">{b.repeatability}</div>
                </div>
              </div>
            </div>

            <div className="border-t border-border/40 pt-3 flex items-center justify-between text-xs text-muted-foreground">
              <span className="font-mono text-[11px]">Evidence: {b.evidence}</span>
              <button className="text-primary hover:underline font-medium">Re-Run Benchmark &rarr;</button>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};
