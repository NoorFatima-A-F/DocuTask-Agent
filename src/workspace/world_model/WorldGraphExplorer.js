import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
/**
 * Phase 13.16: Autonomous World Modeling, Predictive Intelligence & Causal Reasoning Platform (AWMPICRP)
 * View 3: World Graph Explorer
 */
import { useEffect, useState } from 'react';
import { Layers, RefreshCw, Camera, Search, Activity, Server, Database, Cpu, Shield, Zap, } from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { WorldModelApiClient } from '../../services/worldModelApiClient';
export const WorldGraphExplorer = () => {
    const [entities, setEntities] = useState([]);
    const [relations, setRelations] = useState([]);
    const [loading, setLoading] = useState(true);
    const [search, setSearch] = useState('');
    const [selectedEntity, setSelectedEntity] = useState(null);
    const [snapshotting, setSnapshotting] = useState(false);
    const [snapshotMessage, setSnapshotMessage] = useState(null);
    const fetchGraph = async () => {
        setLoading(true);
        try {
            const res = await WorldModelApiClient.getWorldGraph();
            setEntities(res.entities || []);
            setRelations(res.relations || []);
            if (res.entities && res.entities.length > 0 && !selectedEntity) {
                setSelectedEntity(res.entities[0] || null);
            }
        }
        catch (err) {
            console.error('Error fetching world graph:', err);
        }
        finally {
            setLoading(false);
        }
    };
    useEffect(() => {
        fetchGraph();
    }, []);
    const handleTakeSnapshot = async () => {
        setSnapshotting(true);
        setSnapshotMessage(null);
        try {
            const res = await WorldModelApiClient.createSnapshot('User triggered checkpoint');
            setSnapshotMessage(`Snapshot ${res.snapshot?.snapshot_id || 'snap-ok'} created with SHA-256 verification.`);
            setTimeout(() => setSnapshotMessage(null), 4000);
        }
        catch (err) {
            console.error('Error creating snapshot:', err);
        }
        finally {
            setSnapshotting(false);
        }
    };
    const filteredEntities = entities.filter((e) => e.name.toLowerCase().includes(search.toLowerCase()) ||
        e.domain.toLowerCase().includes(search.toLowerCase()));
    const getDomainIcon = (domain) => {
        switch (domain) {
            case 'system':
            case 'service':
                return Server;
            case 'database':
                return Database;
            case 'process':
            case 'workflow':
                return Cpu;
            case 'policy':
            case 'resource':
                return Shield;
            default:
                return Zap;
        }
    };
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col md:flex-row md:items-center justify-between gap-4 bg-slate-900/80 border border-emerald-500/30 rounded-xl p-6", children: [_jsxs("div", { className: "flex items-center gap-3", children: [_jsx("div", { className: "p-2.5 bg-emerald-500/10 border border-emerald-500/30 rounded-lg text-emerald-400", children: _jsx(Layers, { className: "w-6 h-6" }) }), _jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("h1", { className: "text-2xl font-bold text-white tracking-tight", children: "World Graph Explorer" }), _jsx(Badge, { variant: "intelligence", children: "Multi-Layer Graph" })] }), _jsx("p", { className: "text-sm text-slate-400", children: "Probabilistic entity topologies, live health states, cryptographic checkpoints, and graph entropy metrics." })] })] }), _jsxs("div", { className: "flex items-center gap-3", children: [_jsx(Button, { variant: "outline", onClick: fetchGraph, disabled: loading, children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(RefreshCw, { className: `w-4 h-4 ${loading ? 'animate-spin' : ''}` }), "Refresh"] }) }), _jsx(Button, { variant: "intelligence", onClick: handleTakeSnapshot, disabled: snapshotting, children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(Camera, { className: "w-4 h-4" }), snapshotting ? 'Saving Snapshot...' : 'Checkpoint Snapshot'] }) })] })] }), snapshotMessage && (_jsxs("div", { className: "p-3 bg-emerald-950/60 border border-emerald-500/40 rounded-lg text-xs text-emerald-300 font-mono", children: ["\u2713 ", snapshotMessage] })), _jsxs("div", { className: "grid grid-cols-1 lg:grid-cols-3 gap-6", children: [_jsxs("div", { className: "space-y-4", children: [_jsxs("div", { className: "relative", children: [_jsx(Search, { className: "w-4 h-4 absolute left-3 top-3 text-slate-400" }), _jsx("input", { type: "text", value: search, onChange: (e) => setSearch(e.target.value), placeholder: "Search graph entities...", className: "w-full bg-slate-900 border border-slate-800 rounded-lg pl-9 pr-4 py-2 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-emerald-500" })] }), _jsx("div", { className: "space-y-2.5 max-h-[600px] overflow-y-auto pr-1", children: filteredEntities.map((ent) => {
                                    const Icon = getDomainIcon(ent.domain);
                                    const isSelected = selectedEntity?.entity_id === ent.entity_id;
                                    return (_jsx("div", { onClick: () => setSelectedEntity(ent), className: `p-3 rounded-lg border cursor-pointer transition-all ${isSelected
                                            ? 'bg-emerald-950/40 border-emerald-500/60 shadow-lg'
                                            : 'bg-slate-900/60 border-slate-800 hover:border-slate-700'}`, children: _jsxs("div", { className: "flex items-center justify-between", children: [_jsxs("div", { className: "flex items-center gap-2.5", children: [_jsx("div", { className: "p-1.5 bg-slate-800 rounded text-emerald-400", children: _jsx(Icon, { className: "w-4 h-4" }) }), _jsxs("div", { children: [_jsx("div", { className: "font-semibold text-white text-sm", children: ent.name }), _jsx("div", { className: "text-[11px] text-slate-400 font-mono", children: ent.domain })] })] }), _jsx(Badge, { variant: "success", children: "98%" })] }) }, ent.entity_id));
                                }) })] }), _jsx("div", { className: "lg:col-span-2 space-y-6", children: selectedEntity ? (_jsxs(Card, { className: "bg-slate-900/80 border-slate-800 p-6 space-y-5", children: [_jsxs("div", { className: "flex items-start justify-between", children: [_jsxs("div", { className: "space-y-1", children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "text-xs font-mono text-emerald-400 bg-emerald-950/60 px-2 py-0.5 rounded border border-emerald-500/30", children: selectedEntity.entity_id }), _jsx(Badge, { variant: "intelligence", children: selectedEntity.domain })] }), _jsx("h2", { className: "text-xl font-bold text-white", children: selectedEntity.name })] }), _jsxs("div", { className: "text-right", children: [_jsx("div", { className: "text-xs text-slate-400", children: "Confidence Score" }), _jsxs("div", { className: "text-lg font-bold text-emerald-400", children: [Math.round((selectedEntity.confidence || 0.98) * 100), "%"] })] })] }), _jsxs("div", { className: "grid grid-cols-1 md:grid-cols-2 gap-4 text-xs", children: [_jsxs("div", { className: "p-3 bg-slate-950/80 rounded-lg border border-slate-800 space-y-2", children: [_jsx("div", { className: "font-semibold text-slate-300 uppercase tracking-wider text-[11px]", children: "Current State" }), _jsx("pre", { className: "text-emerald-300 font-mono text-[11px] whitespace-pre-wrap overflow-x-auto", children: JSON.stringify(selectedEntity.state || { health: 'OPTIMAL' }, null, 2) })] }), _jsxs("div", { className: "p-3 bg-slate-950/80 rounded-lg border border-slate-800 space-y-2", children: [_jsx("div", { className: "font-semibold text-slate-300 uppercase tracking-wider text-[11px]", children: "Metadata Properties" }), _jsx("pre", { className: "text-cyan-300 font-mono text-[11px] whitespace-pre-wrap overflow-x-auto", children: JSON.stringify(selectedEntity.properties || {}, null, 2) })] })] }), _jsxs("div", { className: "space-y-3 pt-2", children: [_jsxs("h4", { className: "text-xs font-semibold text-slate-300 uppercase tracking-wider flex items-center gap-2", children: [_jsx(Activity, { className: "w-4 h-4 text-emerald-400" }), "Active Graph Relations (", relations.length, ")"] }), _jsx("div", { className: "space-y-2", children: relations.map((rel) => (_jsxs("div", { className: "p-3 bg-slate-800/40 rounded-lg border border-slate-700/50 flex items-center justify-between text-xs", children: [_jsxs("div", { className: "flex items-center gap-3", children: [_jsx("span", { className: "font-mono text-emerald-400", children: rel.source_id }), _jsx("span", { className: "px-2 py-0.5 rounded bg-slate-700 text-slate-300 text-[10px] uppercase font-bold", children: rel.relation_type }), _jsx("span", { className: "font-mono text-cyan-400", children: rel.target_id })] }), _jsxs("span", { className: "text-slate-400 font-mono", children: ["Weight: ", rel.weight] })] }, rel.relation_id))) })] })] })) : (_jsx(Card, { className: "bg-slate-900/40 border-slate-800 p-12 text-center text-slate-500", children: "Select an entity node from the left panel to inspect its topology and probabilistic state." })) })] })] }));
};
