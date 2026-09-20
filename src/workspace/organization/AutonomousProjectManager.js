import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { FolderKanban, RotateCw, Sparkles, Layers, Flag, } from 'lucide-react';
import { organizationPlatformApiClient } from '../../services/organizationPlatformApiClient';
export const AutonomousProjectManager = () => {
    const [projects, setProjects] = useState([]);
    const [loading, setLoading] = useState(true);
    const [selectedProject, setSelectedProject] = useState(null);
    const [replanning, setReplanning] = useState(false);
    const loadProjects = async () => {
        try {
            setLoading(true);
            const data = await organizationPlatformApiClient.getProjects();
            setProjects(data);
            if (data.length > 0 && !selectedProject) {
                setSelectedProject(data[0] || null);
            }
        }
        catch (err) {
            console.error('Failed to load projects:', err);
        }
        finally {
            setLoading(false);
        }
    };
    useEffect(() => {
        loadProjects();
    }, []);
    const handleReplan = async (projectId) => {
        try {
            setReplanning(true);
            const updated = await organizationPlatformApiClient.replanProject(projectId);
            setSelectedProject(updated);
            await loadProjects();
        }
        catch (err) {
            console.error('Error replanning project:', err);
        }
        finally {
            setReplanning(false);
        }
    };
    return (_jsxs("div", { className: "space-y-6 p-6", children: [_jsxs("div", { className: "flex flex-col md:flex-row items-start md:items-center justify-between gap-4 border-b border-border pb-4", children: [_jsxs("div", { className: "flex items-center gap-3", children: [_jsx("div", { className: "p-2 bg-primary/10 rounded-lg text-primary", children: _jsx(FolderKanban, { className: "w-6 h-6" }) }), _jsxs("div", { children: [_jsx("h1", { className: "text-2xl font-bold tracking-tight", children: "Autonomous Project Manager" }), _jsx("p", { className: "text-sm text-muted-foreground", children: "Work Breakdown Structures, Critical Path Method (CPM) Analysis & Autonomous Replanning" })] })] }), _jsx(Button, { variant: "outline", onClick: loadProjects, disabled: loading, children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(RotateCw, { className: `w-4 h-4 ${loading ? 'animate-spin' : ''}` }), "Refresh"] }) })] }), _jsxs("div", { className: "grid grid-cols-1 lg:grid-cols-3 gap-6", children: [_jsxs("div", { className: "space-y-4", children: [_jsxs("h2", { className: "text-sm font-semibold", children: ["Active Virtual Projects (", projects.length, ")"] }), _jsx("div", { className: "space-y-3", children: projects.map((p) => (_jsx(Card, { onClick: () => setSelectedProject(p), className: `border cursor-pointer transition-all ${selectedProject?.project_id === p.project_id
                                        ? 'border-primary bg-primary/5 shadow-sm'
                                        : 'border-border hover:bg-muted/30'}`, children: _jsxs(CardContent, { className: "p-4 space-y-2", children: [_jsxs("div", { className: "flex justify-between items-start", children: [_jsx("span", { className: "font-semibold text-sm line-clamp-1", children: p.title }), _jsx(Badge, { variant: p.status === 'ACTIVE' ? 'success' : 'outline', children: p.status })] }), _jsx("p", { className: "text-xs text-muted-foreground line-clamp-2", children: p.description }), _jsxs("div", { className: "space-y-1 pt-2", children: [_jsxs("div", { className: "flex justify-between text-xs text-muted-foreground", children: [_jsx("span", { children: "Progress:" }), _jsxs("span", { className: "font-semibold text-foreground", children: [p.total_progress_percent, "%"] })] }), _jsx("div", { className: "w-full bg-muted rounded-full h-1.5 overflow-hidden", children: _jsx("div", { className: "bg-primary h-full rounded-full transition-all", style: { width: `${p.total_progress_percent}%` } }) })] })] }) }, p.project_id))) })] }), _jsx("div", { className: "lg:col-span-2 space-y-6", children: selectedProject ? (_jsxs(Card, { className: "border-border shadow-sm", children: [_jsxs(CardHeader, { className: "flex flex-row items-center justify-between pb-3", children: [_jsxs("div", { children: [_jsx(CardTitle, { className: "text-lg", children: selectedProject.title }), _jsxs("p", { className: "text-xs text-muted-foreground mt-0.5", children: ["Lead: ", _jsx("span", { className: "font-mono text-primary", children: selectedProject.lead_agent_id })] })] }), _jsx(Button, { variant: "intelligence", onClick: () => handleReplan(selectedProject.project_id), disabled: replanning, children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(Sparkles, { className: "w-4 h-4" }), replanning ? 'Replanning...' : 'Autonomous Replan'] }) })] }), _jsxs(CardContent, { className: "space-y-4", children: [_jsxs("div", { className: "p-3 bg-primary/5 border border-primary/20 rounded-lg flex items-center justify-between text-xs", children: [_jsxs("div", { children: [_jsx("span", { className: "font-semibold text-primary", children: "CPM Critical Path Duration: " }), _jsxs("span", { className: "font-bold", children: [selectedProject.critical_path_duration_days, " Days"] })] }), _jsx(Badge, { variant: "success", children: "SCHEDULE ON TRACK" })] }), _jsxs("div", { children: [_jsxs("h3", { className: "text-sm font-semibold mb-2 flex items-center gap-2", children: [_jsx(Flag, { className: "w-4 h-4 text-primary" }), "Milestones (", selectedProject.milestones.length, ")"] }), _jsx("div", { className: "grid grid-cols-1 md:grid-cols-2 gap-2", children: selectedProject.milestones.map((m) => (_jsxs("div", { className: "p-2.5 bg-muted/40 border border-border rounded-lg text-xs", children: [_jsxs("div", { className: "flex justify-between items-center", children: [_jsx("span", { className: "font-medium text-foreground", children: m.title }), _jsx(Badge, { variant: m.status === 'ACHIEVED' ? 'success' : 'outline', children: m.status })] }), _jsxs("div", { className: "text-muted-foreground mt-1", children: ["Due Week: ", m.due_week] })] }, m.milestone_id))) })] }), _jsxs("div", { children: [_jsxs("h3", { className: "text-sm font-semibold mb-2 flex items-center gap-2", children: [_jsx(Layers, { className: "w-4 h-4 text-primary" }), "Work Breakdown Structure Tasks (", selectedProject.tasks.length, ")"] }), _jsx("div", { className: "space-y-2", children: selectedProject.tasks.map((task) => (_jsxs("div", { className: `p-3 rounded-lg border text-xs space-y-1.5 ${task.is_critical_path
                                                            ? 'border-red-500/40 bg-red-500/5'
                                                            : 'border-border bg-card'}`, children: [_jsxs("div", { className: "flex justify-between items-start", children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "font-semibold text-sm text-foreground", children: task.title }), task.is_critical_path && (_jsx(Badge, { variant: "error", children: "CRITICAL PATH" }))] }), _jsx(Badge, { variant: task.status === 'COMPLETED' ? 'success' : 'outline', children: task.status })] }), _jsx("p", { className: "text-muted-foreground", children: task.description }), _jsxs("div", { className: "flex items-center justify-between text-muted-foreground pt-1", children: [_jsxs("span", { children: ["Worker: ", _jsx("strong", { className: "text-foreground", children: task.assigned_agent_id })] }), _jsxs("span", { children: ["Est: ", _jsxs("strong", { children: [task.estimated_days, "d"] }), " | Progress: ", _jsxs("strong", { children: [task.progress_percent, "%"] })] })] })] }, task.task_id))) })] })] })] })) : (_jsx(Card, { className: "border-border shadow-sm p-8 text-center text-muted-foreground", children: "Select a project to inspect critical path dependencies and task breakdown." })) })] })] }));
};
