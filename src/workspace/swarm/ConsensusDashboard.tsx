import React, { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import {
  ShieldCheck,
  Lock,
} from 'lucide-react';

interface ConsensusSession {
  id: string;
  topic: string;
  mode: string;
  winningOutcome: string;
  totalVotes: number;
  quorumReached: boolean;
  consensusRatio: number;
  signature: string;
  finalizedAt: string;
  votes: Array<{ agentId: string; choice: string; weight: number; confidence: number }>;
}

export const ConsensusDashboard: React.FC = () => {
  const [sessions] = useState<ConsensusSession[]>([
    {
      id: 'cns-001',
      topic: 'UPGRADE_EXTRACTION_MODEL_V2',
      mode: 'WEIGHTED_REPUTATION',
      winningOutcome: 'APPROVE',
      totalVotes: 3,
      quorumReached: true,
      consensusRatio: 1.0,
      signature: 'a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8',
      finalizedAt: '14:22:06.210',
      votes: [
        { agentId: 'agent-exec-01', choice: 'APPROVE', weight: 1.0, confidence: 0.99 },
        { agentId: 'agent-plan-01', choice: 'APPROVE', weight: 1.0, confidence: 0.98 },
        { agentId: 'agent-val-sec', choice: 'APPROVE', weight: 1.2, confidence: 0.99 },
      ],
    },
    {
      id: 'cns-002',
      topic: 'VERIFY_SCHEMA_INVARIANT_MISSION_9482',
      mode: 'CONFIDENCE_WEIGHTED',
      winningOutcome: 'APPROVED',
      totalVotes: 4,
      quorumReached: true,
      consensusRatio: 0.98,
      signature: 'f1e2d3c4b5a6f7e8d9c0b1a2f3e4d5c6b7a8f9e0d1c2b3a4f5e6d7c8b9a0f1e2',
      finalizedAt: '14:22:06.550',
      votes: [
        { agentId: 'agent-spec-ocr', choice: 'APPROVED', weight: 1.0, confidence: 0.985 },
        { agentId: 'agent-val-sec', choice: 'APPROVED', weight: 1.5, confidence: 0.995 },
        { agentId: 'agent-res-opt', choice: 'APPROVED', weight: 0.9, confidence: 0.960 },
        { agentId: 'agent-coord-01', choice: 'APPROVED', weight: 1.0, confidence: 0.970 },
      ],
    },
  ]);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold tracking-tight">Consensus & Voting Engine</h1>
            <Badge variant="success" size="sm">
              100% Quorum Satisfied
            </Badge>
          </div>
          <p className="text-xs text-muted-foreground mt-1">
            Decentralized multi-agent consensus with weighted reputation scoring, Byzantine fault tolerance, and cryptographic decision proofs.
          </p>
        </div>
      </div>

      {/* Consensus Sessions List */}
      <div className="space-y-4">
        {sessions.map(s => (
          <Card key={s.id} className="p-5 border-border/60 space-y-4">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-border/40 pb-3">
              <div className="flex items-center gap-2">
                <Badge variant="outline" size="sm" className="font-mono">{s.id}</Badge>
                <h3 className="font-bold text-sm">{s.topic}</h3>
              </div>
              <div className="flex items-center gap-2">
                <Badge variant="intelligence" size="sm">{s.mode}</Badge>
                <Badge variant="success" size="sm">WINNER: {s.winningOutcome}</Badge>
              </div>
            </div>

            {/* Voting Metrics */}
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
              <div className="p-3 rounded bg-muted/20 border border-border/30">
                <span className="text-[11px] text-muted-foreground block">Consensus Ratio</span>
                <span className="text-xl font-bold font-mono text-emerald-400">
                  {(s.consensusRatio * 100).toFixed(1)}% Affirmative
                </span>
              </div>
              <div className="p-3 rounded bg-muted/20 border border-border/30">
                <span className="text-[11px] text-muted-foreground block">Quorum Status</span>
                <span className="text-xl font-bold font-mono text-blue-400">
                  {s.quorumReached ? 'Quorum Met' : 'Quorum Pending'}
                </span>
              </div>
              <div className="p-3 rounded bg-muted/20 border border-border/30">
                <span className="text-[11px] text-muted-foreground block">Total Ballots Cast</span>
                <span className="text-xl font-bold font-mono text-purple-400">
                  {s.totalVotes} Verified Votes
                </span>
              </div>
            </div>

            {/* Ballot Breakdown */}
            <div>
              <span className="text-xs font-semibold text-muted-foreground block mb-2">Verified Agent Ballots</span>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                {s.votes.map(v => (
                  <div key={v.agentId} className="flex items-center justify-between p-2.5 rounded bg-muted/10 border border-border/20 text-xs font-mono">
                    <div className="flex items-center gap-2">
                      <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />
                      <span className="font-semibold">{v.agentId}</span>
                    </div>
                    <div className="flex items-center gap-3">
                      <span className="text-muted-foreground">Weight: {v.weight}</span>
                      <span className="text-emerald-400 font-bold">{v.choice}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Signature Proof */}
            <div className="p-2 rounded bg-background/80 border border-border/30 text-[10px] font-mono text-muted-foreground flex items-center gap-2">
              <Lock className="w-3 h-3 text-primary shrink-0" />
              <span className="truncate">Decision Merkle Signature: {s.signature}</span>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};
