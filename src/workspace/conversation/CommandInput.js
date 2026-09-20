import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Button } from '../../components/ui/Button';
export const CommandInput = ({ onSendCommand, placeholder = 'Type natural language instruction (e.g. "Improve invoice extraction on thermal scans")...', disabled = false, }) => {
    const [input, setInput] = useState('');
    const handleSubmit = (e) => {
        e.preventDefault();
        if (!input.trim() || disabled)
            return;
        onSendCommand(input.trim());
        setInput('');
    };
    const handleKeyDown = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSubmit(e);
        }
    };
    return (_jsx("form", { onSubmit: handleSubmit, className: "relative w-full", children: _jsxs("div", { className: "relative rounded-2xl bg-[#0F172A] border border-cyan-500/30 p-2 shadow-[0_0_25px_rgba(0,102,255,0.15)] focus-within:border-cyan-400 focus-within:shadow-[0_0_25px_rgba(0,210,255,0.3)] transition-all", children: [_jsx("textarea", { value: input, onChange: (e) => setInput(e.target.value), onKeyDown: handleKeyDown, placeholder: placeholder, disabled: disabled, rows: 2, className: "w-full bg-transparent px-3 py-2 text-xs lg:text-sm text-[#F8FAFC] placeholder-[#64748B] focus:outline-none resize-none font-mono" }), _jsxs("div", { className: "flex items-center justify-between pt-2 px-3 border-t border-[#1E293B]", children: [_jsx("div", { className: "flex items-center gap-2 text-[11px] font-mono text-[#64748B]", children: _jsx("span", { children: "Shift + Enter for new line \u2022 Enter to dispatch" }) }), _jsx(Button, { type: "submit", variant: "intelligence", size: "sm", disabled: !input.trim() || disabled, children: "Dispatch Instruction \u2794" })] })] }) }));
};
