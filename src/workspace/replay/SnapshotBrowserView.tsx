import React, { useState, useEffect } from 'react';
import type { SnapshotMetadata } from '../../types/esmrReplay';
import { EsmrReplayApiClient } from '../../services/esmrReplayApiClient';

interface SnapshotBrowserViewProps {
  missionId: string;
}

export const SnapshotBrowserView: React.FC<SnapshotBrowserViewProps> = ({ missionId }) => {
  const [snapshots, setSnapshots] = useState<SnapshotMetadata[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    EsmrReplayApiClient.getSnapshots(missionId)
      .then(setSnapshots)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, [missionId]);

  if (loading) {
    return (
      <div className="p-6 bg-slate-900 border border-slate-800 rounded-xl text-slate-400 animate-pulse">
        Fetching State Snapshots & Checkpoints...
      </div>
    );
  }

  return (
    <div className="bg-slate-950 border border-slate-800 rounded-xl p-6 shadow-2xl space-y-6 text-slate-100">
      <div className="flex items-center justify-between border-b border-slate-800 pb-4">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <span>💾</span> Snapshot Manager & Checkpoint Browser
          </h3>
          <p className="text-xs text-slate-400 mt-1">
            Compressed state checkpoints enabling instant seek with deterministic incremental catch-up.
          </p>
        </div>
      </div>

      <div className="space-y-3">
        {snapshots.map((snap) => (
          <div key={snap.snapshot_id} className="bg-slate-900 border border-slate-800 p-4 rounded-xl space-y-2">
            <div className="flex items-center justify-between font-mono text-xs">
              <span className="font-bold text-cyan-400">{snap.snapshot_id}</span>
              <span className="text-emerald-400">Event Index: {snap.event_index}</span>
            </div>
            <div className="grid grid-cols-3 gap-2 text-xs font-mono text-slate-300">
              <div>Uncompressed: {snap.uncompressed_size_bytes} B</div>
              <div>Compressed: {snap.compressed_size_bytes} B</div>
              <div className="text-cyan-400">Ratio: {(snap.compression_ratio * 100).toFixed(1)}%</div>
            </div>
            <div className="text-[10px] font-mono text-slate-500 truncate">
              Checksum: {snap.checksum}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
