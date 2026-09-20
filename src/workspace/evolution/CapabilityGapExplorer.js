import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { Search, Sparkles, PlusCircle, AlertCircle, RefreshCw, } from 'lucide-react';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { EvolutionPlatformApiClient } from '../../services/evolutionPlatformApiClient';
export const CapabilityGapExplorer = () => {
    const [capabilities, setCapabilities] = useState([]);
    const [loading, setLoading] = useState(true);
    const [discovering, setDiscovering] = useState(false);
    const [showRegisterModal, setShowRegisterModal] = useState(false);
    // Form states
    const [name, setName] = useState('');
    const [domain, setDomain] = useState('document_intelligence');
    const [description, setDescription] = useState('');
    const [maturity, setMaturity] = useState('EXPERIMENTAL');
    useEffect(() => {
        loadCapabilities();
    }, []);
    const loadCapabilities = async () => {
        setLoading(true);
        try {
            const data = await EvolutionPlatformApiClient.listCapabilities();
            setCapabilities(data);
        }
        catch (err) {
            console.error('Failed to load capabilities:', err);
        }
        finally {
            setLoading(false);
        }
    };
    const handleDiscover = async () => {
        setDiscovering(true);
        try {
            const data = await EvolutionPlatformApiClient.discoverCapabilities();
            setCapabilities(data);
        }
        catch (err) {
            console.error('Error discovering capabilities:', err);
        }
        finally {
            setDiscovering(false);
        }
    };
    const handleRegister = async (e) => {
        e.preventDefault();
        if (!name.trim())
            return;
        try {
            const newCap = await EvolutionPlatformApiClient.registerCapability({
                name,
                domain,
                description,
                maturity_level: maturity,
                accuracy_score: 0.96,
                latency_ms: 18.0,
                cost_per_invocation: 0.0012,
            });
            setCapabilities((prev) => [...prev, newCap]);
            setShowRegisterModal(false);
            setName('');
            setDescription('');
        }
        catch (err) {
            console.error('Registration failed:', err);
        }
    };
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "bg-gradient-to-r from-slate-900 via-slate-900 to-slate-950 border border-slate-800 rounded-2xl p-6 flex flex-col md:flex-row items-start md:items-center justify-between gap-4 shadow-xl", children: [_jsxs("div", { className: "flex items-center gap-3", children: [_jsx("div", { className: "p-2.5 bg-purple-500/10 border border-purple-500/20 rounded-xl", children: _jsx(Search, { className: "w-6 h-6 text-purple-400" }) }), _jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("h1", { className: "text-xl font-bold text-slate-100", children: "Capability Gap & Architectural Discovery" }), _jsx(Badge, { variant: "intelligence", size: "sm", children: "Autonomous Detection" })] }), _jsx("p", { className: "text-sm text-slate-400 mt-0.5", children: "Uncovers missing capabilities, redundant agent roles, knowledge blind spots, and synthesizes new modular descriptors." })] })] }), _jsxs("div", { className: "flex items-center gap-3", children: [_jsx(Button, { variant: "outline", onClick: loadCapabilities, disabled: loading, children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(RefreshCw, { className: `w-4 h-4 ${loading ? 'animate-spin' : ''}` }), "Refresh"] }) }), _jsx(Button, { variant: "outline", onClick: () => setShowRegisterModal(true), children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(PlusCircle, { className: "w-4 h-4" }), "Register Capability"] }) }), _jsx(Button, { variant: "intelligence", onClick: handleDiscover, disabled: discovering, children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(Sparkles, { className: `w-4 h-4 ${discovering ? 'animate-spin' : ''}` }), discovering ? 'Scanning Platform...' : 'Discover Capability Gaps'] }) })] })] }), _jsx("div", { className: "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5", children: capabilities.map((cap) => (_jsxs("div", { className: `bg-slate-900/80 border ${cap.is_gap ? 'border-amber-500/40' : 'border-slate-800'} rounded-xl p-5 space-y-4 hover:border-slate-700 transition-all flex flex-col justify-between`, children: [_jsxs("div", { className: "space-y-2", children: [_jsxs("div", { className: "flex items-start justify-between gap-2", children: [_jsx("span", { className: "text-sm font-semibold text-slate-100 leading-snug", children: cap.name }), _jsx(Badge, { variant: cap.is_gap ? 'warning' : cap.state === 'ACTIVE' ? 'success' : 'outline', size: "sm", children: cap.is_gap ? 'Gap Discovered' : cap.state })] }), _jsx("p", { className: "text-xs text-slate-400", children: cap.description || 'Core platform modular capability' })] }), cap.is_gap && (_jsxs("div", { className: "p-3 bg-amber-500/10 border border-amber-500/20 rounded-lg text-xs text-amber-200 flex items-start gap-2", children: [_jsx(AlertCircle, { className: "w-4 h-4 flex-shrink-0 mt-0.5 text-amber-400" }), _jsx("span", { children: cap.gap_rationale })] })), _jsxs("div", { className: "pt-3 border-t border-slate-800/80 grid grid-cols-3 gap-2 text-center text-xs font-mono", children: [_jsxs("div", { className: "bg-slate-950/60 p-2 rounded", children: [_jsx("div", { className: "text-slate-500 text-[10px]", children: "EFFICIENCY" }), _jsxs("div", { className: "text-slate-200 font-semibold", children: [(cap.efficiency_score * 100).toFixed(0), "%"] })] }), _jsxs("div", { className: "bg-slate-950/60 p-2 rounded", children: [_jsx("div", { className: "text-slate-500 text-[10px]", children: "LATENCY" }), _jsxs("div", { className: "text-indigo-300 font-semibold", children: [cap.latency_ms.toFixed(0), "ms"] })] }), _jsxs("div", { className: "bg-slate-950/60 p-2 rounded", children: [_jsx("div", { className: "text-slate-500 text-[10px]", children: "ACCURACY" }), _jsxs("div", { className: "text-emerald-300 font-semibold", children: [(cap.accuracy_score * 100).toFixed(0), "%"] })] })] })] }, cap.capability_id))) }), showRegisterModal && (_jsx("div", { className: "fixed inset-0 bg-black/70 backdrop-blur-sm z-50 flex items-center justify-center p-4", children: _jsxs("div", { className: "bg-slate-900 border border-slate-800 rounded-2xl p-6 max-w-lg w-full space-y-4 shadow-2xl", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsx("h3", { className: "text-lg font-bold text-slate-100", children: "Register Subsystem Capability" }), _jsx("button", { onClick: () => setShowRegisterModal(false), className: "text-slate-400 hover:text-slate-200 text-sm font-semibold", children: "\u2715" })] }), _jsxs("form", { onSubmit: handleRegister, className: "space-y-4", children: [_jsxs("div", { children: [_jsx("label", { className: "text-xs font-medium text-slate-300 block mb-1", children: "Capability Name" }), _jsx("input", { type: "text", value: name, onChange: (e) => setName(e.target.value), placeholder: "e.g. Adaptive AST Layout Segmenter", className: "w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-slate-100 focus:outline-none focus:border-purple-500 font-mono", required: true })] }), _jsxs("div", { className: "grid grid-cols-2 gap-4", children: [_jsxs("div", { children: [_jsx("label", { className: "text-xs font-medium text-slate-300 block mb-1", children: "Domain" }), _jsxs("select", { value: domain, onChange: (e) => setDomain(e.target.value), className: "w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-slate-100 focus:outline-none focus:border-purple-500", children: [_jsx("option", { value: "document_intelligence", children: "Document Intelligence" }), _jsx("option", { value: "caching", children: "Caching & Memory" }), _jsx("option", { value: "orchestration", children: "Swarm Orchestration" }), _jsx("option", { value: "governance", children: "Security & Governance" })] })] }), _jsxs("div", { children: [_jsx("label", { className: "text-xs font-medium text-slate-300 block mb-1", children: "Maturity Level" }), _jsxs("select", { value: maturity, onChange: (e) => setMaturity(e.target.value), className: "w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-slate-100 focus:outline-none focus:border-purple-500", children: [_jsx("option", { value: "EXPERIMENTAL", children: "EXPERIMENTAL" }), _jsx("option", { value: "VALIDATING", children: "VALIDATING" }), _jsx("option", { value: "PRODUCTION", children: "PRODUCTION" })] })] })] }), _jsxs("div", { children: [_jsx("label", { className: "text-xs font-medium text-slate-300 block mb-1", children: "Description & Rationale" }), _jsx("textarea", { value: description, onChange: (e) => setDescription(e.target.value), placeholder: "Provide details on throughput, algorithm design, and purpose...", rows: 3, className: "w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-slate-100 focus:outline-none focus:border-purple-500" })] }), _jsxs("div", { className: "flex justify-end gap-3 pt-2", children: [_jsx(Button, { variant: "ghost", onClick: () => setShowRegisterModal(false), children: "Cancel" }), _jsx(Button, { variant: "intelligence", type: "submit", children: "Save Capability" })] })] })] }) }))] }));
};
