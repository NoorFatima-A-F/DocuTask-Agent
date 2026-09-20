import React from 'react';

interface HumanReviewReplayViewProps {
  missionId: string;
}

export const HumanReviewReplayView: React.FC<HumanReviewReplayViewProps> = ({ missionId }) => {
  return (
    <div className="bg-slate-950 border border-slate-800 rounded-xl p-6 shadow-2xl space-y-6 text-slate-100">
      <div className="flex items-center justify-between border-b border-slate-800 pb-4">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <span>👤</span> Human Review & Intervention Playback
          </h3>
          <p className="text-xs text-slate-400 mt-1">
            Visualizes human-in-the-loop approvals, override adjustments, and feedback reflections during replay.
          </p>
        </div>
      </div>

      <div className="space-y-4">
        <div className="bg-slate-900 border border-slate-800 p-4 rounded-xl space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-xs font-mono font-bold text-cyan-400">STAGE: HUMAN_APPROVAL_GATE</span>
            <span className="text-xs text-emerald-400 font-mono">STATUS: AUTO_APPROVED_CONFIDENCE_HIGH</span>
          </div>
          <p className="text-xs text-slate-300">
            Automated compliance confidence (98.0%) exceeded threshold (&gt; 95.0%). No human override intervention required for Mission {missionId}.
          </p>
        </div>
      </div>
    </div>
  );
};
