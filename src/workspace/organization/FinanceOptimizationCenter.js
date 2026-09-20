import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { DollarSign, RotateCw, Sparkles, LineChart, } from 'lucide-react';
import { organizationPlatformApiClient } from '../../services/organizationPlatformApiClient';
export const FinanceOptimizationCenter = () => {
    const [finances, setFinances] = useState(null);
    const [loading, setLoading] = useState(true);
    const [forecasting, setForecasting] = useState(false);
    const [horizonMonths, setHorizonMonths] = useState(12);
    const [activeForecast, setActiveForecast] = useState(null);
    const loadFinances = async () => {
        try {
            setLoading(true);
            const data = await organizationPlatformApiClient.getFinanceROI();
            setFinances(data);
            setActiveForecast(data.cost_forecast);
        }
        catch (err) {
            console.error('Failed to load financial intelligence:', err);
        }
        finally {
            setLoading(false);
        }
    };
    useEffect(() => {
        loadFinances();
    }, []);
    const handleForecast = async () => {
        try {
            setForecasting(true);
            const fc = await organizationPlatformApiClient.forecastFinance(horizonMonths);
            setActiveForecast(fc);
        }
        catch (err) {
            console.error('Error calculating cost forecast:', err);
        }
        finally {
            setForecasting(false);
        }
    };
    return (_jsxs("div", { className: "space-y-6 p-6", children: [_jsxs("div", { className: "flex flex-col md:flex-row items-start md:items-center justify-between gap-4 border-b border-border pb-4", children: [_jsxs("div", { className: "flex items-center gap-3", children: [_jsx("div", { className: "p-2 bg-primary/10 rounded-lg text-primary", children: _jsx(DollarSign, { className: "w-6 h-6" }) }), _jsxs("div", { children: [_jsx("h1", { className: "text-2xl font-bold tracking-tight", children: "Finance & Economic Optimization" }), _jsx("p", { className: "text-sm text-muted-foreground", children: "Autonomous Cost Telemetry, Multi-Quarter Spend Forecasting & Unit Economic ROI Tracking" })] })] }), _jsx("div", { className: "flex items-center gap-3", children: _jsx(Button, { variant: "outline", onClick: loadFinances, disabled: loading, children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(RotateCw, { className: `w-4 h-4 ${loading ? 'animate-spin' : ''}` }), "Refresh"] }) }) })] }), _jsxs("div", { className: "grid grid-cols-1 md:grid-cols-4 gap-4", children: [_jsx(Card, { className: "border-border shadow-sm", children: _jsxs(CardContent, { className: "p-4 space-y-1", children: [_jsx("div", { className: "text-xs text-muted-foreground", children: "Active ROI Multiplier" }), _jsx("div", { className: "text-2xl font-bold text-primary", children: finances ? `${finances.active_roi_multiplier.toFixed(1)}x` : '4.2x' }), _jsx("p", { className: "text-xs text-muted-foreground", children: "Annualized return on compute spend" })] }) }), _jsx(Card, { className: "border-border shadow-sm", children: _jsxs(CardContent, { className: "p-4 space-y-1", children: [_jsx("div", { className: "text-xs text-muted-foreground", children: "Cost per 1k Docs" }), _jsxs("div", { className: "text-2xl font-bold text-emerald-500", children: ["$", finances ? finances.roi_projection.optimized_cost_per_1k_docs_usd.toFixed(2) : '3.20'] }), _jsxs("p", { className: "text-xs text-muted-foreground", children: ["Down from $", finances ? finances.roi_projection.baseline_cost_per_1k_docs_usd.toFixed(2) : '5.80', " (-44.8%)"] })] }) }), _jsx(Card, { className: "border-border shadow-sm", children: _jsxs(CardContent, { className: "p-4 space-y-1", children: [_jsx("div", { className: "text-xs text-muted-foreground", children: "Operating Margin" }), _jsx("div", { className: "text-2xl font-bold text-purple-500", children: finances ? `${finances.net_operating_margin_pct.toFixed(1)}%` : '77.8%' }), _jsx("p", { className: "text-xs text-muted-foreground", children: "Revenue impact vs operational spend" })] }) }), _jsx(Card, { className: "border-border shadow-sm", children: _jsxs(CardContent, { className: "p-4 space-y-1", children: [_jsx("div", { className: "text-xs text-muted-foreground", children: "Break-Even Timeline" }), _jsx("div", { className: "text-2xl font-bold text-blue-500", children: finances ? `${finances.roi_projection.break_even_timeline_days} Days` : '28 Days' }), _jsx("p", { className: "text-xs text-muted-foreground", children: "Full capital recovery window" })] }) })] }), _jsxs(Card, { className: "border-border shadow-sm", children: [_jsx(CardHeader, { children: _jsxs(CardTitle, { className: "text-base flex items-center justify-between", children: [_jsxs("span", { className: "flex items-center gap-2", children: [_jsx(LineChart, { className: "w-4 h-4 text-primary" }), "Multi-Quarter Operational Cost Forecast"] }), _jsxs("div", { className: "flex items-center gap-3", children: [_jsx("span", { className: "text-xs text-muted-foreground", children: "Horizon:" }), _jsxs("select", { value: horizonMonths, onChange: (e) => setHorizonMonths(Number(e.target.value)), className: "px-2.5 py-1 text-xs rounded border border-input bg-background", children: [_jsx("option", { value: 3, children: "3 Months (Q1)" }), _jsx("option", { value: 6, children: "6 Months (H1)" }), _jsx("option", { value: 12, children: "12 Months (1 Year)" }), _jsx("option", { value: 24, children: "24 Months (2 Years)" })] }), _jsx(Button, { variant: "intelligence", onClick: handleForecast, disabled: forecasting, children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(Sparkles, { className: "w-4 h-4" }), forecasting ? 'Calculating...' : 'Run Cost Forecast'] }) })] })] }) }), _jsx(CardContent, { children: activeForecast && (_jsxs("div", { className: "grid grid-cols-1 md:grid-cols-3 gap-4 pt-2", children: [_jsxs("div", { className: "p-4 bg-muted/40 border border-border rounded-lg space-y-1", children: [_jsxs("span", { className: "text-xs text-muted-foreground", children: ["Projected Operating Spend (", activeForecast.horizon_months, " mo):"] }), _jsxs("div", { className: "text-2xl font-bold text-foreground", children: ["$", activeForecast.projected_spend_usd.toLocaleString()] })] }), _jsxs("div", { className: "p-4 bg-emerald-500/10 border border-emerald-500/30 rounded-lg space-y-1", children: [_jsx("span", { className: "text-xs text-muted-foreground", children: "Projected Cumulative Savings:" }), _jsxs("div", { className: "text-2xl font-bold text-emerald-500", children: ["+$", activeForecast.projected_savings_usd.toLocaleString()] })] }), _jsxs("div", { className: "p-4 bg-primary/5 border border-primary/20 rounded-lg space-y-1", children: [_jsx("span", { className: "text-xs text-muted-foreground", children: "Model Confidence Level:" }), _jsxs("div", { className: "text-2xl font-bold text-primary", children: [(activeForecast.confidence_level * 100).toFixed(1), "%"] })] })] })) })] })] }));
};
