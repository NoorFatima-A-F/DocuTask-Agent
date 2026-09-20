import { jsx as _jsx, jsxs as _jsxs, Fragment as _Fragment } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { SaaSApiClient } from '../../services/saasApiClient';
import { Store, Download, Star, RefreshCw, Check } from 'lucide-react';
export const MarketplaceManager = () => {
    const [assets, setAssets] = useState([]);
    const [installedMap, setInstalledMap] = useState({});
    const [loading, setLoading] = useState(true);
    useEffect(() => {
        const load = async () => {
            setLoading(true);
            const list = await SaaSApiClient.listMarketplaceAssets();
            setAssets(list);
            setLoading(false);
        };
        load();
    }, []);
    const handleInstall = async (assetId) => {
        await SaaSApiClient.installAsset(assetId, 'tenant_acme_corp');
        setInstalledMap((prev) => ({ ...prev, [assetId]: true }));
    };
    return (_jsxs("div", { className: "space-y-6", children: [_jsx("div", { className: "flex items-center justify-between", children: _jsxs("div", { children: [_jsxs("h1", { className: "text-2xl font-bold text-white flex items-center gap-3", children: [_jsx(Store, { className: "w-7 h-7 text-indigo-400" }), "Enterprise AI Marketplace"] }), _jsx("p", { className: "text-sm text-slate-400 mt-1", children: "Discover, evaluate, and install verified Agent Packs, OCR Pipelines, and Workflow Templates." })] }) }), loading ? (_jsxs("div", { className: "p-12 text-center text-slate-400", children: [_jsx(RefreshCw, { className: "w-6 h-6 animate-spin mx-auto mb-2" }), " Loading Marketplace Assets..."] })) : (_jsx("div", { className: "grid grid-cols-1 md:grid-cols-2 gap-6", children: assets.map((asset) => {
                    const isInstalled = installedMap[asset.asset_id];
                    return (_jsxs(Card, { className: "bg-slate-900/80 border-slate-800 flex flex-col justify-between", children: [_jsxs(CardHeader, { children: [_jsxs("div", { className: "flex items-center justify-between mb-1", children: [_jsx(Badge, { variant: "intelligence", children: asset.asset_type }), _jsxs("div", { className: "flex items-center gap-1 text-amber-400 text-xs font-bold", children: [_jsx(Star, { className: "w-3.5 h-3.5 fill-current" }), " ", asset.rating] })] }), _jsx(CardTitle, { className: "text-lg text-white", children: asset.title }), _jsxs("span", { className: "text-xs text-slate-400", children: ["Published by ", asset.publisher_name, " \u2022 v", asset.version] })] }), _jsxs(CardContent, { className: "space-y-4", children: [_jsx("p", { className: "text-xs text-slate-300 line-clamp-2", children: asset.description }), _jsx("div", { className: "flex flex-wrap gap-1.5", children: asset.tags.map((tag) => (_jsxs("span", { className: "text-[10px] bg-slate-800 text-slate-300 px-2 py-0.5 rounded border border-slate-700", children: ["#", tag] }, tag))) }), _jsxs("div", { className: "flex items-center justify-between pt-3 border-t border-slate-800", children: [_jsxs("div", { children: [_jsx("span", { className: "text-sm font-bold text-white", children: asset.price_monthly_usd === 0 ? 'Free' : `$${asset.price_monthly_usd}/mo` }), _jsxs("span", { className: "text-[10px] text-slate-400 block", children: [asset.downloads_count, " installs"] })] }), _jsx(Button, { variant: isInstalled ? 'secondary' : 'intelligence', disabled: isInstalled, onClick: () => handleInstall(asset.asset_id), children: _jsx("span", { className: "flex items-center gap-1.5 text-xs", children: isInstalled ? (_jsxs(_Fragment, { children: [_jsx(Check, { className: "w-3.5 h-3.5 text-emerald-400" }), " Installed"] })) : (_jsxs(_Fragment, { children: [_jsx(Download, { className: "w-3.5 h-3.5" }), " Install Pack"] })) }) })] })] })] }, asset.asset_id));
                }) }))] }));
};
