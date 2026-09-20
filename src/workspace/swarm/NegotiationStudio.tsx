import React, { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import {
  Scale,
  Handshake,
  Lock,
  ArrowRightLeft,
} from 'lucide-react';

interface AgreementRecord {
  id: string;
  topic: string;
  initiator: string;
  receiver: string;
  costUsd: number;
  latencyMs: number;
  confidence: number;
  rounds: number;
  sha256Hash: string;
  signedAt: string;
}

export const NegotiationStudio: React.FC = () => {
  const [agreements] = useState<AgreementRecord[]>([
    {
      id: 'agr-001',
      topic: 'OCR_BURST_QUOTA_AND_SLA',
      initiator: 'agent-coord-01',
      receiver: 'agent-spec-ocr',
      costUsd: 0.032,
      latencyMs: 160.0,
      confidence: 0.985,
      rounds: 2,
      sha256Hash: '9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08',
      signedAt: '14:22:04.110',
    },
    {
      id: 'agr-002',
      topic: 'SECURITY_AUDIT_THROUGHPUT',
      initiator: 'agent-plan-01',
      receiver: 'agent-val-sec',
      costUsd: 0.015,
      latencyMs: 90.0,
      confidence: 0.999,
      rounds: 1,
      sha256Hash: '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8',
      signedAt: '14:22:04.450',
    },
    {
      id: 'agr-003',
      topic: 'TOKEN_RATE_LIMIT_ARBITRATION',
      initiator: 'agent-res-opt',
      receiver: 'agent-coord-01',
      costUsd: 0.008,
      latencyMs: 50.0,
      confidence: 0.970,
      rounds: 3,
      sha256Hash: '4b227777d4dd1fc61c6f884f48641d02b4d121d3fd328cb08b5531fcacdabf8a',
      signedAt: '14:22:04.890',
    },
  ]);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold tracking-tight">Autonomous Negotiation Studio</h1>
            <Badge variant="success" size="sm">
              {agreements.length} Agreements Settled
            </Badge>
          </div>
          <p className="text-xs text-muted-foreground mt-1">
            Multi-objective Pareto bargaining over compute cost, latency, and confidence with immutable SHA-256 agreement ledgers.
          </p>
        </div>
      </div>

      {/* Bargaining Concept Visualizer */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        <Card className="p-4 bg-purple-950/10 border-purple-500/20">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-muted-foreground">Demands & Concessions</span>
            <Scale className="w-4 h-4 text-purple-400" />
          </div>
          <div className="text-xl font-bold font-mono text-purple-400 mt-2">Pareto Optimal</div>
          <p className="text-[11px] text-muted-foreground mt-1">Bargaining engine computes 10% concession steps per round.</p>
        </Card>

        <Card className="p-4 bg-emerald-950/10 border-emerald-500/20">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-muted-foreground">Conflict Resolution</span>
            <Handshake className="w-4 h-4 text-emerald-400" />
          </div>
          <div className="text-xl font-bold font-mono text-emerald-400 mt-2">Zero Deadlock</div>
          <p className="text-[11px] text-muted-foreground mt-1">Reputation-weighted arbitration resolves concurrent resource claims.</p>
        </Card>

        <Card className="p-4 bg-blue-950/10 border-blue-500/20">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-muted-foreground">Agreement Ledger</span>
            <Lock className="w-4 h-4 text-blue-400" />
          </div>
          <div className="text-xl font-bold font-mono text-blue-400 mt-2">SHA-256 Chained</div>
          <p className="text-[11px] text-muted-foreground mt-1">Every agreed contract is cryptographically signed and hash-chained.</p>
        </Card>
      </div>

      {/* Agreements Table */}
      <Card className="p-5 border-border/60">
        <h3 className="font-semibold text-sm mb-4">Settled Negotiation Agreements</h3>
        <div className="space-y-3">
          {agreements.map(a => (
            <div key={a.id} className="p-4 rounded-lg bg-muted/20 border border-border/40 space-y-3">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                <div className="flex items-center gap-2">
                  <Badge variant="outline" size="sm" className="font-mono">{a.id}</Badge>
                  <span className="font-bold text-xs">{a.topic}</span>
                </div>
                <div className="flex items-center gap-2">
                  <Badge variant="success" size="sm">SETTLED IN {a.rounds} ROUNDS</Badge>
                  <span className="text-[11px] font-mono text-muted-foreground">{a.signedAt}</span>
                </div>
              </div>

              <div className="flex items-center gap-2 text-xs font-mono text-muted-foreground">
                <span className="font-semibold text-foreground">{a.initiator}</span>
                <ArrowRightLeft className="w-3.5 h-3.5 text-primary" />
                <span className="font-semibold text-foreground">{a.receiver}</span>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs font-mono">
                <div className="p-2 rounded bg-background/50 border border-border/30">
                  <span className="text-[10px] text-muted-foreground block">Agreed Compute Cost</span>
                  <span className="font-bold text-emerald-400">${a.costUsd} USD</span>
                </div>
                <div className="p-2 rounded bg-background/50 border border-border/30">
                  <span className="text-[10px] text-muted-foreground block">Agreed Max Latency</span>
                  <span className="font-bold text-blue-400">{a.latencyMs} ms</span>
                </div>
                <div className="p-2 rounded bg-background/50 border border-border/30">
                  <span className="text-[10px] text-muted-foreground block">Confidence Floor</span>
                  <span className="font-bold text-purple-400">{(a.confidence * 100).toFixed(1)}%</span>
                </div>
              </div>

              <div className="p-2 rounded bg-background/70 border border-border/30 text-[10px] font-mono text-muted-foreground flex items-center gap-2">
                <Lock className="w-3 h-3 text-primary shrink-0" />
                <span className="truncate">SHA-256 Ledger Hash: {a.sha256Hash}</span>
              </div>
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
};
