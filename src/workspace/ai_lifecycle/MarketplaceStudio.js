import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { AILifecycleApiClient } from '../../services/aiLifecycleApiClient';
import { Store, Star, Download, RefreshCw } from 'lucide-react';
export const MarketplaceStudio = () => {
    const [listings, setListings] = useState([]);
    const [loading, setLoading] = useState(true);
    useEffect(() => {
        const load = async () => {
            setLoading(true);
            const list = await AILifecycleApiClient.listMarketplaceListings();
            setListings(list);
            setLoading(false);
        };
        load();
    }, []);
    return (_jsxs("div", { className: "space-y-6", children: [_jsx("div", { className: "flex items-center justify-between", children: _jsxs("div", { children: [_jsxs("h1", { className: "text-2xl font-bold text-white flex items-center gap-3", children: [_jsx(Store, { className: "w-7 h-7 text-indigo-400" }), "Enterprise AI Application Marketplace Studio"] }), _jsx("p", { className: "text-sm text-slate-400 mt-1", children: "Enterprise-wide sharing, verified security certifications, community ratings, and one-click installs." })] }) }), loading ? (_jsxs("div", { className: "p-12 text-center text-slate-400", children: [_jsx(RefreshCw, { className: "w-6 h-6 animate-spin mx-auto mb-2" }), " Loading Marketplace..."] })) : (_jsx("div", { className: "grid grid-cols-1 md:grid-cols-2 gap-6", children: listings.map((l) => (_jsxs(Card, { className: "bg-slate-900/80 border-slate-800 flex flex-col justify-between", children: [_jsxs(CardHeader, { children: [_jsxs("div", { className: "flex items-center justify-between mb-2", children: [_jsx(Badge, { variant: "intelligence", children: l.category }), _jsxs("div", { className: "flex items-center gap-1 text-amber-400 text-xs font-bold", children: [_jsx(Star, { className: "w-3.5 h-3.5 fill-current" }), " ", l.rating] })] }), _jsx(CardTitle, { className: "text-lg text-white", children: l.title }), _jsxs("span", { className: "text-xs text-slate-400", children: ["By ", l.publisher_name, " \u2022 v", l.version] })] }), _jsxs(CardContent, { className: "space-y-4", children: [_jsx("p", { className: "text-xs text-slate-300", children: l.description }), _jsxs("div", { className: "flex items-center justify-between pt-3 border-t border-slate-800", children: [_jsxs("div", { children: [_jsx("span", { className: "text-sm font-bold text-white", children: l.price_monthly_usd === 0 ? 'Free' : `$${l.price_monthly_usd}/mo` }), _jsxs("span", { className: "text-[10px] text-slate-400 block", children: [l.install_count, " installs"] })] }), _jsx(Button, { variant: "intelligence", children: _jsxs("span", { className: "flex items-center gap-1.5 text-xs", children: [_jsx(Download, { className: "w-3.5 h-3.5" }), " Install Application"] }) })] })] })] }, l.listing_id))) }))] }));
};
