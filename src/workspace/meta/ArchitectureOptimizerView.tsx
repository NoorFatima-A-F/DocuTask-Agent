import React from 'react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import {
  Layers,
  PlusCircle,
  Sparkles,
  Zap,
} from 'lucide-react';

interface ArchitectureItem {
  id: string;
  subsystem: string;
  type: string;
  description: string;
  latencySavingMs: number;
  memoryDeltaMb: number;
  confidence: number;
  status: 'PROPOSED' | 'APPROVED' | 'DEPLOYED';
}

export const ArchitectureOptimizerView: React.FC = () => {
  const optimizations: ArchitectureItem[] = [
    {
      id: 'arch-opt-601',
      subsystem: 'EVENT_BUS_AND_DAG_SCHEDULER',
      type: 'COMMUNICATION_TOPOLOGY_FLATTENING',
      description: 'Replace serial point-to-point task routing with publish-subscribe multicast channels for validator strike teams.',
      latencySavingMs: 180.0,
      memoryDeltaMb: -24.0,
      confidence: 0.985,
      status: 'DEPLOYED',
    },
    {
      id: 'arch-opt-602',
      subsystem: 'DAG_EXECUTION_ENGINE',
      type: 'DAG_REDUNDANCY_REMOVAL',
      description: 'Eliminate redundant intermediate validation nodes when cryptographic SHA-256 parent hash matches trusted schema cache.',
      latencySavingMs: 95.0,
      memoryDeltaMb: -8.0,
      confidence: 0.992,
      status: 'APPROVED',
    },
    {
      id: 'arch-opt-603',
      subsystem: 'RUNTIME_MEMORY_LAYER',
      type: 'LOCK_FREE_RING_BUFFER',
      description: 'Transition hot telemetry fact emission from synchronized mutex to atomic lock-free circular ring buffer.',
      latencySavingMs: 45.0,
      memoryDeltaMb: +12.0,
      confidence: 0.978,
      status: 'PROPOSED',
    },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold tracking-tight">Architecture Optimizer</h1>
            <Badge variant="intelligence" size="sm" hasDot isPulsing>
              STRUCTURAL REFACTORING ACTIVE
            </Badge>
            <Badge variant="outline" size="sm">
              AMRS-RSIP Phase 13.9
            </Badge>
          </div>
          <p className="text-xs text-muted-foreground mt-1">
            Continuous topological refactoring, DAG redundancy elimination, communication flattening, and memory concurrency optimization.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Button variant="intelligence" size="sm">
            <PlusCircle className="w-3.5 h-3.5 mr-1.5" />
            Propose Optimization
          </Button>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <Card className="p-4 bg-purple-950/10 border-purple-500/20">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Total Latency Saved</span>
            <Zap className="w-4 h-4 text-purple-400" />
          </div>
          <div className="text-2xl font-bold font-mono text-purple-400 mt-2">320ms / Mission</div>
          <div className="text-[11px] text-muted-foreground mt-1">Sum of structural refactors</div>
        </Card>

        <Card className="p-4 bg-emerald-950/10 border-emerald-500/20">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">RAM Footprint Delta</span>
            <Layers className="w-4 h-4 text-emerald-400" />
          </div>
          <div className="text-2xl font-bold font-mono text-emerald-400 mt-2">-20.0 MB</div>
          <div className="text-[11px] text-muted-foreground mt-1">Net memory reduction</div>
        </Card>

        <Card className="p-4 bg-blue-950/10 border-blue-500/20">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Mean Confidence</span>
            <Sparkles className="w-4 h-4 text-blue-400" />
          </div>
          <div className="text-2xl font-bold font-mono text-blue-400 mt-2">98.5%</div>
          <div className="text-[11px] text-muted-foreground mt-1">Mathematical verification score</div>
        </Card>
      </div>

      {/* Optimizations List */}
      <div className="space-y-4">
        {optimizations.map((opt) => (
          <Card key={opt.id} className="p-5 border-border/40 space-y-3 hover:border-purple-500/30 transition-colors">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
              <div className="space-y-1">
                <div className="flex items-center gap-2">
                  <span className="text-xs font-mono font-bold text-foreground">{opt.subsystem}</span>
                  <Badge
                    variant={
                      opt.status === 'DEPLOYED'
                        ? 'success'
                        : opt.status === 'APPROVED'
                        ? 'info'
                        : 'default'
                    }
                    size="sm"
                  >
                    {opt.status}
                  </Badge>
                </div>
                <span className="text-xs font-semibold text-purple-300">{opt.type.replace(/_/g, ' ')}</span>
              </div>
              <div className="flex items-center gap-2">
                <Badge variant="success" size="sm">
                  -{opt.latencySavingMs}ms Latency
                </Badge>
                <Badge variant="outline" size="sm">
                  {opt.memoryDeltaMb > 0 ? `+${opt.memoryDeltaMb}MB` : `${opt.memoryDeltaMb}MB`} RAM
                </Badge>
              </div>
            </div>

            <p className="text-xs text-muted-foreground leading-relaxed">{opt.description}</p>

            <div className="flex items-center justify-between text-xs pt-3 border-t border-border/30">
              <span className="font-mono text-muted-foreground">Confidence: {(opt.confidence * 100).toFixed(1)}%</span>
              {opt.status === 'PROPOSED' && (
                <Button variant="outline" size="sm">
                  Benchmark & Deploy
                </Button>
              )}
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};
