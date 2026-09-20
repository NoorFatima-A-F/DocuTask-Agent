import React, { useState } from 'react';
import {
  Activity,
  Server,
  Cpu,
  RefreshCw,
  HardDrive,
  ShieldCheck,
  Zap
} from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';

interface ResourceHealthCapacityDashboardProps {
  missionId?: string;
}

interface WorkerHealthNode {
  id: string;
  name: string;
  category: 'LLM_BACKEND' | 'OCR_CLUSTER' | 'WORKER_AGENT' | 'GPU_INFERENCE';
  status: 'HEALTHY' | 'DEGRADED' | 'RATE_LIMITED' | 'DRAINING';
  cpuUtilization: number;
  memoryUtilization: number;
  activeConcurrency: number;
  maxConcurrency: number;
  errorRate: number;
  p95LatencyMs: number;
  failoverTarget: string;
}

export const ResourceHealthCapacityDashboard: React.FC<ResourceHealthCapacityDashboardProps> = ({
  missionId = 'mission-current',
}) => {
  const [nodes] = useState<WorkerHealthNode[]>([
    {
      id: 'node-llm-01',
      name: 'Gemini 1.5 Pro (Global Gateway)',
      category: 'LLM_BACKEND',
      status: 'HEALTHY',
      cpuUtilization: 34,
      memoryUtilization: 42,
      activeConcurrency: 14,
      maxConcurrency: 50,
      errorRate: 0.02,
      p95LatencyMs: 1450,
      failoverTarget: 'Claude 3.5 Sonnet (Direct)',
    },
    {
      id: 'node-llm-02',
      name: 'Gemini 1.5 Flash (Low-Latency)',
      category: 'LLM_BACKEND',
      status: 'HEALTHY',
      cpuUtilization: 28,
      memoryUtilization: 31,
      activeConcurrency: 45,
      maxConcurrency: 150,
      errorRate: 0.00,
      p95LatencyMs: 420,
      failoverTarget: 'Local LLaVA Quantized',
    },
    {
      id: 'node-ocr-01',
      name: 'Azure Computer Vision Engine',
      category: 'OCR_CLUSTER',
      status: 'HEALTHY',
      cpuUtilization: 52,
      memoryUtilization: 60,
      activeConcurrency: 8,
      maxConcurrency: 20,
      errorRate: 0.01,
      p95LatencyMs: 890,
      failoverTarget: 'Tesseract High-DPI Local',
    },
    {
      id: 'node-gpu-01',
      name: 'NVIDIA RTX 4090 Dedicated Inference',
      category: 'GPU_INFERENCE',
      status: 'HEALTHY',
      cpuUtilization: 78,
      memoryUtilization: 85,
      activeConcurrency: 3,
      maxConcurrency: 4,
      errorRate: 0.00,
      p95LatencyMs: 310,
      failoverTarget: 'Gemini 1.5 Flash (Cloud API)',
    },
    {
      id: 'node-wrk-01',
      name: 'Document Segmentation Agent Pool',
      category: 'WORKER_AGENT',
      status: 'HEALTHY',
      cpuUtilization: 45,
      memoryUtilization: 55,
      activeConcurrency: 12,
      maxConcurrency: 24,
      errorRate: 0.00,
      p95LatencyMs: 210,
      failoverTarget: 'Fallback Sync Worker',
    },
  ]);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-slate-100 flex items-center gap-2">
            <Activity className="w-5 h-5 text-emerald-400" />
            Resource Health, Capacity & Failover Monitor
          </h2>
          <p className="text-sm text-slate-400">
            Real-time health telemetry, cluster concurrency saturation, and zero-downtime failover targets for mission: <code className="text-emerald-300 font-mono text-xs">{missionId}</code>
          </p>
        </div>
        <div className="flex items-center gap-3">
          <Badge variant="success" size="md">
            Cluster Status: 100% OPERATIONAL
          </Badge>
          <button className="flex items-center gap-1.5 px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-medium rounded-lg border border-slate-700">
            <RefreshCw className="w-3.5 h-3.5" />
            Poll Health
          </button>
        </div>
      </div>

      {/* Overview Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card className="p-4 bg-slate-900 border-slate-800">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-medium text-slate-400">Total Registered Nodes</span>
            <Server className="w-4 h-4 text-indigo-400" />
          </div>
          <div className="text-2xl font-bold text-slate-100 font-mono">
            {nodes.length}
            <span className="text-xs text-emerald-400 font-normal"> (5/5 healthy)</span>
          </div>
          <span className="text-[11px] text-slate-400 mt-1 block">0 degraded or draining</span>
        </Card>

        <Card className="p-4 bg-slate-900 border-slate-800">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-medium text-slate-400">Active Concurrency</span>
            <Zap className="w-4 h-4 text-amber-400" />
          </div>
          <div className="text-2xl font-bold text-amber-400 font-mono">
            82 / 248
          </div>
          <span className="text-[11px] text-slate-400 mt-1 block">33.1% Total Pool Saturation</span>
        </Card>

        <Card className="p-4 bg-slate-900 border-slate-800">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-medium text-slate-400">Mean P95 Latency</span>
            <Activity className="w-4 h-4 text-purple-400" />
          </div>
          <div className="text-2xl font-bold text-purple-400 font-mono">
            656 ms
          </div>
          <span className="text-[11px] text-slate-400 mt-1 block">Sub-second execution SLA met</span>
        </Card>

        <Card className="p-4 bg-slate-900 border-slate-800">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-medium text-slate-400">Failover Readiness</span>
            <ShieldCheck className="w-4 h-4 text-emerald-400" />
          </div>
          <div className="text-2xl font-bold text-emerald-400 font-mono">
            100%
          </div>
          <span className="text-[11px] text-slate-400 mt-1 block">All nodes paired with warm backups</span>
        </Card>
      </div>

      {/* Cluster Node List */}
      <Card className="p-5 bg-slate-900 border-slate-800">
        <h3 className="text-sm font-semibold text-slate-200 mb-4 flex items-center gap-2">
          <Server className="w-4 h-4 text-indigo-400" />
          Active Execution Nodes & Concurrency Breakdown
        </h3>

        <div className="space-y-3">
          {nodes.map(node => {
            const saturation = (node.activeConcurrency / node.maxConcurrency) * 100;
            return (
              <div key={node.id} className="p-4 rounded-xl bg-slate-950 border border-slate-800 hover:border-slate-700 transition-all">
                <div className="flex items-center justify-between mb-3">
                  <div className="flex items-center gap-2.5">
                    <div className="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse" />
                    <div>
                      <span className="text-xs font-bold text-slate-200 block">{node.name}</span>
                      <span className="text-[10px] text-slate-400 font-mono">{node.id} • {node.category}</span>
                    </div>
                  </div>

                  <div className="flex items-center gap-2">
                    <Badge variant="success" size="sm">{node.status}</Badge>
                    <span className="text-xs font-mono text-slate-300">
                      Concurrency: <strong className="text-amber-400">{node.activeConcurrency}</strong> / {node.maxConcurrency}
                    </span>
                  </div>
                </div>

                {/* Resource Gauges */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-3 pt-2 border-t border-slate-800/80 text-xs">
                  <div>
                    <div className="flex justify-between text-slate-400 mb-1">
                      <span className="flex items-center gap-1"><Cpu className="w-3 h-3" /> CPU Load</span>
                      <span className="font-mono text-slate-200">{node.cpuUtilization}%</span>
                    </div>
                    <div className="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
                      <div className="bg-indigo-500 h-full rounded-full" style={{ width: `${node.cpuUtilization}%` }} />
                    </div>
                  </div>

                  <div>
                    <div className="flex justify-between text-slate-400 mb-1">
                      <span className="flex items-center gap-1"><HardDrive className="w-3 h-3" /> Memory / VRAM</span>
                      <span className="font-mono text-slate-200">{node.memoryUtilization}%</span>
                    </div>
                    <div className="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
                      <div className="bg-purple-500 h-full rounded-full" style={{ width: `${node.memoryUtilization}%` }} />
                    </div>
                  </div>

                  <div>
                    <div className="flex justify-between text-slate-400 mb-1">
                      <span className="flex items-center gap-1"><Zap className="w-3 h-3" /> Pool Saturation</span>
                      <span className="font-mono text-slate-200">{saturation.toFixed(0)}%</span>
                    </div>
                    <div className="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
                      <div className="bg-amber-500 h-full rounded-full" style={{ width: `${saturation}%` }} />
                    </div>
                  </div>
                </div>

                <div className="mt-3 flex items-center justify-between text-[11px] text-slate-400 bg-slate-900/60 p-2 rounded border border-slate-800">
                  <div className="flex items-center gap-2">
                    <span className="text-slate-500 font-mono">Warm Failover Target:</span>
                    <span className="text-indigo-300 font-semibold">{node.failoverTarget}</span>
                  </div>
                  <div className="flex items-center gap-3 font-mono text-[10px]">
                    <span>P95 Latency: <strong className="text-amber-300">{node.p95LatencyMs}ms</strong></span>
                    <span>Error Rate: <strong className="text-emerald-400">{(node.errorRate * 100).toFixed(1)}%</strong></span>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </Card>
    </div>
  );
};
