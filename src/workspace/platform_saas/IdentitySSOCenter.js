import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { SaaSApiClient } from '../../services/saasApiClient';
import { KeyRound, ShieldCheck, Users, RefreshCw } from 'lucide-react';
export const IdentitySSOCenter = () => {
    const [ssoList, setSsoList] = useState([]);
    const [users, setUsers] = useState([]);
    const [loading, setLoading] = useState(true);
    useEffect(() => {
        const load = async () => {
            setLoading(true);
            const [sso, u] = await Promise.all([
                SaaSApiClient.listSSOConfigs('tenant_acme_corp'),
                SaaSApiClient.listUsers('tenant_acme_corp'),
            ]);
            setSsoList(sso);
            setUsers(u);
            setLoading(false);
        };
        load();
    }, []);
    return (_jsxs("div", { className: "space-y-6", children: [_jsx("div", { className: "flex items-center justify-between", children: _jsxs("div", { children: [_jsxs("h1", { className: "text-2xl font-bold text-white flex items-center gap-3", children: [_jsx(KeyRound, { className: "w-7 h-7 text-indigo-400" }), "Enterprise Identity & SSO Control"] }), _jsx("p", { className: "text-sm text-slate-400 mt-1", children: "Configure SAML 2.0, OIDC identity federations, SCIM 2.0 user sync, and MFA enforcement." })] }) }), _jsxs("div", { className: "grid grid-cols-1 lg:grid-cols-3 gap-6", children: [_jsxs(Card, { className: "bg-slate-900/80 border-slate-800 lg:col-span-1", children: [_jsx(CardHeader, { children: _jsxs(CardTitle, { className: "text-base text-white flex items-center gap-2", children: [_jsx(ShieldCheck, { className: "w-5 h-5 text-emerald-400" }), " SSO Identity Provider"] }) }), _jsxs(CardContent, { className: "space-y-4", children: [ssoList.map((sso) => (_jsxs("div", { className: "p-4 bg-slate-800/60 rounded border border-slate-700/60 space-y-3", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsx("span", { className: "text-sm font-semibold text-white", children: sso.name }), _jsx(Badge, { variant: "success", children: "ACTIVE" })] }), _jsxs("div", { className: "text-xs text-slate-400 space-y-1", children: [_jsxs("div", { children: ["Protocol: ", _jsx("span", { className: "text-slate-200 font-mono", children: sso.protocol })] }), _jsxs("div", { children: ["Issuer: ", _jsx("span", { className: "text-slate-200 truncate block font-mono", children: sso.issuer_url })] }), _jsxs("div", { children: ["Endpoint: ", _jsx("span", { className: "text-slate-200 truncate block font-mono", children: sso.sso_endpoint })] }), _jsxs("div", { children: ["Fingerprint: ", _jsx("span", { className: "text-cyan-400 font-mono text-[10px] block truncate", children: sso.certificate_fingerprint })] })] })] }, sso.provider_id))), _jsx(Button, { variant: "outline", className: "w-full", children: _jsxs("span", { className: "flex items-center justify-center gap-2", children: [_jsx(RefreshCw, { className: "w-4 h-4" }), " Trigger SCIM Directory Sync"] }) })] })] }), _jsxs(Card, { className: "bg-slate-900/80 border-slate-800 lg:col-span-2", children: [_jsx(CardHeader, { children: _jsxs(CardTitle, { className: "text-base text-white flex items-center gap-2", children: [_jsx(Users, { className: "w-5 h-5 text-indigo-400" }), " Provisioned Enterprise Directory (", users.length, ")"] }) }), _jsx(CardContent, { children: loading ? (_jsx("div", { className: "p-8 text-center text-slate-400", children: "Loading directory..." })) : (_jsx("div", { className: "space-y-3", children: users.map((u) => (_jsxs("div", { className: "p-3 bg-slate-800/40 rounded border border-slate-700/50 flex items-center justify-between", children: [_jsxs("div", { children: [_jsx("span", { className: "text-sm font-semibold text-white block", children: u.display_name }), _jsxs("span", { className: "text-xs text-slate-400", children: [u.email, " \u2022 ", u.department] })] }), _jsxs("div", { className: "flex items-center gap-3", children: [_jsx(Badge, { variant: "intelligence", children: u.role }), _jsx(Badge, { variant: u.mfa_enabled ? 'success' : 'warning', children: u.mfa_enabled ? 'MFA Enabled' : 'No MFA' })] })] }, u.user_id))) })) })] })] })] }));
};
