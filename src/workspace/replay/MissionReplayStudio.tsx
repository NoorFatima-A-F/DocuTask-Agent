import React, { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { Play, Pause, SkipBack, SkipForward, RotateCcw, Bookmark, FastForward, ShieldCheck } from 'lucide-react';

export const MissionReplayStudio: React.FC = () => {
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentCursor, setCurrentCursor] = useState(4);
  const [playbackSpeed, setPlaybackSpeed] = useState<number>(1.0);
  const totalEvents = 10;

  const mockFrames = [
    { cursor: 0, title: 'Mission Ingested & Goal Parsed', time: '00:00:01', sub: 'mission.started', conf: '50.0%' },
    { cursor: 1, title: 'Planner Strategy Decomposed (14-State)', time: '00:00:02', sub: 'planner.lifecycle', conf: '65.0%' },
    { cursor: 2, title: 'DAG Wavefront Partitioning', time: '00:00:03', sub: 'planner.dag', conf: '75.0%' },
    { cursor: 3, title: 'GPU Worker Assigned to OCR Pipeline', time: '00:00:04', sub: 'schedule.assigned', conf: '88.0%' },
    { cursor: 4, title: 'OCR Execution Succeeded (285ms)', time: '00:00:08', sub: 'worker.completed', conf: '94.2%' },
    { cursor: 5, title: 'Confidence Re-evaluation (v1.3.0)', time: '00:00:09', sub: 'confidence.evaluated', conf: '96.5%' },
    { cursor: 6, title: 'SMT Invariant Proof Verified', time: '00:00:12', sub: 'truth.invariant', conf: '98.0%' },
    { cursor: 7, title: 'Truth Ledger Merkle Root Sealed', time: '00:00:13', sub: 'truth.merkle', conf: '99.2%' },
    { cursor: 8, title: 'Mission Completed with 100% Truth Proof', time: '00:00:15', sub: 'mission.completed', conf: '98.42%' },
  ];

  const currentFrame = mockFrames[Math.min(currentCursor, mockFrames.length - 1)];

  return (
    <div className="p-6 space-y-6 bg-[#0B1120] min-h-screen text-[#F8FAFC]">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4 border-b border-[#1E293B] pb-6">
        <div className="space-y-1">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-gradient-to-br from-cyan-500/20 to-blue-500/20 border border-cyan-500/30 rounded-xl text-cyan-400">
              <Play className="w-5 h-5" />
            </div>
            <div>
              <h1 className="text-xl font-bold font-mono tracking-tight text-white flex items-center gap-2">
                Mission Replay Studio
                <Badge variant="success" size="sm">Phase 13.4 Reconstructor</Badge>
              </h1>
              <p className="text-xs text-slate-400">
                Deterministic event-sourced replay engine with frame-by-frame state derivation and speed control.
              </p>
            </div>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <Badge variant="intelligence" size="sm">Event Store: 10 Immutable Events</Badge>
          <Badge variant="outline" size="sm">Root: sha256:7fa189c4...</Badge>
        </div>
      </div>

      {/* Playback Control Bar */}
      <Card className="p-5 bg-[#0F172A] border-[#1E293B] space-y-4">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div className="flex items-center gap-2">
            <button
              onClick={() => setCurrentCursor(0)}
              className="p-2 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-lg transition-colors"
              title="Reset to start"
            >
              <RotateCcw className="w-4 h-4" />
            </button>
            <button
              onClick={() => setCurrentCursor(Math.max(0, currentCursor - 1))}
              className="p-2 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-lg transition-colors"
              title="Step Backward"
            >
              <SkipBack className="w-4 h-4" />
            </button>
            <button
              onClick={() => setIsPlaying(!isPlaying)}
              className="px-4 py-2 bg-gradient-to-r from-cyan-500 to-blue-500 hover:from-cyan-400 hover:to-blue-400 text-slate-950 font-bold rounded-lg flex items-center gap-2 transition-all font-mono"
            >
              {isPlaying ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4" />}
              {isPlaying ? 'PAUSE' : 'PLAY'}
            </button>
            <button
              onClick={() => setCurrentCursor(Math.min(totalEvents - 1, currentCursor + 1))}
              className="p-2 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-lg transition-colors"
              title="Step Forward"
            >
              <SkipForward className="w-4 h-4" />
            </button>
          </div>

          <div className="flex items-center gap-3 font-mono text-xs">
            <span className="text-slate-400">Speed:</span>
            {[0.5, 1.0, 2.0, 5.0].map((s) => (
              <button
                key={s}
                onClick={() => setPlaybackSpeed(s)}
                className={`px-2.5 py-1 rounded border text-xs font-semibold ${
                  playbackSpeed === s
                    ? 'bg-cyan-500/20 border-cyan-500/50 text-cyan-400'
                    : 'bg-slate-900 border-slate-800 text-slate-400 hover:text-white'
                }`}
              >
                {s}x
              </button>
            ))}
          </div>

          <button className="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-amber-300 text-xs font-mono rounded-lg flex items-center gap-1.5 border border-amber-500/30">
            <Bookmark className="w-3.5 h-3.5" /> Bookmark Frame
          </button>
        </div>

        {/* Scrubber Progress Bar */}
        <div className="space-y-2 font-mono">
          <div className="flex justify-between text-xs text-slate-400">
            <span>Event Cursor: #{currentCursor} / {totalEvents - 1}</span>
            <span className="text-cyan-400">{currentFrame?.time || '00:00:00'}</span>
          </div>
          <input
            type="range"
            min="0"
            max={totalEvents - 1}
            value={currentCursor}
            onChange={(e) => setCurrentCursor(parseInt(e.target.value, 10))}
            className="w-full accent-cyan-400 bg-slate-800 rounded-lg h-2 cursor-pointer"
          />
        </div>
      </Card>

      {/* Active Replay Frame Inspector */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <Card className="lg:col-span-2 p-5 bg-[#0F172A] border-[#1E293B] space-y-4">
          <div className="flex items-center justify-between border-b border-[#1E293B] pb-3">
            <div className="font-mono text-sm font-bold text-white flex items-center gap-2">
              <FastForward className="w-4 h-4 text-cyan-400" />
              Reconstructed Frame #{currentCursor}
            </div>
            <Badge variant="intelligence" size="sm">{currentFrame?.sub}</Badge>
          </div>

          <div className="space-y-3 font-mono text-xs">
            <div className="p-3 bg-slate-900/60 rounded-lg border border-slate-800">
              <div className="text-slate-400 font-semibold mb-1">State Summary:</div>
              <div className="text-white text-sm font-bold">{currentFrame?.title}</div>
            </div>

            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
              <div className="p-2.5 bg-slate-900/40 rounded border border-slate-800">
                <div className="text-slate-500 text-[10px]">Planner State</div>
                <div className="text-indigo-400 font-bold mt-1">DECOMPOSING</div>
              </div>
              <div className="p-2.5 bg-slate-900/40 rounded border border-slate-800">
                <div className="text-slate-500 text-[10px]">Active Worker</div>
                <div className="text-emerald-400 font-bold mt-1">worker_gpu_ocr</div>
              </div>
              <div className="p-2.5 bg-slate-900/40 rounded border border-slate-800">
                <div className="text-slate-500 text-[10px]">Confidence</div>
                <div className="text-cyan-400 font-bold mt-1">{currentFrame?.conf}</div>
              </div>
              <div className="p-2.5 bg-slate-900/40 rounded border border-slate-800">
                <div className="text-slate-500 text-[10px]">Truth Invariant</div>
                <div className="text-emerald-400 font-bold mt-1">SATISFIED</div>
              </div>
            </div>
          </div>
        </Card>

        {/* Verification seal */}
        <Card className="p-5 bg-[#0F172A] border-[#1E293B] flex flex-col justify-between font-mono">
          <div className="space-y-3">
            <div className="text-xs font-bold text-slate-300 flex items-center gap-2">
              <ShieldCheck className="w-4 h-4 text-emerald-400" />
              Replay Authenticity
            </div>
            <div className="text-xs text-slate-400 space-y-1.5">
              <div>Merkle Root: <code className="text-emerald-400 text-[11px]">sha256:7fa189c4...</code></div>
              <div>Event Continuity: <span className="text-emerald-400 font-bold">100% (0 breaks)</span></div>
              <div>Formula Monotonicity: <span className="text-cyan-400 font-bold">Guaranteed</span></div>
            </div>
          </div>
          <Badge variant="success" size="sm" className="w-full justify-center py-1 mt-4">
            Cryptographically Verified
          </Badge>
        </Card>
      </div>
    </div>
  );
};
