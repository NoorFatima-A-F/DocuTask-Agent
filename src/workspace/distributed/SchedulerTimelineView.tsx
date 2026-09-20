import React, { useState, useEffect } from 'react';
import {
  Calendar,
  RefreshCw,
  Plus,
  Play,
  User,
} from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { DistributedApiClient } from '../../services/distributedApiClient';
import { ScheduledJob } from '../../types/distributedPlatform';

export const SchedulerTimelineView: React.FC = () => {
  const [jobs, setJobs] = useState<ScheduledJob[]>([]);
  const [loading, setLoading] = useState(true);
  const [showSubmitModal, setShowSubmitModal] = useState(false);
  const [taskName, setTaskName] = useState('Extract Invoices from Storage Bucket');
  const [priority, setPriority] = useState('HIGH');
  const [submitting, setSubmitting] = useState(false);

  const loadJobs = async () => {
    try {
      setLoading(true);
      const res = await DistributedApiClient.listJobs(50);
      setJobs(res);
    } catch (err) {
      console.error('Failed to load scheduled jobs:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadJobs();
  }, []);

  const handleSubmitJob = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      setSubmitting(true);
      await DistributedApiClient.submitJob({
        workflow_id: `wf_manual_${Date.now().toString().slice(-4)}`,
        agent_id: 'agent_doc_extractor',
        task_name: taskName,
        priority,
      });
      setShowSubmitModal(false);
      await loadJobs();
    } catch (err) {
      console.error('Failed to submit job:', err);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-slate-900/60 p-6 rounded-2xl border border-slate-800 backdrop-blur-md">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-indigo-500/10 rounded-xl border border-indigo-500/20 text-indigo-400">
            <Calendar className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-white">Scheduler Timeline View</h1>
            <p className="text-sm text-slate-400">
              Real-time multi-tenant fair-share scheduling with SLA deadline monitoring
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <Button variant="outline" onClick={loadJobs} disabled={loading}>
            <span className="flex items-center gap-2">
              <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
              Refresh
            </span>
          </Button>

          <Button variant="intelligence" onClick={() => setShowSubmitModal(true)}>
            <span className="flex items-center gap-2">
              <Plus className="w-4 h-4" />
              Submit Scheduled Job
            </span>
          </Button>
        </div>
      </div>

      {/* Jobs Table */}
      <Card className="p-6 bg-slate-900/40 border-slate-800">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm text-slate-300">
            <thead className="bg-slate-800/60 text-xs uppercase text-slate-400 border-b border-slate-700">
              <tr>
                <th className="py-3 px-4">Job ID</th>
                <th className="py-3 px-4">Task Name</th>
                <th className="py-3 px-4">Agent</th>
                <th className="py-3 px-4">Priority</th>
                <th className="py-3 px-4">State</th>
                <th className="py-3 px-4">Assigned Worker</th>
                <th className="py-3 px-4">SLA Deadline</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60 text-xs font-mono">
              {jobs.map((job) => (
                <tr key={job.job_id} className="hover:bg-slate-800/30 transition-colors">
                  <td className="py-3 px-4 font-semibold text-white">{job.job_id}</td>
                  <td className="py-3 px-4 text-slate-200 font-sans">{job.task_name}</td>
                  <td className="py-3 px-4 text-indigo-400 font-sans flex items-center gap-1.5">
                    <User className="w-3.5 h-3.5" />
                    {job.agent_id}
                  </td>
                  <td className="py-3 px-4">
                    <Badge
                      variant={
                        job.priority === 'CRITICAL'
                          ? 'error'
                          : job.priority === 'HIGH'
                          ? 'warning'
                          : 'default'
                      }
                    >
                      {job.priority}
                    </Badge>
                  </td>
                  <td className="py-3 px-4">
                    <Badge
                      variant={
                        job.state === 'RUNNING'
                          ? 'intelligence'
                          : job.state === 'COMPLETED'
                          ? 'success'
                          : 'outline'
                      }
                    >
                      {job.state}
                    </Badge>
                  </td>
                  <td className="py-3 px-4 text-cyan-300">
                    {job.assigned_worker_id || 'unassigned (queued)'}
                  </td>
                  <td className="py-3 px-4 text-amber-400">
                    {job.sla_deadline_ms} ms
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>

      {/* Submit Job Modal */}
      {showSubmitModal && (
        <div className="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4">
          <Card className="max-w-md w-full p-6 bg-slate-900 border-slate-700 space-y-4">
            <h3 className="text-lg font-bold text-white">Submit New Job to Distributed Fabric</h3>
            <form onSubmit={handleSubmitJob} className="space-y-4 text-sm">
              <div>
                <label className="block text-slate-400 text-xs mb-1">Task Name</label>
                <input
                  type="text"
                  value={taskName}
                  onChange={(e) => setTaskName(e.target.value)}
                  className="w-full bg-slate-800 border border-slate-700 text-white rounded-lg p-2.5 text-xs"
                  required
                />
              </div>

              <div>
                <label className="block text-slate-400 text-xs mb-1">Priority Tier</label>
                <select
                  value={priority}
                  onChange={(e) => setPriority(e.target.value)}
                  className="w-full bg-slate-800 border border-slate-700 text-white rounded-lg p-2.5 text-xs"
                >
                  <option value="CRITICAL">CRITICAL (P0 - SLA under 2s)</option>
                  <option value="HIGH">HIGH (P1 - SLA under 5s)</option>
                  <option value="NORMAL">NORMAL (P2 - Standard)</option>
                  <option value="BATCH">BATCH (P3 - Offpeak)</option>
                </select>
              </div>

              <div className="flex justify-end gap-3 pt-3">
                <Button variant="ghost" onClick={() => setShowSubmitModal(false)} type="button">
                  Cancel
                </Button>
                <Button variant="intelligence" type="submit" disabled={submitting}>
                  <span className="flex items-center gap-2">
                    {submitting ? <RefreshCw className="w-4 h-4 animate-spin" /> : <Play className="w-4 h-4" />}
                    Submit Job
                  </span>
                </Button>
              </div>
            </form>
          </Card>
        </div>
      )}
    </div>
  );
};
