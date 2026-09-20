import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
export const ManagerConsole = () => {
    const [reviews, setReviews] = useState([]);
    useEffect(() => {
        // Seed default review display
        setReviews([
            {
                id: 'rev-q1-doc-spec',
                tenant_id: 'default-tenant',
                employee_id: 'emp-doc-spec-01',
                manager_id: 'emp-eng-vp',
                review_period: '2026-Q1',
                performance_rating: 4.9,
                strengths: ['Zero error rate in table extraction', 'High reuse of experience memory'],
                areas_for_growth: ['Can mentor junior parser agents'],
                workload_balance_action: 'OPTIMAL',
                promotion_recommended: true,
                created_at: new Date().toISOString()
            }
        ]);
    }, []);
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "bg-slate-900/60 p-5 rounded-2xl border border-slate-800", children: [_jsxs("h1", { className: "text-2xl font-bold text-white flex items-center gap-3", children: [_jsx("span", { className: "p-2 bg-blue-500/20 text-blue-400 rounded-xl", children: "\uD83D\uDC54" }), "Manager Console & Review Studio"] }), _jsx("p", { className: "text-slate-400 text-sm mt-1", children: "Departmental Coaching, Workload Leveling, and Performance Appraisals" })] }), _jsx("div", { className: "grid grid-cols-1 md:grid-cols-2 gap-6", children: reviews.map((r) => (_jsxs(Card, { className: "p-5 bg-slate-900/50 border-slate-800", children: [_jsxs("div", { className: "flex justify-between items-start mb-3", children: [_jsxs("div", { children: [_jsxs("div", { className: "text-base font-bold text-white", children: ["Employee: ", r.employee_id] }), _jsxs("div", { className: "text-xs text-slate-400", children: ["Manager: ", r.manager_id, " \u2022 Period: ", r.review_period] })] }), _jsxs(Badge, { variant: "default", children: ["Rating: ", r.performance_rating, " / 5.0"] })] }), _jsxs("div", { className: "space-y-3 my-4 text-xs", children: [_jsxs("div", { children: [_jsx("div", { className: "font-semibold text-emerald-400 mb-1", children: "Key Strengths:" }), _jsx("ul", { className: "list-disc list-inside text-slate-300 space-y-0.5", children: r.strengths.map((s, idx) => _jsx("li", { children: s }, idx)) })] }), _jsxs("div", { children: [_jsx("div", { className: "font-semibold text-amber-400 mb-1", children: "Growth Opportunities:" }), _jsx("ul", { className: "list-disc list-inside text-slate-300 space-y-0.5", children: r.areas_for_growth.map((g, idx) => _jsx("li", { children: g }, idx)) })] })] }), _jsxs("div", { className: "border-t border-slate-800 pt-3 flex justify-between items-center text-xs", children: [_jsxs("span", { className: "text-slate-400", children: ["Action: ", _jsx("strong", { className: "text-white", children: r.workload_balance_action })] }), r.promotion_recommended && (_jsx(Badge, { variant: "default", children: "\u2605 Promotion Recommended" }))] })] }, r.id))) })] }));
};
