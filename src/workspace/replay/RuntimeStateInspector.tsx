import React from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { Eye, Cpu, Database, Network, ShieldCheck, Activity } from 'lucide-react';

export const RuntimeStateInspector: React.FC = () => {
  return (
    <div className="p-6 space-y-6 bg-[#0B1120] min-h-screen text-[#F8FAFC]">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4 border-b border-[#1E293B] pb-6">
        <div className="space-y-1">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-gradient-to-br from-emerald-500/20 to-teal-500/20 border border-emerald-500/30 rounded-xl text-emerald-400">
              <Eye className="w-5 h-5" />
            </div>
            <div>
              <h1 className="text-xl font-bold font-mono tracking-tight text-white flex items-center gap-2">
                Runtime State Inspector
                <Badge variant="success" size="sm">Point-in-Time Reconstruction</Badge>
              </h1>
              <p className="text-xs text-slate-400">
                Inspect synchronized runtime subsystems (Planner, DAG, Queues, Workers, Confidence, Memory, Truth).
              </p>
            </div>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <Badge variant="intelligence" size="sm">Active Cursor: Frame #6</Badge>
        </div>
      </div>

      {/* Subsystem Inspection Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 font-mono text-xs">
        {/* Planner state */}
        <Card className="p-5 bg-[#0F172A] border-[#1E293B] space-y-3">
          <div className="flex items-center justify-between border-b border-slate-800 pb-2">
            <span className="font-bold text-slate-200 flex items-center gap-2">
              <Activity className="w-4 h-4 text-cyan-400" />
              Planner State
            </span>
            <Badge variant="intelligence" size="sm">DECOMPOSING</Badge>
          </div>
          <div className="space-y-1 text-slate-400">
            <div>Active Goal: <span className="text-white">Multimodal Invoice Extraction</span></div>
            <div>Decomposed Tasks: <span className="text-cyan-300 font-bold">3 Tasks</span></div>
            <div>Critical Path: <span className="text-slate-300">task_ocr_01 &rarr; task_schema_01</span></div>
            <div>Estimated Duration: <span className="text-emerald-400">680.0ms</span></div>
          </div>
        </Card>

        {/* Scheduler Queues */}
        <Card className="p-5 bg-[#0F172A] border-[#1E293B] space-y-3">
          <div className="flex items-center justify-between border-b border-slate-800 pb-2">
            <span className="font-bold text-slate-200 flex items-center gap-2">
              <Network className="w-4 h-4 text-indigo-400" />
              Scheduler Queues
            </span>
            <Badge variant="outline" size="sm">Wavefront #0</Badge>
          </div>
          <div className="space-y-1.5 text-slate-400">
            <div className="flex justify-between">
              <span>Ready Queue:</span>
              <span className="text-emerald-400 font-bold">0</span>
            </div>
            <div className="flex justify-between">
              <span>Running Queue:</span>
              <span className="text-cyan-400 font-bold">1 (task_ocr_01)</span>
            </div>
            <div className="flex justify-between">
              <span>Blocked (Deps):</span>
              <span className="text-amber-400 font-bold">2</span>
            </div>
            <div className="flex justify-between">
              <span>Completed:</span>
              <span className="text-slate-300 font-bold">0</span>
            </div>
          </div>
        </Card>

        {/* Worker Allocations */}
        <Card className="p-5 bg-[#0F172A] border-[#1E293B] space-y-3">
          <div className="flex items-center justify-between border-b border-slate-800 pb-2">
            <span className="font-bold text-slate-200 flex items-center gap-2">
              <Cpu className="w-4 h-4 text-purple-400" />
              Worker Allocations
            </span>
            <Badge variant="success" size="sm">1 Active</Badge>
          </div>
          <div className="space-y-1 text-slate-400">
            <div>Worker: <span className="text-purple-300 font-bold">worker_gpu_ocr_01</span></div>
            <div>Role: <span className="text-slate-300">OCR Specialist</span></div>
            <div>Current Task: <span className="text-cyan-300">task_ocr_01</span></div>
            <div>Tool Executions: <span className="text-slate-300">Tesseract-v5, LayoutLM</span></div>
          </div>
        </Card>

        {/* Confidence state */}
        <Card className="p-5 bg-[#0F172A] border-[#1E293B] space-y-3">
          <div className="flex items-center justify-between border-b border-slate-800 pb-2">
            <span className="font-bold text-slate-200 flex items-center gap-2">
              <ShieldCheck className="w-4 h-4 text-emerald-400" />
              Confidence State
            </span>
            <Badge variant="success" size="sm">94.20%</Badge>
          </div>
          <div className="space-y-1 text-slate-400">
            <div>Formula: <span className="text-cyan-300">WeightedEnsemble (v1.3.0)</span></div>
            <div>95% CI: <span className="text-slate-300">[92.5%, 95.9%]</span></div>
            <div>Aleatoric Noise: <span className="text-slate-300">0.008</span></div>
            <div>Epistemic Uncertainty: <span className="text-emerald-400">0.006 (Low)</span></div>
          </div>
        </Card>

        {/* Truth Ledger */}
        <Card className="p-5 bg-[#0F172A] border-[#1E293B] space-y-3">
          <div className="flex items-center justify-between border-b border-slate-800 pb-2">
            <span className="font-bold text-slate-200 flex items-center gap-2">
              <Database className="w-4 h-4 text-amber-400" />
              Truth Ledger Proofs
            </span>
            <Badge variant="success" size="sm">All Passed</Badge>
          </div>
          <div className="space-y-1 text-slate-400">
            <div>Active Invariant: <span className="text-emerald-300">SMT Balance Check</span></div>
            <div>Proof Status: <span className="text-emerald-400 font-bold">PROVED (Z3 Solver)</span></div>
            <div>Root Seal: <span className="text-amber-400">sha256:7fa189c4...</span></div>
            <div>Violations: <span className="text-slate-500">0</span></div>
          </div>
        </Card>

        {/* Memory state */}
        <Card className="p-5 bg-[#0F172A] border-[#1E293B] space-y-3">
          <div className="flex items-center justify-between border-b border-slate-800 pb-2">
            <span className="font-bold text-slate-200 flex items-center gap-2">
              <Database className="w-4 h-4 text-blue-400" />
              Agent Memory
            </span>
            <Badge variant="outline" size="sm">Hit Ratio: 85%</Badge>
          </div>
          <div className="space-y-1 text-slate-400">
            <div>Retrieved Experiences: <span className="text-slate-300">2 Mined Templates</span></div>
            <div>Belief Node: <span className="text-blue-300">VendorFormat::Standard</span></div>
            <div>Causal Graph Links: <span className="text-slate-300">4 Active Nodes</span></div>
          </div>
        </Card>
      </div>
    </div>
  );
};
