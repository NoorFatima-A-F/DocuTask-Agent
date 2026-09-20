import React, { useState } from 'react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import {
  Brain,
  Sparkles,
  AlertTriangle,
  ArrowRight,
  RefreshCw,
  Zap,
  Target,
  Search,
  CheckCircle2,
} from 'lucide-react';

interface BottleneckItem {
  id: string;
  subsystem: string;
  type: string;
  severity: 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW';
  rootCause: string;
  impactMs: number;
  mitigation: string;
}

interface StrategicAlternativeItem {
  id: string;
  title: string;
  description: string;
  latencyGainPct: number;
  costReductionPct: number;
  confidence: number;
  tradeoffs: string[];
}

export const MetaReasoningCenter: React.FC = () => {
  const selectedGoal = 'Process 500 Enterprise Invoice Documents within $50 compute budget and 30s SLA';
  const [isSynthesizing, setIsSynthesizing] = useState<boolean>(false);
  const [searchFilter, setSearchFilter] = useState<string>('');

  const bottlenecks: BottleneckItem[] = [
    {
      id: 'btn-991',
      subsystem: 'OCR_EXTRACTION_PIPELINE',
      type: 'DEPENDENCY_SERIALIZATION',
      severity: 'HIGH',
      rootCause: 'Sequential page parsing in DAG without chunk partitioning',
      impactMs: 450,
      mitigation: 'Implement dynamic chunk fan-out across specialist swarm agents',
    },
    {
      id: 'btn-992',
      subsystem: 'CONSENSUS_QUORUM',
      type: 'GOVERNANCE_OVERHEAD',
      severity: 'MEDIUM',
      rootCause: 'Repeated cryptographic signature verification on static schemas',
      impactMs: 85,
      mitigation: 'Cache validated schema signatures in zero-trust memory layer',
    },
    {
      id: 'btn-993',
      subsystem: 'EVENT_BUS_ROUTER',
      type: 'RESOURCE_QUOTA',
      severity: 'LOW',
      rootCause: 'High burst event queuing during peak multi-page ingestion',
      impactMs: 35,
      mitigation: 'Dynamic memory buffer pool expansion up to 512MB',
    },
  ];

  const alternatives: StrategicAlternativeItem[] = [
    {
      id: 'alt-101',
      title: 'Dynamic DAG Chunk Fan-Out',
      description: 'Split multi-page documents into isolated sub-DAG tasks executed in parallel across available specialist agents.',
      latencyGainPct: 42.5,
      costReductionPct: 15.0,
      confidence: 0.982,
      tradeoffs: ['Requires 15% higher burst RAM allocation during peak load'],
    },
    {
      id: 'alt-102',
      title: 'Speculative Token Cache',
      description: 'Pre-compute and cache token embeddings for recurring corporate vendor invoice templates.',
      latencyGainPct: 28.0,
      costReductionPct: 22.0,
      confidence: 0.965,
      tradeoffs: ['Requires 150MB hot RAM cache reservation'],
    },
    {
      id: 'alt-103',
      title: 'Adaptive Specialist Auction Routing',
      description: 'Route complex balance sheet tables to high-reputation mathematical verification agents automatically.',
      latencyGainPct: 19.5,
      costReductionPct: 8.5,
      confidence: 0.991,
      tradeoffs: ['Slightly higher consensus voting latency (+15ms)'],
    },
  ];

  const handleSynthesize = () => {
    setIsSynthesizing(true);
    setTimeout(() => {
      setIsSynthesizing(false);
    }, 1200);
  };

  const filteredBottlenecks = bottlenecks.filter(
    (b) =>
      b.subsystem.toLowerCase().includes(searchFilter.toLowerCase()) ||
      b.rootCause.toLowerCase().includes(searchFilter.toLowerCase())
  );

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold tracking-tight">Meta-Reasoning Center</h1>
            <Badge variant="intelligence" size="sm" hasDot isPulsing>
              META-COGNITION ACTIVE
            </Badge>
            <Badge variant="outline" size="sm">
              AMRS-RSIP Phase 13.9
            </Badge>
          </div>
          <p className="text-xs text-muted-foreground mt-1">
            Autonomous goal abstraction, intent inference, systemic bottleneck detection, and counterfactual strategy formulation.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Button variant="outline" size="sm" onClick={handleSynthesize} disabled={isSynthesizing}>
            <RefreshCw className={`w-3.5 h-3.5 mr-1.5 ${isSynthesizing ? 'animate-spin' : ''}`} />
            {isSynthesizing ? 'Synthesizing...' : 'Re-synthesize Graph'}
          </Button>
          <Button variant="intelligence" size="sm">
            <Sparkles className="w-3.5 h-3.5 mr-1.5" />
            Trigger Deep Meta-Reasoning
          </Button>
        </div>
      </div>

      {/* Goal Abstraction Banner */}
      <Card className="p-5 bg-gradient-to-r from-purple-950/30 via-indigo-950/20 to-background border-purple-500/30">
        <div className="flex items-start gap-4">
          <div className="p-3 bg-purple-500/10 rounded-xl border border-purple-500/20 text-purple-400">
            <Brain className="w-6 h-6" />
          </div>
          <div className="space-y-1.5 flex-1">
            <div className="flex items-center gap-2">
              <span className="text-xs font-semibold text-purple-400 uppercase tracking-wider">Active Goal Abstraction</span>
              <Badge variant="success" size="sm">Confidence 98.4%</Badge>
            </div>
            <p className="text-sm font-medium text-foreground">{selectedGoal}</p>
            <div className="flex flex-wrap items-center gap-4 text-xs text-muted-foreground pt-1">
              <span>Abstracted Intent: <strong className="text-foreground">Maximize Multi-Document Throughput under Hard Budget Ceiling</strong></span>
              <span>•</span>
              <span>Decomposition Horizon: <strong className="text-purple-400">Multi-Stage Speculative DAG</strong></span>
            </div>
          </div>
        </div>
      </Card>

      {/* KPI Stats */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card className="p-4 bg-purple-950/10 border-purple-500/20">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Meta-Cognitive Depth</span>
            <Brain className="w-4 h-4 text-purple-400" />
          </div>
          <div className="text-2xl font-bold font-mono text-purple-400 mt-2">7 Tiers</div>
          <div className="text-[11px] text-muted-foreground mt-1">Hierarchical recursive critique active</div>
        </Card>

        <Card className="p-4 bg-amber-950/10 border-amber-500/20">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Active Bottlenecks</span>
            <AlertTriangle className="w-4 h-4 text-amber-400" />
          </div>
          <div className="text-2xl font-bold font-mono text-amber-400 mt-2">{bottlenecks.length} Detected</div>
          <div className="text-[11px] text-muted-foreground mt-1">1 Critical serialization pattern</div>
        </Card>

        <Card className="p-4 bg-emerald-950/10 border-emerald-500/20">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Predicted Throughput Gain</span>
            <Zap className="w-4 h-4 text-emerald-400" />
          </div>
          <div className="text-2xl font-bold font-mono text-emerald-400 mt-2">+42.5%</div>
          <div className="text-[11px] text-muted-foreground mt-1">Validated via replay simulation</div>
        </Card>

        <Card className="p-4 bg-blue-950/10 border-blue-500/20">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Pareto Optimization Score</span>
            <Target className="w-4 h-4 text-blue-400" />
          </div>
          <div className="text-2xl font-bold font-mono text-blue-400 mt-2">0.985 / 1.0</div>
          <div className="text-[11px] text-muted-foreground mt-1">Optimal latency-cost frontier</div>
        </Card>
      </div>

      {/* Main Grid: Bottlenecks & Strategic Alternatives */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Identified Systemic Bottlenecks */}
        <Card className="p-5 border-border/40 space-y-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <AlertTriangle className="w-4 h-4 text-amber-400" />
              <h2 className="text-base font-semibold">Detected Systemic Bottlenecks</h2>
            </div>
            <div className="relative w-48">
              <Search className="w-3.5 h-3.5 absolute left-2.5 top-2.5 text-muted-foreground" />
              <input
                type="text"
                value={searchFilter}
                onChange={(e) => setSearchFilter(e.target.value)}
                placeholder="Filter bottlenecks..."
                className="w-full bg-secondary/50 text-xs rounded-md pl-8 pr-2 py-1.5 border border-border/40 focus:outline-none focus:border-primary"
              />
            </div>
          </div>

          <div className="space-y-3">
            {filteredBottlenecks.map((btn) => (
              <div
                key={btn.id}
                className="p-3.5 rounded-lg border border-border/40 bg-secondary/20 hover:bg-secondary/40 transition-colors space-y-2"
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-mono font-bold text-foreground">{btn.subsystem}</span>
                    <Badge
                      variant={
                        btn.severity === 'CRITICAL'
                          ? 'error'
                          : btn.severity === 'HIGH'
                          ? 'warning'
                          : 'default'
                      }
                      size="sm"
                    >
                      {btn.severity}
                    </Badge>
                  </div>
                  <span className="text-xs font-mono text-amber-400">+{btn.impactMs}ms impact</span>
                </div>
                <p className="text-xs text-muted-foreground">{btn.rootCause}</p>
                <div className="flex items-center gap-1.5 text-xs text-purple-400 bg-purple-500/10 p-2 rounded border border-purple-500/20">
                  <ArrowRight className="w-3.5 h-3.5 flex-shrink-0" />
                  <span>Mitigation: {btn.mitigation}</span>
                </div>
              </div>
            ))}
          </div>
        </Card>

        {/* Counterfactual Strategic Alternatives */}
        <Card className="p-5 border-border/40 space-y-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Sparkles className="w-4 h-4 text-purple-400" />
              <h2 className="text-base font-semibold">Synthesized Strategic Alternatives</h2>
            </div>
            <Badge variant="outline" size="sm">
              Pareto Evaluated
            </Badge>
          </div>

          <div className="space-y-3">
            {alternatives.map((alt) => (
              <div
                key={alt.id}
                className="p-3.5 rounded-lg border border-purple-500/20 bg-purple-950/10 hover:bg-purple-950/20 transition-colors space-y-2.5"
              >
                <div className="flex items-center justify-between">
                  <span className="text-xs font-semibold text-purple-300">{alt.title}</span>
                  <div className="flex items-center gap-2">
                    <Badge variant="success" size="sm">+{alt.latencyGainPct}% Speed</Badge>
                    <Badge variant="info" size="sm">-{alt.costReductionPct}% Cost</Badge>
                  </div>
                </div>
                <p className="text-xs text-muted-foreground">{alt.description}</p>
                <div className="flex items-center justify-between text-xs pt-1 border-t border-border/30">
                  <div className="flex items-center gap-1 text-muted-foreground">
                    <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                    <span>Confidence: {(alt.confidence * 100).toFixed(1)}%</span>
                  </div>
                  <Button variant="outline" size="sm">
                    Formulate Plan
                  </Button>
                </div>
              </div>
            ))}
          </div>
        </Card>
      </div>
    </div>
  );
};
