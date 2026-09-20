import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { Globe, MapPin, RefreshCw, ArrowRightLeft, } from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { DistributedApiClient } from '../../services/distributedApiClient';
export const MultiRegionFabricMap = () => {
    const [regions, setRegions] = useState([]);
    const [loading, setLoading] = useState(true);
    const loadRegions = async () => {
        try {
            setLoading(true);
            const res = await DistributedApiClient.getRegions();
            setRegions(res);
        }
        catch (err) {
            console.error('Failed to load regions:', err);
        }
        finally {
            setLoading(false);
        }
    };
    useEffect(() => {
        loadRegions();
    }, []);
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col md:flex-row md:items-center justify-between gap-4 bg-slate-900/60 p-6 rounded-2xl border border-slate-800 backdrop-blur-md", children: [_jsxs("div", { className: "flex items-center gap-3", children: [_jsx("div", { className: "p-2 bg-indigo-500/10 rounded-xl border border-indigo-500/20 text-indigo-400", children: _jsx(Globe, { className: "w-6 h-6" }) }), _jsxs("div", { children: [_jsx("h1", { className: "text-2xl font-bold text-white", children: "Multi-Region Fabric Map" }), _jsx("p", { className: "text-sm text-slate-400", children: "Global agent node topology, edge mesh routing, and inter-region latency matrices" })] })] }), _jsx(Button, { variant: "outline", onClick: loadRegions, disabled: loading, children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(RefreshCw, { className: `w-4 h-4 ${loading ? 'animate-spin' : ''}` }), "Refresh Topology"] }) })] }), _jsx("div", { className: "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5", children: regions.map((reg) => (_jsxs(Card, { className: "p-5 bg-slate-900/40 border-slate-800 space-y-4", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx(MapPin, { className: "w-4 h-4 text-indigo-400" }), _jsx("h3", { className: "font-bold text-white font-mono text-sm", children: reg.region })] }), _jsx(Badge, { variant: "success", children: reg.status })] }), _jsx("p", { className: "text-xs text-slate-300 font-sans", children: reg.location }), _jsxs("div", { className: "pt-2 border-t border-slate-800 flex justify-between items-center text-xs font-mono", children: [_jsx("span", { className: "text-slate-400", children: "Intra-Region Latency:" }), _jsxs("span", { className: "text-emerald-400 font-bold", children: [reg.avg_latency_ms.toFixed(1), " ms"] })] })] }, reg.region))) }), _jsxs(Card, { className: "p-6 bg-slate-900/40 border-slate-800 space-y-4", children: [_jsxs("h3", { className: "text-base font-semibold text-white flex items-center gap-2", children: [_jsx(ArrowRightLeft, { className: "w-4 h-4 text-cyan-400" }), "Inter-Region Latency Matrix (Round-Trip ms)"] }), _jsx("div", { className: "overflow-x-auto", children: _jsxs("table", { className: "w-full text-left text-xs font-mono text-slate-300", children: [_jsx("thead", { className: "bg-slate-800/60 uppercase text-slate-400 border-b border-slate-700", children: _jsxs("tr", { children: [_jsx("th", { className: "py-3 px-4", children: "From / To" }), _jsx("th", { className: "py-3 px-4", children: "us-east-1" }), _jsx("th", { className: "py-3 px-4", children: "us-west-2" }), _jsx("th", { className: "py-3 px-4", children: "eu-central-1" }), _jsx("th", { className: "py-3 px-4", children: "asia-east-1" }), _jsx("th", { className: "py-3 px-4", children: "pk-south-1" })] }) }), _jsxs("tbody", { className: "divide-y divide-slate-800/60", children: [_jsxs("tr", { className: "hover:bg-slate-800/30", children: [_jsx("td", { className: "py-3 px-4 font-bold text-white", children: "us-east-1" }), _jsx("td", { className: "py-3 px-4 text-emerald-400", children: "8.5 ms" }), _jsx("td", { className: "py-3 px-4 text-slate-300", children: "65.0 ms" }), _jsx("td", { className: "py-3 px-4 text-slate-300", children: "85.0 ms" }), _jsx("td", { className: "py-3 px-4 text-amber-400", children: "180.0 ms" }), _jsx("td", { className: "py-3 px-4 text-amber-400", children: "210.0 ms" })] }), _jsxs("tr", { className: "hover:bg-slate-800/30", children: [_jsx("td", { className: "py-3 px-4 font-bold text-white", children: "eu-central-1" }), _jsx("td", { className: "py-3 px-4 text-slate-300", children: "85.0 ms" }), _jsx("td", { className: "py-3 px-4 text-slate-300", children: "140.0 ms" }), _jsx("td", { className: "py-3 px-4 text-emerald-400", children: "10.2 ms" }), _jsx("td", { className: "py-3 px-4 text-amber-400", children: "190.0 ms" }), _jsx("td", { className: "py-3 px-4 text-slate-300", children: "115.0 ms" })] }), _jsxs("tr", { className: "hover:bg-slate-800/30", children: [_jsx("td", { className: "py-3 px-4 font-bold text-white", children: "pk-south-1" }), _jsx("td", { className: "py-3 px-4 text-amber-400", children: "210.0 ms" }), _jsx("td", { className: "py-3 px-4 text-amber-400", children: "240.0 ms" }), _jsx("td", { className: "py-3 px-4 text-slate-300", children: "115.0 ms" }), _jsx("td", { className: "py-3 px-4 text-slate-300", children: "95.0 ms" }), _jsx("td", { className: "py-3 px-4 text-emerald-400", children: "6.0 ms" })] })] })] }) })] })] }));
};
