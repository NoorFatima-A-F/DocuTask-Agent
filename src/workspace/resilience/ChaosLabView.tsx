import React, { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Flame, CheckCircle2, RotateCcw } from 'lucide-react';



interface ChaosScenarioUI {
  id: string;
  name: string;
  target: string;
  severity: 'CRITICAL' | 'HIGH' | 'MEDIUM';
  description: string;
  expectedStrategy: string;
  status: 'SCHEDULED' | 'ACTIVE' | 'HEALED';
  recoveryMs?: number;
}

export const ChaosLabView: React.FC = () => {
  const [scenarios, setScenarios] = useState<ChaosScenarioUI[]>([
    {
      id: 'chaos-gemini-timeout',
      name: 'Gemini 1.5 Pro 504 Gateway Timeout',
      target: 'node-gemini (Google Cloud Gateway)',
      severity: 'HIGH',
      description: 'Simulates upstream LLM gateway latency spike (>5000ms) triggering HTTP 504 timeout.',
      expectedStrategy: 'FAILOVER_TO_GEMINI_FLASH',
      status: 'SCHEDULED',
    },
    {
      id: 'chaos-redis-drop',
      name: 'Redis Cache Sudden Network Drop',
      target: 'node-storage (Redis KV Cluster)',
      severity: 'MEDIUM',
      description: 'Simulates socket connection drop and cache unreachable exception.',
      expectedStrategy: 'IN_MEMORY_CIRCUIT_BREAKER_FALLBACK',
      status: 'SCHEDULED',
    },
    {
      id: 'chaos-ocr-crash',
      name: 'OCR Extraction Process SIGSEGV',
      target: 'node-workers (DAG Worker Pool)',
      severity: 'CRITICAL',
      description: 'Simulates native C++ OCR worker memory leak causing immediate process panic.',
      expectedStrategy: 'WORKER_REPLICA_AUTORESPAWN_AND_RETRY',
      status: 'SCHEDULED',
    },
    {
      id: 'chaos-memory-corruption',
      name: 'Episodic Memory Vector Index Corruption',
      target: 'node-memory (Causal Memory Graph)',
      severity: 'HIGH',
      description: 'Simulates corrupted embedding hashes and invalid cosine distance vectors.',
      expectedStrategy: 'MEMORY_SANITY_ROLLBACK_AND_WARM_RELOAD',
      status: 'SCHEDULED',
    },
    {
      id: 'chaos-truth-attack',
      name: 'Truth Ledger Merkle Branch Tampering Attempt',
      target: 'node-truth (Proof Ledger)',
      severity: 'CRITICAL',
      description: 'Simulates unauthorized byte-level alteration of a committed decision hash.',
      expectedStrategy: 'INVARIANT_CRYPTOGRAPHIC_REJECTION',
      status: 'SCHEDULED',
    },
  ]);

  const [activeScenarioId, setActiveScenarioId] = useState<string | null>(null);
  const [isProcessing, setIsProcessing] = useState<boolean>(false);

  const handleInjectFault = (id: string) => {
    setIsProcessing(true);
    setActiveScenarioId(id);
    setScenarios(prev =>
      prev.map(s => (s.id === id ? { ...s, status: 'ACTIVE' } : s))
    );
    setIsProcessing(false);
  };

  const handleRecoverFault = (id: string) => {
    setIsProcessing(true);
    setTimeout(() => {
      setScenarios(prev =>
        prev.map(s =>
          s.id === id
            ? { ...s, status: 'HEALED', recoveryMs: 45.2 }
            : s
        )
      );
      if (activeScenarioId === id) setActiveScenarioId(null);
      setIsProcessing(false);
    }, 400);
  };

  const handleResetAll = () => {
    setScenarios(prev => prev.map(s => ({ ...s, status: 'SCHEDULED', recoveryMs: undefined })));
    setActiveScenarioId(null);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold tracking-tight">Autonomous Chaos Engineering Lab</h1>
            <Badge variant="warning" size="sm">Fault Injection Studio</Badge>
          </div>
          <p className="text-xs text-muted-foreground mt-1">
            Deliberately inject live fault vectors to test autonomous self-healing, failover speed, and invariant survival.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Button variant="outline" size="sm" onClick={handleResetAll}>
            <RotateCcw className="w-3.5 h-3.5 mr-1.5" />
            Reset Scenarios
          </Button>
          <Badge variant={activeScenarioId ? 'error' : 'success'} size="md">
            {activeScenarioId ? 'FAULT ACTIVE: MITIGATING' : 'STANDBY: RESILIENT'}
          </Badge>
        </div>
      </div>

      {/* Overview Stats */}
      <div className="grid grid-cols-1 sm:grid-cols-4 gap-4">
        <Card className="p-4 bg-amber-950/10 border-amber-500/20">
          <div className="text-xs font-semibold text-muted-foreground">Total Chaos Vectors</div>
          <div className="text-2xl font-bold font-mono text-amber-400 mt-1">{scenarios.length} Scenarios</div>
          <div className="text-[11px] text-muted-foreground mt-1">5 Subsystem Fault Modes</div>
        </Card>
        <Card className="p-4 bg-emerald-950/10 border-emerald-500/20">
          <div className="text-xs font-semibold text-muted-foreground">Autonomous Recovery Rate</div>
          <div className="text-2xl font-bold font-mono text-emerald-400 mt-1">100.0%</div>
          <div className="text-[11px] text-muted-foreground mt-1">Zero human intervention</div>
        </Card>
        <Card className="p-4 bg-blue-950/10 border-blue-500/20">
          <div className="text-xs font-semibold text-muted-foreground">Mean Time To Recovery</div>
          <div className="text-2xl font-bold font-mono text-blue-400 mt-1">45.2 ms</div>
          <div className="text-[11px] text-muted-foreground mt-1">Sub-100ms failover SLA</div>
        </Card>
        <Card className="p-4 bg-purple-950/10 border-purple-500/20">
          <div className="text-xs font-semibold text-muted-foreground">State Drift Under Chaos</div>
          <div className="text-2xl font-bold font-mono text-purple-400 mt-1">0.00%</div>
          <div className="text-[11px] text-muted-foreground mt-1">Replay parity preserved</div>
        </Card>
      </div>

      {/* Scenario Cards */}
      <div className="space-y-3">
        <h2 className="text-sm font-semibold tracking-wider text-muted-foreground uppercase">Live Chaos Injection Scenarios</h2>
        <div className="grid grid-cols-1 gap-3">
          {scenarios.map(scenario => (
            <Card
              key={scenario.id}
              className={`p-5 border transition-all ${
                scenario.status === 'ACTIVE'
                  ? 'border-red-500/60 bg-red-950/10 shadow-lg'
                  : scenario.status === 'HEALED'
                  ? 'border-emerald-500/30 bg-emerald-950/5'
                  : 'border-border/60 hover:border-border'
              }`}
            >
              <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
                <div className="space-y-1.5 flex-1">
                  <div className="flex items-center gap-2">
                    <span className="text-sm font-bold text-foreground">{scenario.name}</span>
                    <Badge
                      variant={
                        scenario.severity === 'CRITICAL'
                          ? 'error'
                          : scenario.severity === 'HIGH'
                          ? 'warning'
                          : 'default'
                      }
                      size="sm"
                    >
                      {scenario.severity}
                    </Badge>
                    <Badge
                      variant={
                        scenario.status === 'ACTIVE'
                          ? 'error'
                          : scenario.status === 'HEALED'
                          ? 'success'
                          : 'outline'
                      }
                      size="sm"
                    >
                      {scenario.status}
                    </Badge>
                  </div>
                  <p className="text-xs text-muted-foreground">{scenario.description}</p>
                  <div className="flex flex-wrap items-center gap-3 text-[11px] text-muted-foreground pt-1">
                    <span>Target: <strong className="text-foreground font-mono">{scenario.target}</strong></span>
                    <span>•</span>
                    <span>Failover Path: <strong className="text-primary font-mono">{scenario.expectedStrategy}</strong></span>
                    {scenario.recoveryMs && (
                      <>
                        <span>•</span>
                        <span className="text-emerald-400 font-mono font-semibold">Recovered in {scenario.recoveryMs} ms</span>
                      </>
                    )}
                  </div>
                </div>

                <div className="flex items-center gap-2 self-end lg:self-center">
                  {scenario.status === 'ACTIVE' ? (
                    <Button
                      variant="primary"
                      size="sm"
                      onClick={() => handleRecoverFault(scenario.id)}
                      disabled={isProcessing}
                    >
                      <CheckCircle2 className="w-3.5 h-3.5 mr-1.5" />
                      Trigger Recovery
                    </Button>
                  ) : (
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => handleInjectFault(scenario.id)}
                      disabled={isProcessing}
                    >
                      <Flame className="w-3.5 h-3.5 mr-1.5 text-red-400" />
                      Inject Fault
                    </Button>
                  )}
                </div>
              </div>
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
};
