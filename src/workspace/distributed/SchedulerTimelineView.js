import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { Calendar, RefreshCw, Plus, Play, User, } from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { DistributedApiClient } from '../../services/distributedApiClient';
export const SchedulerTimelineView = () => {
    const [jobs, setJobs] = useState([]);
    const [loading, setLoading] = useState(true);
    const [showSubmitModal, setShowSubmitModal] = useState(false);
    const [taskName, setTaskName] = useState('Extract Invoices from Storage Bucket');
    const [priority, setPriority] = useState('HIGH');
    const [submitting, setSubmitting] = useState(false);
    const loadJobs = async () => {
        try {
            setLoading(true);
            const res = await DistributedApiClient.listJobs(50);
            setJobs(res);
        }
        catch (err) {
            console.error('Failed to load scheduled jobs:', err);
        }
        finally {
            setLoading(false);
        }
    };
    useEffect(() => {
        loadJobs();
    }, []);
    const handleSubmitJob = async (e) => {
        e.preventDefault();
        try {
            setSubmitting(true);
            await DistributedApiClient.submitJob({
                workflow_id: `wf_manual_${Date.now().toString().slice(-4)}`,
                agent_id: 'agent_doc_extractor',
                task_name: taskName,
                priority,
            });
            setShowSubmitModal(false);
            await loadJobs();
        }
        catch (err) {
            console.error('Failed to submit job:', err);
        }
        finally {
            setSubmitting(false);
        }
    };
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col md:flex-row md:items-center justify-between gap-4 bg-slate-900/60 p-6 rounded-2xl border border-slate-800 backdrop-blur-md", children: [_jsxs("div", { className: "flex items-center gap-3", children: [_jsx("div", { className: "p-2 bg-indigo-500/10 rounded-xl border border-indigo-500/20 text-indigo-400", children: _jsx(Calendar, { className: "w-6 h-6" }) }), _jsxs("div", { children: [_jsx("h1", { className: "text-2xl font-bold text-white", children: "Scheduler Timeline View" }), _jsx("p", { className: "text-sm text-slate-400", children: "Real-time multi-tenant fair-share scheduling with SLA deadline monitoring" })] })] }), _jsxs("div", { className: "flex items-center gap-3", children: [_jsx(Button, { variant: "outline", onClick: loadJobs, disabled: loading, children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(RefreshCw, { className: `w-4 h-4 ${loading ? 'animate-spin' : ''}` }), "Refresh"] }) }), _jsx(Button, { variant: "intelligence", onClick: () => setShowSubmitModal(true), children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(Plus, { className: "w-4 h-4" }), "Submit Scheduled Job"] }) })] })] }), _jsx(Card, { className: "p-6 bg-slate-900/40 border-slate-800", children: _jsx("div", { className: "overflow-x-auto", children: _jsxs("table", { className: "w-full text-left text-sm text-slate-300", children: [_jsx("thead", { className: "bg-slate-800/60 text-xs uppercase text-slate-400 border-b border-slate-700", children: _jsxs("tr", { children: [_jsx("th", { className: "py-3 px-4", children: "Job ID" }), _jsx("th", { className: "py-3 px-4", children: "Task Name" }), _jsx("th", { className: "py-3 px-4", children: "Agent" }), _jsx("th", { className: "py-3 px-4", children: "Priority" }), _jsx("th", { className: "py-3 px-4", children: "State" }), _jsx("th", { className: "py-3 px-4", children: "Assigned Worker" }), _jsx("th", { className: "py-3 px-4", children: "SLA Deadline" })] }) }), _jsx("tbody", { className: "divide-y divide-slate-800/60 text-xs font-mono", children: jobs.map((job) => (_jsxs("tr", { className: "hover:bg-slate-800/30 transition-colors", children: [_jsx("td", { className: "py-3 px-4 font-semibold text-white", children: job.job_id }), _jsx("td", { className: "py-3 px-4 text-slate-200 font-sans", children: job.task_name }), _jsxs("td", { className: "py-3 px-4 text-indigo-400 font-sans flex items-center gap-1.5", children: [_jsx(User, { className: "w-3.5 h-3.5" }), job.agent_id] }), _jsx("td", { className: "py-3 px-4", children: _jsx(Badge, { variant: job.priority === 'CRITICAL'
                                                    ? 'error'
                                                    : job.priority === 'HIGH'
                                                        ? 'warning'
                                                        : 'default', children: job.priority }) }), _jsx("td", { className: "py-3 px-4", children: _jsx(Badge, { variant: job.state === 'RUNNING'
                                                    ? 'intelligence'
                                                    : job.state === 'COMPLETED'
                                                        ? 'success'
                                                        : 'outline', children: job.state }) }), _jsx("td", { className: "py-3 px-4 text-cyan-300", children: job.assigned_worker_id || 'unassigned (queued)' }), _jsxs("td", { className: "py-3 px-4 text-amber-400", children: [job.sla_deadline_ms, " ms"] })] }, job.job_id))) })] }) }) }), showSubmitModal && (_jsx("div", { className: "fixed inset-0 z-50 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4", children: _jsxs(Card, { className: "max-w-md w-full p-6 bg-slate-900 border-slate-700 space-y-4", children: [_jsx("h3", { className: "text-lg font-bold text-white", children: "Submit New Job to Distributed Fabric" }), _jsxs("form", { onSubmit: handleSubmitJob, className: "space-y-4 text-sm", children: [_jsxs("div", { children: [_jsx("label", { className: "block text-slate-400 text-xs mb-1", children: "Task Name" }), _jsx("input", { type: "text", value: taskName, onChange: (e) => setTaskName(e.target.value), className: "w-full bg-slate-800 border border-slate-700 text-white rounded-lg p-2.5 text-xs", required: true })] }), _jsxs("div", { children: [_jsx("label", { className: "block text-slate-400 text-xs mb-1", children: "Priority Tier" }), _jsxs("select", { value: priority, onChange: (e) => setPriority(e.target.value), className: "w-full bg-slate-800 border border-slate-700 text-white rounded-lg p-2.5 text-xs", children: [_jsx("option", { value: "CRITICAL", children: "CRITICAL (P0 - SLA under 2s)" }), _jsx("option", { value: "HIGH", children: "HIGH (P1 - SLA under 5s)" }), _jsx("option", { value: "NORMAL", children: "NORMAL (P2 - Standard)" }), _jsx("option", { value: "BATCH", children: "BATCH (P3 - Offpeak)" })] })] }), _jsxs("div", { className: "flex justify-end gap-3 pt-3", children: [_jsx(Button, { variant: "ghost", onClick: () => setShowSubmitModal(false), type: "button", children: "Cancel" }), _jsx(Button, { variant: "intelligence", type: "submit", disabled: submitting, children: _jsxs("span", { className: "flex items-center gap-2", children: [submitting ? _jsx(RefreshCw, { className: "w-4 h-4 animate-spin" }) : _jsx(Play, { className: "w-4 h-4" }), "Submit Job"] }) })] })] })] }) }))] }));
};
