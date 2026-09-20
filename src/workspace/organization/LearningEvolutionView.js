import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
export const LearningEvolutionView = () => {
    const knowledgeItems = [
        {
            dept: 'Optical Perception (dept_ocr)',
            category: 'HEURISTIC',
            title: 'Bilateral Filtering for Thermal Receipts',
            content: 'Apply bilateral filter with diameter 9 and sigmaColor 75 when document luminance variance is < 12.0.',
            gain: '+3.8% Accuracy Boost',
            confidence: '96.0%',
        },
        {
            dept: 'Structured Extraction (dept_extraction)',
            category: 'PROMPT_TEMPLATE',
            title: 'European VAT Multi-Rate Extraction Anchor',
            content: 'Explicitly prompt Gemini 2.5 Flash with table line-item VAT rate mapping when vendor country is EU.',
            gain: '+4.5% Accuracy Boost',
            confidence: '98.0%',
        },
        {
            dept: 'Mathematical Validation (dept_validation)',
            category: 'SCHEMA_RULE',
            title: 'Dynamic Currency Symbol Normalization',
            content: 'Strip non-breaking currency whitespace characters prior to decimal invariant arithmetic evaluation.',
            gain: '+1.2% Accuracy Boost',
            confidence: '99.0%',
        },
    ];
    const retrospectives = [
        {
            dept: 'Optical Perception',
            score: '0.94',
            gain: '+4.2% projected speedup',
            bottleneck: 'Multi-column skewed tables caused 15ms latency tail in LayoutLM bounding box assignment.',
            action: 'Synthesize pre-rotation OpenCV affine transform before LayoutLM tokenization.',
        },
        {
            dept: 'Structured Extraction',
            score: '0.96',
            gain: '+6.5% projected speedup',
            bottleneck: 'Nested invoice line-item sub-tables required single retry due to trailing semicolon.',
            action: 'Update extraction prompt with explicit JSON schema regex validator.',
        },
    ];
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col md:flex-row items-start md:items-center justify-between gap-4 p-5 rounded-2xl bg-[#0F172A] border border-[#1E293B] shadow-xl", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "text-2xl", children: "\uD83E\uDDE0" }), _jsx("h2", { className: "text-xl font-bold text-[#F8FAFC]", children: "Organizational Learning & Cognitive Evolution" }), _jsx(Badge, { variant: "intelligence", size: "sm", children: "Self-Improving Enterprise" })] }), _jsx("p", { className: "text-sm text-[#94A3B8] mt-1", children: "Independent departmental retrospectives, procedural memory accumulation, and organization-wide policy synthesis." })] }), _jsxs("div", { className: "text-right", children: [_jsx("div", { className: "text-xs text-[#94A3B8]", children: "Cumulative Accuracy Gain" }), _jsx("div", { className: "text-2xl font-bold font-mono text-[#10B981]", children: "+9.5% Macro Boost" })] })] }), _jsxs(Card, { className: "p-5 bg-[#0F172A] border-[#1E293B] space-y-4", children: [_jsx("div", { className: "text-sm font-bold text-[#F8FAFC]", children: "Active Department Procedural Memories" }), _jsx("div", { className: "space-y-3", children: knowledgeItems.map((item, idx) => (_jsxs("div", { className: "p-4 rounded-xl bg-[#020617] border border-[#1E293B] space-y-2", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "text-xs font-bold font-mono text-[#38BDF8]", children: item.dept }), _jsx(Badge, { variant: "intelligence", size: "sm", children: item.category })] }), _jsxs("div", { className: "flex items-center gap-2", children: [_jsx(Badge, { variant: "success", size: "sm", children: item.gain }), _jsxs("span", { className: "text-xs font-mono text-[#64748B]", children: ["Conf: ", item.confidence] })] })] }), _jsx("div", { className: "text-sm font-semibold text-[#F8FAFC]", children: item.title }), _jsx("p", { className: "text-xs text-[#94A3B8] font-mono", children: item.content })] }, idx))) })] }), _jsxs(Card, { className: "p-5 bg-[#0F172A] border-[#1E293B] space-y-4", children: [_jsx("div", { className: "text-sm font-bold text-[#F8FAFC]", children: "Recent Post-Mission Departmental Retrospectives" }), _jsx("div", { className: "grid grid-cols-1 md:grid-cols-2 gap-4", children: retrospectives.map((r, idx) => (_jsxs("div", { className: "p-4 rounded-xl bg-[#020617] border border-[#1E293B] space-y-2 text-xs font-mono", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsx("span", { className: "font-bold text-[#F8FAFC]", children: r.dept }), _jsx("span", { className: "text-[#10B981]", children: r.gain })] }), _jsxs("div", { className: "text-[#EF4444] pt-1", children: [_jsx("span", { className: "text-[#64748B] block text-[10px]", children: "IDENTIFIED BOTTLENECK:" }), r.bottleneck] }), _jsxs("div", { className: "text-[#00D2FF] pt-1", children: [_jsx("span", { className: "text-[#64748B] block text-[10px]", children: "SYNTHESIZED ACTION:" }), r.action] })] }, idx))) })] })] }));
};
