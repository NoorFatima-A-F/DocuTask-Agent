import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Cloud, Terminal, RefreshCw, Play, FileCode, } from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
export const DeploymentCenter = () => {
    const [selectedTarget, setSelectedTarget] = useState('CLOUDRUN');
    const [deploying, setDeploying] = useState(false);
    const [deployLog, setDeployLog] = useState([]);
    const handleDeploy = () => {
        setDeploying(true);
        const startMsg = `[${new Date().toLocaleTimeString()}] Building container image for ${selectedTarget}...`;
        setDeployLog([startMsg]);
        setTimeout(() => {
            setDeployLog((prev) => [
                `[${new Date().toLocaleTimeString()}] Pushing image to gcr.io/docutask-agent/runtime:v1.18.0`,
                ...prev,
            ]);
        }, 1000);
        setTimeout(() => {
            setDeployLog((prev) => [
                `[${new Date().toLocaleTimeString()}] Deploying service revision to ${selectedTarget}...`,
                ...prev,
            ]);
        }, 2000);
        setTimeout(() => {
            setDeployLog((prev) => [
                `[${new Date().toLocaleTimeString()}] Deployment successful! 5 worker replicas online. Health check: 200 OK.`,
                ...prev,
            ]);
            setDeploying(false);
        }, 3000);
    };
    const sampleDockerfile = `# Phase 13.18 Cloud-Native Autonomous Agent Runtime
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ app/
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]`;
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col md:flex-row md:items-center justify-between gap-4 bg-slate-900/60 p-6 rounded-2xl border border-slate-800 backdrop-blur-md", children: [_jsxs("div", { className: "flex items-center gap-3", children: [_jsx("div", { className: "p-2 bg-indigo-500/10 rounded-xl border border-indigo-500/20 text-indigo-400", children: _jsx(Cloud, { className: "w-6 h-6" }) }), _jsxs("div", { children: [_jsx("h1", { className: "text-2xl font-bold text-white", children: "Cloud Deployment Center" }), _jsx("p", { className: "text-sm text-slate-400", children: "Provider-agnostic multi-cloud packaging: Cloud Run, Kubernetes (GKE), ECS & ACA" })] })] }), _jsx("div", { className: "flex items-center gap-3", children: _jsx(Button, { variant: "intelligence", onClick: handleDeploy, disabled: deploying, children: _jsxs("span", { className: "flex items-center gap-2", children: [deploying ? _jsx(RefreshCw, { className: "w-4 h-4 animate-spin" }) : _jsx(Play, { className: "w-4 h-4" }), "Deploy Revision"] }) }) })] }), _jsx("div", { className: "grid grid-cols-2 md:grid-cols-4 gap-4", children: [
                    { id: 'CLOUDRUN', label: 'Google Cloud Run', desc: 'Serverless Auto-scaling' },
                    { id: 'GKE', label: 'Google GKE', desc: 'Kubernetes Cluster Mesh' },
                    { id: 'AWS_ECS', label: 'AWS ECS Fargate', desc: 'Elastic Container Service' },
                    { id: 'AZURE_ACA', label: 'Azure Container Apps', desc: 'Microservice Fabric' },
                ].map((t) => (_jsxs(Card, { onClick: () => setSelectedTarget(t.id), className: `p-4 cursor-pointer border transition-all ${selectedTarget === t.id
                        ? 'bg-slate-800/80 border-indigo-500 shadow-md'
                        : 'bg-slate-900/40 border-slate-800 hover:border-slate-700'}`, children: [_jsx("span", { className: "font-bold text-white text-sm block", children: t.label }), _jsx("span", { className: "text-xs text-slate-400 block mt-1", children: t.desc })] }, t.id))) }), _jsxs("div", { className: "grid grid-cols-1 lg:grid-cols-2 gap-6", children: [_jsxs(Card, { className: "p-6 bg-slate-900/40 border-slate-800 space-y-3", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsxs("h3", { className: "text-sm font-semibold text-white flex items-center gap-2", children: [_jsx(FileCode, { className: "w-4 h-4 text-indigo-400" }), "Dockerfile Manifest"] }), _jsx(Badge, { variant: "outline", children: "Multi-Stage Ready" })] }), _jsx("pre", { className: "p-4 bg-slate-950/80 rounded-xl border border-slate-800 font-mono text-xs text-indigo-300 overflow-x-auto", children: sampleDockerfile })] }), _jsxs(Card, { className: "p-6 bg-slate-900/40 border-slate-800 space-y-3", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsxs("h3", { className: "text-sm font-semibold text-white flex items-center gap-2", children: [_jsx(Terminal, { className: "w-4 h-4 text-emerald-400" }), "Deployment Pipeline Log"] }), _jsx(Badge, { variant: deploying ? 'warning' : 'success', children: deploying ? 'Deploying...' : 'Idle' })] }), _jsx("div", { className: "p-4 bg-slate-950/80 rounded-xl border border-slate-800 font-mono text-xs text-slate-300 space-y-2 min-h-48 max-h-72 overflow-y-auto", children: deployLog.length > 0 ? (deployLog.map((log, idx) => (_jsx("div", { className: "border-b border-slate-800/60 pb-1 text-emerald-300 last:border-0", children: log }, idx)))) : (_jsx("p", { className: "text-slate-500 italic", children: "Click \"Deploy Revision\" to trigger cloud deployment." })) })] })] })] }));
};
