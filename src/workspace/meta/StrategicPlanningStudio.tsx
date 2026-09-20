import React, { useState } from 'react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import {
  Compass,
  Calendar,
  Layers,
  TrendingUp,
  PlusCircle,
  Clock,
} from 'lucide-react';

interface MilestoneItem {
  id: string;
  phase: string;
  timeframe: string;
  title: string;
  objective: string;
  targetGain: string;
  status: 'COMPLETED' | 'IN_PROGRESS' | 'SCHEDULED';
  risk: 'LOW' | 'MEDIUM' | 'HIGH';
}

export const StrategicPlanningStudio: React.FC = () => {
  const [horizonFilter, setHorizonFilter] = useState<'ALL' | 'MULTI_HOUR' | 'MULTI_DAY' | 'MULTI_WEEK'>('ALL');

  const milestones: MilestoneItem[] = [
    {
      id: 'mls-01',
      phase: 'Phase 1: Dynamic Partitioning',
      timeframe: 'T+2 Hours',
      title: 'Dynamic Fan-Out DAG Sub-Scheduler',
      objective: 'Split multi-page invoice documents into concurrent child DAG tasks executed across specialist swarm agents.',
      targetGain: '+38.5% Latency Reduction',
      status: 'COMPLETED',
      risk: 'LOW',
    },
    {
      id: 'mls-02',
      phase: 'Phase 2: Embedding Caching',
      timeframe: 'T+1 Day',
      title: 'Speculative Token Cache Layer',
      objective: 'Deploy in-memory zero-copy cache for recurrent invoice table templates and common document schemas.',
      targetGain: '+22.0% Compute Savings',
      status: 'IN_PROGRESS',
      risk: 'MEDIUM',
    },
    {
      id: 'mls-03',
      phase: 'Phase 3: Autonomous Coalition',
      timeframe: 'T+3 Days',
      title: 'Dynamic Strike Team Formation',
      objective: 'Autonomously compose multi-agent verification strike teams for complex multi-column balance sheets.',
      targetGain: '+45.0% Throughput',
      status: 'SCHEDULED',
      risk: 'LOW',
    },
    {
      id: 'mls-04',
      phase: 'Phase 4: Invariant Audit',
      timeframe: 'T+7 Days',
      title: 'Cryptographic SHA-256 Ledger Hardening',
      objective: 'Enforce dual-signature threshold voting on all policy evolutionary changes across the runtime operating system.',
      targetGain: '100% Anti-Usurpation Invariant',
      status: 'SCHEDULED',
      risk: 'LOW',
    },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold tracking-tight">Strategic Planning Studio</h1>
            <Badge variant="intelligence" size="sm" hasDot isPulsing>
              LONG-HORIZON ROADMAP ACTIVE
            </Badge>
            <Badge variant="outline" size="sm">
              Multi-Stage Planning
            </Badge>
          </div>
          <p className="text-xs text-muted-foreground mt-1">
            Formulation, Pareto front evaluation, and milestone execution for multi-hour, multi-day, and multi-week strategic roadmaps.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Button variant="outline" size="sm">
            <Calendar className="w-3.5 h-3.5 mr-1.5" />
            Recalculate Horizons
          </Button>
          <Button variant="intelligence" size="sm">
            <PlusCircle className="w-3.5 h-3.5 mr-1.5" />
            Formulate New Roadmap
          </Button>
        </div>
      </div>

      {/* Strategic Roadmap Banner */}
      <Card className="p-5 bg-gradient-to-r from-blue-950/30 via-purple-950/20 to-background border-blue-500/30 space-y-3">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
          <div className="flex items-center gap-3">
            <div className="p-2.5 bg-blue-500/10 rounded-lg border border-blue-500/20 text-blue-400">
              <Compass className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-sm font-bold text-foreground">
                Enterprise Autonomous Platform High-Throughput & Zero-Fabrication Roadmap
              </h2>
              <p className="text-xs text-muted-foreground">
                Primary Goal: Sub-200ms Document Processing with Verifiable Cryptographic Zero-Fabrication Guarantees
              </p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <Badge variant="success" size="sm">Pareto Frontier Optimal</Badge>
            <Badge variant="outline" size="sm">Confidence 98.5%</Badge>
          </div>
        </div>

        {/* Milestone Progress Bar */}
        <div className="space-y-1.5 pt-2">
          <div className="flex justify-between text-xs text-muted-foreground">
            <span>Overall Roadmap Completion</span>
            <span className="font-mono text-foreground font-semibold">50% Complete</span>
          </div>
          <div className="h-2 w-full bg-secondary/50 rounded-full overflow-hidden">
            <div className="h-full bg-gradient-to-r from-blue-500 to-purple-500 w-1/2 rounded-full transition-all duration-500" />
          </div>
        </div>
      </Card>

      {/* Horizon Filter Tabs */}
      <div className="flex items-center gap-2 border-b border-border/40 pb-2">
        {(['ALL', 'MULTI_HOUR', 'MULTI_DAY', 'MULTI_WEEK'] as const).map((h) => (
          <Button
            key={h}
            variant={horizonFilter === h ? 'primary' : 'ghost'}
            size="sm"
            onClick={() => setHorizonFilter(h)}
          >
            {h.replace('_', ' ')}
          </Button>
        ))}
      </div>

      {/* Milestone Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {milestones.map((m) => (
          <Card
            key={m.id}
            className={`p-5 border transition-all ${
              m.status === 'COMPLETED'
                ? 'border-emerald-500/30 bg-emerald-950/10'
                : m.status === 'IN_PROGRESS'
                ? 'border-blue-500/30 bg-blue-950/10'
                : 'border-border/40 bg-secondary/10'
            }`}
          >
            <div className="flex items-start justify-between gap-2">
              <div className="space-y-1">
                <span className="text-[11px] font-mono text-muted-foreground">{m.phase}</span>
                <h3 className="text-sm font-semibold text-foreground">{m.title}</h3>
              </div>
              <Badge
                variant={
                  m.status === 'COMPLETED'
                    ? 'success'
                    : m.status === 'IN_PROGRESS'
                    ? 'info'
                    : 'default'
                }
                size="sm"
              >
                {m.status}
              </Badge>
            </div>

            <p className="text-xs text-muted-foreground my-3">{m.objective}</p>

            <div className="flex items-center justify-between text-xs pt-3 border-t border-border/30">
              <div className="flex items-center gap-1.5 text-purple-400 font-mono">
                <TrendingUp className="w-3.5 h-3.5" />
                <span>{m.targetGain}</span>
              </div>
              <div className="flex items-center gap-1 text-muted-foreground font-mono">
                <Clock className="w-3.5 h-3.5" />
                <span>{m.timeframe}</span>
              </div>
            </div>
          </Card>
        ))}
      </div>

      {/* Pareto Strategy Matrix */}
      <Card className="p-5 border-border/40 space-y-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Layers className="w-4 h-4 text-purple-400" />
            <h2 className="text-base font-semibold">Pareto Optimization Strategy Frontier</h2>
          </div>
          <Badge variant="outline" size="sm">
            Optimal Configuration
          </Badge>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <div className="p-3.5 rounded-lg border border-purple-500/20 bg-purple-950/10 space-y-1">
            <span className="text-xs text-muted-foreground">Throughput Acceleration</span>
            <div className="text-xl font-bold font-mono text-purple-400">+45.0%</div>
            <span className="text-[11px] text-muted-foreground">Parallel sub-DAG execution</span>
          </div>

          <div className="p-3.5 rounded-lg border border-emerald-500/20 bg-emerald-950/10 space-y-1">
            <span className="text-xs text-muted-foreground">Compute Cost Reduction</span>
            <div className="text-xl font-bold font-mono text-emerald-400">-22.0%</div>
            <span className="text-[11px] text-muted-foreground">Embedding cache hits</span>
          </div>

          <div className="p-3.5 rounded-lg border border-blue-500/20 bg-blue-950/10 space-y-1">
            <span className="text-xs text-muted-foreground">Zero-Fabrication Floor</span>
            <div className="text-xl font-bold font-mono text-blue-400">99.8%</div>
            <span className="text-[11px] text-muted-foreground">Triadic consensus verification</span>
          </div>
        </div>
      </Card>
    </div>
  );
};
