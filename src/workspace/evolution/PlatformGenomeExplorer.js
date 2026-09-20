import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { Dna, RefreshCw, Copy, Check, Code2, } from 'lucide-react';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { EvolutionPlatformApiClient } from '../../services/evolutionPlatformApiClient';
export const PlatformGenomeExplorer = () => {
    const [genome, setGenome] = useState(null);
    const [loading, setLoading] = useState(true);
    const [copied, setCopied] = useState(false);
    useEffect(() => {
        loadGenome();
    }, []);
    const loadGenome = async () => {
        setLoading(true);
        try {
            const data = await EvolutionPlatformApiClient.getPlatformGenome();
            setGenome(data);
        }
        catch (err) {
            console.error('Failed to load platform genome:', err);
        }
        finally {
            setLoading(false);
        }
    };
    const copyJson = () => {
        if (!genome)
            return;
        navigator.clipboard.writeText(JSON.stringify(genome, null, 2));
        setCopied(true);
        setTimeout(() => setCopied(false), 2000);
    };
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "bg-gradient-to-r from-slate-900 via-slate-900 to-slate-950 border border-slate-800 rounded-2xl p-6 flex flex-col md:flex-row items-start md:items-center justify-between gap-4 shadow-xl", children: [_jsxs("div", { className: "flex items-center gap-3", children: [_jsx("div", { className: "p-2.5 bg-purple-500/10 border border-purple-500/20 rounded-xl", children: _jsx(Dna, { className: "w-6 h-6 text-purple-400" }) }), _jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("h1", { className: "text-xl font-bold text-slate-100", children: "Platform Architecture Genome Explorer" }), _jsx(Badge, { variant: "intelligence", size: "sm", children: "Blueprint Specification" })] }), _jsx("p", { className: "text-sm text-slate-400 mt-0.5", children: "Inspect the comprehensive genome configuration, active hyperparameters, modular subsystems, and immutable rollback manifests." })] })] }), _jsxs("div", { className: "flex items-center gap-3", children: [_jsx(Button, { variant: "outline", onClick: loadGenome, disabled: loading, children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(RefreshCw, { className: `w-4 h-4 ${loading ? 'animate-spin' : ''}` }), "Refresh"] }) }), _jsx(Button, { variant: "outline", onClick: copyJson, children: _jsxs("span", { className: "flex items-center gap-2", children: [copied ? _jsx(Check, { className: "w-4 h-4 text-emerald-400" }) : _jsx(Copy, { className: "w-4 h-4" }), copied ? 'Copied Genome' : 'Export Genome JSON'] }) })] })] }), _jsxs("div", { className: "grid grid-cols-1 lg:grid-cols-3 gap-6", children: [_jsxs("div", { className: "bg-slate-900/80 border border-slate-800 rounded-xl p-6 space-y-4", children: [_jsx("h2", { className: "text-base font-semibold text-slate-100", children: "Genome Manifest" }), _jsxs("div", { className: "space-y-3 text-xs font-mono text-slate-300", children: [_jsxs("div", { className: "p-3 bg-slate-950/80 border border-slate-800 rounded-lg space-y-1", children: [_jsx("div", { className: "text-slate-500 text-[10px]", children: "GENOME ID" }), _jsx("div", { className: "text-purple-300 font-bold", children: genome?.genome_id ?? 'genome_v13_13_prime' })] }), _jsxs("div", { className: "p-3 bg-slate-950/80 border border-slate-800 rounded-lg space-y-1", children: [_jsx("div", { className: "text-slate-500 text-[10px]", children: "ACTIVE PLATFORM VERSION" }), _jsx("div", { className: "text-emerald-300 font-bold", children: genome?.version ?? 'v13.13.0' })] }), _jsxs("div", { className: "p-3 bg-slate-950/80 border border-slate-800 rounded-lg space-y-1", children: [_jsx("div", { className: "text-slate-500 text-[10px]", children: "TIMESTAMP" }), _jsx("div", { className: "text-slate-300", children: genome?.timestamp ?? new Date().toISOString() })] })] })] }), _jsxs("div", { className: "lg:col-span-2 bg-slate-900/80 border border-slate-800 rounded-xl p-6 space-y-4", children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx(Code2, { className: "w-5 h-5 text-indigo-400" }), _jsx("h2", { className: "text-base font-semibold text-slate-100", children: "Genome JSON Inspector" })] }), _jsx("pre", { className: "bg-slate-950 border border-slate-800 rounded-xl p-4 text-xs font-mono text-slate-300 overflow-x-auto max-h-[460px] leading-relaxed", children: genome ? JSON.stringify(genome, null, 2) : 'Loading Platform Genome...' })] })] })] }));
};
