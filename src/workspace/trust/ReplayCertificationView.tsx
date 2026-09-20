import React from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';

export const ReplayCertificationView: React.FC = () => {
  const reports = [
    {
      certId: 'cert_rep_001',
      missionId: 'msn_1001',
      domain: 'Invoice',
      origLat: 940.5,
      repLat: 942.0,
      latDelta: '+0.16%',
      origCost: 0.0084,
      repCost: 0.0084,
      costDelta: '0.00%',
      stateMatch: '99.98%',
      outputSimilarity: '99.95%',
      tier: 'SCIENTIFIC_REPRODUCIBLE',
      certified: true,
      signature: '0x3c7e...b44a',
    },
    {
      certId: 'cert_rep_002',
      missionId: 'msn_1002',
      domain: 'Contract',
      origLat: 2150.0,
      repLat: 2162.0,
      latDelta: '+0.56%',
      origCost: 0.0342,
      repCost: 0.0342,
      costDelta: '0.00%',
      stateMatch: '99.96%',
      outputSimilarity: '99.92%',
      tier: 'SCIENTIFIC_REPRODUCIBLE',
      certified: true,
      signature: '0x991a...fe82',
    },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold tracking-tight">Runtime Replay Certification</h1>
            <Badge variant="intelligence" size="sm">Pillar 3</Badge>
          </div>
          <p className="text-xs text-muted-foreground mt-1">
            Scientific replay verification comparing original execution traces against deterministic replayed runs.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Badge variant="success" size="md">
            Parity Pass Rate: 100.0%
          </Badge>
        </div>
      </div>

      {/* Reports List */}
      <div className="space-y-4">
        {reports.map((r) => (
          <Card key={r.certId} className="p-5 border-border/60">
            <div className="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-2 border-b border-border/40 pb-3 mb-4">
              <div>
                <span className="font-mono text-xs text-primary font-semibold">{r.certId}</span>
                <h3 className="text-sm font-semibold text-foreground mt-0.5">
                  Deterministic Replay Certificate for Mission <strong className="font-mono text-primary">{r.missionId}</strong>
                </h3>
              </div>
              <div className="flex items-center gap-2">
                <Badge variant="success" size="sm">{r.tier}</Badge>
              </div>
            </div>

            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-center text-xs mb-4">
              <div className="p-3 rounded bg-muted/20 border border-border/40">
                <div className="text-[10px] text-muted-foreground">Bitwise State Match</div>
                <div className="font-mono font-bold text-emerald-400 text-sm mt-0.5">{r.stateMatch}</div>
                <div className="text-[10px] text-muted-foreground mt-0.5">&ge; 99.0% Floor</div>
              </div>
              <div className="p-3 rounded bg-muted/20 border border-border/40">
                <div className="text-[10px] text-muted-foreground">Output JSON Similarity</div>
                <div className="font-mono font-bold text-emerald-400 text-sm mt-0.5">{r.outputSimilarity}</div>
                <div className="text-[10px] text-muted-foreground mt-0.5">Cosine / AST Match</div>
              </div>
              <div className="p-3 rounded bg-muted/20 border border-border/40">
                <div className="text-[10px] text-muted-foreground">Latency Parity</div>
                <div className="font-mono font-bold text-foreground text-sm mt-0.5">{r.origLat} &rarr; {r.repLat} ms</div>
                <div className="text-[10px] text-emerald-400 mt-0.5">{r.latDelta} Delta</div>
              </div>
              <div className="p-3 rounded bg-muted/20 border border-border/40">
                <div className="text-[10px] text-muted-foreground">Cost Parity</div>
                <div className="font-mono font-bold text-foreground text-sm mt-0.5">${r.origCost.toFixed(4)}</div>
                <div className="text-[10px] text-emerald-400 mt-0.5">{r.costDelta} Delta</div>
              </div>
            </div>

            <div className="text-xs text-muted-foreground flex items-center justify-between border-t border-border/40 pt-3 font-mono">
              <span>Verifier Authority Signature: <strong className="text-foreground">{r.signature}</strong></span>
              <button className="text-primary hover:underline font-medium font-sans">View Replay Bitstream &rarr;</button>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};
