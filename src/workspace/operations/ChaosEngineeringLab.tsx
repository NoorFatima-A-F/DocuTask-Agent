import React, { useState } from 'react';
import {
  Flame,
  CheckCircle2,
  RefreshCw,
  Play,
  Layers,
  StopCircle
} from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';

interface ChaosEngineeringLabProps {
  missionId?: string;
}

export const ChaosEngineeringLab: React.FC<ChaosEngineeringLabProps> = ({
  missionId = 'cluster-primary-master',
}) => {
  const [experiments] = useState([
    {
      experimentId: 'exp-wrk-01',
      name: 'Worker Crash & Auto-Heal Resilience',
      target: 'WORKERS',
      fault: 'WORKER_CRASH',
      status: 'COMPLETED',
      mttrMs: 185.0,
      resilienceScore: 98.2,
      invariantsPreserved: true,
      timestamp: '10:14 UTC',
    },
    {
      experimentId: 'exp-net-02',
      name: 'Simulated LLM Rate Limit Injection',
      target: 'API',
      fault: 'LLM_RATE_LIMIT',
      status: 'COMPLETED',
      mttrMs: 82.0,
      resilienceScore: 99.4,
      invariantsPreserved: true,
      timestamp: '09:42 UTC',
    },
    {
      experimentId: 'exp-gpu-03',
      name: 'OCR Latency Spike Injection',
      target: 'WORKERS',
      fault: 'OCR_FAILURE',
      status: 'COMPLETED',
      mttrMs: 210.0,
      resilienceScore: 97.5,
      invariantsPreserved: true,
      timestamp: '08:30 UTC',
    },
  ]);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-slate-100 flex items-center gap-2">
            <Flame className="w-5 h-5 text-rose-400" />
            Controlled Chaos Engineering & Resilience Lab
          </h2>
          <p className="text-sm text-slate-400">
            Automated fault injection, recovery evaluation, zero data-loss invariant validation, and resilience benchmarking for: <code className="text-rose-300 font-mono text-xs">{missionId}</code>
          </p>
        </div>
        <div className="flex items-center gap-3">
          <Badge variant="success" size="md">
            Invariant Preservation: 100%
          </Badge>
          <button className="flex items-center gap-1.5 px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-medium rounded-lg border border-slate-700">
            <RefreshCw className="w-3.5 h-3.5" />
            Scan Resilience
          </button>
        </div>
      </div>

      {/* Fault Injector Panel */}
      <Card className="p-5 bg-slate-900 border-slate-800 space-y-4 font-mono">
        <div className="flex items-center justify-between border-b border-slate-800 pb-3">
          <h3 className="text-sm font-semibold text-slate-200 flex items-center gap-2">
            <Play className="w-4 h-4 text-emerald-400" />
            Fault Injection Control Panel
          </h3>
          <Badge variant="intelligence" size="sm">Blast Radius: ISOLATED_CONTAINER</Badge>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
          <button className="p-3.5 bg-slate-950 hover:bg-slate-800 border border-slate-800 rounded-xl text-left space-y-1 transition-all">
            <span className="text-xs font-bold text-slate-200 block flex items-center gap-1.5">
              <Flame className="w-3.5 h-3.5 text-rose-400" /> Inject Worker Crash
            </span>
            <span className="text-[11px] text-slate-400 block">Simulates worker segfault</span>
          </button>

          <button className="p-3.5 bg-slate-950 hover:bg-slate-800 border border-slate-800 rounded-xl text-left space-y-1 transition-all">
            <span className="text-xs font-bold text-slate-200 block flex items-center gap-1.5">
              <Flame className="w-3.5 h-3.5 text-amber-400" /> Inject 429 Rate Limit
            </span>
            <span className="text-[11px] text-slate-400 block">Tests fallback model engagement</span>
          </button>

          <button className="p-3.5 bg-slate-950 hover:bg-slate-800 border border-slate-800 rounded-xl text-left space-y-1 transition-all">
            <span className="text-xs font-bold text-slate-200 block flex items-center gap-1.5">
              <StopCircle className="w-3.5 h-3.5 text-indigo-400" /> Inject 3s Latency Delay
            </span>
            <span className="text-[11px] text-slate-400 block">Validates circuit breaker triggers</span>
          </button>
        </div>
      </Card>

      {/* Chaos Experiment History */}
      <div className="space-y-3 font-mono">
        <h3 className="text-sm font-semibold text-slate-200 flex items-center gap-2">
          <Layers className="w-4 h-4 text-cyan-400" />
          Completed Chaos Experiment Reports
        </h3>

        {experiments.map((exp) => (
          <Card key={exp.experimentId} className="p-4 bg-slate-900 border-slate-800 space-y-2">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <span className="text-xs font-bold text-indigo-400">{exp.experimentId}</span>
                <span className="text-xs font-bold text-slate-200">{exp.name}</span>
                <Badge variant="intelligence" size="sm">{exp.target}</Badge>
              </div>
              <div className="flex items-center gap-2">
                <Badge variant="success" size="sm">
                  <CheckCircle2 className="w-3 h-3 mr-1" />
                  Score: {exp.resilienceScore}%
                </Badge>
                <span className="text-xs text-slate-400">{exp.mttrMs}ms MTTR</span>
              </div>
            </div>

            <div className="flex items-center justify-between text-[11px] bg-slate-950 p-2.5 rounded border border-slate-800 text-slate-400">
              <span>Fault: <strong className="text-amber-400">{exp.fault}</strong></span>
              <span>Invariants Preserved: <strong className="text-emerald-400">TRUE (0 LEAKS)</strong></span>
              <span>Run Time: <strong className="text-slate-300">{exp.timestamp}</strong></span>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};
