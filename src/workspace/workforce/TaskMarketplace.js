import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { workforceApiClient } from '../../services/workforceApiClient';
import { ShoppingCart, DollarSign, Clock, Gavel, Plus } from 'lucide-react';
export const TaskMarketplace = () => {
    const [tasks, setTasks] = useState([]);
    const [title, setTitle] = useState('');
    const [desc, setDesc] = useState('');
    const [budget, setBudget] = useState('30');
    useEffect(() => {
        workforceApiClient.getMarketplaceTasks().then(setTasks);
    }, []);
    const handlePost = async () => {
        if (!title || !desc)
            return;
        const newTask = await workforceApiClient.postTask({
            title,
            description: desc,
            required_skills: ['Document Extraction'],
            budget_max_usd: parseFloat(budget) || 30.0
        });
        setTasks([...tasks, newTask]);
        setTitle('');
        setDesc('');
    };
    const handleAssign = async (taskId) => {
        const updated = await workforceApiClient.submitBid({
            task_id: taskId,
            employee_id: 'emp-doc-spec-01',
            bid_cost_usd: 12.0,
            estimated_duration_minutes: 10.0,
            solution_outline: 'Automated Stream Sharding'
        });
        setTasks(tasks.map(t => t.id === taskId ? updated : t));
    };
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "bg-slate-900/60 p-5 rounded-2xl border border-slate-800", children: [_jsxs("h1", { className: "text-2xl font-bold text-white flex items-center gap-3", children: [_jsx("span", { className: "p-2 bg-amber-500/20 text-amber-400 rounded-xl", children: "\uD83D\uDED2" }), "Task Marketplace & Internal Economy"] }), _jsx("p", { className: "text-slate-400 text-sm mt-1", children: "Autonomous Agent Job Bidding, Auction Mechanisms, and Value Optimization" })] }), _jsxs("div", { className: "grid grid-cols-1 lg:grid-cols-3 gap-6", children: [_jsxs(Card, { className: "p-5 bg-slate-900/50 border-slate-800 lg:col-span-1", children: [_jsxs("h3", { className: "text-base font-bold text-white mb-4 flex items-center gap-2", children: [_jsx(Plus, { className: "w-4 h-4 text-emerald-400" }), " Post Work Request"] }), _jsxs("div", { className: "space-y-3", children: [_jsxs("div", { children: [_jsx("label", { className: "text-xs text-slate-400 block mb-1", children: "Task Title" }), _jsx("input", { placeholder: "e.g. Audit Ledger Line Items", value: title, onChange: (e) => setTitle(e.target.value), className: "bg-slate-950 border border-slate-800 text-slate-200 rounded-xl px-3 py-2 text-sm w-full" })] }), _jsxs("div", { children: [_jsx("label", { className: "text-xs text-slate-400 block mb-1", children: "Task Description" }), _jsx("input", { placeholder: "Details on required accuracy and inputs", value: desc, onChange: (e) => setDesc(e.target.value), className: "bg-slate-950 border border-slate-800 text-slate-200 rounded-xl px-3 py-2 text-sm w-full" })] }), _jsxs("div", { children: [_jsx("label", { className: "text-xs text-slate-400 block mb-1", children: "Max Budget (USD)" }), _jsx("input", { placeholder: "30", value: budget, onChange: (e) => setBudget(e.target.value), className: "bg-slate-950 border border-slate-800 text-slate-200 rounded-xl px-3 py-2 text-sm w-full" })] }), _jsx(Button, { className: "w-full mt-2", onClick: handlePost, children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(ShoppingCart, { className: "w-4 h-4" }), " Publish to Marketplace"] }) })] })] }), _jsxs("div", { className: "lg:col-span-2 space-y-4", children: [_jsxs("h3", { className: "text-base font-bold text-white flex items-center gap-2", children: [_jsx(Gavel, { className: "w-4 h-4 text-indigo-400" }), " Active Bidding Auctions"] }), _jsx("div", { className: "space-y-4", children: tasks.map((t) => (_jsxs(Card, { className: "p-5 bg-slate-900/50 border-slate-800", children: [_jsxs("div", { className: "flex justify-between items-start mb-2", children: [_jsxs("div", { children: [_jsx("div", { className: "text-base font-bold text-white", children: t.title }), _jsx("div", { className: "text-xs text-slate-400 mt-0.5", children: t.description })] }), _jsx(Badge, { variant: t.status === 'OPEN' ? 'default' : 'outline', children: t.status })] }), _jsxs("div", { className: "flex gap-4 my-3 text-xs text-slate-400", children: [_jsxs("span", { className: "flex items-center gap-1", children: [_jsx(DollarSign, { className: "w-3.5 h-3.5 text-emerald-400" }), " Max Budget: $", t.budget_max_usd] }), _jsxs("span", { className: "flex items-center gap-1", children: [_jsx(Clock, { className: "w-3.5 h-3.5 text-blue-400" }), " Priority: ", t.priority] }), _jsxs("span", { children: ["Bids: ", _jsx("strong", { children: t.bids.length })] })] }), t.bids.length > 0 && (_jsxs("div", { className: "my-3 space-y-2", children: [_jsx("div", { className: "text-[11px] font-semibold text-slate-400 uppercase", children: "Current Leading Bids" }), t.bids.map((b) => (_jsxs("div", { className: "p-2.5 bg-slate-950/60 rounded-lg border border-slate-800 flex justify-between items-center text-xs", children: [_jsxs("div", { children: [_jsx("strong", { className: "text-indigo-400", children: b.employee_id }), ": $", b.bid_cost_usd, " in ", b.estimated_duration_minutes, "m", _jsx("div", { className: "text-[10px] text-slate-500", children: b.proposed_solution_outline })] }), _jsxs(Badge, { variant: "outline", children: [Math.round(b.confidence_score * 100), "% Conf"] })] }, b.bid_id)))] })), _jsx("div", { className: "pt-2 flex justify-end", children: _jsx(Button, { size: "sm", variant: "outline", onClick: () => handleAssign(t.id), children: _jsxs("span", { className: "flex items-center gap-1", children: [_jsx(Gavel, { className: "w-3.5 h-3.5" }), " Submit Agent Bid"] }) }) })] }, t.id))) })] })] })] }));
};
