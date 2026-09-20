import React, { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';

export const ReproducibilityStudioView: React.FC = () => {
  const [isReplaying, setIsReplaying] = useState<boolean>(false);
  const [reproduceResult, setReproduceResult] = useState<any | null>(null);

  const snapshots = [
    {
      id: 'snap-baseline-001',
      missionId: 'mission-alpha-889',
      stepIndex: 1,
      seed: 42,
      timestamp: '2026-09-10T18:22:10Z',
      hash: '9a8f3b20c91e847ad3ef0192a83c7482910fae12089bb3c17820aedfa9102bc4',
      envHash: 'e7102fae89bb3c17820aedfa9102bc45a8f3b20c91e847ad3ef0192a83c74829',
      outputDigest: 'f81d4fae7dec11d0a76500a0c91e6bf6012',
    },
    {
      id: 'snap-complex-table-002',
      missionId: 'mission-table-912',
      stepIndex: 2,
      seed: 1337,
      timestamp: '2026-09-10T18:25:44Z',
      hash: '3bc17820aedfa9102bc45a8f3b20c91e847ad3ef0192a83c7482910fae12089b',
      envHash: 'e7102fae89bb3c17820aedfa9102bc45a8f3b20c91e847ad3ef0192a83c74829',
      outputDigest: '482910fae12089bb3c17820aedfa9102bc45a8f3b20c91e847ad3ef0192a83c7',
    },
  ];

  const handleRunReplay = () => {
    setIsReplaying(true);
    setTimeout(() => {
      setIsReplaying(false);
      setReproduceResult({
        reproductionId: 'rep-' + Date.now(),
        snapshotId: 'snap-baseline-001',
        isReproduced: true,
        fidelityScore: 1.0,
        originalHash: 'f81d4fae7dec11d0a76500a0c91e6bf6012',
        reproducedHash: 'f81d4fae7dec11d0a76500a0c91e6bf6012',
        executionTimeMs: 14.8,
        bitForBitMatch: true,
        metrics: {
          precision: 0.994,
          recall: 0.991,
          f1Score: 0.9925,
          latencyVarianceMs: 1.2,
        },
        log: [
          'Restoring environment state (Python 3.14.4, win32)',
          'Setting deterministic RNG seed: 42',
          'Injecting input payload digest: c7e12f00a891...',
          'Replaying execution graph DAG steps...',
          'Replay finished in 14.8ms with 100% hash parity.',
        ],
      });
    }, 600);
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold tracking-tight">Reproducibility Studio</h1>
            <Badge variant="success" size="sm">Bit-for-Bit Deterministic</Badge>
          </div>
          <p className="text-xs text-muted-foreground mt-1">
            Capture frozen execution snapshots and re-run deterministic replay pipelines to prove 100% mathematical fidelity.
          </p>
        </div>
        <button
          onClick={handleRunReplay}
          disabled={isReplaying}
          className="px-4 py-2 bg-primary hover:bg-primary/90 text-primary-foreground font-semibold text-xs rounded-lg transition-all flex items-center gap-2 shadow-sm cursor-pointer"
        >
          {isReplaying ? 'Replaying Pipeline...' : '▶ Execute Deterministic Replay'}
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Snapshots List */}
        <div className="space-y-4">
          <div className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
            Captured State Snapshots ({snapshots.length})
          </div>
          {snapshots.map((snap) => (
            <Card key={snap.id} className="p-5 space-y-3">
              <div className="flex items-center justify-between">
                <span className="font-mono text-sm font-bold text-foreground">{snap.id}</span>
                <Badge variant="intelligence" size="sm">Seed: {snap.seed}</Badge>
              </div>
              <div className="text-xs text-muted-foreground">
                Mission: <span className="font-mono text-foreground">{snap.missionId}</span> | Step: <span className="font-mono text-foreground">#{snap.stepIndex}</span>
              </div>
              <div className="p-2.5 bg-muted/30 rounded border border-border/40 font-mono text-[11px] text-muted-foreground space-y-1">
                <div><span className="text-foreground">Snapshot Hash: </span>{snap.hash.slice(0, 24)}...</div>
                <div><span className="text-foreground">Expected Output: </span>{snap.outputDigest}</div>
              </div>
            </Card>
          ))}
        </div>

        {/* Replay Verification Console */}
        <div className="space-y-4">
          <div className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
            Replay Verification Console
          </div>
          <Card className="p-5 space-y-4">
            {reproduceResult ? (
              <div className="space-y-4">
                <div className="flex items-center justify-between border-b border-border/40 pb-3">
                  <div className="flex items-center gap-2">
                    <Badge variant="success" size="md">100% BIT-FOR-BIT MATCH</Badge>
                    <span className="text-xs font-mono text-muted-foreground">{reproduceResult.reproductionId}</span>
                  </div>
                  <span className="text-xs font-mono text-foreground font-bold">{reproduceResult.executionTimeMs} ms</span>
                </div>

                <div className="grid grid-cols-3 gap-2">
                  <div className="p-2.5 bg-card border border-border/40 rounded text-center">
                    <div className="text-[10px] text-muted-foreground">Precision</div>
                    <div className="text-sm font-bold font-mono text-emerald-400">{(reproduceResult.metrics.precision * 100).toFixed(1)}%</div>
                  </div>
                  <div className="p-2.5 bg-card border border-border/40 rounded text-center">
                    <div className="text-[10px] text-muted-foreground">Recall</div>
                    <div className="text-sm font-bold font-mono text-emerald-400">{(reproduceResult.metrics.recall * 100).toFixed(1)}%</div>
                  </div>
                  <div className="p-2.5 bg-card border border-border/40 rounded text-center">
                    <div className="text-[10px] text-muted-foreground">Variance</div>
                    <div className="text-sm font-bold font-mono text-foreground">±{reproduceResult.metrics.latencyVarianceMs} ms</div>
                  </div>
                </div>

                <div className="p-3 bg-black/80 rounded border border-border/40 font-mono text-xs text-emerald-400 space-y-1">
                  {reproduceResult.log.map((line: string, i: number) => (
                    <div key={i}>&gt; {line}</div>
                  ))}
                </div>
              </div>
            ) : (
              <div className="py-12 text-center text-muted-foreground text-xs">
                Click &quot;Execute Deterministic Replay&quot; above to re-run the snapshot and verify bitwise parity.
              </div>
            )}
          </Card>
        </div>
      </div>
    </div>
  );
};
