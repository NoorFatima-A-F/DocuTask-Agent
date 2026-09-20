import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { Scale, RotateCw, Sparkles, CheckCircle2, ArrowRight, } from 'lucide-react';
import { organizationPlatformApiClient } from '../../services/organizationPlatformApiClient';
export const NegotiationArena = () => {
    const [negotiations, setNegotiations] = useState([]);
    const [loading, setLoading] = useState(true);
    const [negotiating, setNegotiating] = useState(false);
    const [selectedNeg, setSelectedNeg] = useState(null);
    // Form State
    const [initiator, setInitiator] = useState('RESEARCH_AGENT');
    const [respondent, setRespondent] = useState('OPERATIONS_AGENT');
    const [topic] = useState('GPU Compute Allocation: Distillation vs Ingestion');
    const [resource, setResource] = useState('GPU_SLOTS');
    const [units, setUnits] = useState(16.0);
    const [rationale, setRationale] = useState('Urgent 4-bit model distillation experiments require temporary dedicated cluster burst.');
    const loadNegotiations = async () => {
        try {
            setLoading(true);
            const data = await organizationPlatformApiClient.getNegotiations();
            setNegotiations(data);
            if (data.length > 0 && !selectedNeg) {
                setSelectedNeg(data[0] || null);
            }
        }
        catch (err) {
            console.error('Failed to load negotiations:', err);
        }
        finally {
            setLoading(false);
        }
    };
    useEffect(() => {
        loadNegotiations();
    }, []);
    const handleStartNegotiation = async (e) => {
        e.preventDefault();
        try {
            setNegotiating(true);
            const res = await organizationPlatformApiClient.initiateNegotiation(initiator, respondent, topic, resource, units, rationale);
            await loadNegotiations();
            setSelectedNeg(res.negotiation);
        }
        catch (err) {
            console.error('Error in agent negotiation:', err);
        }
        finally {
            setNegotiating(false);
        }
    };
    return (_jsxs("div", { className: "space-y-6 p-6", children: [_jsxs("div", { className: "flex flex-col md:flex-row items-start md:items-center justify-between gap-4 border-b border-border pb-4", children: [_jsxs("div", { className: "flex items-center gap-3", children: [_jsx("div", { className: "p-2 bg-primary/10 rounded-lg text-primary", children: _jsx(Scale, { className: "w-6 h-6" }) }), _jsxs("div", { children: [_jsx("h1", { className: "text-2xl font-bold tracking-tight", children: "Multi-Agent Negotiation Arena" }), _jsx("p", { className: "text-sm text-muted-foreground", children: "Game-Theoretic Dispute Resolution, Concession Bargaining & Automated Nash Equilibrium Settlements" })] })] }), _jsx(Button, { variant: "outline", onClick: loadNegotiations, disabled: loading, children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(RotateCw, { className: `w-4 h-4 ${loading ? 'animate-spin' : ''}` }), "Refresh"] }) })] }), _jsxs(Card, { className: "border-border shadow-sm", children: [_jsx(CardHeader, { children: _jsxs(CardTitle, { className: "text-base flex items-center gap-2", children: [_jsx(Scale, { className: "w-4 h-4 text-primary" }), "Initiate Inter-Agent Resource Dispute & Bargaining"] }) }), _jsx(CardContent, { children: _jsxs("form", { onSubmit: handleStartNegotiation, className: "space-y-3", children: [_jsxs("div", { className: "grid grid-cols-1 md:grid-cols-4 gap-3", children: [_jsxs("div", { children: [_jsx("label", { className: "text-xs text-muted-foreground", children: "Initiating Agent" }), _jsxs("select", { value: initiator, onChange: (e) => setInitiator(e.target.value), className: "w-full mt-1 px-3 py-1.5 text-xs rounded border border-input bg-background", children: [_jsx("option", { value: "RESEARCH_AGENT", children: "RESEARCH_AGENT" }), _jsx("option", { value: "ENGINEERING_AGENT", children: "ENGINEERING_AGENT" }), _jsx("option", { value: "ANALYST_AGENT", children: "ANALYST_AGENT" })] })] }), _jsxs("div", { children: [_jsx("label", { className: "text-xs text-muted-foreground", children: "Responding Agent" }), _jsxs("select", { value: respondent, onChange: (e) => setRespondent(e.target.value), className: "w-full mt-1 px-3 py-1.5 text-xs rounded border border-input bg-background", children: [_jsx("option", { value: "OPERATIONS_AGENT", children: "OPERATIONS_AGENT" }), _jsx("option", { value: "FINANCE_AGENT", children: "FINANCE_AGENT" }), _jsx("option", { value: "CTO_AGENT", children: "CTO_AGENT" })] })] }), _jsxs("div", { children: [_jsx("label", { className: "text-xs text-muted-foreground", children: "Resource Type" }), _jsx("input", { type: "text", value: resource, onChange: (e) => setResource(e.target.value), className: "w-full mt-1 px-3 py-1.5 text-xs rounded border border-input bg-background" })] }), _jsxs("div", { children: [_jsx("label", { className: "text-xs text-muted-foreground", children: "Requested Units" }), _jsx("input", { type: "number", value: units, onChange: (e) => setUnits(Number(e.target.value)), className: "w-full mt-1 px-3 py-1.5 text-xs rounded border border-input bg-background" })] })] }), _jsxs("div", { children: [_jsx("label", { className: "text-xs text-muted-foreground", children: "Demand Rationale" }), _jsx("input", { type: "text", value: rationale, onChange: (e) => setRationale(e.target.value), className: "w-full mt-1 px-3 py-1.5 text-xs rounded border border-input bg-background" })] }), _jsx("div", { className: "flex justify-end pt-1", children: _jsx(Button, { type: "submit", variant: "intelligence", disabled: negotiating, children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(Sparkles, { className: "w-4 h-4" }), negotiating ? 'Solving Nash Equilibrium...' : 'Simulate & Solve Bargaining Session'] }) }) })] }) })] }), _jsxs("div", { className: "grid grid-cols-1 lg:grid-cols-3 gap-6", children: [_jsxs("div", { className: "space-y-4", children: [_jsxs("h2", { className: "text-sm font-semibold", children: ["Negotiation Logs (", negotiations.length, ")"] }), _jsx("div", { className: "space-y-3", children: negotiations.map((n) => (_jsx(Card, { onClick: () => setSelectedNeg(n), className: `border cursor-pointer transition-all ${selectedNeg?.negotiation_id === n.negotiation_id
                                        ? 'border-primary bg-primary/5 shadow-sm'
                                        : 'border-border hover:bg-muted/30'}`, children: _jsxs(CardContent, { className: "p-4 space-y-2", children: [_jsxs("div", { className: "flex justify-between items-start", children: [_jsx("span", { className: "font-semibold text-sm line-clamp-1", children: n.topic }), _jsx(Badge, { variant: n.status === 'RESOLVED' ? 'success' : 'warning', children: n.status })] }), _jsxs("div", { className: "flex items-center gap-2 text-xs text-muted-foreground", children: [_jsx(Badge, { variant: "outline", children: n.initiating_role }), _jsx(ArrowRight, { className: "w-3 h-3" }), _jsx(Badge, { variant: "outline", children: n.responding_role })] })] }) }, n.negotiation_id))) })] }), _jsx("div", { className: "lg:col-span-2 space-y-6", children: selectedNeg ? (_jsxs(Card, { className: "border-border shadow-sm", children: [_jsxs(CardHeader, { className: "flex flex-row items-center justify-between pb-3", children: [_jsxs("div", { children: [_jsx(CardTitle, { className: "text-lg", children: selectedNeg.topic }), _jsx("p", { className: "text-xs text-muted-foreground font-mono mt-0.5", children: selectedNeg.negotiation_id })] }), _jsx(Badge, { variant: selectedNeg.status === 'RESOLVED' ? 'success' : 'warning', children: selectedNeg.status })] }), _jsxs(CardContent, { className: "space-y-4", children: [_jsxs("div", { className: "space-y-3", children: [_jsxs("div", { className: "p-3 bg-primary/5 border border-primary/20 rounded-lg text-xs space-y-1", children: [_jsxs("div", { className: "flex justify-between font-semibold text-primary", children: [_jsxs("span", { children: ["Initial Proposal: ", selectedNeg.initiating_role] }), _jsxs("span", { children: ["Demand: ", selectedNeg.proposals[0]?.requested_units, " units"] })] }), _jsx("p", { className: "text-muted-foreground", children: selectedNeg.proposals[0]?.rationale })] }), selectedNeg.counter_proposals.map((cp) => (_jsxs("div", { className: "p-3 bg-muted/40 border border-border rounded-lg text-xs space-y-1", children: [_jsxs("div", { className: "flex justify-between font-semibold text-foreground", children: [_jsxs("span", { children: ["Counter Offer: ", cp.responding_role] }), _jsxs("span", { children: ["Offered: ", cp.offered_units, " units"] })] }), _jsx("ul", { className: "list-disc pl-4 text-muted-foreground space-y-0.5", children: cp.compromise_conditions.map((c, i) => (_jsx("li", { children: c }, i))) })] }, cp.counter_id)))] }), selectedNeg.agreement && (_jsxs("div", { className: "p-4 bg-emerald-500/10 border border-emerald-500/30 rounded-lg space-y-2", children: [_jsxs("div", { className: "flex justify-between items-center", children: [_jsxs("span", { className: "font-semibold text-sm text-emerald-500 flex items-center gap-1.5", children: [_jsx(CheckCircle2, { className: "w-4 h-4" }), " Nash Bargaining Equilibrium Settlement"] }), _jsxs(Badge, { variant: "success", children: ["Nash Score: ", (selectedNeg.agreement.nash_product_score * 100).toFixed(0), "%"] })] }), _jsx("p", { className: "text-xs text-foreground font-medium", children: selectedNeg.agreement.compromise_summary }), _jsxs("div", { className: "text-xs text-muted-foreground pt-1 border-t border-emerald-500/20", children: ["Settled Allocation: ", _jsxs("strong", { className: "text-foreground", children: [selectedNeg.agreement.settled_units, " units"] }), " (Pareto Optimal)"] })] }))] })] })) : (_jsx(Card, { className: "border-border shadow-sm p-8 text-center text-muted-foreground", children: "Select a negotiation log to inspect proposal rounds and Nash agreements." })) })] })] }));
};
