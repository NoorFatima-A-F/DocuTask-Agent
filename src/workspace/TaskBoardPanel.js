import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useWorkspace } from './context/WorkspaceContext';
import { CardHeader, CardTitle, CardContent } from '../components/ui/Card';
import { Badge } from '../components/ui/Badge';
import { Button } from '../components/ui/Button';
export const TaskBoardPanel = () => {
    const { tasks, updateTaskStatus } = useWorkspace();
    const columns = [
        { id: 'TODO', title: 'Pending Queue', badgeVariant: 'default' },
        { id: 'IN_PROGRESS', title: 'In Progress (Active Cognition)', badgeVariant: 'intelligence' },
        { id: 'DONE', title: 'Completed & Certified', badgeVariant: 'success' },
    ];
    return (_jsxs("div", { className: "w-full flex flex-col h-[700px] rounded-2xl bg-[#0F172A]/90 border border-[#1E293B] shadow-2xl overflow-hidden", children: [_jsx(CardHeader, { className: "flex flex-row items-center justify-between py-4 px-6 border-b border-[#1E293B] bg-[#131D35]/50", children: _jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx(Badge, { variant: "intelligence", size: "sm", children: "COLLABORATIVE TASK BOARD" }), _jsxs("span", { className: "text-xs text-[#94A3B8] font-mono", children: [tasks.length, " Autonomous Units"] })] }), _jsx(CardTitle, { className: "mt-1 text-base font-bold text-[#F8FAFC]", children: "Live Multi-Agent Task Execution Board" })] }) }), _jsx(CardContent, { className: "flex-1 overflow-x-auto p-6 grid grid-cols-1 md:grid-cols-3 gap-6", children: columns.map((col) => {
                    const colTasks = tasks.filter((t) => t.status === col.id);
                    return (_jsxs("div", { className: "flex flex-col rounded-xl bg-[#131D35]/50 border border-[#1E293B] p-4 h-full", children: [_jsxs("div", { className: "flex items-center justify-between pb-3 border-b border-[#1E293B] mb-3", children: [_jsx("span", { className: "text-xs font-bold text-[#F8FAFC]", children: col.title }), _jsx(Badge, { variant: col.badgeVariant, size: "sm", children: colTasks.length })] }), _jsx("div", { className: "flex-1 overflow-y-auto space-y-3", children: colTasks.map((task) => (_jsxs("div", { className: "p-4 rounded-xl bg-[#131D35] border border-[#1E293B] hover:border-cyan-500/40 transition-all space-y-2", children: [_jsxs("div", { className: "flex items-center justify-between text-[11px] font-mono", children: [_jsx(Badge, { variant: "intelligence", size: "sm", children: task.assignedAgentRole }), _jsx("span", { className: task.priority === 'CRITICAL'
                                                        ? 'text-red-400 font-bold'
                                                        : 'text-[#94A3B8]', children: task.priority })] }), _jsx("h4", { className: "text-xs font-bold text-[#F8FAFC]", children: task.title }), task.producedArtifact && (_jsxs("div", { className: "text-[10px] font-mono text-[#A855F7] truncate", children: ["\uD83D\uDCC4 ", task.producedArtifact] })), _jsxs("div", { className: "pt-2 border-t border-[#1E293B] flex items-center justify-between text-[10px] font-mono", children: [task.status === 'TODO' && (_jsx(Button, { variant: "ghost", size: "sm", onClick: () => updateTaskStatus(task.id, 'IN_PROGRESS'), className: "text-[10px] py-1", children: "Start Task \u2794" })), task.status === 'IN_PROGRESS' && (_jsx(Button, { variant: "intelligence", size: "sm", onClick: () => updateTaskStatus(task.id, 'DONE'), className: "text-[10px] py-1", children: "Mark Complete \u2713" })), task.status === 'DONE' && (_jsx("span", { className: "text-[#10B981]", children: "\u2713 Completed" }))] })] }, task.id))) })] }, col.id));
                }) })] }));
};
