import React, { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Activity, ShieldCheck, Cpu, HardDrive, Zap, RefreshCw, AlertTriangle } from 'lucide-react';

export const DigitalTwinView: React.FC = () => {
  const [selectedNode, setSelectedNode] = useState<string>('node-planner');
  const [isSyncing, setIsSyncing] = useState<boolean>(false);

  const nodes = [
    { id: 'node-planner', name: 'Autonomous Planner Engine', category: 'PLANNER', health: 'HEALTHY', latency: 18.2, errorRate: 0.00, cpu: 14.5, mem: 128, replicas: 2, invariants: '14/14 Passed' },
    { id: 'node-workers', name: 'DAG Dynamic Worker Pool', category: 'WORKER', health: 'HEALTHY', latency: 32.4, errorRate: 0.00, cpu: 28.1, mem: 512, replicas: 4, invariants: '14/14 Passed' },
    { id: 'node-memory', name: 'Episodic & Causal Memory Graph', category: 'MEMORY', health: 'HEALTHY', latency: 12.1, errorRate: 0.00, cpu: 8.4, mem: 256, replicas: 3, invariants: '14/14 Passed' },
    { id: 'node-truth', name: 'Runtime Truth & Proof Ledger', category: 'TRUTH_LEDGER', health: 'HEALTHY', latency: 8.5, errorRate: 0.00, cpu: 6.2, mem: 96, replicas: 3, invariants: '14/14 Passed' },
    { id: 'node-evidence', name: 'Cryptographic Evidence Store', category: 'EVIDENCE', health: 'HEALTHY', latency: 9.1, errorRate: 0.00, cpu: 5.5, mem: 80, replicas: 3, invariants: '14/14 Passed' },
    { id: 'node-policy', name: 'Dynamic Policy & Sandbox Engine', category: 'POLICY', health: 'HEALTHY', latency: 11.0, errorRate: 0.00, cpu: 7.0, mem: 64, replicas: 2, invariants: '14/14 Passed' },
    { id: 'node-storage', name: 'Redis State & Fast KV Cache', category: 'STORAGE', health: 'HEALTHY', latency: 4.2, errorRate: 0.00, cpu: 11.0, mem: 1024, replicas: 3, invariants: '14/14 Passed' },
    { id: 'node-gemini', name: 'Google Cloud Gemini 1.5 Pro/Flash', category: 'PROVIDER', health: 'HEALTHY', latency: 145.0, errorRate: 0.00, cpu: 0.0, mem: 0, replicas: 1, invariants: '14/14 Passed' },
    { id: 'node-commander', name: 'Autonomous Incident Commander', category: 'INCIDENT_COMMANDER', health: 'HEALTHY', latency: 6.8, errorRate: 0.00, cpu: 3.2, mem: 48, replicas: 2, invariants: '14/14 Passed' },
  ];

  const edges = [
    { from: 'node-planner', to: 'node-workers', type: 'DISPATCHES_TASKS', rps: 85.0, p95: '22ms' },
    { from: 'node-workers', to: 'node-gemini', type: 'INVOKES_MODELS', rps: 45.0, p95: '160ms' },
    { from: 'node-workers', to: 'node-memory', type: 'QUERIES_EXPERIENCES', rps: 120.0, p95: '15ms' },
    { from: 'node-planner', to: 'node-truth', type: 'COMMITS_PROOFS', rps: 60.0, p95: '10ms' },
    { from: 'node-workers', to: 'node-evidence', type: 'RECORDS_EVIDENCE', rps: 110.0, p95: '12ms' },
    { from: 'node-workers', to: 'node-storage', type: 'SYNCS_STATE', rps: 250.0, p95: '5ms' },
  ];

  const currentNode = (nodes.find(n => n.id === selectedNode) || nodes[0])!;

  const handleSync = () => {
    setIsSyncing(true);
    setTimeout(() => setIsSyncing(false), 500);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold tracking-tight">Operational Digital Twin</h1>
            <Badge variant="intelligence" size="sm">Live Topology</Badge>
          </div>
          <p className="text-xs text-muted-foreground mt-1">
            Real-time mirrored state graph tracking micro-engines, external providers, latency drift, and replica parity.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Button variant="outline" size="sm" onClick={handleSync} disabled={isSyncing}>
            <RefreshCw className={`w-3.5 h-3.5 mr-1.5 ${isSyncing ? 'animate-spin' : ''}`} />
            Sync Twin State
          </Button>
          <Badge variant="success" size="md">
            Parity: 99.98% Synced
          </Badge>
        </div>
      </div>

      {/* Top Metric Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-4 gap-4">
        <Card className="p-4 bg-emerald-950/10 border-emerald-500/20">
          <div className="text-xs font-semibold text-muted-foreground">Digital Twin Health</div>
          <div className="text-2xl font-bold font-mono text-emerald-400 mt-1">100.0%</div>
          <div className="text-[11px] text-muted-foreground mt-1">9/9 Nodes Healthy</div>
        </Card>
        <Card className="p-4 bg-blue-950/10 border-blue-500/20">
          <div className="text-xs font-semibold text-muted-foreground">Active Replicas</div>
          <div className="text-2xl font-bold font-mono text-blue-400 mt-1">22 Instances</div>
          <div className="text-[11px] text-muted-foreground mt-1">Sub-second failover</div>
        </Card>
        <Card className="p-4 bg-purple-950/10 border-purple-500/20">
          <div className="text-xs font-semibold text-muted-foreground">Global P95 Latency</div>
          <div className="text-2xl font-bold font-mono text-purple-400 mt-1">18.4ms</div>
          <div className="text-[11px] text-muted-foreground mt-1">Provider-excluded</div>
        </Card>
        <Card className="p-4 bg-cyan-950/10 border-cyan-500/20">
          <div className="text-xs font-semibold text-muted-foreground">Invariant Assertion Rate</div>
          <div className="text-2xl font-bold font-mono text-cyan-400 mt-1">100.0%</div>
          <div className="text-[11px] text-muted-foreground mt-1">0 Invariant breaches</div>
        </Card>
      </div>

      {/* Node Matrix and Detail Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-4">
          <h2 className="text-sm font-semibold tracking-wider text-muted-foreground uppercase">Runtime Component Graph</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {nodes.map(node => (
              <Card
                key={node.id}
                onClick={() => setSelectedNode(node.id)}
                className={`p-4 cursor-pointer transition-all border ${
                  selectedNode === node.id ? 'border-primary bg-primary/5 shadow-md' : 'border-border/60 hover:border-border'
                }`}
              >
                <div className="flex items-start justify-between">
                  <div>
                    <div className="text-xs font-semibold text-foreground">{node.name}</div>
                    <div className="text-[10px] text-muted-foreground font-mono mt-0.5">{node.id}</div>
                  </div>
                  <Badge variant="success" size="sm">{node.health}</Badge>
                </div>
                <div className="grid grid-cols-3 gap-2 mt-3 pt-3 border-t border-border/40 text-center">
                  <div>
                    <div className="text-[10px] text-muted-foreground">Latency</div>
                    <div className="text-xs font-mono font-semibold text-foreground">{node.latency}ms</div>
                  </div>
                  <div>
                    <div className="text-[10px] text-muted-foreground">CPU</div>
                    <div className="text-xs font-mono font-semibold text-foreground">{node.cpu}%</div>
                  </div>
                  <div>
                    <div className="text-[10px] text-muted-foreground">Replicas</div>
                    <div className="text-xs font-mono font-semibold text-foreground">{node.replicas}</div>
                  </div>
                </div>
              </Card>
            ))}
          </div>

          {/* Inter-Node Dataflow Edges */}
          <h2 className="text-sm font-semibold tracking-wider text-muted-foreground uppercase pt-2">Active Dataflow & Circuit Breakers</h2>
          <div className="border border-border/40 rounded-lg overflow-hidden">
            <table className="w-full text-left text-xs">
              <thead className="bg-muted/40 text-muted-foreground border-b border-border/40">
                <tr>
                  <th className="p-2.5 font-medium">Source</th>
                  <th className="p-2.5 font-medium">Target</th>
                  <th className="p-2.5 font-medium">Relationship</th>
                  <th className="p-2.5 font-medium text-right">Throughput</th>
                  <th className="p-2.5 font-medium text-right">P95</th>
                  <th className="p-2.5 font-medium text-center">Circuit Breaker</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-border/20 font-mono">
                {edges.map((e, idx) => (
                  <tr key={idx} className="hover:bg-muted/20">
                    <td className="p-2.5 text-foreground">{e.from}</td>
                    <td className="p-2.5 text-foreground">{e.to}</td>
                    <td className="p-2.5 text-primary text-[11px]">{e.type}</td>
                    <td className="p-2.5 text-right text-muted-foreground">{e.rps} RPS</td>
                    <td className="p-2.5 text-right text-muted-foreground">{e.p95}</td>
                    <td className="p-2.5 text-center">
                      <Badge variant="success" size="sm">CLOSED</Badge>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Selected Node Telemetry Inspector */}
        <div className="space-y-4">
          <h2 className="text-sm font-semibold tracking-wider text-muted-foreground uppercase">Telemetry Inspector</h2>
          <Card className="p-5 border-border/60 space-y-4">
            <div>
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold text-muted-foreground uppercase">{currentNode.category}</span>
                <Badge variant="success" size="sm">{currentNode.health}</Badge>
              </div>
              <div className="text-base font-bold text-foreground mt-1">{currentNode.name}</div>
              <div className="text-xs font-mono text-muted-foreground">{currentNode.id}</div>
            </div>

            <div className="space-y-2.5 pt-2 border-t border-border/40">
              <div className="flex justify-between items-center text-xs">
                <span className="text-muted-foreground flex items-center gap-1.5"><Activity className="w-3.5 h-3.5 text-blue-400" /> Latency</span>
                <span className="font-mono font-semibold text-foreground">{currentNode.latency} ms</span>
              </div>
              <div className="flex justify-between items-center text-xs">
                <span className="text-muted-foreground flex items-center gap-1.5"><AlertTriangle className="w-3.5 h-3.5 text-amber-400" /> Error Rate</span>
                <span className="font-mono font-semibold text-foreground">{currentNode.errorRate}%</span>
              </div>
              <div className="flex justify-between items-center text-xs">
                <span className="text-muted-foreground flex items-center gap-1.5"><Cpu className="w-3.5 h-3.5 text-purple-400" /> CPU Allocation</span>
                <span className="font-mono font-semibold text-foreground">{currentNode.cpu}%</span>
              </div>
              <div className="flex justify-between items-center text-xs">
                <span className="text-muted-foreground flex items-center gap-1.5"><HardDrive className="w-3.5 h-3.5 text-emerald-400" /> Memory Working Set</span>
                <span className="font-mono font-semibold text-foreground">{currentNode.mem} MB</span>
              </div>
              <div className="flex justify-between items-center text-xs">
                <span className="text-muted-foreground flex items-center gap-1.5"><ShieldCheck className="w-3.5 h-3.5 text-cyan-400" /> Invariant Assertions</span>
                <span className="font-mono font-semibold text-cyan-400">{currentNode.invariants}</span>
              </div>
            </div>

            <div className="p-3 bg-muted/40 rounded border border-border/40 space-y-1">
              <div className="text-[11px] font-semibold text-foreground flex items-center gap-1.5">
                <Zap className="w-3.5 h-3.5 text-amber-400" /> Auto-Healing Capability
              </div>
              <p className="text-[11px] text-muted-foreground">
                In the event of an anomalous latency spike or worker crash, the Autonomous Incident Commander will isolate this node and trigger sub-50ms replica failover.
              </p>
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
};
