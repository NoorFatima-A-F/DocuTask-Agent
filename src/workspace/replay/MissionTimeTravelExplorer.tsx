import React from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { Compass, RotateCcw } from 'lucide-react';

export const MissionTimeTravelExplorer: React.FC = () => {
  const checkpoints = [
    { id: 'chk_00', cursor: 0, label: 'Prior Ingestion Baseline', hash: 'sha256:0018fa...', size: '1.2 KB' },
    { id: 'chk_04', cursor: 4, label: 'OCR Step Completion Checkpoint', hash: 'sha256:7fa189...', size: '3.4 KB' },
    { id: 'chk_08', cursor: 8, label: 'Final Truth Ledger Sealing', hash: 'sha256:99cba1...', size: '4.8 KB' },
  ];

  return (
    <div className="p-6 space-y-6 bg-[#0B1120] min-h-screen text-[#F8FAFC]">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4 border-b border-[#1E293B] pb-6">
        <div className="space-y-1">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-gradient-to-br from-indigo-500/20 to-teal-500/20 border border-indigo-500/30 rounded-xl text-indigo-400">
              <Compass className="w-5 h-5" />
            </div>
            <div>
              <h1 className="text-xl font-bold font-mono tracking-tight text-white flex items-center gap-2">
                Mission Time Travel & Checkpoint Explorer
                <Badge variant="intelligence" size="sm">Instant Point-in-Time Restore</Badge>
              </h1>
              <p className="text-xs text-slate-400">
                Jump to historical execution checkpoints, restore state snapshots, and inspect point-in-time runtime graphs.
              </p>
            </div>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <Badge variant="outline" size="sm">3 Checkpoints Indexed</Badge>
        </div>
      </div>

      {/* Checkpoints List */}
      <div className="space-y-4 font-mono text-xs">
        {checkpoints.map((cp) => (
          <Card key={cp.id} className="p-5 bg-[#0F172A] border-[#1E293B] hover:border-indigo-500/40 transition-all flex flex-wrap items-center justify-between gap-4">
            <div className="space-y-1">
              <div className="flex items-center gap-3">
                <span className="text-indigo-400 font-bold">#{cp.cursor}</span>
                <span className="text-white font-bold text-sm">{cp.label}</span>
                <Badge variant="outline" size="sm">{cp.id}</Badge>
              </div>
              <div className="text-slate-400 text-[11px] flex items-center gap-3 mt-1">
                <span>State Hash: <code className="text-slate-300 bg-slate-900 px-1 py-0.5 rounded">{cp.hash}</code></span>
                <span>Size: <span className="text-slate-300">{cp.size}</span></span>
              </div>
            </div>

            <button className="px-3 py-1.5 bg-indigo-500/20 hover:bg-indigo-500/30 text-indigo-300 border border-indigo-500/40 rounded-lg flex items-center gap-1.5 transition-colors text-xs font-semibold">
              <RotateCcw className="w-3.5 h-3.5" /> Restore State at #{cp.cursor}
            </button>
          </Card>
        ))}
      </div>
    </div>
  );
};
