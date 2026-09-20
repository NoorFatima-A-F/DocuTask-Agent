import React from 'react';
import { useWorkspace } from './context/WorkspaceContext';
import { CardHeader, CardTitle, CardContent } from '../components/ui/Card';
import { Badge } from '../components/ui/Badge';
import { Button } from '../components/ui/Button';
import type { WorkspaceTaskItem } from './types/workspace';

export const TaskBoardPanel: React.FC = () => {
  const { tasks, updateTaskStatus } = useWorkspace();

  const columns: { id: WorkspaceTaskItem['status']; title: string; badgeVariant: 'default' | 'intelligence' | 'success' }[] = [
    { id: 'TODO', title: 'Pending Queue', badgeVariant: 'default' },
    { id: 'IN_PROGRESS', title: 'In Progress (Active Cognition)', badgeVariant: 'intelligence' },
    { id: 'DONE', title: 'Completed & Certified', badgeVariant: 'success' },
  ];

  return (
    <div className="w-full flex flex-col h-[700px] rounded-2xl bg-[#0F172A]/90 border border-[#1E293B] shadow-2xl overflow-hidden">
      <CardHeader className="flex flex-row items-center justify-between py-4 px-6 border-b border-[#1E293B] bg-[#131D35]/50">
        <div>
          <div className="flex items-center gap-2">
            <Badge variant="intelligence" size="sm">
              COLLABORATIVE TASK BOARD
            </Badge>
            <span className="text-xs text-[#94A3B8] font-mono">
              {tasks.length} Autonomous Units
            </span>
          </div>
          <CardTitle className="mt-1 text-base font-bold text-[#F8FAFC]">
            Live Multi-Agent Task Execution Board
          </CardTitle>
        </div>
      </CardHeader>

      <CardContent className="flex-1 overflow-x-auto p-6 grid grid-cols-1 md:grid-cols-3 gap-6">
        {columns.map((col) => {
          const colTasks = tasks.filter((t) => t.status === col.id);

          return (
            <div
              key={col.id}
              className="flex flex-col rounded-xl bg-[#131D35]/50 border border-[#1E293B] p-4 h-full"
            >
              <div className="flex items-center justify-between pb-3 border-b border-[#1E293B] mb-3">
                <span className="text-xs font-bold text-[#F8FAFC]">{col.title}</span>
                <Badge variant={col.badgeVariant} size="sm">
                  {colTasks.length}
                </Badge>
              </div>

              <div className="flex-1 overflow-y-auto space-y-3">
                {colTasks.map((task) => (
                  <div
                    key={task.id}
                    className="p-4 rounded-xl bg-[#131D35] border border-[#1E293B] hover:border-cyan-500/40 transition-all space-y-2"
                  >
                    <div className="flex items-center justify-between text-[11px] font-mono">
                      <Badge variant="intelligence" size="sm">
                        {task.assignedAgentRole}
                      </Badge>
                      <span
                        className={
                          task.priority === 'CRITICAL'
                            ? 'text-red-400 font-bold'
                            : 'text-[#94A3B8]'
                        }
                      >
                        {task.priority}
                      </span>
                    </div>

                    <h4 className="text-xs font-bold text-[#F8FAFC]">{task.title}</h4>

                    {task.producedArtifact && (
                      <div className="text-[10px] font-mono text-[#A855F7] truncate">
                        📄 {task.producedArtifact}
                      </div>
                    )}

                    <div className="pt-2 border-t border-[#1E293B] flex items-center justify-between text-[10px] font-mono">
                      {task.status === 'TODO' && (
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => updateTaskStatus(task.id, 'IN_PROGRESS')}
                          className="text-[10px] py-1"
                        >
                          Start Task ➔
                        </Button>
                      )}
                      {task.status === 'IN_PROGRESS' && (
                        <Button
                          variant="intelligence"
                          size="sm"
                          onClick={() => updateTaskStatus(task.id, 'DONE')}
                          className="text-[10px] py-1"
                        >
                          Mark Complete ✓
                        </Button>
                      )}
                      {task.status === 'DONE' && (
                        <span className="text-[#10B981]">✓ Completed</span>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          );
        })}
      </CardContent>
    </div>
  );
};
