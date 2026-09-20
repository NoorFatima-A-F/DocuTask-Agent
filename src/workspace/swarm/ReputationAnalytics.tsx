import React, { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import {
  Award,
} from 'lucide-react';

interface ReputationScorecard {
  agentId: string;
  name: string;
  compositeScore: number;
  accuracyScore: number;
  slaAdherenceScore: number;
  collaborationQuality: number;
  governanceCompliance: number;
  evaluations: number;
}

export const ReputationAnalytics: React.FC = () => {
  const [scorecards] = useState<ReputationScorecard[]>([
    {
      agentId: 'agent-exec-01',
      name: 'Executive Director Alpha',
      compositeScore: 0.990,
      accuracyScore: 0.995,
      slaAdherenceScore: 0.990,
      collaborationQuality: 0.980,
      governanceCompliance: 1.000,
      evaluations: 142,
    },
    {
      agentId: 'agent-spec-ocr',
      name: 'Vision & OCR Specialist',
      compositeScore: 0.982,
      accuracyScore: 0.988,
      slaAdherenceScore: 0.975,
      collaborationQuality: 0.965,
      governanceCompliance: 1.000,
      evaluations: 1250,
    },
    {
      agentId: 'agent-val-sec',
      name: 'Cryptographic Security Validator',
      compositeScore: 0.994,
      accuracyScore: 0.998,
      slaAdherenceScore: 0.992,
      collaborationQuality: 0.990,
      governanceCompliance: 1.000,
      evaluations: 890,
    },
    {
      agentId: 'agent-plan-01',
      name: 'Lead DAG Planner',
      compositeScore: 0.976,
      accuracyScore: 0.980,
      slaAdherenceScore: 0.970,
      collaborationQuality: 0.960,
      governanceCompliance: 1.000,
      evaluations: 310,
    },
    {
      agentId: 'agent-res-opt',
      name: 'Resource & Token Governor',
      compositeScore: 0.964,
      accuracyScore: 0.965,
      slaAdherenceScore: 0.955,
      collaborationQuality: 0.970,
      governanceCompliance: 1.000,
      evaluations: 620,
    },
  ]);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold tracking-tight">Reputation & Trust Analytics</h1>
            <Badge variant="success" size="sm">
              MATHEMATICALLY CALIBRATED
            </Badge>
          </div>
          <p className="text-xs text-muted-foreground mt-1">
            Multi-dimensional reputation scoring across accuracy, SLA fulfillment, collaboration synergy, and zero-fabrication compliance.
          </p>
        </div>
      </div>

      {/* Scorecards Grid */}
      <div className="space-y-4">
        {scorecards.map(sc => (
          <Card key={sc.agentId} className="p-5 border-border/60 space-y-4">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-border/40 pb-3">
              <div className="flex items-center gap-2.5">
                <Award className="w-5 h-5 text-emerald-400" />
                <div>
                  <h3 className="font-bold text-sm">{sc.name}</h3>
                  <span className="text-[11px] font-mono text-muted-foreground">{sc.agentId}</span>
                </div>
              </div>

              <div className="flex items-center gap-3">
                <span className="text-xs text-muted-foreground">{sc.evaluations} Verified Missions</span>
                <div className="px-3 py-1 rounded bg-emerald-950/20 border border-emerald-500/30 text-emerald-400 font-mono font-bold text-sm">
                  {(sc.compositeScore * 100).toFixed(1)}% Score
                </div>
              </div>
            </div>

            {/* 4 Dimension Bars */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
              <div className="p-3 rounded bg-muted/20 border border-border/30">
                <div className="flex items-center justify-between text-xs mb-1.5">
                  <span className="text-muted-foreground">Accuracy</span>
                  <span className="font-mono font-bold text-emerald-400">{(sc.accuracyScore * 100).toFixed(1)}%</span>
                </div>
                <div className="w-full bg-background h-1.5 rounded-full overflow-hidden">
                  <div className="bg-emerald-400 h-full rounded-full" style={{ width: `${sc.accuracyScore * 100}%` }} />
                </div>
              </div>

              <div className="p-3 rounded bg-muted/20 border border-border/30">
                <div className="flex items-center justify-between text-xs mb-1.5">
                  <span className="text-muted-foreground">SLA Adherence</span>
                  <span className="font-mono font-bold text-blue-400">{(sc.slaAdherenceScore * 100).toFixed(1)}%</span>
                </div>
                <div className="w-full bg-background h-1.5 rounded-full overflow-hidden">
                  <div className="bg-blue-400 h-full rounded-full" style={{ width: `${sc.slaAdherenceScore * 100}%` }} />
                </div>
              </div>

              <div className="p-3 rounded bg-muted/20 border border-border/30">
                <div className="flex items-center justify-between text-xs mb-1.5">
                  <span className="text-muted-foreground">Collaboration</span>
                  <span className="font-mono font-bold text-purple-400">{(sc.collaborationQuality * 100).toFixed(1)}%</span>
                </div>
                <div className="w-full bg-background h-1.5 rounded-full overflow-hidden">
                  <div className="bg-purple-400 h-full rounded-full" style={{ width: `${sc.collaborationQuality * 100}%` }} />
                </div>
              </div>

              <div className="p-3 rounded bg-muted/20 border border-border/30">
                <div className="flex items-center justify-between text-xs mb-1.5">
                  <span className="text-muted-foreground">Compliance</span>
                  <span className="font-mono font-bold text-teal-400">{(sc.governanceCompliance * 100).toFixed(1)}%</span>
                </div>
                <div className="w-full bg-background h-1.5 rounded-full overflow-hidden">
                  <div className="bg-teal-400 h-full rounded-full" style={{ width: `${sc.governanceCompliance * 100}%` }} />
                </div>
              </div>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};
