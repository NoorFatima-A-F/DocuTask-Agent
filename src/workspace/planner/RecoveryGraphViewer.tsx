import React, { useState } from 'react';
import {
  ShieldAlert,
  Sparkles,
  CheckCircle,
} from 'lucide-react';
import { ApdlePlannerApiClient } from '../../services/apdlePlannerApiClient';

export const RecoveryGraphViewer: React.FC = () => {
  const [injected, setInjected] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(false);

  const handleSimulateRecovery = async () => {
    setLoading(true);
    try {
      await ApdlePlannerApiClient.triggerReplan(
        'default_mission',
        'node_ocr_01',
        'Low OCR Confidence Holdout Scan (0.38)'
      );
      setInjected(true);
    } catch (e) {
      console.error('Recovery failed:', e);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6 font-mono">
      {/* Header Banner */}
      <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-5 space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-800 pb-3">
          <div>
            <h3 className="text-sm font-bold text-cyan-300 flex items-center gap-2">
              <ShieldAlert className="w-4 h-4 text-purple-400" />
              Autonomous Recovery DAG Subsystem
            </h3>
            <p className="text-xs text-slate-400 mt-0.5">
              Replaces blind retry loops with executable recovery DAG branches (Deskewing $\to$ Schema Relaxation $\to$ Re-validation).
            </p>
          </div>

          <button
            onClick={handleSimulateRecovery}
            disabled={loading}
            className="flex items-center gap-1.5 px-3 py-1.5 bg-purple-950/60 hover:bg-purple-900/60 border border-purple-800 text-purple-300 rounded-lg text-xs font-mono transition-all disabled:opacity-50"
          >
            <Sparkles className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
            Inject Recovery Pipeline
          </button>
        </div>

        {injected && (
          <div className="p-3 bg-emerald-950/40 border border-emerald-800/80 rounded-lg flex items-center gap-2 text-xs text-emerald-300">
            <CheckCircle className="w-4 h-4 text-emerald-400 shrink-0" />
            <span>Recovery subgraph successfully injected! Generation incremented and wavefront re-evaluated.</span>
          </div>
        )}

        {/* Recovery Pipeline Steps */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="p-4 bg-slate-950/80 border border-red-800/60 rounded-xl space-y-2 text-xs">
            <div className="text-[10px] text-red-400 uppercase font-bold">1. Failure Point</div>
            <div className="text-sm font-bold text-slate-100">Adaptive OCR Scan</div>
            <div className="text-[11px] text-slate-400">Low confidence scan (0.38 &lt; 0.70 threshold)</div>
            <div className="text-[10px] text-red-400 font-bold">STATUS: FAILED / MUTATED</div>
          </div>

          <div className="p-4 bg-slate-950/80 border border-purple-800/80 rounded-xl space-y-2 text-xs">
            <div className="text-[10px] text-purple-400 uppercase font-bold">2. Injected Recovery Branch</div>
            <div className="text-sm font-bold text-purple-200">Image Contrast & Deskew Filter</div>
            <div className="text-[11px] text-slate-400">Pre-processes image raster before secondary OCR pass</div>
            <div className="text-[10px] text-purple-400 font-bold">STATUS: INJECTED & EXECUTING</div>
          </div>

          <div className="p-4 bg-slate-950/80 border border-emerald-800/60 rounded-xl space-y-2 text-xs">
            <div className="text-[10px] text-emerald-400 uppercase font-bold">3. Resume Target</div>
            <div className="text-sm font-bold text-slate-100">Table Line-Item Parsing</div>
            <div className="text-[11px] text-slate-400">Consumes recovered high-resolution OCR text</div>
            <div className="text-[10px] text-emerald-400 font-bold">STATUS: READY TO RESUME</div>
          </div>
        </div>
      </div>
    </div>
  );
};
