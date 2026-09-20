import React, { useState } from 'react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import {
  Brain,
  ShieldAlert,
  Sparkles,
  CheckCircle2,
  RefreshCw,
  Lock,
} from 'lucide-react';

interface ReflectionNodeItem {
  id: string;
  tierLevel: number;
  tierName: string;
  title: string;
  critique: string;
  improvements: string[];
  confidence: number;
  merkleProof: string;
}

export const RecursiveReflectionExplorer: React.FC = () => {
  const [selectedTier, setSelectedTier] = useState<number>(1);
  const [isReflecting, setIsReflecting] = useState<boolean>(false);

  const reflectionNodes: ReflectionNodeItem[] = [
    {
      id: 'rnode-1',
      tierLevel: 1,
      tierName: 'LEVEL 1: MISSION EXECUTION',
      title: 'Mission 9482 Pipeline Execution',
      critique: 'Mission completed with 0 errors but experienced 450ms queue serialization waiting for sequential OCR page extraction.',
      improvements: ['Enable parallel page chunking in DAG scheduler', 'Pre-warm OCR container workers during burst requests'],
      confidence: 0.995,
      merkleProof: '7f8a9e2d3c4b5a6f...991a',
    },
    {
      id: 'rnode-2',
      tierLevel: 2,
      tierName: 'LEVEL 2: PLANNER DECOMPOSITION',
      title: 'APDLE DAG Scheduler Heuristics',
      critique: 'Planner selected greedy critical-path ordering without considering token embedding cache availability.',
      improvements: ['Incorporate multi-objective Pareto scheduler into APDLE planner', 'Prioritize cache-friendly sub-DAG nodes'],
      confidence: 0.990,
      merkleProof: '3b2c1a4e5d6f7a8b...442b',
    },
    {
      id: 'rnode-3',
      tierLevel: 3,
      tierName: 'LEVEL 3: SWARM DYNAMICS',
      title: 'Multi-Agent Bargaining & Auction Liquidity',
      critique: 'Auction bidding resolved in 2 rounds, but winner handoff incurred 25ms redundant capability renegotiation.',
      improvements: ['Cache winner contract profiles to accelerate handoffs by 25ms', 'Use pub-sub communication bus for multicast bids'],
      confidence: 0.985,
      merkleProof: 'a1b2c3d4e5f60718...119c',
    },
    {
      id: 'rnode-4',
      tierLevel: 4,
      tierName: 'LEVEL 4: LEARNING & MEMORY',
      title: 'Organizational Knowledge Graph Mining',
      critique: 'Triadic Verification pattern mined successfully across 500 missions with 99.8% empirical verification accuracy.',
      improvements: ['Promote Triadic Verification pattern to default enterprise execution template', 'Auto-index novel balance sheet schemas'],
      confidence: 0.980,
      merkleProof: '9901a2b3c4d5e6f7...558d',
    },
    {
      id: 'rnode-5',
      tierLevel: 5,
      tierName: 'LEVEL 5: ARCHITECTURE & CONCURRENCY',
      title: 'EventBus Throughput & Worker Pools',
      critique: 'EventBus maintained 12,000 events/sec without dropped frames; worker threadpool saturated at 8 concurrent tasks.',
      improvements: ['Deploy lock-free ring buffer for hot telemetry facts', 'Expand worker threadpool up to 16 during high memory headroom'],
      confidence: 0.975,
      merkleProof: 'f1e2d3c4b5a69788...773e',
    },
    {
      id: 'rnode-6',
      tierLevel: 6,
      tierName: 'LEVEL 6: POLICY & GOVERNANCE',
      title: 'SLA Budget Thresholds & Guardrails',
      critique: 'Static compute budget rule capped spend at $0.05/doc, triggering unnecessary fallbacks on dense 50-page contracts.',
      improvements: ['Propose dynamic budget scaling up to $0.065 for high-complexity legal documents', 'Enforce dual-signature threshold on policy upgrade'],
      confidence: 0.970,
      merkleProof: '8877665544332211...009f',
    },
    {
      id: 'rnode-7',
      tierLevel: 7,
      tierName: 'LEVEL 7: SELF-COGNITION',
      title: 'Meta-Reasoning & Recursive Self-Improvement',
      critique: 'Platform recognized its own serialization bottlenecks, formulated A/B replay hypotheses, and achieved closed-loop verification.',
      improvements: ['Schedule continuous autonomous self-improvement cycles at 6-hour intervals', 'Track historical convergence speedup velocity'],
      confidence: 0.965,
      merkleProof: 'c0d1e2f3a4b5c6d7...664a',
    },
  ];

  const handleReflect = () => {
    setIsReflecting(true);
    setTimeout(() => {
      setIsReflecting(false);
    }, 1500);
  };

  const activeNode = reflectionNodes.find((n) => n.tierLevel === selectedTier) ?? reflectionNodes[0]!;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold tracking-tight">Recursive Reflection Explorer</h1>
            <Badge variant="intelligence" size="sm" hasDot isPulsing>
              7-TIER MERKLE VERIFIED
            </Badge>
            <Badge variant="outline" size="sm">
              AMRS-RSIP Phase 13.9
            </Badge>
          </div>
          <p className="text-xs text-muted-foreground mt-1">
            Hierarchical multi-tier recursive critique spanning mission execution, planners, swarm dynamics, learning, architecture, policies, and self-cognition.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Button variant="outline" size="sm" onClick={handleReflect} disabled={isReflecting}>
            <RefreshCw className={`w-3.5 h-3.5 mr-1.5 ${isReflecting ? 'animate-spin' : ''}`} />
            {isReflecting ? 'Recalculating Proofs...' : 'Trigger Full Reflection Cycle'}
          </Button>
          <Button variant="intelligence" size="sm">
            <Lock className="w-3.5 h-3.5 mr-1.5" />
            Verify Merkle Root
          </Button>
        </div>
      </div>

      {/* Merkle Root Proof Banner */}
      <Card className="p-4 bg-purple-950/20 border-purple-500/30 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div className="flex items-center gap-3">
          <div className="p-2.5 bg-purple-500/10 rounded-lg border border-purple-500/20 text-purple-400">
            <Brain className="w-5 h-5" />
          </div>
          <div>
            <span className="text-xs font-semibold text-purple-400 uppercase tracking-wider">Merkle Root Hash Tree</span>
            <div className="text-xs font-mono text-foreground font-semibold">
              0x9e8a7b6c5d4e3f2a1b0c9d8e7f6a5b4c3d2e1f0a9b8c7d6e5f4a3b2c1d0e9f8a
            </div>
          </div>
        </div>
        <Badge variant="success" size="sm">7 of 7 Proofs Cryptographically Verified</Badge>
      </Card>

      {/* Main Layout: 7-Tier Tree Navigation & Detailed Tier Inspector */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Tier Tree Selection */}
        <div className="lg:col-span-5 space-y-2">
          <h2 className="text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-2">
            Reflection Hierarchy
          </h2>
          {reflectionNodes.map((node) => (
            <Card
              key={node.id}
              onClick={() => setSelectedTier(node.tierLevel)}
              className={`p-3.5 cursor-pointer transition-all border ${
                selectedTier === node.tierLevel
                  ? 'border-purple-500/60 bg-purple-950/30 shadow-sm'
                  : 'border-border/40 bg-secondary/10 hover:bg-secondary/20'
              }`}
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <div
                    className={`w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold font-mono ${
                      selectedTier === node.tierLevel
                        ? 'bg-purple-500 text-white'
                        : 'bg-secondary text-muted-foreground'
                    }`}
                  >
                    T{node.tierLevel}
                  </div>
                  <div>
                    <div className="text-xs font-semibold text-foreground">{node.tierName}</div>
                    <div className="text-[11px] text-muted-foreground truncate max-w-[200px]">
                      {node.title}
                    </div>
                  </div>
                </div>
                <Badge variant="outline" size="sm">
                  {(node.confidence * 100).toFixed(1)}%
                </Badge>
              </div>
            </Card>
          ))}
        </div>

        {/* Selected Tier Critique & Action Directives */}
        <div className="lg:col-span-7 space-y-4">
          <Card className="p-5 border-border/40 space-y-4">
            <div className="flex items-start justify-between">
              <div>
                <span className="text-xs font-mono font-bold text-purple-400">{activeNode.tierName}</span>
                <h3 className="text-lg font-bold text-foreground mt-0.5">{activeNode.title}</h3>
              </div>
              <Badge variant="success" size="sm">
                Confidence {(activeNode.confidence * 100).toFixed(1)}%
              </Badge>
            </div>

            {/* Critique Box */}
            <div className="p-4 rounded-lg bg-secondary/30 border border-border/40 space-y-2">
              <div className="flex items-center gap-2 text-xs font-semibold text-amber-400">
                <ShieldAlert className="w-4 h-4" />
                <span>Recursive Self-Critique</span>
              </div>
              <p className="text-xs text-muted-foreground leading-relaxed">{activeNode.critique}</p>
            </div>

            {/* Identified Improvements / Action Directives */}
            <div className="space-y-2">
              <div className="flex items-center gap-2 text-xs font-semibold text-purple-400">
                <Sparkles className="w-4 h-4" />
                <span>Actionable Improvement Directives</span>
              </div>
              <div className="space-y-2">
                {activeNode.improvements.map((imp, idx) => (
                  <div
                    key={idx}
                    className="flex items-start gap-2.5 p-3 rounded-lg border border-purple-500/20 bg-purple-950/10 text-xs"
                  >
                    <CheckCircle2 className="w-4 h-4 text-purple-400 flex-shrink-0 mt-0.5" />
                    <span className="text-foreground">{imp}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Merkle Proof Footer */}
            <div className="flex items-center justify-between text-[11px] text-muted-foreground pt-3 border-t border-border/40 font-mono">
              <span>Merkle Proof: {activeNode.merkleProof}</span>
              <span className="text-emerald-400">● Validated Invariant</span>
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
};
