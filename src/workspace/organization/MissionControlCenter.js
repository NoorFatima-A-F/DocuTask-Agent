import { jsx as _jsx, jsxs as _jsxs, Fragment as _Fragment } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { Target, Plus, CheckCircle2, RotateCw, Sparkles, Calendar, Layers, ShieldAlert, } from 'lucide-react';
import { organizationPlatformApiClient } from '../../services/organizationPlatformApiClient';
export const MissionControlCenter = () => {
    const [missions, setMissions] = useState([]);
    const [loading, setLoading] = useState(true);
    const [selectedMission, setSelectedMission] = useState(null);
    const [newGoal, setNewGoal] = useState('');
    const [timelineDays, setTimelineDays] = useState(90);
    const [creating, setCreating] = useState(false);
    const [validating, setValidating] = useState(false);
    const [validationResult, setValidationResult] = useState(null);
    const loadMissions = async () => {
        try {
            setLoading(true);
            const data = await organizationPlatformApiClient.getMissions();
            setMissions(data);
            if (data.length > 0 && !selectedMission) {
                setSelectedMission(data[0] || null);
            }
        }
        catch (err) {
            console.error('Failed to load missions:', err);
        }
        finally {
            setLoading(false);
        }
    };
    useEffect(() => {
        loadMissions();
    }, []);
    const handleCreateMission = async (e) => {
        e.preventDefault();
        if (!newGoal.trim())
            return;
        try {
            setCreating(true);
            const created = await organizationPlatformApiClient.createMission(newGoal, 'HIGH', timelineDays);
            setNewGoal('');
            await loadMissions();
            setSelectedMission(created);
        }
        catch (err) {
            console.error('Failed to create mission:', err);
        }
        finally {
            setCreating(false);
        }
    };
    const handleValidate = async (missionId) => {
        try {
            setValidating(true);
            const res = await organizationPlatformApiClient.validateMission(missionId);
            setValidationResult(res);
            await loadMissions();
        }
        catch (err) {
            console.error('Failed to validate mission:', err);
        }
        finally {
            setValidating(false);
        }
    };
    return (_jsxs("div", { className: "space-y-6 p-6", children: [_jsxs("div", { className: "flex flex-col md:flex-row items-start md:items-center justify-between gap-4 border-b border-border pb-4", children: [_jsxs("div", { className: "flex items-center gap-3", children: [_jsx("div", { className: "p-2 bg-primary/10 rounded-lg text-primary", children: _jsx(Target, { className: "w-6 h-6" }) }), _jsxs("div", { children: [_jsx("h1", { className: "text-2xl font-bold tracking-tight", children: "Mission Understanding & Control" }), _jsx("p", { className: "text-sm text-muted-foreground", children: "Autonomous Goal Decomposition, Mathematical Constraint Bounds & Strategic KPI Derivation" })] })] }), _jsx(Button, { variant: "outline", onClick: loadMissions, disabled: loading, children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(RotateCw, { className: `w-4 h-4 ${loading ? 'animate-spin' : ''}` }), "Refresh"] }) })] }), _jsxs(Card, { className: "border-border shadow-sm", children: [_jsx(CardHeader, { children: _jsxs(CardTitle, { className: "text-base flex items-center gap-2", children: [_jsx(Sparkles, { className: "w-4 h-4 text-primary" }), "Decompose Natural Language Enterprise Goal"] }) }), _jsx(CardContent, { children: _jsx("form", { onSubmit: handleCreateMission, className: "space-y-4", children: _jsxs("div", { className: "flex flex-col md:flex-row gap-4", children: [_jsx("input", { type: "text", value: newGoal, onChange: (e) => setNewGoal(e.target.value), placeholder: "e.g. Reduce document processing cost by 40% while maintaining >=98% accuracy", className: "flex-1 px-3.5 py-2 text-sm rounded-md border border-input bg-background focus:outline-none focus:ring-1 focus:ring-primary" }), _jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "text-xs text-muted-foreground whitespace-nowrap", children: "Timeline (Days):" }), _jsx("input", { type: "number", value: timelineDays, onChange: (e) => setTimelineDays(Number(e.target.value)), min: 7, max: 365, className: "w-20 px-2.5 py-2 text-sm rounded-md border border-input bg-background focus:outline-none focus:ring-1 focus:ring-primary" })] }), _jsx(Button, { type: "submit", variant: "primary", disabled: creating || !newGoal.trim(), children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(Plus, { className: "w-4 h-4" }), creating ? 'Decomposing...' : 'Decompose Goal'] }) })] }) }) })] }), _jsxs("div", { className: "grid grid-cols-1 lg:grid-cols-3 gap-6", children: [_jsxs(Card, { className: "border-border shadow-sm", children: [_jsx(CardHeader, { children: _jsx(CardTitle, { className: "text-base flex items-center justify-between", children: _jsxs("span", { children: ["Active Missions (", missions.length, ")"] }) }) }), _jsx(CardContent, { className: "space-y-2", children: missions.map((m) => (_jsxs("div", { onClick: () => {
                                        setSelectedMission(m);
                                        setValidationResult(null);
                                    }, className: `p-3 rounded-lg border cursor-pointer transition-all ${selectedMission?.mission_id === m.mission_id
                                        ? 'border-primary bg-primary/5 shadow-sm'
                                        : 'border-border hover:bg-muted/40'}`, children: [_jsxs("div", { className: "flex items-start justify-between gap-2", children: [_jsx("span", { className: "font-semibold text-sm line-clamp-1", children: m.title }), _jsx(Badge, { variant: m.priority === 'CRITICAL' ? 'error' : 'intelligence', children: m.priority })] }), _jsx("p", { className: "text-xs text-muted-foreground mt-1 line-clamp-2", children: m.raw_goal }), _jsxs("div", { className: "flex items-center gap-3 mt-2 text-xs text-muted-foreground", children: [_jsxs("span", { className: "flex items-center gap-1", children: [_jsx(Calendar, { className: "w-3.5 h-3.5" }), " ", m.timeline_days, "d"] }), _jsxs("span", { className: "flex items-center gap-1", children: [_jsx(Layers, { className: "w-3.5 h-3.5" }), " ", m.objectives.length, " Objectives"] })] })] }, m.mission_id))) })] }), _jsx("div", { className: "lg:col-span-2 space-y-6", children: selectedMission ? (_jsx(_Fragment, { children: _jsxs(Card, { className: "border-border shadow-sm", children: [_jsxs(CardHeader, { className: "flex flex-row items-center justify-between pb-3", children: [_jsxs("div", { children: [_jsx(CardTitle, { className: "text-lg", children: selectedMission.title }), _jsx("p", { className: "text-xs text-muted-foreground font-mono mt-0.5", children: selectedMission.mission_id })] }), _jsx(Button, { variant: "outline", onClick: () => handleValidate(selectedMission.mission_id), disabled: validating, children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(CheckCircle2, { className: "w-4 h-4 text-emerald-500" }), validating ? 'Validating...' : 'Validate Feasibility'] }) })] }), _jsxs(CardContent, { className: "space-y-4", children: [validationResult && (_jsxs("div", { className: "p-3 bg-emerald-500/10 border border-emerald-500/30 rounded-lg text-xs space-y-1", children: [_jsxs("div", { className: "font-semibold text-emerald-500 flex items-center gap-1.5", children: [_jsx(CheckCircle2, { className: "w-4 h-4" }), " Mission Strategically Validated & Approved"] }), _jsxs("div", { className: "text-muted-foreground", children: ["Confidence: ", (validationResult.confidence_score * 100).toFixed(1), "% | Alignment:", ' ', (validationResult.alignment_score * 100).toFixed(1), "%"] })] })), _jsxs("div", { children: [_jsxs("h3", { className: "text-sm font-semibold mb-2 flex items-center gap-2", children: [_jsx(Target, { className: "w-4 h-4 text-primary" }), "Decomposed Objectives (", selectedMission.objectives.length, ")"] }), _jsx("div", { className: "space-y-2", children: selectedMission.objectives.map((obj) => (_jsxs("div", { className: "p-3 bg-muted/30 border border-border rounded-lg text-sm", children: [_jsxs("div", { className: "flex justify-between items-start", children: [_jsx("span", { className: "font-medium", children: obj.title }), _jsx(Badge, { variant: "outline", children: obj.status })] }), _jsx("p", { className: "text-xs text-muted-foreground mt-1", children: obj.description }), _jsxs("div", { className: "mt-2 flex items-center gap-4 text-xs text-muted-foreground", children: [_jsxs("span", { children: ["Target: ", obj.target_value, " (", obj.target_metric, ")"] }), _jsxs("span", { children: ["Progress: ", obj.progress_percent, "%"] })] })] }, obj.objective_id))) })] }), _jsxs("div", { children: [_jsxs("h3", { className: "text-sm font-semibold mb-2 flex items-center gap-2", children: [_jsx(ShieldAlert, { className: "w-4 h-4 text-amber-500" }), "Hard & Soft Constraints (", selectedMission.constraints.length, ")"] }), _jsx("div", { className: "grid grid-cols-1 md:grid-cols-2 gap-2", children: selectedMission.constraints.map((c) => (_jsxs("div", { className: "p-2.5 bg-card border border-border rounded-lg text-xs", children: [_jsxs("div", { className: "flex justify-between items-center", children: [_jsx(Badge, { variant: c.is_strict ? 'error' : 'warning', children: c.is_strict ? 'STRICT' : 'FLEXIBLE' }), _jsxs("span", { className: "font-mono text-muted-foreground", children: [c.threshold_value, " ", c.unit] })] }), _jsx("p", { className: "mt-1 font-medium", children: c.description })] }, c.constraint_id))) })] })] })] }) })) : (_jsx(Card, { className: "border-border shadow-sm p-8 text-center text-muted-foreground", children: "Select a mission to inspect objectives and constraints." })) })] })] }));
};
