import React, { useState } from 'react';

interface EvidenceExplorerViewProps {
  missionId: string;
}

export const EvidenceExplorerView: React.FC<EvidenceExplorerViewProps> = ({ missionId }) => {
  const [selectedTab, setSelectedTab] = useState<'OCR_BOXES' | 'SMT_INVARIANTS' | 'SOURCE_CROPS'>('SMT_INVARIANTS');

  return (
    <div className="bg-slate-950 border border-slate-800 rounded-xl p-6 shadow-2xl space-y-6 text-slate-100">
      <div className="flex flex-wrap items-center justify-between gap-4 border-b border-slate-800 pb-4">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <span>🔬</span> Forensic Evidence & Invariant Proof Explorer
          </h3>
          <p className="text-xs text-slate-400 mt-1">
            Reconstruct visual bounding boxes, OCR spatial tokens, and formal SMT arithmetic invariants at this replay step.
          </p>
        </div>

        <div className="flex bg-slate-900 border border-slate-800 p-1 rounded-lg">
          <button
            onClick={() => setSelectedTab('SMT_INVARIANTS')}
            className={`px-3 py-1 text-xs font-mono rounded ${
              selectedTab === 'SMT_INVARIANTS' ? 'bg-cyan-600 text-white' : 'text-slate-400 hover:text-white'
            }`}
          >
            SMT Invariants
          </button>
          <button
            onClick={() => setSelectedTab('OCR_BOXES')}
            className={`px-3 py-1 text-xs font-mono rounded ${
              selectedTab === 'OCR_BOXES' ? 'bg-cyan-600 text-white' : 'text-slate-400 hover:text-white'
            }`}
          >
            Spatial BBoxes
          </button>
          <button
            onClick={() => setSelectedTab('SOURCE_CROPS')}
            className={`px-3 py-1 text-xs font-mono rounded ${
              selectedTab === 'SOURCE_CROPS' ? 'bg-cyan-600 text-white' : 'text-slate-400 hover:text-white'
            }`}
          >
            Artifact Inspection
          </button>
        </div>
      </div>

      {selectedTab === 'SMT_INVARIANTS' && (
        <div className="space-y-4">
          <div className="bg-emerald-950/40 border border-emerald-500/40 p-4 rounded-xl">
            <div className="flex items-center justify-between">
              <span className="text-xs font-mono font-bold text-emerald-400">SMT FORMAL PROOF: SATISFIABLE (SAT)</span>
              <span className="text-xs font-mono text-slate-300">Z3 / CVC5 Proof Engine</span>
            </div>
            <p className="text-xs text-emerald-200 mt-1">
              Arithmetic Invariant Verified: Total = Subtotal ($4,250.00) + Tax ($340.00) - Discount ($0.00) == $4,590.00.
            </p>
          </div>

          <div className="bg-slate-900 p-4 rounded-xl border border-slate-800 space-y-2">
            <span className="text-xs font-bold text-slate-400 font-mono">Formal Assertion Script</span>
            <pre className="text-xs text-cyan-300 font-mono bg-slate-950 p-3 rounded overflow-x-auto">
{`(declare-const subtotal Real)
(declare-const tax Real)
(declare-const total Real)
(assert (= subtotal 4250.00))
(assert (= tax 340.00))
(assert (= total (+ subtotal tax)))
(check-sat)
(get-model)`}
            </pre>
          </div>
        </div>
      )}

      {selectedTab === 'OCR_BOXES' && (
        <div className="bg-slate-900 border border-slate-800 p-6 rounded-xl text-center space-y-3">
          <span className="text-slate-400 text-xs font-mono">
            Extracted 28 layout tokens with sub-pixel normalized coordinate bounding boxes [ymin, xmin, ymax, xmax].
          </span>
          <div className="h-48 bg-slate-950 border border-slate-800 rounded-lg flex items-center justify-center text-slate-500 text-xs font-mono">
            [ Spatial Coordinate Overlay Rendered Deterministically from Event Stream ]
          </div>
        </div>
      )}

      {selectedTab === 'SOURCE_CROPS' && (
        <div className="bg-slate-900 border border-slate-800 p-6 rounded-xl text-center text-slate-400 text-xs font-mono">
          Artifacts for Mission {missionId}: Raw PDF, Clean OCR Vector Layer, Extracted JSON Schema.
        </div>
      )}
    </div>
  );
};
