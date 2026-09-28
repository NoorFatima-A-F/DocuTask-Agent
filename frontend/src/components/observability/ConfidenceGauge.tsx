import React from 'react';
import { BrainCircuit } from 'lucide-react';

interface ConfidenceGaugeProps {
  score: number; // 0.0 to 1.0
}

export const ConfidenceGauge: React.FC<ConfidenceGaugeProps> = ({ score }) => {
  const percentage = (score * 100).toFixed(1);

  return (
    <div className="p-4 rounded-xl border border-slate-800 bg-slate-900/40 space-y-3">
      <div className="flex items-center justify-between">
        <span className="text-xs font-mono font-semibold text-slate-300 flex items-center gap-1.5">
          <BrainCircuit className="w-3.5 h-3.5 text-indigo-400" />
          Bayesian Evidence & Confidence Engine
        </span>
        <span className="text-xs font-mono font-bold text-emerald-400">
          {percentage}% Posterior
        </span>
      </div>

      <div className="w-full bg-slate-950 rounded-full h-2 overflow-hidden border border-slate-800">
        <div
          className="bg-gradient-to-r from-amber-500 via-cyan-400 to-emerald-400 h-full rounded-full transition-all duration-500"
          style={{ width: `${percentage}%` }}
        />
      </div>

      <div className="grid grid-cols-3 gap-2 text-[11px] font-mono text-slate-400 pt-1">
        <div className="p-2 rounded bg-slate-950/60 border border-slate-800 flex flex-col">
          <span className="text-[10px] text-slate-500">OCR Evidence</span>
          <span className="text-slate-200 font-semibold">96.5%</span>
        </div>
        <div className="p-2 rounded bg-slate-950/60 border border-slate-800 flex flex-col">
          <span className="text-[10px] text-slate-500">Schema Invariant</span>
          <span className="text-slate-200 font-semibold">98.5%</span>
        </div>
        <div className="p-2 rounded bg-slate-950/60 border border-slate-800 flex flex-col">
          <span className="text-[10px] text-slate-500">Consensus Audit</span>
          <span className="text-slate-200 font-semibold">97.2%</span>
        </div>
      </div>
    </div>
  );
};
