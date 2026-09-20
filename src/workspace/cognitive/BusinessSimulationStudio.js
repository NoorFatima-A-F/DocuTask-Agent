import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Play, TrendingUp, Sliders } from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { cognitiveApiClient } from '../../services/cognitiveApiClient';
export const BusinessSimulationStudio = () => {
    const [scenarioName, setScenarioName] = useState('Switch Document Classification from Pro to Flash Model');
    const [selectedModel, setSelectedModel] = useState('gemini-1.5-flash');
    const [scenario, setScenario] = useState(null);
    const [simulating, setSimulating] = useState(false);
    const handleSimulate = async () => {
        setSimulating(true);
        try {
            const res = await cognitiveApiClient.simulate(scenarioName, { model: selectedModel });
            setScenario(res);
        }
        finally {
            setSimulating(false);
        }
    };
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { children: [_jsxs("h1", { className: "text-2xl font-bold text-slate-100 flex items-center gap-2", children: [_jsx(TrendingUp, { className: "w-7 h-7 text-cyan-400" }), "Autonomous Business & Architecture Simulation Studio"] }), _jsx("p", { className: "text-slate-400 text-sm mt-1", children: "Perform multi-variable \"what-if\" simulations over model upgrades, concurrency limits, latency, and ROI scaling." })] }), _jsxs(Card, { className: "p-5 bg-slate-900/60 border-slate-800 space-y-4", children: [_jsxs("div", { className: "space-y-3", children: [_jsx("label", { className: "text-xs font-semibold text-slate-400 uppercase", children: "Simulation Scenario Hypothesis" }), _jsx("input", { value: scenarioName, onChange: (e) => setScenarioName(e.target.value), className: "w-full px-3 py-2 bg-slate-800/80 border border-slate-700 rounded-lg text-slate-200 text-sm focus:outline-none focus:border-cyan-500" })] }), _jsxs("div", { className: "flex flex-wrap items-center justify-between pt-2 border-t border-slate-800", children: [_jsxs("div", { className: "flex items-center gap-3", children: [_jsx(Sliders, { className: "w-4 h-4 text-slate-400" }), _jsx("span", { className: "text-xs text-slate-400", children: "Target Model Parameter:" }), ['gemini-1.5-flash', 'gemini-1.5-pro', 'claude-3-5-sonnet', 'gpt-4o'].map((m) => (_jsx(Button, { variant: selectedModel === m ? 'primary' : 'outline', size: "sm", onClick: () => setSelectedModel(m), children: m }, m)))] }), _jsx(Button, { variant: "intelligence", onClick: handleSimulate, disabled: simulating, children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(Play, { className: "w-4 h-4" }), simulating ? 'Simulating...' : 'Run Simulation'] }) })] })] }), scenario && (_jsxs("div", { className: "grid grid-cols-1 md:grid-cols-3 gap-4", children: [_jsxs(Card, { className: "p-5 bg-slate-900/60 border-slate-800", children: [_jsx("span", { className: "text-xs text-slate-400 uppercase font-semibold", children: "Projected Latency Impact" }), _jsxs("p", { className: "text-2xl font-bold text-emerald-400 mt-2", children: [scenario.projected_latency_change_pct, "%"] }), _jsx("p", { className: "text-xs text-slate-400 mt-1", children: "Expected reduction in cycle time" })] }), _jsxs(Card, { className: "p-5 bg-slate-900/60 border-slate-800", children: [_jsx("span", { className: "text-xs text-slate-400 uppercase font-semibold", children: "Projected Token Cost Impact" }), _jsxs("p", { className: "text-2xl font-bold text-cyan-400 mt-2", children: [scenario.projected_cost_change_pct, "%"] }), _jsx("p", { className: "text-xs text-slate-400 mt-1", children: "Monthly cloud expenditure delta" })] }), _jsxs(Card, { className: "p-5 bg-slate-900/60 border-slate-800", children: [_jsx("span", { className: "text-xs text-slate-400 uppercase font-semibold", children: "Projected Business ROI Factor" }), _jsxs("p", { className: "text-2xl font-bold text-indigo-400 mt-2", children: [scenario.projected_roi_factor, "x"] }), _jsx("p", { className: "text-xs text-slate-400 mt-1", children: "Efficiency multiplier score" })] })] }))] }));
};
