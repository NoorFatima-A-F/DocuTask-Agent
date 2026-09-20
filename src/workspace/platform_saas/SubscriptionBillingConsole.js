import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { SaaSApiClient } from '../../services/saasApiClient';
import { CreditCard, CheckCircle2, Receipt, ArrowUpRight, RefreshCw } from 'lucide-react';
export const SubscriptionBillingConsole = () => {
    const [subs, setSubs] = useState([]);
    const [invoices, setInvoices] = useState([]);
    const [loading, setLoading] = useState(true);
    useEffect(() => {
        const load = async () => {
            setLoading(true);
            const [s, inv] = await Promise.all([
                SaaSApiClient.listSubscriptions(),
                SaaSApiClient.listInvoices('tenant_acme_corp'),
            ]);
            setSubs(s);
            setInvoices(inv);
            setLoading(false);
        };
        load();
    }, []);
    const activeSub = subs.find((s) => s.tenant_id === 'tenant_acme_corp') || subs[0];
    return (_jsxs("div", { className: "space-y-6", children: [_jsx("div", { className: "flex items-center justify-between", children: _jsxs("div", { children: [_jsxs("h1", { className: "text-2xl font-bold text-white flex items-center gap-3", children: [_jsx(CreditCard, { className: "w-7 h-7 text-indigo-400" }), "Subscription & Invoicing Gateway"] }), _jsx("p", { className: "text-sm text-slate-400 mt-1", children: "Enterprise plans, recurring billing schedules, Stripe/Paddle gateways, and invoice ledgers." })] }) }), loading ? (_jsxs("div", { className: "p-12 text-center text-slate-400", children: [_jsx(RefreshCw, { className: "w-6 h-6 animate-spin mx-auto mb-2" }), " Loading Billing Data..."] })) : (_jsxs("div", { className: "grid grid-cols-1 lg:grid-cols-3 gap-6", children: [_jsxs(Card, { className: "bg-slate-900/80 border-slate-800 lg:col-span-1", children: [_jsx(CardHeader, { children: _jsx(CardTitle, { className: "text-base text-white", children: "Current Enterprise Plan" }) }), _jsxs(CardContent, { className: "space-y-4", children: [_jsxs("div", { className: "p-4 bg-gradient-to-br from-indigo-950/40 to-slate-900 border border-indigo-800/40 rounded-lg", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsxs("span", { className: "text-xl font-bold text-white", children: [activeSub?.tier, " PLAN"] }), _jsx(Badge, { variant: "intelligence", children: activeSub?.billing_interval })] }), _jsxs("div", { className: "mt-3", children: [_jsxs("span", { className: "text-3xl font-extrabold text-white", children: ["$", activeSub?.base_price_monthly_usd] }), _jsx("span", { className: "text-xs text-slate-400", children: " / month" })] })] }), _jsxs("div", { className: "space-y-2 text-xs text-slate-300", children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx(CheckCircle2, { className: "w-4 h-4 text-emerald-400" }), " Unlimited Autonomous Agent Meshes"] }), _jsxs("div", { className: "flex items-center gap-2", children: [_jsx(CheckCircle2, { className: "w-4 h-4 text-emerald-400" }), " 1 Billion Tokens / Month included"] }), _jsxs("div", { className: "flex items-center gap-2", children: [_jsx(CheckCircle2, { className: "w-4 h-4 text-emerald-400" }), " Multi-Region Isolated Sandbox"] }), _jsxs("div", { className: "flex items-center gap-2", children: [_jsx(CheckCircle2, { className: "w-4 h-4 text-emerald-400" }), " 24/7 Dedicated SLA & SOC2 Compliance"] })] }), _jsx(Button, { variant: "intelligence", className: "w-full", children: _jsxs("span", { className: "flex items-center justify-center gap-2", children: [_jsx(ArrowUpRight, { className: "w-4 h-4" }), " Manage Subscription"] }) })] })] }), _jsxs(Card, { className: "bg-slate-900/80 border-slate-800 lg:col-span-2", children: [_jsx(CardHeader, { children: _jsxs(CardTitle, { className: "text-base text-white flex items-center gap-2", children: [_jsx(Receipt, { className: "w-5 h-5 text-emerald-400" }), " Invoice History & Payment Status"] }) }), _jsx(CardContent, { className: "space-y-3", children: invoices.map((inv) => (_jsxs("div", { className: "p-4 bg-slate-800/40 rounded border border-slate-700/50 flex items-center justify-between", children: [_jsxs("div", { children: [_jsx("span", { className: "text-sm font-semibold text-white block", children: inv.invoice_id }), _jsxs("span", { className: "text-xs text-slate-400", children: ["Period: ", inv.billing_period, " \u2022 Created: ", new Date(inv.created_at).toLocaleDateString()] })] }), _jsxs("div", { className: "flex items-center gap-4", children: [_jsxs("span", { className: "text-base font-bold text-white", children: ["$", inv.amount_due_usd.toLocaleString()] }), _jsx(Badge, { variant: inv.status === 'PAID' ? 'success' : 'warning', children: inv.status })] })] }, inv.invoice_id))) })] })] }))] }));
};
