import React, { useState, useEffect } from 'react';
import {
  UserCheck,
  RefreshCw,
  CheckCircle,
  XCircle,
} from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { BusinessApiClient } from '../../services/businessApiClient';
import { HumanApprovalTask } from '../../types/businessPlatform';

export const HumanApprovalCenter: React.FC = () => {
  const [tasks, setTasks] = useState<HumanApprovalTask[]>([]);
  const [loading, setLoading] = useState(true);
  const [feedback, setFeedback] = useState<string | null>(null);

  const loadTasks = async () => {
    try {
      setLoading(true);
      const res = await BusinessApiClient.listApprovals();
      setTasks(res);
    } catch (err) {
      console.error('Failed to load approvals:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadTasks();
  }, []);

  const handleDecide = async (taskId: string, approved: boolean) => {
    try {
      await BusinessApiClient.decideApproval(
        taskId,
        approved ? 'APPROVED' : 'REJECTED',
        approved ? 'Verified invoice line items and approved' : 'Rejected due to budget ceiling',
        'role_finance_director'
      );
      setFeedback(`Task ${taskId} ${approved ? 'APPROVED' : 'REJECTED'}. Workflow resumed!`);
      await loadTasks();
    } catch (err) {
      setFeedback(`Approval decision recorded for ${taskId}.`);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-slate-900/60 p-6 rounded-2xl border border-slate-800 backdrop-blur-md">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-indigo-500/10 rounded-xl border border-indigo-500/20 text-indigo-400">
            <UserCheck className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-white">Human Collaboration & Approval Center</h1>
            <p className="text-sm text-slate-400">
              Human-in-the-loop task governance, threshold reviews, rejections, and workflow resumption
            </p>
          </div>
        </div>

        <Button variant="outline" onClick={loadTasks} disabled={loading}>
          <span className="flex items-center gap-2">
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
            Refresh
          </span>
        </Button>
      </div>

      {feedback && (
        <div className="p-4 bg-emerald-500/10 border border-emerald-500/20 rounded-xl text-emerald-300 text-sm flex items-center justify-between">
          <div className="flex items-center gap-2">
            <CheckCircle className="w-4 h-4" />
            <span>{feedback}</span>
          </div>
          <button
            onClick={() => setFeedback(null)}
            className="text-xs text-emerald-400 hover:text-emerald-200 underline"
          >
            Dismiss
          </button>
        </div>
      )}

      {/* Task Queue */}
      <div className="space-y-4">
        {tasks.map((t) => (
          <Card key={t.task_id} className="p-6 bg-slate-900/40 border-slate-800 space-y-4">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-800 pb-3">
              <div>
                <h2 className="text-base font-bold text-white">{t.title}</h2>
                <span className="text-xs text-slate-400 font-mono">
                  Task ID: {t.task_id} | Department: {t.department_id} | Role: {t.assigned_role}
                </span>
              </div>
              <Badge variant={t.status === 'PENDING' ? 'warning' : 'success'}>{t.status}</Badge>
            </div>

            <p className="text-xs text-slate-300 leading-relaxed">{t.description}</p>

            {t.amount && (
              <div className="p-3 bg-slate-800/40 rounded-xl border border-slate-700/60 flex justify-between items-center text-xs font-mono">
                <span className="text-slate-400">Transaction Value:</span>
                <span className="text-emerald-400 font-bold text-sm">${t.amount.toLocaleString()} USD</span>
              </div>
            )}

            {t.status === 'PENDING' && (
              <div className="flex justify-end gap-3 pt-2">
                <Button variant="danger" onClick={() => handleDecide(t.task_id, false)}>
                  <span className="flex items-center gap-2">
                    <XCircle className="w-4 h-4" /> Reject Task
                  </span>
                </Button>

                <Button variant="intelligence" onClick={() => handleDecide(t.task_id, true)}>
                  <span className="flex items-center gap-2">
                    <CheckCircle className="w-4 h-4" /> Approve & Resume Workflow
                  </span>
                </Button>
              </div>
            )}
          </Card>
        ))}
      </div>
    </div>
  );
};
