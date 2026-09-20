import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { EsmrReplayApiClient } from '../../services/esmrReplayApiClient';
export const SnapshotBrowserView = ({ missionId }) => {
    const [snapshots, setSnapshots] = useState([]);
    const [loading, setLoading] = useState(true);
    useEffect(() => {
        EsmrReplayApiClient.getSnapshots(missionId)
            .then(setSnapshots)
            .catch(console.error)
            .finally(() => setLoading(false));
    }, [missionId]);
    if (loading) {
        return (_jsx("div", { className: "p-6 bg-slate-900 border border-slate-800 rounded-xl text-slate-400 animate-pulse", children: "Fetching State Snapshots & Checkpoints..." }));
    }
    return (_jsxs("div", { className: "bg-slate-950 border border-slate-800 rounded-xl p-6 shadow-2xl space-y-6 text-slate-100", children: [_jsx("div", { className: "flex items-center justify-between border-b border-slate-800 pb-4", children: _jsxs("div", { children: [_jsxs("h3", { className: "text-lg font-bold text-white flex items-center gap-2", children: [_jsx("span", { children: "\uD83D\uDCBE" }), " Snapshot Manager & Checkpoint Browser"] }), _jsx("p", { className: "text-xs text-slate-400 mt-1", children: "Compressed state checkpoints enabling instant seek with deterministic incremental catch-up." })] }) }), _jsx("div", { className: "space-y-3", children: snapshots.map((snap) => (_jsxs("div", { className: "bg-slate-900 border border-slate-800 p-4 rounded-xl space-y-2", children: [_jsxs("div", { className: "flex items-center justify-between font-mono text-xs", children: [_jsx("span", { className: "font-bold text-cyan-400", children: snap.snapshot_id }), _jsxs("span", { className: "text-emerald-400", children: ["Event Index: ", snap.event_index] })] }), _jsxs("div", { className: "grid grid-cols-3 gap-2 text-xs font-mono text-slate-300", children: [_jsxs("div", { children: ["Uncompressed: ", snap.uncompressed_size_bytes, " B"] }), _jsxs("div", { children: ["Compressed: ", snap.compressed_size_bytes, " B"] }), _jsxs("div", { className: "text-cyan-400", children: ["Ratio: ", (snap.compression_ratio * 100).toFixed(1), "%"] })] }), _jsxs("div", { className: "text-[10px] font-mono text-slate-500 truncate", children: ["Checksum: ", snap.checksum] })] }, snap.snapshot_id))) })] }));
};
