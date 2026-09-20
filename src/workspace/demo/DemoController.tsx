import React from 'react';
import { useWorkspace } from '../context/WorkspaceContext';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';

export const DemoController: React.FC = () => {
  const { isDemoRunning, demoProgressPhase, startAutonomousDemo, stopAutonomousDemo } =
    useWorkspace();

  return (
    <div className="w-full rounded-xl bg-[#131D35] border border-cyan-500/40 p-4 shadow-[0_0_25px_rgba(0,210,255,0.15)] flex flex-col sm:flex-row sm:items-center justify-between gap-4">
      <div className="flex items-center gap-3">
        <div className="h-10 w-10 rounded-xl bg-gradient-to-tr from-[#0066FF] to-[#00D2FF] flex items-center justify-center text-white font-bold text-lg shadow-[0_0_15px_rgba(0,210,255,0.6)]">
          🚀
        </div>

        <div>
          <div className="flex items-center gap-2">
            <span className="text-xs font-bold text-[#F8FAFC]">
              One-Click Autonomous Demo Controller
            </span>
            {isDemoRunning && (
              <Badge variant="intelligence" size="sm" hasDot isPulsing>
                DEMO RUNNING: {demoProgressPhase}
              </Badge>
            )}
          </div>
          <p className="text-[11px] text-[#94A3B8] mt-0.5">
            Auto-executes complete coworker flow: Intent ➔ Planning ➔ Multi-Agent Inbox ➔ Feedback ➔ Memory Invariants ➔ Confidence Target.
          </p>
        </div>
      </div>

      <div className="flex items-center gap-3 shrink-0">
        {isDemoRunning ? (
          <Button variant="danger" size="sm" onClick={stopAutonomousDemo}>
            ⏹ Stop Demo
          </Button>
        ) : (
          <Button variant="intelligence" size="sm" onClick={startAutonomousDemo}>
            ▶ Start Autonomous Demo
          </Button>
        )}
      </div>
    </div>
  );
};
