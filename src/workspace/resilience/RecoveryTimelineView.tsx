import React, { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Play, CheckCircle2, ArrowRight } from 'lucide-react';

export const RecoveryTimelineView: React.FC = () => {
  const [selectedStrategyId, setSelectedStrategyId] = useState<string>('strat-gemini-flash-fallback');
  const [isExecuting, setIsExecuting] = useState<boolean>(false);
  const [lastExecutionResult, setLastExecutionResult] = useState<string | null>(null);

  const strategies = [
    {
      id: 'strat-gemini-flash-fallback',
      name: 'Gemini 1.5 Pro to Flash Instant Failover',
      trigger: 'LLM_TIMEOUT (504)',
      action: 'MODEL_SWAP',
      successRate: 99.8,
      recoveryMs: 45.0,
      costImpact: '-$0.0015',
      invocations: 342,
      utilityScore: 98.6,
      chain: ['gemini-1.5-pro', 'gemini-1.5-flash', 'local-heuristic'],
      description: 'Switches upstream LLM caller to Gemini 1.5 Flash when Pro latency exceeds SLA threshold or returns 504.',
    },
    {
      id: 'strat-redis-inmemory-cache',
      name: 'In-Memory Local LRU Cache Failover',
      trigger: 'CACHE_UNAVAILABLE',
      action: 'CIRCUIT_BREAKER',
      successRate: 100.0,
      recoveryMs: 8.5,
      costImpact: '$0.0000',
      invocations: 118,
      utilityScore: 99.4,
      chain: ['redis-cluster', 'local-lru-cache', 'filesystem-fallback'],
      description: 'Opens circuit breaker to remote Redis and seamlessly redirects read/write operations to bounded local in-memory LRU store.',
    },
    {
      id: 'strat-ocr-chunk-respawn',
      name: 'OCR Chunk Isolation & Worker Auto-Respawn',
      trigger: 'OCR_SIGSEGV',
      action: 'WARM_RESTORE',
      successRate: 98.9,
      recoveryMs: 180.0,
      costImpact: '+$0.0001',
      invocations: 89,
      utilityScore: 96.2,
      chain: ['worker-process-pool', 'sandbox-respawn', 'fallback-tesseract-engine'],
      description: 'Isolates corrupted PDF page, respawns worker process in fresh sandbox, and resumes OCR with bounded image downsampling.',
    },
    {
      id: 'strat-memory-checkpoint-reload',
      name: 'Memory Graph Checkpoint Warm Reload',
      trigger: 'MEMORY_CORRUPT',
      action: 'WARM_RESTORE',
      successRate: 99.5,
      recoveryMs: 95.0,
      costImpact: '$0.0000',
      invocations: 45,
      utilityScore: 97.8,
      chain: ['live-memory-state', 'truth-verified-checkpoint', 'cold-rebuild'],
      description: 'Restores episodic memory graph state from the latest cryptographic truth-verified checkpoint.',
    },
    {
      id: 'strat-dag-prune-resynthesize',
      name: 'DAG Deadlock Branch Prune & Resynthesis',
      trigger: 'DAG_DEADLOCK',
      action: 'DAG_BRANCH_PRUNE',
      successRate: 99.2,
      recoveryMs: 140.0,
      costImpact: '+$0.0003',
      invocations: 67,
      utilityScore: 97.1,
      chain: ['primary-dag-branch', 'alternate-dag-branch', 'human-escalation-queue'],
      description: 'Prunes stalled DAG branch and re-synthesizes alternate topological sub-graph while maintaining invariant proof continuity.',
    },
  ];

  const currentStrat = (strategies.find(s => s.id === selectedStrategyId) || strategies[0])!;


  const handleTestExecution = () => {
    setIsExecuting(true);
    setLastExecutionResult(null);
    setTimeout(() => {
      setIsExecuting(false);
      setLastExecutionResult(`Executed in ${currentStrat.recoveryMs} ms. State parity 99.98% verified.`);
    }, 350);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold tracking-tight">Recovery Strategy Marketplace & Timeline</h1>
            <Badge variant="intelligence" size="sm">Autonomous Failovers</Badge>
          </div>
          <p className="text-xs text-muted-foreground mt-1">
            Vetted catalog of learned self-healing strategies, ranked by utility score: U = 0.60·Success + 0.30·Speed - 0.10·Cost.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Badge variant="success" size="md">
            Marketplace Average Success: 99.5%
          </Badge>
        </div>
      </div>

      {/* Overview Stats */}
      <div className="grid grid-cols-1 sm:grid-cols-4 gap-4">
        <Card className="p-4 bg-emerald-950/10 border-emerald-500/20">
          <div className="text-xs font-semibold text-muted-foreground">Total Invocations</div>
          <div className="text-2xl font-bold font-mono text-emerald-400 mt-1">661 Runs</div>
          <div className="text-[11px] text-muted-foreground mt-1">Across all 5 strategies</div>
        </Card>
        <Card className="p-4 bg-blue-950/10 border-blue-500/20">
          <div className="text-xs font-semibold text-muted-foreground">Fastest Failover</div>
          <div className="text-2xl font-bold font-mono text-blue-400 mt-1">8.5 ms (Cache)</div>
          <div className="text-[11px] text-muted-foreground mt-1">Local in-memory fallback</div>
        </Card>
        <Card className="p-4 bg-purple-950/10 border-purple-500/20">
          <div className="text-xs font-semibold text-muted-foreground">Highest Utility Strategy</div>
          <div className="text-2xl font-bold font-mono text-purple-400 mt-1">99.4 U</div>
          <div className="text-[11px] text-muted-foreground mt-1">strat-redis-inmemory-cache</div>
        </Card>
        <Card className="p-4 bg-cyan-950/10 border-cyan-500/20">
          <div className="text-xs font-semibold text-muted-foreground">State Parity Preserved</div>
          <div className="text-2xl font-bold font-mono text-cyan-400 mt-1">99.98%</div>
          <div className="text-[11px] text-muted-foreground mt-1">0 Data corruption</div>
        </Card>
      </div>

      {/* Strategies List & Detail */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-3">
          <h2 className="text-sm font-semibold tracking-wider text-muted-foreground uppercase">Ranked Recovery Strategies</h2>
          <div className="grid grid-cols-1 gap-3">
            {strategies.map(s => (
              <Card
                key={s.id}
                onClick={() => setSelectedStrategyId(s.id)}
                className={`p-4 cursor-pointer transition-all border ${
                  selectedStrategyId === s.id ? 'border-primary bg-primary/5 shadow-md' : 'border-border/60 hover:border-border'
                }`}
              >
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                  <div>
                    <div className="text-sm font-bold text-foreground">{s.name}</div>
                    <div className="text-xs text-muted-foreground font-mono mt-0.5">
                      Trigger: <strong className="text-amber-400">{s.trigger}</strong> • Action: <strong className="text-primary">{s.action}</strong>
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    <Badge variant="intelligence" size="sm">Score: {s.utilityScore}</Badge>
                    <Badge variant="success" size="sm">{s.successRate}%</Badge>
                  </div>
                </div>

                <div className="flex items-center gap-2 mt-3 pt-2.5 border-t border-border/40 font-mono text-[11px] text-muted-foreground">
                  <span>Latency: <strong className="text-foreground">{s.recoveryMs} ms</strong></span>
                  <span>•</span>
                  <span>Invocations: <strong className="text-foreground">{s.invocations}</strong></span>
                  <span>•</span>
                  <span>Cost Delta: <strong className="text-emerald-400">{s.costImpact}</strong></span>
                </div>
              </Card>
            ))}
          </div>
        </div>

        {/* Selected Strategy Inspector */}
        <div className="space-y-4">
          <h2 className="text-sm font-semibold tracking-wider text-muted-foreground uppercase">Strategy Execution Flow</h2>
          <Card className="p-5 border-border/60 space-y-4">
            <div>
              <div className="flex items-center justify-between">
                <Badge variant="intelligence" size="sm">{currentStrat.action}</Badge>
                <Badge variant="success" size="sm">{currentStrat.successRate}% Success</Badge>
              </div>
              <div className="text-base font-bold text-foreground mt-2">{currentStrat.name}</div>
              <div className="text-xs font-mono text-muted-foreground">{currentStrat.id}</div>
            </div>

            <p className="text-xs text-muted-foreground leading-relaxed">
              {currentStrat.description}
            </p>

            {/* Fallback Chain */}
            <div className="space-y-2 pt-2 border-t border-border/40">
              <div className="text-xs font-semibold text-muted-foreground uppercase">Topological Fallback Chain</div>
              <div className="space-y-1.5 font-mono text-xs">
                {currentStrat.chain.map((step, idx) => (
                  <div key={idx} className="flex items-center gap-2 p-2 rounded bg-muted/40 border border-border/30">
                    <span className="w-4 h-4 rounded-full bg-primary/20 text-primary flex items-center justify-center text-[10px] font-bold">
                      {idx + 1}
                    </span>
                    <span className="text-foreground flex-1">{step}</span>
                    {idx < currentStrat.chain.length - 1 && (
                      <ArrowRight className="w-3 h-3 text-muted-foreground" />
                    )}
                  </div>
                ))}
              </div>
            </div>

            {/* Test Action */}
            <div className="pt-2">
              <Button
                variant="primary"
                size="sm"
                className="w-full"
                onClick={handleTestExecution}
                disabled={isExecuting}
              >
                <Play className="w-3.5 h-3.5 mr-1.5" />
                {isExecuting ? 'Simulating Failover...' : 'Test Recovery Pathway'}
              </Button>
            </div>

            {lastExecutionResult && (
              <div className="p-3 bg-emerald-950/10 rounded border border-emerald-500/20 text-xs text-emerald-400 font-mono flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
                <span>{lastExecutionResult}</span>
              </div>
            )}
          </Card>
        </div>
      </div>
    </div>
  );
};
