import { jsx as _jsx, jsxs as _jsxs, Fragment as _Fragment } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { Compass, RotateCw, Sparkles, Activity, CheckCircle2, ListOrdered, } from 'lucide-react';
import { organizationPlatformApiClient } from '../../services/organizationPlatformApiClient';
export const StrategyGenerationStudio = () => {
    const [strategies, setStrategies] = useState([]);
    const [loading, setLoading] = useState(true);
    const [generating, setGenerating] = useState(false);
    const [evaluating, setEvaluating] = useState(false);
    const [selectedStrategy, setSelectedStrategy] = useState(null);
    const [simulationResult, setSimulationResult] = useState(null);
    const loadStrategies = async () => {
        try {
            setLoading(true);
            const data = await organizationPlatformApiClient.getStrategies('msn_reduce_cost_40pct');
            setStrategies(data);
            if (data.length > 0 && !selectedStrategy) {
                setSelectedStrategy(data[0] || null);
            }
        }
        catch (err) {
            console.error('Failed to load strategies:', err);
        }
        finally {
            setLoading(false);
        }
    };
    useEffect(() => {
        loadStrategies();
    }, []);
    const handleGenerate = async () => {
        try {
            setGenerating(true);
            const created = await organizationPlatformApiClient.generateStrategies('msn_reduce_cost_40pct', 3);
            setStrategies(created);
            if (created.length > 0)
                setSelectedStrategy(created[0] || null);
        }
        catch (err) {
            console.error('Error generating strategies:', err);
        }
        finally {
            setGenerating(false);
        }
    };
    const handleRunMonteCarlo = async (strategyId) => {
        try {
            setEvaluating(true);
            const res = await fetch(`/api/v1/organization/strategies/${strategyId}/evaluate?iterations=500`, {
                method: 'POST',
            });
            const data = await res.json();
            setSimulationResult(data);
        }
        catch (err) {
            console.error('Error running strategy simulation:', err);
        }
        finally {
            setEvaluating(false);
        }
    };
    return (_jsxs("div", { className: "space-y-6 p-6", children: [_jsxs("div", { className: "flex flex-col md:flex-row items-start md:items-center justify-between gap-4 border-b border-border pb-4", children: [_jsxs("div", { className: "flex items-center gap-3", children: [_jsx("div", { className: "p-2 bg-primary/10 rounded-lg text-primary", children: _jsx(Compass, { className: "w-6 h-6" }) }), _jsxs("div", { children: [_jsx("h1", { className: "text-2xl font-bold tracking-tight", children: "Strategy Generation Studio" }), _jsx("p", { className: "text-sm text-muted-foreground", children: "Multi-Alternative Organizational Strategy Synthesis, Bayesian Utility Ranking & Monte Carlo Simulations" })] })] }), _jsxs("div", { className: "flex items-center gap-3", children: [_jsx(Button, { variant: "outline", onClick: loadStrategies, disabled: loading, children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(RotateCw, { className: `w-4 h-4 ${loading ? 'animate-spin' : ''}` }), "Refresh"] }) }), _jsx(Button, { variant: "intelligence", onClick: handleGenerate, disabled: generating, children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(Sparkles, { className: "w-4 h-4" }), generating ? 'Synthesizing...' : 'Synthesize Alternative Strategies'] }) })] })] }), _jsxs("div", { className: "grid grid-cols-1 lg:grid-cols-3 gap-6", children: [_jsxs("div", { className: "space-y-4", children: [_jsx("h2", { className: "text-sm font-semibold flex items-center justify-between", children: _jsxs("span", { children: ["Generated Strategies (", strategies.length, ")"] }) }), _jsx("div", { className: "space-y-3", children: strategies.map((s) => (_jsx(Card, { onClick: () => {
                                        setSelectedStrategy(s);
                                        setSimulationResult(null);
                                    }, className: `border cursor-pointer transition-all ${selectedStrategy?.strategy_id === s.strategy_id
                                        ? 'border-primary bg-primary/5 shadow-sm'
                                        : 'border-border hover:bg-muted/30'}`, children: _jsxs(CardContent, { className: "p-4 space-y-2", children: [_jsxs("div", { className: "flex justify-between items-start", children: [_jsx("span", { className: "font-semibold text-sm line-clamp-1", children: s.title }), s.is_selected && _jsx(Badge, { variant: "success", children: "OPTIMAL" })] }), _jsx("p", { className: "text-xs text-muted-foreground line-clamp-2", children: s.rationale }), _jsxs("div", { className: "grid grid-cols-2 gap-2 pt-2 border-t border-border/60 text-xs", children: [_jsxs("div", { children: [_jsx("span", { className: "text-muted-foreground", children: "Expected ROI:" }), _jsxs("span", { className: "font-semibold text-primary ml-1", children: [s.expected_roi_multiplier, "x"] })] }), _jsxs("div", { children: [_jsx("span", { className: "text-muted-foreground", children: "Est. Cost:" }), _jsxs("span", { className: "font-medium ml-1", children: ["$", s.total_estimated_cost_usd.toLocaleString()] })] }), _jsxs("div", { children: [_jsx("span", { className: "text-muted-foreground", children: "Sim Pass Rate:" }), _jsxs("span", { className: "font-semibold text-emerald-500 ml-1", children: [(s.simulation_pass_rate * 100).toFixed(0), "%"] })] }), _jsxs("div", { children: [_jsx("span", { className: "text-muted-foreground", children: "Risk Index:" }), _jsx("span", { className: "font-medium ml-1", children: s.risk_score })] })] })] }) }, s.strategy_id))) })] }), _jsx("div", { className: "lg:col-span-2 space-y-6", children: selectedStrategy ? (_jsx(_Fragment, { children: _jsxs(Card, { className: "border-border shadow-sm", children: [_jsxs(CardHeader, { className: "flex flex-row items-center justify-between pb-3", children: [_jsxs("div", { children: [_jsx(CardTitle, { className: "text-lg", children: selectedStrategy.title }), _jsx("p", { className: "text-xs text-muted-foreground font-mono mt-0.5", children: selectedStrategy.strategy_id })] }), _jsx(Button, { variant: "outline", onClick: () => handleRunMonteCarlo(selectedStrategy.strategy_id), disabled: evaluating, children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(Activity, { className: "w-4 h-4 text-primary" }), evaluating ? 'Simulating...' : 'Run Monte Carlo (500 runs)'] }) })] }), _jsxs(CardContent, { className: "space-y-4", children: [_jsxs("div", { className: "p-3 bg-muted/40 border border-border rounded-lg text-xs leading-relaxed", children: [_jsx("span", { className: "font-semibold text-foreground", children: "Strategic Rationale: " }), selectedStrategy.rationale] }), simulationResult && (_jsxs("div", { className: "p-4 bg-primary/5 border border-primary/20 rounded-lg space-y-2", children: [_jsxs("div", { className: "font-semibold text-sm text-primary flex items-center gap-1.5", children: [_jsx(CheckCircle2, { className: "w-4 h-4" }), " Monte Carlo Simulation Report (", simulationResult.iterations, " runs)"] }), _jsxs("div", { className: "grid grid-cols-2 md:grid-cols-4 gap-3 text-xs pt-1", children: [_jsxs("div", { children: [_jsx("span", { className: "text-muted-foreground", children: "Success Prob:" }), _jsxs("div", { className: "font-bold text-emerald-500 text-sm", children: [(simulationResult.probability_of_success * 100).toFixed(1), "%"] })] }), _jsxs("div", { children: [_jsx("span", { className: "text-muted-foreground", children: "Mean ROI:" }), _jsxs("div", { className: "font-bold text-sm", children: [simulationResult.mean_expected_roi, "x"] })] }), _jsxs("div", { children: [_jsx("span", { className: "text-muted-foreground", children: "Mean Cost:" }), _jsxs("div", { className: "font-bold text-sm", children: ["$", simulationResult.mean_expected_cost_usd] })] }), _jsxs("div", { children: [_jsx("span", { className: "text-muted-foreground", children: "Verdict:" }), _jsx(Badge, { variant: "success", children: simulationResult.verdict })] })] })] })), _jsxs("div", { children: [_jsxs("h3", { className: "text-sm font-semibold mb-2 flex items-center gap-2", children: [_jsx(ListOrdered, { className: "w-4 h-4 text-primary" }), "Operational Actions (", selectedStrategy.actions.length, ")"] }), _jsx("div", { className: "space-y-2", children: selectedStrategy.actions.map((act) => (_jsxs("div", { className: "p-3 bg-card border border-border rounded-lg text-xs", children: [_jsxs("div", { className: "flex justify-between items-start", children: [_jsx("span", { className: "font-medium text-sm", children: act.title }), _jsx(Badge, { variant: "outline", children: act.target_department })] }), _jsxs("div", { className: "grid grid-cols-3 gap-2 mt-2 text-muted-foreground", children: [_jsxs("span", { children: ["Cost: $", act.estimated_cost_usd.toLocaleString()] }), _jsxs("span", { children: ["Utility: ", (act.expected_utility * 100).toFixed(0), "%"] }), _jsxs("span", { children: ["Timeline: ", act.timeline_weeks, " wks"] })] })] }, act.action_id))) })] })] })] }) })) : (_jsx(Card, { className: "border-border shadow-sm p-8 text-center text-muted-foreground", children: "Select a strategy plan to inspect actions and utility parameters." })) })] })] }));
};
