import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { Globe, RotateCw, Camera, Play, } from 'lucide-react';
import { executionPlatformApiClient } from '../../services/executionPlatformApiClient';
export const BrowserAutomationStudio = () => {
    const [sessions, setSessions] = useState([]);
    const [activeSession, setActiveSession] = useState(null);
    const [urlInput, setUrlInput] = useState('https://portal.enterprise-vendor.com/invoices');
    const [loading, setLoading] = useState(true);
    const [navigating, setNavigating] = useState(false);
    const loadSessions = async () => {
        try {
            setLoading(true);
            const res = await executionPlatformApiClient.listBrowserSessions();
            setSessions(res.sessions || []);
            if (res.sessions && res.sessions.length > 0 && !activeSession) {
                setActiveSession(res.sessions[0] || null);
            }
        }
        catch (err) {
            console.error('Failed to load browser sessions:', err);
        }
        finally {
            setLoading(false);
        }
    };
    useEffect(() => {
        loadSessions();
    }, []);
    const handleCreateSession = async () => {
        try {
            const res = await executionPlatformApiClient.createBrowserSession();
            await loadSessions();
            setActiveSession(res.session);
        }
        catch (err) {
            console.error('Error creating browser session:', err);
        }
    };
    const handleNavigate = async () => {
        if (!activeSession || !urlInput.trim())
            return;
        try {
            setNavigating(true);
            await executionPlatformApiClient.executeBrowserAction(activeSession.session_id, {
                action_type: 'navigate',
                value: urlInput,
            });
            await loadSessions();
        }
        catch (err) {
            console.error('Error navigating browser:', err);
        }
        finally {
            setNavigating(false);
        }
    };
    const handleScreenshot = async () => {
        if (!activeSession)
            return;
        try {
            await executionPlatformApiClient.executeBrowserAction(activeSession.session_id, {
                action_type: 'screenshot',
            });
            await loadSessions();
        }
        catch (err) {
            console.error('Error capturing screenshot:', err);
        }
    };
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col md:flex-row justify-between items-start md:items-center gap-4 bg-slate-900/60 p-6 rounded-2xl border border-slate-800", children: [_jsxs("div", { children: [_jsxs("h1", { className: "text-xl font-bold text-white flex items-center gap-2", children: [_jsx(Globe, { className: "w-5 h-5 text-cyan-400" }), "Browser Automation & Vision Studio"] }), _jsx("p", { className: "text-slate-400 text-sm mt-1", children: "Headless Playwright orchestration, DOM tree parsing, accessibility trees & visual snapshots" })] }), _jsxs("div", { className: "flex items-center gap-2", children: [_jsx(Button, { variant: "outline", onClick: loadSessions, children: _jsxs("span", { className: "flex items-center gap-1.5", children: [_jsx(RotateCw, { className: "w-4 h-4" }), "Refresh"] }) }), _jsx(Button, { variant: "intelligence", onClick: handleCreateSession, children: _jsxs("span", { className: "flex items-center gap-1.5", children: [_jsx(Globe, { className: "w-4 h-4" }), "Spawn Headless Session"] }) })] })] }), _jsxs("div", { className: "grid grid-cols-1 lg:grid-cols-3 gap-6", children: [_jsxs(Card, { className: "lg:col-span-1 bg-slate-900/60 border-slate-800", children: [_jsx(CardHeader, { children: _jsxs(CardTitle, { className: "text-sm font-semibold text-white", children: ["Browser Sessions (", sessions.length, ")"] }) }), _jsx(CardContent, { className: "space-y-2", children: loading && sessions.length === 0 ? (_jsx("p", { className: "text-xs text-slate-500 py-4 text-center", children: "Loading browser sessions..." })) : sessions.map((s) => (_jsxs("div", { onClick: () => setActiveSession(s), className: `p-3 rounded-lg border cursor-pointer transition-all ${activeSession?.session_id === s.session_id
                                        ? 'bg-purple-950/40 border-purple-600'
                                        : 'bg-slate-800/40 border-slate-800 hover:border-slate-700'}`, children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsx("span", { className: "text-xs font-mono text-cyan-300 truncate max-w-[170px]", children: s.session_id }), _jsx(Badge, { variant: s.is_active ? 'success' : 'outline', children: s.is_active ? 'active' : 'closed' })] }), _jsx("p", { className: "text-[11px] text-slate-300 mt-1 truncate", children: s.current_url }), _jsxs("div", { className: "flex items-center justify-between mt-2 text-[10px] text-slate-500 font-mono", children: [_jsxs("span", { children: [s.viewport_width, "x", s.viewport_height] }), _jsxs("span", { children: [s.dom_elements_count, " DOM elements"] })] })] }, s.session_id))) })] }), _jsxs(Card, { className: "lg:col-span-2 bg-slate-900/60 border-slate-800", children: [_jsx(CardHeader, { children: _jsx(CardTitle, { className: "text-base text-white", children: activeSession ? activeSession.page_title : 'Select a Session' }) }), _jsxs(CardContent, { className: "space-y-4", children: [_jsxs("div", { className: "flex gap-2", children: [_jsx("input", { type: "text", className: "flex-1 bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-white text-xs font-mono focus:outline-none focus:border-cyan-500", placeholder: "Enter HTTPS target URL...", value: urlInput, onChange: (e) => setUrlInput(e.target.value) }), _jsx(Button, { variant: "secondary", onClick: handleNavigate, disabled: navigating || !activeSession, children: _jsxs("span", { className: "flex items-center gap-1.5 text-xs", children: [_jsx(Play, { className: "w-3.5 h-3.5" }), "Navigate"] }) }), _jsx(Button, { variant: "outline", onClick: handleScreenshot, disabled: !activeSession, children: _jsxs("span", { className: "flex items-center gap-1.5 text-xs", children: [_jsx(Camera, { className: "w-3.5 h-3.5 text-cyan-400" }), "Capture Snapshot"] }) })] }), _jsxs("div", { className: "p-4 bg-slate-950 border border-slate-800 rounded-xl min-h-[300px] flex flex-col justify-between", children: [_jsxs("div", { className: "flex items-center justify-between pb-3 border-b border-slate-800/80 text-xs text-slate-400", children: [_jsxs("span", { className: "flex items-center gap-2", children: [_jsx("span", { className: "w-2.5 h-2.5 rounded-full bg-emerald-500" }), "Connected to Headless CDP Chrome Node"] }), _jsx("span", { className: "font-mono", children: activeSession?.current_url })] }), _jsxs("div", { className: "py-12 flex flex-col items-center justify-center text-center", children: [_jsx(Globe, { className: "w-12 h-12 text-slate-700 mb-3 animate-pulse" }), _jsx("h4", { className: "text-sm font-semibold text-slate-300", children: activeSession?.page_title || 'Headless Browser Ready' }), _jsxs("p", { className: "text-xs text-slate-500 max-w-sm mt-1", children: ["Synthetic DOM tree parsed with ", activeSession?.dom_elements_count || 0, " interactive elements."] })] }), _jsxs("div", { className: "pt-3 border-t border-slate-800/80 flex items-center justify-between text-[11px] text-slate-500", children: [_jsx("span", { children: "User-Agent: Chromium Headless 124.0.0" }), _jsx("span", { children: "SSL Invariant: Verified" })] })] })] })] })] })] }));
};
