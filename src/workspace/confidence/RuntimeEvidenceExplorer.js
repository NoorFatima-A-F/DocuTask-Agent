import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { Database, Search, CheckCircle2, AlertTriangle, ArrowUpRight, Hash, Layers } from 'lucide-react';
const mockEvidences = [
    {
        id: 'ev-901',
        sourceEventId: 'evt_dag_exec_8832',
        eventType: 'worker.step.completed',
        dimension: 'ocr_quality',
        featureKey: 'character_recognition_rate',
        observedValue: 0.994,
        expectedRange: '[0.950, 1.000]',
        statisticalWeight: 0.18,
        provenanceHash: 'sha256:7f9a12c8e3...',
        status: 'VALID',
        timestamp: '2026-09-11T22:45:10Z',
    },
    {
        id: 'ev-902',
        sourceEventId: 'evt_dag_exec_8833',
        eventType: 'worker.schema.validated',
        dimension: 'schema_extraction',
        featureKey: 'field_match_f1',
        observedValue: 0.982,
        expectedRange: '[0.900, 1.000]',
        statisticalWeight: 0.22,
        provenanceHash: 'sha256:4b219cf10a...',
        status: 'VALID',
        timestamp: '2026-09-11T22:45:12Z',
    },
    {
        id: 'ev-903',
        sourceEventId: 'evt_dag_exec_8834',
        eventType: 'truth_ledger.invariant.checked',
        dimension: 'invariant_validation',
        featureKey: 'invariant_violation_count',
        observedValue: 0.0,
        expectedRange: '[0.000, 0.000]',
        statisticalWeight: 0.25,
        provenanceHash: 'sha256:88e09f21ab...',
        status: 'VALID',
        timestamp: '2026-09-11T22:45:15Z',
    },
    {
        id: 'ev-904',
        sourceEventId: 'evt_resilience_probe_102',
        eventType: 'resilience.circuit_breaker.heartbeat',
        dimension: 'worker_reliability',
        featureKey: 'consecutive_error_rate',
        observedValue: 0.012,
        expectedRange: '[0.000, 0.050]',
        statisticalWeight: 0.15,
        provenanceHash: 'sha256:12cba89721...',
        status: 'VALID',
        timestamp: '2026-09-11T22:45:18Z',
    },
    {
        id: 'ev-905',
        sourceEventId: 'evt_planner_mutation_441',
        eventType: 'planner.dag.repartitioned',
        dimension: 'planner_efficiency',
        featureKey: 'dag_schedule_slack_ratio',
        observedValue: 0.068,
        expectedRange: '[0.000, 0.100]',
        statisticalWeight: 0.20,
        provenanceHash: 'sha256:bb18290fa4...',
        status: 'VALID',
        timestamp: '2026-09-11T22:45:22Z',
    },
];
export const RuntimeEvidenceExplorer = () => {
    const [searchTerm, setSearchTerm] = useState('');
    const [selectedDimension, setSelectedDimension] = useState('ALL');
    const filtered = mockEvidences.filter((item) => {
        const matchesSearch = item.id.toLowerCase().includes(searchTerm.toLowerCase()) ||
            item.sourceEventId.toLowerCase().includes(searchTerm.toLowerCase()) ||
            item.featureKey.toLowerCase().includes(searchTerm.toLowerCase()) ||
            item.eventType.toLowerCase().includes(searchTerm.toLowerCase());
        const matchesDim = selectedDimension === 'ALL' || item.dimension === selectedDimension;
        return matchesSearch && matchesDim;
    });
    return (_jsxs("div", { className: "p-6 space-y-6 bg-[#0B1120] min-h-screen text-[#F8FAFC]", children: [_jsxs("div", { className: "flex flex-wrap items-center justify-between gap-4 border-b border-[#1E293B] pb-6", children: [_jsx("div", { className: "space-y-1", children: _jsxs("div", { className: "flex items-center gap-3", children: [_jsx("div", { className: "p-2 bg-gradient-to-br from-emerald-500/20 to-teal-500/20 border border-emerald-500/30 rounded-xl text-emerald-400", children: _jsx(Database, { className: "w-5 h-5" }) }), _jsxs("div", { children: [_jsxs("h1", { className: "text-xl font-bold font-mono tracking-tight text-white flex items-center gap-2", children: ["Runtime Evidence Explorer", _jsx(Badge, { variant: "success", size: "sm", children: "Immutable Ledger" })] }), _jsx("p", { className: "text-xs text-slate-400", children: "Direct projection of domain events into verified statistical features backing confidence scores." })] })] }) }), _jsxs("div", { className: "flex items-center gap-3", children: [_jsx(Badge, { variant: "intelligence", size: "sm", children: "5 Total Samples" }), _jsx(Badge, { variant: "outline", size: "sm", children: "0 Anomalies" })] })] }), _jsxs("div", { className: "flex flex-wrap items-center gap-4 bg-[#0F172A] p-4 rounded-xl border border-[#1E293B]", children: [_jsxs("div", { className: "relative flex-1 min-w-[240px]", children: [_jsx(Search, { className: "w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" }), _jsx("input", { type: "text", placeholder: "Search by Evidence ID, Event ID, Feature...", value: searchTerm, onChange: (e) => setSearchTerm(e.target.value), className: "w-full pl-9 pr-4 py-2 bg-[#0B1120] border border-[#1E293B] rounded-lg text-sm text-slate-200 placeholder-slate-500 focus:outline-none focus:border-emerald-500" })] }), _jsxs("select", { value: selectedDimension, onChange: (e) => setSelectedDimension(e.target.value), className: "bg-[#0B1120] border border-[#1E293B] rounded-lg px-3 py-2 text-sm text-slate-200 focus:outline-none focus:border-emerald-500", children: [_jsx("option", { value: "ALL", children: "All Dimensions" }), _jsx("option", { value: "ocr_quality", children: "OCR Quality" }), _jsx("option", { value: "schema_extraction", children: "Schema Extraction" }), _jsx("option", { value: "invariant_validation", children: "Invariant Validation" }), _jsx("option", { value: "worker_reliability", children: "Worker Reliability" }), _jsx("option", { value: "planner_efficiency", children: "Planner Efficiency" })] })] }), _jsx(Card, { className: "bg-[#0F172A] border-[#1E293B] overflow-hidden", children: _jsx("div", { className: "overflow-x-auto", children: _jsxs("table", { className: "w-full text-left text-xs font-mono", children: [_jsx("thead", { className: "bg-[#1E293B]/60 text-slate-400 border-b border-[#1E293B]", children: _jsxs("tr", { children: [_jsx("th", { className: "p-3", children: "Evidence ID / Timestamp" }), _jsx("th", { className: "p-3", children: "Source Event" }), _jsx("th", { className: "p-3", children: "Dimension & Feature" }), _jsx("th", { className: "p-3", children: "Observed / Range" }), _jsx("th", { className: "p-3", children: "Weight" }), _jsx("th", { className: "p-3", children: "Provenance Hash" }), _jsx("th", { className: "p-3", children: "Status" })] }) }), _jsx("tbody", { className: "divide-y divide-[#1E293B]/40", children: filtered.map((item) => (_jsxs("tr", { className: "hover:bg-slate-800/30 transition-colors", children: [_jsxs("td", { className: "p-3", children: [_jsxs("div", { className: "font-semibold text-emerald-400 flex items-center gap-1", children: [_jsx(Hash, { className: "w-3.5 h-3.5" }), item.id] }), _jsx("div", { className: "text-[10px] text-slate-500", children: item.timestamp })] }), _jsxs("td", { className: "p-3", children: [_jsx("div", { className: "text-slate-200", children: item.eventType }), _jsxs("div", { className: "text-[10px] text-slate-500 flex items-center gap-1", children: [_jsx(Layers, { className: "w-3 h-3" }), item.sourceEventId] })] }), _jsxs("td", { className: "p-3", children: [_jsx("div", { className: "text-slate-300 capitalize", children: item.dimension.replace('_', ' ') }), _jsx("div", { className: "text-[10px] text-slate-400", children: item.featureKey })] }), _jsxs("td", { className: "p-3", children: [_jsxs("div", { className: "text-slate-200 font-bold", children: [(item.observedValue * 100).toFixed(1), "%"] }), _jsx("div", { className: "text-[10px] text-slate-500", children: item.expectedRange })] }), _jsx("td", { className: "p-3 text-slate-300", children: item.statisticalWeight.toFixed(2) }), _jsx("td", { className: "p-3 text-[10px] text-slate-400", children: _jsx("span", { className: "bg-slate-900/80 px-1.5 py-0.5 rounded border border-slate-700", children: item.provenanceHash }) }), _jsx("td", { className: "p-3", children: item.status === 'VALID' ? (_jsxs(Badge, { variant: "success", size: "sm", className: "flex items-center gap-1", children: [_jsx(CheckCircle2, { className: "w-3 h-3" }), "Valid"] })) : (_jsxs(Badge, { variant: "warning", size: "sm", className: "flex items-center gap-1", children: [_jsx(AlertTriangle, { className: "w-3 h-3" }), item.status] })) })] }, item.id))) })] }) }) }), _jsxs("div", { className: "flex items-center justify-between text-xs text-slate-500 border-t border-[#1E293B] pt-4", children: [_jsx("span", { children: "Verified against Truth Ledger invariant rule `#INV-CONF-001`" }), _jsxs("a", { href: "#audit", className: "text-emerald-400 hover:underline flex items-center gap-1", children: ["Export Evidence Provenance Chain ", _jsx(ArrowUpRight, { className: "w-3.5 h-3.5" })] })] })] }));
};
