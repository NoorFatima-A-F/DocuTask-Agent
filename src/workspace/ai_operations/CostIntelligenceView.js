import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { DollarSign, TrendingDown, PieChart, Lightbulb, Zap, RefreshCw, } from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { AIOperationsApiClient } from '../../services/aiOperationsApiClient';
export const CostIntelligenceView = () => {
    const [costData, setCostData] = useState(null);
    const [loading, setLoading] = useState(true);
    const loadCostData = async () => {
        try {
            setLoading(true);
            const data = await AIOperationsApiClient.getCostAnalytics();
            setCostData(data);
        }
        catch (err) {
            console.error('Failed to load cost analytics:', err);
        }
        finally {
            setLoading(false);
        }
    };
    useEffect(() => {
        loadCostData();
    }, []);
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex items-center justify-between bg-slate-900/60 p-5 rounded-2xl border border-slate-800 backdrop-blur-md", children: [_jsxs("div", { className: "flex items-center gap-3", children: [_jsx("div", { className: "p-2.5 bg-emerald-500/10 rounded-xl border border-emerald-500/20", children: _jsx(DollarSign, { className: "w-6 h-6 text-emerald-400" }) }), _jsxs("div", { children: [_jsx("h1", { className: "text-xl font-bold text-white", children: "Cost & Token Intelligence" }), _jsx("p", { className: "text-xs text-slate-400", children: "Token burn analytics, model tier spend breakdown, and savings recommendations" })] })] }), _jsx(Button, { variant: "outline", onClick: loadCostData, disabled: loading, children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(RefreshCw, { className: `w-4 h-4 ${loading ? 'animate-spin' : ''}` }), "Refresh"] }) })] }), _jsxs("div", { className: "grid grid-cols-1 md:grid-cols-3 gap-4", children: [_jsxs(Card, { className: "p-5 bg-slate-900/40 border-slate-800", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsx("span", { className: "text-sm font-medium text-slate-400", children: "Current Spend" }), _jsx(DollarSign, { className: "w-5 h-5 text-emerald-400" })] }), _jsx("div", { className: "mt-2", children: _jsxs("span", { className: "text-3xl font-bold text-white", children: ["$", costData?.total_cost_usd ?? 0.0] }) }), _jsxs("p", { className: "mt-1 text-xs text-slate-500", children: [(costData?.total_tokens_consumed ?? 0).toLocaleString(), " tokens processed"] })] }), _jsxs(Card, { className: "p-5 bg-slate-900/40 border-slate-800", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsx("span", { className: "text-sm font-medium text-slate-400", children: "Projected Monthly" }), _jsx(TrendingDown, { className: "w-5 h-5 text-indigo-400" })] }), _jsx("div", { className: "mt-2", children: _jsxs("span", { className: "text-3xl font-bold text-white", children: ["$", costData?.projected_monthly_spend_usd ?? 0.0] }) }), _jsx("p", { className: "mt-1 text-xs text-slate-500", children: "Based on trailing 24h consumption" })] }), _jsxs(Card, { className: "p-5 bg-slate-900/40 border-slate-800", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsx("span", { className: "text-sm font-medium text-slate-400", children: "Optimization Potential" }), _jsx(Zap, { className: "w-5 h-5 text-amber-400" })] }), _jsx("div", { className: "mt-2", children: _jsx("span", { className: "text-3xl font-bold text-amber-300", children: "~25-35%" }) }), _jsx("p", { className: "mt-1 text-xs text-slate-500", children: "Via prompt caching & tier routing" })] })] }), _jsxs("div", { className: "grid grid-cols-1 lg:grid-cols-2 gap-6", children: [_jsxs(Card, { className: "p-6 bg-slate-900/50 border-slate-800", children: [_jsxs("h2", { className: "text-base font-semibold text-white mb-4 flex items-center gap-2", children: [_jsx(PieChart, { className: "w-4 h-4 text-emerald-400" }), " Spend by Model Tier"] }), _jsx("div", { className: "space-y-3", children: costData?.cost_by_model &&
                                    Object.entries(costData.cost_by_model).map(([model, cost]) => (_jsxs("div", { className: "p-3 bg-slate-950/60 rounded-xl border border-slate-800", children: [_jsxs("div", { className: "flex items-center justify-between text-xs mb-1", children: [_jsx("span", { className: "font-semibold text-slate-200", children: model }), _jsxs("span", { className: "font-mono text-emerald-400", children: ["$", cost] })] }), _jsx("div", { className: "w-full bg-slate-800 h-2 rounded-full overflow-hidden", children: _jsx("div", { className: "bg-emerald-400 h-full rounded-full", style: {
                                                        width: `${Math.min(100, (cost / Math.max(0.01, costData.total_cost_usd)) * 100)}%`,
                                                    } }) })] }, model))) })] }), _jsxs(Card, { className: "p-6 bg-slate-900/50 border-slate-800", children: [_jsxs("h2", { className: "text-base font-semibold text-white mb-4 flex items-center gap-2", children: [_jsx(Lightbulb, { className: "w-4 h-4 text-amber-400" }), " AI Cost Optimization Recommendations"] }), _jsx("div", { className: "space-y-3", children: costData?.savings_recommendations?.map((rec) => (_jsxs("div", { className: "p-4 bg-slate-950/60 rounded-xl border border-slate-800/80", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsx("h3", { className: "font-semibold text-white text-xs", children: rec.title }), _jsxs(Badge, { variant: "success", children: ["Save $", rec.potential_monthly_savings_usd, "/mo"] })] }), _jsxs("div", { className: "flex items-center justify-between mt-2.5 text-xs text-slate-400", children: [_jsxs("span", { children: ["Confidence: ", (rec.confidence * 100).toFixed(0), "%"] }), _jsxs("span", { className: "text-emerald-400 font-semibold", children: [rec.savings_pct, "% Reduction"] })] })] }, rec.recommendation_id))) })] })] })] }));
};
