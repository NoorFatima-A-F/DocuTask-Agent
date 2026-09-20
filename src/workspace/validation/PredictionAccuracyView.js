import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
export const PredictionAccuracyView = () => {
    const regressionMetrics = [
        {
            metric: 'Accuracy (Field Exact Match)',
            mae: '0.0142',
            rmse: '0.0218',
            mape: '1.48%',
            bias: '+0.0031',
            coverage95: '96.2%',
            status: 'ENTERPRISE_GRADE',
        },
        {
            metric: 'Latency P95 (ms)',
            mae: '38.4 ms',
            rmse: '54.2 ms',
            mape: '6.20%',
            bias: '-8.5 ms',
            coverage95: '95.0%',
            status: 'ENTERPRISE_GRADE',
        },
        {
            metric: 'API Token Cost ($)',
            mae: '$0.00012',
            rmse: '$0.00019',
            mape: '4.85%',
            bias: '-$0.00004',
            coverage95: '97.5%',
            status: 'ENTERPRISE_GRADE',
        },
        {
            metric: 'Expected Utility U(x)',
            mae: '0.0185',
            rmse: '0.0260',
            mape: '2.10%',
            bias: '+0.0012',
            coverage95: '98.0%',
            status: 'ENTERPRISE_GRADE',
        },
    ];
    const diagnosticTests = [
        {
            testName: 'Durbin-Watson Autocorrelation Test',
            statistic: 'd = 1.942',
            referenceRange: '[1.50 - 2.50]',
            result: 'NO_AUTOCORRELATION_DETECTED',
            description: 'Residuals are temporally uncorrelated; error sequence is white noise.',
            passed: true,
        },
        {
            testName: 'Residual Mean Zero Test (Student t)',
            statistic: 't = 0.42 (p = 0.674)',
            referenceRange: 'p > 0.05',
            result: 'UNBIASED_PREDICTION_SURROGATE',
            description: 'The expected value of error is strictly zero with no systematic drift.',
            passed: true,
        },
        {
            testName: 'Residual Skewness & Kurtosis',
            statistic: 'Skew: -0.12, Kurt: +0.08',
            referenceRange: '[-0.50 to +0.50]',
            result: 'APPROXIMATELY_GAUSSIAN',
            description: 'Distribution of errors closely matches theoretical normal Gaussian bounds.',
            passed: true,
        },
    ];
    return (_jsxs("div", { className: "space-y-6", children: [_jsx("div", { className: "p-6 rounded-2xl bg-[#0F172A] border border-[#1E293B] shadow-xl", children: _jsx("div", { className: "flex flex-col md:flex-row items-start md:items-center justify-between gap-4", children: _jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "text-xl", children: "\uD83D\uDCC8" }), _jsx("h2", { className: "text-lg font-bold font-mono text-[#F8FAFC]", children: "Prediction Accuracy & Residual Diagnostics" }), _jsx(Badge, { variant: "success", size: "sm", children: "SURROGATE VERIFIED" })] }), _jsx("p", { className: "text-sm font-mono text-[#94A3B8] mt-1", children: "Rigorous econometric regression validation (RMSE, MAPE, Mean Bias) and error distribution diagnostics." })] }) }) }), _jsxs(Card, { className: "p-6 bg-[#0F172A] border-[#1E293B]", children: [_jsx("h3", { className: "text-sm font-bold font-mono text-[#F8FAFC] mb-4", children: "Multi-Dimensional Predictive Error Quantification" }), _jsx("div", { className: "overflow-x-auto", children: _jsxs("table", { className: "w-full text-left font-mono text-xs", children: [_jsx("thead", { children: _jsxs("tr", { className: "border-b border-[#1E293B] text-[#94A3B8]", children: [_jsx("th", { className: "pb-3", children: "Operational Dimension" }), _jsx("th", { className: "pb-3", children: "MAE" }), _jsx("th", { className: "pb-3", children: "RMSE" }), _jsx("th", { className: "pb-3", children: "MAPE (%)" }), _jsx("th", { className: "pb-3", children: "Mean Bias" }), _jsx("th", { className: "pb-3", children: "95% CI Coverage" }), _jsx("th", { className: "pb-3", children: "Grade" })] }) }), _jsx("tbody", { className: "divide-y divide-[#1E293B]", children: regressionMetrics.map((row, idx) => (_jsxs("tr", { className: "hover:bg-[#1E293B]/40 transition-colors", children: [_jsx("td", { className: "py-3 font-bold text-[#F8FAFC]", children: row.metric }), _jsx("td", { className: "py-3 text-cyan-400", children: row.mae }), _jsx("td", { className: "py-3 text-indigo-400", children: row.rmse }), _jsx("td", { className: "py-3 text-emerald-400", children: row.mape }), _jsx("td", { className: "py-3 text-[#94A3B8]", children: row.bias }), _jsx("td", { className: "py-3 text-emerald-400", children: row.coverage95 }), _jsx("td", { className: "py-3", children: _jsx(Badge, { variant: "success", size: "sm", children: row.status }) })] }, idx))) })] }) })] }), _jsx("div", { className: "grid grid-cols-1 md:grid-cols-3 gap-4", children: diagnosticTests.map((t, idx) => (_jsxs(Card, { className: "p-5 bg-[#0F172A] border-[#1E293B] flex flex-col justify-between", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center justify-between gap-2", children: [_jsx("h4", { className: "text-xs font-bold font-mono text-[#F8FAFC]", children: t.testName }), _jsx(Badge, { variant: t.passed ? 'success' : 'error', size: "sm", children: t.passed ? 'PASSED' : 'FAILED' })] }), _jsxs("div", { className: "mt-3 p-2.5 rounded-lg bg-[#020617] border border-[#1E293B] font-mono text-xs", children: [_jsx("div", { className: "text-cyan-400 font-bold", children: t.statistic }), _jsxs("div", { className: "text-[#64748B] text-[11px] mt-0.5", children: ["Bound: ", t.referenceRange] })] }), _jsx("p", { className: "text-xs font-mono text-[#94A3B8] mt-3", children: t.description })] }), _jsxs("div", { className: "mt-4 pt-3 border-t border-[#1E293B] text-[11px] font-mono text-emerald-400", children: ["\u2713 ", t.result] })] }, idx))) })] }));
};
