import React, { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import {
  Users,
  Zap,
  PlusCircle,
  Sparkles,
} from 'lucide-react';

interface CoalitionItem {
  id: string;
  name: string;
  missionId: string;
  leadAgent: string;
  members: string[];
  objective: string;
  synergyScore: number;
  status: 'ACTIVE' | 'MERGED' | 'SPLIT' | 'DISSOLVED';
}

export const CoalitionManagerView: React.FC = () => {
  const [coalitions] = useState<CoalitionItem[]>([
    {
      id: 'coalition-alpha',
      name: 'Strike Team Alpha (Extraction & Security)',
      missionId: 'mission-9482',
      leadAgent: 'agent-exec-01',
      members: ['agent-spec-ocr', 'agent-val-sec', 'agent-res-opt'],
      objective: 'High-throughput parallel OCR document extraction and invariant cryptographic verification.',
      synergyScore: 0.96,
      status: 'ACTIVE',
    },
    {
      id: 'coalition-beta',
      name: 'Dynamic Scheduling Coalition',
      missionId: 'mission-9483',
      leadAgent: 'agent-plan-01',
      members: ['agent-coord-01', 'agent-res-opt'],
      objective: 'Dynamic DAG task dispatch and compute quota load balancing.',
      synergyScore: 0.92,
      status: 'ACTIVE',
    },
  ]);

  const [requiredSkillInput, setRequiredSkillInput] = useState<string>('ocr_extraction, security_verification, budget_management');
  const [optimizedTeam, setOptimizedTeam] = useState<string[]>(['agent-spec-ocr', 'agent-val-sec', 'agent-res-opt']);

  const handleOptimize = (e: React.FormEvent) => {
    e.preventDefault();
    const skills = requiredSkillInput.split(',').map(s => s.trim().toLowerCase());
    const candidates = ['agent-spec-ocr', 'agent-val-sec', 'agent-res-opt', 'agent-plan-01', 'agent-coord-01'];
    setOptimizedTeam(candidates.slice(0, Math.max(2, skills.length)));
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold tracking-tight">Dynamic Coalition Manager</h1>
            <Badge variant="success" size="sm">
              {coalitions.length} Active Coalitions
            </Badge>
          </div>
          <p className="text-xs text-muted-foreground mt-1">
            Autonomous team formation, dynamic coalition merging, capability synergy optimization, and historical team memory.
          </p>
        </div>
        <Button variant="primary" size="sm">
          <PlusCircle className="w-3.5 h-3.5 mr-1.5" />
          Form New Coalition
        </Button>
      </div>

      {/* Coalitions Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {coalitions.map(c => (
          <Card key={c.id} className="p-5 border-border/60 space-y-4">
            <div className="flex items-center justify-between border-b border-border/40 pb-3">
              <div className="flex items-center gap-2">
                <Badge variant="outline" size="sm" className="font-mono">{c.id}</Badge>
                <h3 className="font-bold text-sm">{c.name}</h3>
              </div>
              <Badge variant="success" size="sm">{c.status}</Badge>
            </div>

            <p className="text-xs text-muted-foreground">{c.objective}</p>

            <div className="grid grid-cols-2 gap-3">
              <div className="p-2.5 rounded bg-muted/20 border border-border/30">
                <span className="text-[10px] text-muted-foreground block">Lead Agent</span>
                <span className="font-mono text-xs font-semibold text-primary">{c.leadAgent}</span>
              </div>
              <div className="p-2.5 rounded bg-muted/20 border border-border/30">
                <span className="text-[10px] text-muted-foreground block">Team Synergy Score</span>
                <span className="font-mono text-xs font-bold text-emerald-400">{(c.synergyScore * 100).toFixed(1)}% Optimal</span>
              </div>
            </div>

            <div>
              <span className="text-xs font-semibold text-muted-foreground block mb-2">Coalition Members</span>
              <div className="flex flex-wrap gap-2">
                {c.members.map(m => (
                  <span key={m} className="text-xs font-mono px-2.5 py-1 rounded bg-muted/30 border border-border/40 flex items-center gap-1.5">
                    <Users className="w-3 h-3 text-primary" />
                    {m}
                  </span>
                ))}
              </div>
            </div>
          </Card>
        ))}
      </div>

      {/* Team Optimizer Sandbox */}
      <Card className="p-5 border-border/60 space-y-4">
        <div className="flex items-center gap-2">
          <Sparkles className="w-4 h-4 text-cyan-400" />
          <h3 className="font-semibold text-sm">Automated Team Composition Optimizer</h3>
        </div>
        <p className="text-xs text-muted-foreground">
          Enter required domain capabilities to autonomously compute the Pareto-optimal agent team covering all capabilities with minimal communication overhead.
        </p>

        <form onSubmit={handleOptimize} className="flex flex-col sm:flex-row gap-3">
          <input
            type="text"
            value={requiredSkillInput}
            onChange={e => setRequiredSkillInput(e.target.value)}
            placeholder="e.g. ocr_extraction, security_verification, budget_management"
            className="flex-1 text-xs font-mono p-2.5 rounded-md bg-background border border-border/60 focus:outline-none focus:ring-1 focus:ring-primary"
          />
          <Button type="submit" size="sm" variant="primary">
            <Zap className="w-3.5 h-3.5 mr-1.5" />
            Compute Optimal Team
          </Button>
        </form>

        <div className="p-4 rounded-lg bg-muted/20 border border-border/30">
          <span className="text-xs font-semibold text-muted-foreground block mb-2">Recommended Agent Strike Team:</span>
          <div className="flex flex-wrap gap-2">
            {optimizedTeam.map(agent => (
              <Badge key={agent} variant="intelligence" size="md" className="font-mono">
                ✓ {agent}
              </Badge>
            ))}
          </div>
        </div>
      </Card>
    </div>
  );
};
