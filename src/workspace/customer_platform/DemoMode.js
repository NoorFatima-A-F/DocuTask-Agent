import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
export const DemoMode = () => {
    const [isRunning, setIsRunning] = useState(false);
    const [currentStage, setCurrentStage] = useState(0);
    const stages = [
        { title: '1. Ingestion & Security Pre-flight', agent: 'SecurityGuardAgent', desc: 'Validated TLS, checked PDF macro safety, verified tenant KMS key.' },
        { title: '2. Multimodal OCR & Layout Extraction', agent: 'MultimodalOCRAgent', desc: 'Parsed 8 table rows and header metadata with 0.998 character fidelity.' },
        { title: '3. LLM Reasoning & Grounding', agent: 'ReasoningExtractionAgent', desc: 'Extracted canonical schema: Acme Solutions, Total: $14,500.50 (99.4% faithfulness).' },
        { title: '4. 3-Way PO Matching Verification', agent: 'PolicyVerificationAgent', desc: 'Matched line items against NetSuite PO #PO-9912. 0 discrepancies.' },
        { title: '5. Fast-Track Human Approval', agent: 'SupervisionCoordinator', desc: 'Confidence > 95% threshold met. Emitted signed audit event.' },
        { title: '6. QuickBooks & Slack Dispatch', agent: 'EnterpriseConnectorAgent', desc: 'Posted Vendor Bill #QB-99812 to General Ledger and notified #finance-ops.' },
    ];
    const handleRunDemo = () => {
        setIsRunning(true);
        setCurrentStage(1);
        const interval = setInterval(() => {
            setCurrentStage((prev) => {
                if (prev >= stages.length) {
                    clearInterval(interval);
                    setIsRunning(false);
                    return stages.length;
                }
                return prev + 1;
            });
        }, 600);
    };
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center justify-between gap-4 p-6 rounded-2xl bg-gradient-to-r from-[#0F172A] to-[#1E293B] border border-[#334155]/60 shadow-xl", children: [_jsxs("div", { children: [_jsx(Badge, { variant: "intelligence", size: "sm", children: "1-CLICK LIVE DEMONSTRATION" }), _jsx("h1", { className: "text-2xl font-black text-white mt-1", children: "Interactive Enterprise Automation Player" }), _jsx("p", { className: "text-sm text-[#94A3B8]", children: "Simulate an end-to-end multi-agent document lifecycle in real-time." })] }), _jsx(Button, { variant: "primary", size: "lg", onClick: handleRunDemo, disabled: isRunning, className: "bg-gradient-to-r from-[#0066FF] to-[#00D2FF] text-white shadow-lg shadow-[#00D2FF]/20", children: isRunning ? 'Processing Multi-Agent Flow...' : '▶ Run Invoice Automation Demo' })] }), _jsx("div", { className: "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4", children: stages.map((st, idx) => {
                    const isPassed = currentStage > idx;
                    const isCurrent = currentStage === idx + 1;
                    return (_jsxs("div", { className: `p-5 rounded-2xl border transition-all space-y-2.5 ${isCurrent
                            ? 'bg-[#0066FF]/20 border-[#00D2FF] shadow-[0_0_20px_rgba(0,210,255,0.4)] scale-102'
                            : isPassed
                                ? 'bg-[#0F172A]/80 border-emerald-500/50'
                                : 'bg-[#0A0F1D]/60 border-[#1E293B] opacity-50'}`, children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsx(Badge, { variant: "default", size: "sm", children: st.agent }), isPassed && _jsx("span", { className: "text-emerald-400 text-xs font-bold", children: "\u2713 DONE" }), isCurrent && _jsx("span", { className: "text-cyan-400 text-xs font-bold animate-pulse", children: "\u25CF RUNNING" })] }), _jsx("h3", { className: "text-xs font-bold text-white", children: st.title }), _jsx("p", { className: "text-[11px] text-[#94A3B8] leading-relaxed", children: st.desc })] }, idx));
                }) }), currentStage === stages.length && (_jsxs("div", { className: "p-6 rounded-2xl bg-gradient-to-r from-emerald-950/40 to-[#0F172A] border border-emerald-500/50 shadow-2xl flex flex-col sm:flex-row items-center justify-between gap-4", children: [_jsxs("div", { className: "space-y-1", children: [_jsx("span", { className: "text-xs font-bold text-emerald-400 font-mono", children: "AUTOMATION COMPLETED IN 285ms" }), _jsx("h2", { className: "text-lg font-black text-white", children: "Invoice INV-2026-8891 Cleared & Posted to QuickBooks" }), _jsx("p", { className: "text-xs text-[#CBD5E1]", children: "Saved $34.975 vs manual processing. 0 human touches required. 100% cryptographic audit trail generated." })] }), _jsx(Button, { variant: "secondary", size: "md", onClick: () => setCurrentStage(0), children: "Reset Simulation" })] }))] }));
};
