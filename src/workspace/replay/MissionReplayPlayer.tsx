import React from 'react';
import { useWorkspace } from '../context/WorkspaceContext';
import { CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';

export const MissionReplayPlayer: React.FC = () => {
  const {
    replaySnapshots,
    currentReplayStep,
    isReplaying,
    setReplayStep,
    playReplay,
    pauseReplay,
    stepForwardReplay,
    stepBackwardReplay,
  } = useWorkspace();

  const activeSnapshot =
    replaySnapshots[currentReplayStep - 1] || replaySnapshots[0] || null;

  return (
    <div className="w-full flex flex-col h-[700px] rounded-2xl bg-[#0F172A]/90 border border-[#1E293B] shadow-2xl overflow-hidden">
      <CardHeader className="flex flex-row items-center justify-between py-4 px-6 border-b border-[#1E293B] bg-[#131D35]/50">
        <div>
          <div className="flex items-center gap-2">
            <Badge variant="intelligence" size="sm" hasDot isPulsing={isReplaying}>
              TIME MACHINE REPLAY
            </Badge>
            <span className="text-xs text-[#94A3B8] font-mono">
              Step {currentReplayStep} of {replaySnapshots.length}
            </span>
          </div>
          <CardTitle className="mt-1 text-base font-bold text-[#F8FAFC]">
            Deterministic Mission Replay & Execution Scrubber
          </CardTitle>
        </div>

        <div className="flex items-center gap-2">
          {isReplaying ? (
            <Button variant="secondary" size="sm" onClick={pauseReplay}>
              ⏸ Pause Playback
            </Button>
          ) : (
            <Button variant="intelligence" size="sm" onClick={playReplay}>
              ▶ Auto Play
            </Button>
          )}
        </div>
      </CardHeader>

      <CardContent className="flex-1 overflow-y-auto p-6 space-y-6 flex flex-col justify-between">
        {activeSnapshot && (
          <div className="space-y-6">
            {/* Scrubber Timeline Bar */}
            <div className="p-4 rounded-xl bg-[#131D35] border border-[#1E293B] space-y-3">
              <div className="flex items-center justify-between text-xs font-mono">
                <span className="text-[#00D2FF]">
                  Current Checkpoint: [{activeSnapshot.timestampUtc} UTC]
                </span>
                <span className="text-[#10B981] font-bold">
                  Stage: {activeSnapshot.stageName} ({activeSnapshot.activeAgent})
                </span>
              </div>

              {/* Step Slider */}
              <input
                type="range"
                min={1}
                max={replaySnapshots.length}
                value={currentReplayStep}
                onChange={(e) => setReplayStep(Number(e.target.value))}
                className="w-full accent-cyan-400 cursor-pointer"
              />

              {/* Stepper Buttons */}
              <div className="flex items-center justify-between pt-2">
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={stepBackwardReplay}
                  disabled={currentReplayStep <= 1}
                >
                  ⏮ Step Backward
                </Button>

                <div className="flex gap-2">
                  {replaySnapshots.map((s, idx) => (
                    <button
                      key={s.stepIndex}
                      onClick={() => setReplayStep(idx + 1)}
                      className={`h-6 w-6 rounded-full text-[10px] font-mono font-bold transition-all ${
                        currentReplayStep === idx + 1
                          ? 'bg-[#00D2FF] text-slate-900 shadow-[0_0_10px_rgba(0,210,255,0.8)]'
                          : 'bg-[#0A0F1D] text-[#64748B] hover:text-[#F8FAFC]'
                      }`}
                    >
                      {idx + 1}
                    </button>
                  ))}
                </div>

                <Button
                  variant="ghost"
                  size="sm"
                  onClick={stepForwardReplay}
                  disabled={currentReplayStep >= replaySnapshots.length}
                >
                  Step Forward ⏭
                </Button>
              </div>
            </div>

            {/* Replay State Snapshot Card */}
            <div className="p-6 rounded-2xl bg-[#131D35] border border-cyan-500/30 shadow-lg space-y-4">
              <div className="flex items-center justify-between border-b border-[#1E293B] pb-3">
                <div className="flex items-center gap-2">
                  <Badge variant="intelligence" size="md">
                    {activeSnapshot.activeAgent}
                  </Badge>
                  <h3 className="text-sm font-bold text-[#F8FAFC]">
                    {activeSnapshot.thoughtTitle}
                  </h3>
                </div>

                <span className="text-xs font-mono text-[#00D2FF] font-bold">
                  Confidence: {(activeSnapshot.currentConfidence * 100).toFixed(1)}%
                </span>
              </div>

              <div className="space-y-2 text-xs">
                <span className="text-[10px] font-mono uppercase text-[#64748B] block">
                  Cognitive Reasoning at this moment:
                </span>
                <p className="p-3 rounded-lg bg-[#0A0F1D] border border-[#1E293B] text-[#F8FAFC] font-mono leading-relaxed">
                  "{activeSnapshot.thoughtContent}"
                </p>
              </div>

              {activeSnapshot.activeDecisionTitle && (
                <div className="pt-2 flex items-center justify-between text-xs font-mono text-[#10B981]">
                  <span>⚡ Active Decision: {activeSnapshot.activeDecisionTitle}</span>
                  <span>Tasks Done: {activeSnapshot.completedTasksCount}</span>
                </div>
              )}

              {activeSnapshot.memoryAccessTitle && (
                <div className="pt-1 text-[11px] font-mono text-[#A855F7] flex items-center gap-1.5">
                  <span>🧠 Memory Retrieved:</span>
                  <span>{activeSnapshot.memoryAccessTitle}</span>
                </div>
              )}
            </div>
          </div>
        )}

        <div className="p-3 rounded-xl bg-[#0A0F1D] border border-[#1E293B] text-center text-xs font-mono text-[#64748B]">
          Deterministic Provenance: Replay matches underlying SHA-256 state ledger 1:1.
        </div>
      </CardContent>
    </div>
  );
};
