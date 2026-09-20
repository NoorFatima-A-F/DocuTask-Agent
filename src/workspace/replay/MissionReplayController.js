import { jsxs as _jsxs, jsx as _jsx } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { EsmrReplayApiClient } from '../../services/esmrReplayApiClient';
export const MissionReplayController = ({ missionId, onStateChange, }) => {
    const [session, setSession] = useState(null);
    const [bookmarks, setBookmarks] = useState([]);
    const [loading, setLoading] = useState(true);
    const [isPlaying, setIsPlaying] = useState(false);
    const fetchState = async () => {
        try {
            const data = await EsmrReplayApiClient.getReplayState(missionId);
            setSession(data);
            if (onStateChange)
                onStateChange(data);
        }
        catch (err) {
            console.error('Failed to load replay state:', err);
        }
        finally {
            setLoading(false);
        }
    };
    useEffect(() => {
        fetchState();
        EsmrReplayApiClient.getBookmarks(missionId).then(setBookmarks).catch(console.error);
    }, [missionId]);
    const handleSeek = async (index) => {
        const updated = await EsmrReplayApiClient.seek(missionId, index);
        setSession(updated);
        if (onStateChange)
            onStateChange(updated);
    };
    const handleStepForward = async () => {
        const updated = await EsmrReplayApiClient.stepForward(missionId);
        setSession(updated);
        if (onStateChange)
            onStateChange(updated);
    };
    const handleStepBackward = async () => {
        const updated = await EsmrReplayApiClient.stepBackward(missionId);
        setSession(updated);
        if (onStateChange)
            onStateChange(updated);
    };
    const handleSpeedChange = async (speed) => {
        await EsmrReplayApiClient.setSpeed(missionId, speed);
        if (session) {
            setSession({ ...session, speed });
        }
    };
    const speeds = ['0.25x', '0.5x', '1x', '2x', '4x', '8x', '16x', 'INSTANT'];
    if (loading || !session) {
        return (_jsxs("div", { className: "p-6 bg-slate-900 border border-slate-800 rounded-xl text-slate-400 animate-pulse", children: ["Initializing Event-Sourced Replay Runtime for Mission ", missionId, "..."] }));
    }
    const { cursor, state } = session;
    return (_jsxs("div", { className: "bg-slate-950 border border-slate-800 rounded-xl p-6 shadow-2xl space-y-6 text-slate-100", children: [_jsxs("div", { className: "flex flex-wrap items-center justify-between gap-4 border-b border-slate-800 pb-4", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-3", children: [_jsx("span", { className: "h-3 w-3 rounded-full bg-emerald-500 animate-ping" }), _jsx("h2", { className: "text-xl font-bold tracking-tight text-white", children: "Event-Sourced Mission Replay Runtime" }), _jsx("span", { className: "px-2.5 py-0.5 text-xs font-mono font-semibold bg-emerald-950/80 border border-emerald-500/40 text-emerald-400 rounded-md", children: "DETERMINISTIC" })] }), _jsxs("p", { className: "text-xs text-slate-400 font-mono mt-1", children: ["Mission: ", _jsx("span", { className: "text-cyan-400", children: missionId }), " | Events Applied: ", state.total_events_applied, " / ", cursor.total_events] })] }), _jsxs("div", { className: "flex items-center gap-1.5 bg-slate-900 border border-slate-800 p-1.5 rounded-lg", children: [_jsx("span", { className: "text-xs font-medium text-slate-400 px-2", children: "Speed:" }), speeds.map((s) => (_jsx("button", { onClick: () => handleSpeedChange(s), className: `px-2 py-1 text-xs font-mono font-medium rounded transition-all ${session.speed === s
                                    ? 'bg-cyan-600 text-white shadow-sm'
                                    : 'text-slate-400 hover:text-white hover:bg-slate-800'}`, children: s }, s)))] })] }), _jsxs("div", { className: "space-y-2", children: [_jsxs("div", { className: "flex justify-between text-xs font-mono text-slate-400", children: [_jsxs("span", { children: ["Event Cursor: ", cursor.current_index + 1, " / ", cursor.total_events] }), _jsxs("span", { children: [cursor.progress_percentage.toFixed(1), "% Replayed"] }), _jsxs("span", { children: ["Event ID: ", cursor.current_event_id || 'None'] })] }), _jsx("input", { type: "range", min: "0", max: Math.max(0, cursor.total_events - 1), value: cursor.current_index, onChange: (e) => handleSeek(parseInt(e.target.value, 10)), className: "w-full h-2.5 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-cyan-500 hover:accent-cyan-400 transition-all" }), bookmarks.length > 0 && (_jsx("div", { className: "flex gap-2 pt-1 overflow-x-auto", children: bookmarks.map((bm) => (_jsxs("button", { onClick: () => handleSeek(bm.event_index), className: "px-2 py-0.5 text-[11px] font-mono bg-indigo-950/70 border border-indigo-500/40 text-indigo-300 rounded hover:bg-indigo-900 transition-colors flex items-center gap-1.5 shrink-0", children: [_jsx("span", { children: "\uD83D\uDCCD" }), _jsx("span", { children: bm.label }), _jsxs("span", { className: "text-indigo-400", children: ["(", bm.bookmark_type, ")"] })] }, bm.bookmark_id))) }))] }), _jsxs("div", { className: "flex flex-wrap items-center justify-between gap-4 bg-slate-900/80 border border-slate-800 p-4 rounded-xl", children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("button", { onClick: () => handleSeek(0), title: "Seek to Genesis (0)", className: "p-2 text-slate-300 hover:text-white bg-slate-800 hover:bg-slate-700 rounded-lg transition-colors text-sm", children: "\u23EE Genesis" }), _jsx("button", { onClick: handleStepBackward, title: "Step 1 Event Backward", className: "p-2 text-slate-300 hover:text-white bg-slate-800 hover:bg-slate-700 rounded-lg transition-colors text-sm", children: "\u23EA Step Back" }), _jsx("button", { onClick: () => setIsPlaying(!isPlaying), className: `px-4 py-2 font-semibold text-sm rounded-lg transition-colors ${isPlaying
                                    ? 'bg-amber-600 hover:bg-amber-500 text-white'
                                    : 'bg-cyan-600 hover:bg-cyan-500 text-white'}`, children: isPlaying ? '⏸ Pause' : '▶ Play Replay' }), _jsx("button", { onClick: handleStepForward, title: "Step 1 Event Forward", className: "p-2 text-slate-300 hover:text-white bg-slate-800 hover:bg-slate-700 rounded-lg transition-colors text-sm", children: "\u23E9 Step Forward" }), _jsx("button", { onClick: () => handleSeek(cursor.total_events - 1), title: "Seek to Live Head", className: "p-2 text-slate-300 hover:text-white bg-slate-800 hover:bg-slate-700 rounded-lg transition-colors text-sm", children: "\u23ED Live Head" })] }), _jsxs("div", { className: "flex items-center gap-6 text-xs font-mono", children: [_jsxs("div", { children: [_jsx("span", { className: "text-slate-400", children: "Current Stage: " }), _jsx("span", { className: "font-semibold text-amber-400", children: state.current_stage })] }), _jsxs("div", { children: [_jsx("span", { className: "text-slate-400", children: "Confidence: " }), _jsxs("span", { className: "font-semibold text-emerald-400", children: [(state.confidence_score * 100).toFixed(1), "%"] })] }), _jsxs("div", { children: [_jsx("span", { className: "text-slate-400", children: "Cost: " }), _jsxs("span", { className: "font-semibold text-cyan-400", children: ["$", state.total_cost_usd.toFixed(4)] })] }), _jsxs("div", { children: [_jsx("span", { className: "text-slate-400", children: "DAG Ver: " }), _jsxs("span", { className: "font-semibold text-purple-400", children: ["v", state.dag_version] })] })] })] })] }));
};
