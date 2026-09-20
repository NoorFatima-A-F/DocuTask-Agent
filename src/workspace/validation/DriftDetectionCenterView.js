import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
export const DriftDetectionCenterView = () => {
    const monitoredFeatures = [
        {
            featureName: 'Latency Distribution (ms)',
            psi: 0.042,
            klDivergence: 0.018,
            wasserstein: 14.5,
            sequentialAlarm: 'NO_ALARM',
            status: 'NEGLIGIBLE_DRIFT',
            mitigation: 'Distribution stable. No recalibration needed.',
        },
        {
            featureName: 'Extraction Accuracy (Exact Match)',
            psi: 0.028,
            klDivergence: 0.011,
            wasserstein: 0.008,
            sequentialAlarm: 'NO_ALARM',
            status: 'NEGLIGIBLE_DRIFT',
            mitigation: 'Ground-truth accuracy remains calibrated.',
        },
        {
            featureName: 'Document OCR Noise Level',
            psi: 0.142,
            klDivergence: 0.089,
            wasserstein: 0.045,
            sequentialAlarm: 'WARNING_ADWIN',
            status: 'DRIFT_WARNING',
            mitigation: 'Increase shadow sampling rate; monitor residual autocorrelation.',
        },
        {
            featureName: 'API Token Consumption',
            psi: 0.065,
            klDivergence: 0.032,
            wasserstein: 22.0,
            sequentialAlarm: 'NO_ALARM',
            status: 'NEGLIGIBLE_DRIFT',
            mitigation: 'Token budget within ±5% bounds.',
        },
    ];
    return (_jsxs("div", { className: "space-y-6", children: [_jsx("div", { className: "p-6 rounded-2xl bg-[#0F172A] border border-[#1E293B] shadow-xl", children: _jsx("div", { className: "flex flex-col md:flex-row items-start md:items-center justify-between gap-4", children: _jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "text-xl", children: "\uD83C\uDF0A" }), _jsx("h2", { className: "text-lg font-bold font-mono text-[#F8FAFC]", children: "Online Statistical Drift Detection Center" }), _jsx(Badge, { variant: "success", size: "sm", children: "ADWIN & PSI ACTIVE" })] }), _jsx("p", { className: "text-sm font-mono text-[#94A3B8] mt-1", children: "Streaming distribution divergence tracking (PSI, KL, Wasserstein) and sequential change-point alarms (ADWIN, CUSUM)." })] }) }) }), _jsxs(Card, { className: "p-6 bg-[#0F172A] border-[#1E293B]", children: [_jsx("h3", { className: "text-sm font-bold font-mono text-[#F8FAFC] mb-4", children: "Feature Distribution Divergence & Sequential Alarms" }), _jsx("div", { className: "overflow-x-auto", children: _jsxs("table", { className: "w-full text-left font-mono text-xs", children: [_jsx("thead", { children: _jsxs("tr", { className: "border-b border-[#1E293B] text-[#94A3B8]", children: [_jsx("th", { className: "pb-3", children: "Monitored Feature" }), _jsx("th", { className: "pb-3", children: "PSI (Pop. Stability)" }), _jsx("th", { className: "pb-3", children: "KL Divergence" }), _jsx("th", { className: "pb-3", children: "Wasserstein (EMD)" }), _jsx("th", { className: "pb-3", children: "Sequential Alarm" }), _jsx("th", { className: "pb-3", children: "Severity" }), _jsx("th", { className: "pb-3", children: "Prescribed Mitigation" })] }) }), _jsx("tbody", { className: "divide-y divide-[#1E293B]", children: monitoredFeatures.map((m, idx) => (_jsxs("tr", { className: "hover:bg-[#1E293B]/40 transition-colors", children: [_jsx("td", { className: "py-3 font-bold text-[#F8FAFC]", children: m.featureName }), _jsxs("td", { className: "py-3", children: [_jsx("span", { className: m.psi < 0.1 ? 'text-emerald-400' : 'text-amber-400 font-bold', children: m.psi.toFixed(3) }), _jsx("span", { className: "text-[#64748B] text-[10px] ml-1", children: "(<0.10)" })] }), _jsx("td", { className: "py-3 text-cyan-400", children: m.klDivergence.toFixed(3) }), _jsx("td", { className: "py-3 text-indigo-400", children: m.wasserstein.toFixed(2) }), _jsx("td", { className: "py-3", children: _jsx(Badge, { variant: m.sequentialAlarm === 'NO_ALARM' ? 'default' : 'warning', size: "sm", children: m.sequentialAlarm }) }), _jsx("td", { className: "py-3", children: _jsx(Badge, { variant: m.status === 'NEGLIGIBLE_DRIFT' ? 'success' : 'warning', size: "sm", children: m.status }) }), _jsx("td", { className: "py-3 text-[#94A3B8] text-[11px]", children: m.mitigation })] }, idx))) })] }) })] })] }));
};
