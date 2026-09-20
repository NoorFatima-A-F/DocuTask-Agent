import React, { useState, useEffect } from 'react';
import type { ReplaySessionState, ReplaySpeed, ReplayBookmark } from '../../types/esmrReplay';
import { EsmrReplayApiClient } from '../../services/esmrReplayApiClient';

interface MissionReplayControllerProps {
  missionId: string;
  onStateChange?: (state: ReplaySessionState) => void;
}

export const MissionReplayController: React.FC<MissionReplayControllerProps> = ({
  missionId,
  onStateChange,
}) => {
  const [session, setSession] = useState<ReplaySessionState | null>(null);
  const [bookmarks, setBookmarks] = useState<ReplayBookmark[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [isPlaying, setIsPlaying] = useState<boolean>(false);

  const fetchState = async () => {
    try {
      const data = await EsmrReplayApiClient.getReplayState(missionId);
      setSession(data);
      if (onStateChange) onStateChange(data);
    } catch (err) {
      console.error('Failed to load replay state:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchState();
    EsmrReplayApiClient.getBookmarks(missionId).then(setBookmarks).catch(console.error);
  }, [missionId]);

  const handleSeek = async (index: number) => {
    const updated = await EsmrReplayApiClient.seek(missionId, index);
    setSession(updated);
    if (onStateChange) onStateChange(updated);
  };

  const handleStepForward = async () => {
    const updated = await EsmrReplayApiClient.stepForward(missionId);
    setSession(updated);
    if (onStateChange) onStateChange(updated);
  };

  const handleStepBackward = async () => {
    const updated = await EsmrReplayApiClient.stepBackward(missionId);
    setSession(updated);
    if (onStateChange) onStateChange(updated);
  };

  const handleSpeedChange = async (speed: ReplaySpeed) => {
    await EsmrReplayApiClient.setSpeed(missionId, speed);
    if (session) {
      setSession({ ...session, speed });
    }
  };

  const speeds: ReplaySpeed[] = ['0.25x', '0.5x', '1x', '2x', '4x', '8x', '16x', 'INSTANT'];

  if (loading || !session) {
    return (
      <div className="p-6 bg-slate-900 border border-slate-800 rounded-xl text-slate-400 animate-pulse">
        Initializing Event-Sourced Replay Runtime for Mission {missionId}...
      </div>
    );
  }

  const { cursor, state } = session;

  return (
    <div className="bg-slate-950 border border-slate-800 rounded-xl p-6 shadow-2xl space-y-6 text-slate-100">
      {/* Header & Status */}
      <div className="flex flex-wrap items-center justify-between gap-4 border-b border-slate-800 pb-4">
        <div>
          <div className="flex items-center gap-3">
            <span className="h-3 w-3 rounded-full bg-emerald-500 animate-ping" />
            <h2 className="text-xl font-bold tracking-tight text-white">Event-Sourced Mission Replay Runtime</h2>
            <span className="px-2.5 py-0.5 text-xs font-mono font-semibold bg-emerald-950/80 border border-emerald-500/40 text-emerald-400 rounded-md">
              DETERMINISTIC
            </span>
          </div>
          <p className="text-xs text-slate-400 font-mono mt-1">
            Mission: <span className="text-cyan-400">{missionId}</span> | Events Applied: {state.total_events_applied} / {cursor.total_events}
          </p>
        </div>

        {/* Speed Selector */}
        <div className="flex items-center gap-1.5 bg-slate-900 border border-slate-800 p-1.5 rounded-lg">
          <span className="text-xs font-medium text-slate-400 px-2">Speed:</span>
          {speeds.map((s) => (
            <button
              key={s}
              onClick={() => handleSpeedChange(s)}
              className={`px-2 py-1 text-xs font-mono font-medium rounded transition-all ${
                session.speed === s
                  ? 'bg-cyan-600 text-white shadow-sm'
                  : 'text-slate-400 hover:text-white hover:bg-slate-800'
              }`}
            >
              {s}
            </button>
          ))}
        </div>
      </div>

      {/* Scrubbing Timeline Bar */}
      <div className="space-y-2">
        <div className="flex justify-between text-xs font-mono text-slate-400">
          <span>Event Cursor: {cursor.current_index + 1} / {cursor.total_events}</span>
          <span>{cursor.progress_percentage.toFixed(1)}% Replayed</span>
          <span>Event ID: {cursor.current_event_id || 'None'}</span>
        </div>
        <input
          type="range"
          min="0"
          max={Math.max(0, cursor.total_events - 1)}
          value={cursor.current_index}
          onChange={(e) => handleSeek(parseInt(e.target.value, 10))}
          className="w-full h-2.5 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-cyan-500 hover:accent-cyan-400 transition-all"
        />
        {/* Bookmarks bar */}
        {bookmarks.length > 0 && (
          <div className="flex gap-2 pt-1 overflow-x-auto">
            {bookmarks.map((bm) => (
              <button
                key={bm.bookmark_id}
                onClick={() => handleSeek(bm.event_index)}
                className="px-2 py-0.5 text-[11px] font-mono bg-indigo-950/70 border border-indigo-500/40 text-indigo-300 rounded hover:bg-indigo-900 transition-colors flex items-center gap-1.5 shrink-0"
              >
                <span>📍</span>
                <span>{bm.label}</span>
                <span className="text-indigo-400">({bm.bookmark_type})</span>
              </button>
            ))}
          </div>
        )}
      </div>

      {/* Transport Controls */}
      <div className="flex flex-wrap items-center justify-between gap-4 bg-slate-900/80 border border-slate-800 p-4 rounded-xl">
        <div className="flex items-center gap-2">
          <button
            onClick={() => handleSeek(0)}
            title="Seek to Genesis (0)"
            className="p-2 text-slate-300 hover:text-white bg-slate-800 hover:bg-slate-700 rounded-lg transition-colors text-sm"
          >
            ⏮ Genesis
          </button>
          <button
            onClick={handleStepBackward}
            title="Step 1 Event Backward"
            className="p-2 text-slate-300 hover:text-white bg-slate-800 hover:bg-slate-700 rounded-lg transition-colors text-sm"
          >
            ⏪ Step Back
          </button>
          <button
            onClick={() => setIsPlaying(!isPlaying)}
            className={`px-4 py-2 font-semibold text-sm rounded-lg transition-colors ${
              isPlaying
                ? 'bg-amber-600 hover:bg-amber-500 text-white'
                : 'bg-cyan-600 hover:bg-cyan-500 text-white'
            }`}
          >
            {isPlaying ? '⏸ Pause' : '▶ Play Replay'}
          </button>
          <button
            onClick={handleStepForward}
            title="Step 1 Event Forward"
            className="p-2 text-slate-300 hover:text-white bg-slate-800 hover:bg-slate-700 rounded-lg transition-colors text-sm"
          >
            ⏩ Step Forward
          </button>
          <button
            onClick={() => handleSeek(cursor.total_events - 1)}
            title="Seek to Live Head"
            className="p-2 text-slate-300 hover:text-white bg-slate-800 hover:bg-slate-700 rounded-lg transition-colors text-sm"
          >
            ⏭ Live Head
          </button>
        </div>

        {/* State snapshot metrics */}
        <div className="flex items-center gap-6 text-xs font-mono">
          <div>
            <span className="text-slate-400">Current Stage: </span>
            <span className="font-semibold text-amber-400">{state.current_stage}</span>
          </div>
          <div>
            <span className="text-slate-400">Confidence: </span>
            <span className="font-semibold text-emerald-400">{(state.confidence_score * 100).toFixed(1)}%</span>
          </div>
          <div>
            <span className="text-slate-400">Cost: </span>
            <span className="font-semibold text-cyan-400">${state.total_cost_usd.toFixed(4)}</span>
          </div>
          <div>
            <span className="text-slate-400">DAG Ver: </span>
            <span className="font-semibold text-purple-400">v{state.dag_version}</span>
          </div>
        </div>
      </div>
    </div>
  );
};
