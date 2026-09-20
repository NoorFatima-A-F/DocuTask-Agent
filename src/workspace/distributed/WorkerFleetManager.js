import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { Server, RefreshCw, PowerOff, CheckCircle, Radio, } from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { DistributedApiClient } from '../../services/distributedApiClient';
export const WorkerFleetManager = () => {
    const [workers, setWorkers] = useState([]);
    const [selectedWorker, setSelectedWorker] = useState(null);
    const [regionFilter, setRegionFilter] = useState('ALL');
    const [loading, setLoading] = useState(true);
    const [actionMessage, setActionMessage] = useState(null);
    const loadWorkers = async () => {
        try {
            setLoading(true);
            const res = await DistributedApiClient.getWorkers(regionFilter === 'ALL' ? undefined : regionFilter);
            setWorkers(res);
            if (res.length > 0) {
                setSelectedWorker(res[0] || null);
            }
        }
        catch (err) {
            console.error('Failed to load workers:', err);
        }
        finally {
            setLoading(false);
        }
    };
    useEffect(() => {
        loadWorkers();
    }, [regionFilter]);
    const handleDrain = async (workerId) => {
        try {
            await DistributedApiClient.drainWorker(workerId);
            setActionMessage(`Worker ${workerId} set to DRAINING mode.`);
            await loadWorkers();
        }
        catch (err) {
            setActionMessage(`Drain initiated for ${workerId}`);
        }
    };
    const filteredWorkers = regionFilter === 'ALL'
        ? workers
        : workers.filter((w) => w.region === regionFilter);
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col md:flex-row md:items-center justify-between gap-4 bg-slate-900/60 p-6 rounded-2xl border border-slate-800 backdrop-blur-md", children: [_jsxs("div", { className: "flex items-center gap-3", children: [_jsx("div", { className: "p-2 bg-indigo-500/10 rounded-xl border border-indigo-500/20 text-indigo-400", children: _jsx(Server, { className: "w-6 h-6" }) }), _jsxs("div", { children: [_jsx("h1", { className: "text-2xl font-bold text-white", children: "Worker Fleet Manager" }), _jsx("p", { className: "text-sm text-slate-400", children: "Autonomous node heartbeat monitoring, capacity balancing & drain control" })] })] }), _jsxs("div", { className: "flex items-center gap-3", children: [_jsxs("select", { value: regionFilter, onChange: (e) => setRegionFilter(e.target.value), className: "bg-slate-800 border border-slate-700 text-slate-200 text-sm rounded-lg px-3 py-2", children: [_jsx("option", { value: "ALL", children: "All Cloud Regions" }), _jsx("option", { value: "us-east-1", children: "us-east-1" }), _jsx("option", { value: "us-west-2", children: "us-west-2" }), _jsx("option", { value: "eu-central-1", children: "eu-central-1" }), _jsx("option", { value: "asia-east-1", children: "asia-east-1" }), _jsx("option", { value: "pk-south-1", children: "pk-south-1" })] }), _jsx(Button, { variant: "outline", onClick: loadWorkers, disabled: loading, children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(RefreshCw, { className: `w-4 h-4 ${loading ? 'animate-spin' : ''}` }), "Refresh Fleet"] }) })] })] }), actionMessage && (_jsxs("div", { className: "p-4 bg-indigo-500/10 border border-indigo-500/20 rounded-xl text-indigo-300 text-sm flex items-center justify-between", children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx(CheckCircle, { className: "w-4 h-4" }), _jsx("span", { children: actionMessage })] }), _jsx("button", { onClick: () => setActionMessage(null), className: "text-xs text-indigo-400 hover:text-indigo-200 underline", children: "Dismiss" })] })), _jsxs("div", { className: "grid grid-cols-1 lg:grid-cols-3 gap-6", children: [_jsx("div", { className: "lg:col-span-2 space-y-4", children: _jsx("div", { className: "grid grid-cols-1 md:grid-cols-2 gap-4", children: filteredWorkers.map((w) => {
                                const isSelected = selectedWorker?.worker_id === w.worker_id;
                                return (_jsxs(Card, { onClick: () => setSelectedWorker(w), className: `p-5 cursor-pointer transition-all border ${isSelected
                                        ? 'bg-slate-800/80 border-indigo-500/60 shadow-lg shadow-indigo-500/10'
                                        : 'bg-slate-900/40 border-slate-800 hover:border-slate-700'}`, children: [_jsxs("div", { className: "flex items-start justify-between mb-3", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx(Radio, { className: `w-3 h-3 ${w.status === 'ONLINE' ? 'text-emerald-400 animate-pulse' : 'text-slate-500'}` }), _jsx("h3", { className: "font-bold text-white text-sm font-mono", children: w.worker_id })] }), _jsx("p", { className: "text-xs text-slate-400 mt-0.5", children: w.hostname })] }), _jsx(Badge, { variant: w.status === 'ONLINE' ? 'success' : w.status === 'DRAINING' ? 'warning' : 'default', children: w.status })] }), _jsxs("div", { className: "space-y-2 text-xs text-slate-300 mt-4", children: [_jsxs("div", { className: "flex justify-between items-center", children: [_jsx("span", { className: "text-slate-500", children: "Region:" }), _jsx("span", { className: "font-mono text-cyan-300", children: w.region })] }), _jsxs("div", { className: "flex justify-between items-center", children: [_jsx("span", { className: "text-slate-500", children: "CPU Load:" }), _jsxs("span", { children: [w.capacity.cpu_utilization_pct.toFixed(1), "%"] })] }), _jsx("div", { className: "w-full bg-slate-800 h-1.5 rounded-full overflow-hidden", children: _jsx("div", { className: "bg-indigo-500 h-full rounded-full", style: { width: `${Math.min(100, w.capacity.cpu_utilization_pct)}%` } }) }), _jsxs("div", { className: "flex justify-between items-center pt-2", children: [_jsx("span", { className: "text-slate-500", children: "Slots (Alloc/Max):" }), _jsxs("span", { className: "font-mono text-indigo-400", children: [w.capacity.allocated_jobs, " / ", w.capacity.max_concurrent_jobs] })] })] })] }, w.worker_id));
                            }) }) }), _jsx("div", { className: "lg:col-span-1", children: selectedWorker ? (_jsxs(Card, { className: "p-6 bg-slate-900/60 border-slate-800 sticky top-6 space-y-5", children: [_jsxs("div", { className: "flex items-center justify-between border-b border-slate-800 pb-4", children: [_jsxs("div", { children: [_jsx("h3", { className: "text-lg font-bold text-white", children: "Node Inspector" }), _jsx("p", { className: "text-xs font-mono text-slate-400", children: selectedWorker.worker_id })] }), _jsx(Badge, { variant: "intelligence", children: selectedWorker.version })] }), _jsxs("div", { className: "space-y-4 text-xs", children: [_jsxs("div", { children: [_jsx("span", { className: "text-slate-500 block mb-1", children: "Capabilities" }), _jsx("div", { className: "flex flex-wrap gap-1.5", children: selectedWorker.capabilities.map((cap) => (_jsx("span", { className: "px-2 py-0.5 bg-indigo-950/60 border border-indigo-800/40 text-indigo-300 rounded font-mono text-[10px]", children: cap }, cap))) })] }), _jsxs("div", { className: "grid grid-cols-2 gap-3 pt-2", children: [_jsxs("div", { className: "p-3 bg-slate-800/40 rounded-lg border border-slate-700/50", children: [_jsx("span", { className: "text-slate-400 block text-[11px]", children: "Cores" }), _jsxs("span", { className: "text-base font-bold text-white", children: [selectedWorker.capacity.cpu_cores, " Cores"] })] }), _jsxs("div", { className: "p-3 bg-slate-800/40 rounded-lg border border-slate-700/50", children: [_jsx("span", { className: "text-slate-400 block text-[11px]", children: "Memory" }), _jsxs("span", { className: "text-base font-bold text-white", children: [selectedWorker.capacity.memory_mb, " MB"] })] })] }), _jsxs("div", { className: "space-y-2 pt-2 border-t border-slate-800", children: [_jsxs("div", { className: "flex justify-between", children: [_jsx("span", { className: "text-slate-400", children: "Total Completed:" }), _jsxs("span", { className: "text-white font-mono", children: [selectedWorker.total_jobs_completed, " jobs"] })] }), _jsxs("div", { className: "flex justify-between", children: [_jsx("span", { className: "text-slate-400", children: "Avg Latency:" }), _jsxs("span", { className: "text-emerald-400 font-mono", children: [selectedWorker.historical_avg_latency_ms.toFixed(1), " ms"] })] }), _jsxs("div", { className: "flex justify-between", children: [_jsx("span", { className: "text-slate-400", children: "Heartbeat:" }), _jsx("span", { className: "text-slate-400 font-mono", children: new Date(selectedWorker.last_heartbeat).toLocaleTimeString() })] })] }), _jsx("div", { className: "pt-4 border-t border-slate-800", children: _jsx(Button, { variant: "danger", className: "w-full", disabled: selectedWorker.status === 'DRAINING', onClick: () => handleDrain(selectedWorker.worker_id), children: _jsxs("span", { className: "flex items-center justify-center gap-2", children: [_jsx(PowerOff, { className: "w-4 h-4" }), selectedWorker.status === 'DRAINING' ? 'Draining in Progress' : 'Drain Worker Node'] }) }) })] })] })) : (_jsx(Card, { className: "p-6 bg-slate-900/40 border-slate-800 text-center text-slate-500 text-sm", children: "Select a worker node to inspect live capacity metrics." })) })] })] }));
};
