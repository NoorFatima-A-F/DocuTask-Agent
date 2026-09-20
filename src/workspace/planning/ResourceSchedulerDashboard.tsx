/**
 * Resource Scheduler & Worker Leasing Dashboard.
 * Visualizes worker cluster state, active leases, priority queues, and preemption statuses.
 */

import React, { useState, useEffect } from 'react';
import { SchedulerClusterStatus } from '../../types/autonomousPlanning';
import { PlanningApiClient } from '../../services/planningApiClient';

export const ResourceSchedulerDashboardView: React.FC = () => {
  const [status, setStatus] = useState<SchedulerClusterStatus | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    loadStatus();
    const interval = setInterval(loadStatus, 4000);
    return () => clearInterval(interval);
  }, []);

  const loadStatus = async () => {
    try {
      const data = await PlanningApiClient.getSchedulerStatus();
      setStatus(data);
    } catch (err) {
      console.error('Failed to load scheduler status', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading || !status) {
    return (
      <div className="flex items-center justify-center p-12 text-slate-400">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-500 mr-3"></div>
        <span>Connecting to Enterprise Resource Scheduler...</span>
      </div>
    );
  }

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 text-slate-100 shadow-2xl space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between border-b border-slate-800 pb-4 gap-4">
        <div>
          <div className="flex items-center space-x-3">
            <span className="px-2.5 py-1 text-xs font-bold uppercase tracking-wider bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 rounded-md">
              Enterprise Resource Scheduler
            </span>
            <span className="text-xs text-slate-400 font-mono">Cluster: us-east-prod-01</span>
          </div>
          <h2 className="text-xl font-bold text-white mt-1">Worker Leasing & Priority Execution Matrix</h2>
          <p className="text-sm text-slate-400">
            Real-time hardware leases, preemption supervisor, GPU reservations, and elasticity metrics.
          </p>
        </div>

        <div className="flex items-center space-x-2">
          <div className="bg-slate-800 px-3 py-1.5 rounded-lg border border-slate-700 text-right">
            <span className="block text-[10px] uppercase text-slate-400 font-semibold">Cluster Utilization</span>
            <span className="text-sm font-bold text-indigo-400">{status.utilization_pct.toFixed(1)}%</span>
          </div>
        </div>
      </div>

      {/* Cluster Metrics Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 font-mono">
        <div className="bg-slate-950/60 p-4 rounded-lg border border-slate-800">
          <span className="text-xs text-slate-400 uppercase tracking-wider block">Total Workers</span>
          <span className="text-2xl font-bold text-white mt-1 block">{status.total_workers}</span>
          <span className="text-[11px] text-slate-500">Auto-scaling enabled</span>
        </div>

        <div className="bg-slate-950/60 p-4 rounded-lg border border-slate-800">
          <span className="text-xs text-slate-400 uppercase tracking-wider block">Active Leases</span>
          <span className="text-2xl font-bold text-indigo-400 mt-1 block">{status.active_leases_count}</span>
          <span className="text-[11px] text-slate-500">Time-bounded TTL</span>
        </div>

        <div className="bg-slate-950/60 p-4 rounded-lg border border-slate-800">
          <span className="text-xs text-slate-400 uppercase tracking-wider block">Idle Capacity</span>
          <span className="text-2xl font-bold text-emerald-400 mt-1 block">{status.idle_workers}</span>
          <span className="text-[11px] text-slate-500">Immediate dispatch</span>
        </div>

        <div className="bg-slate-950/60 p-4 rounded-lg border border-slate-800">
          <span className="text-xs text-slate-400 uppercase tracking-wider block">Queue Depth</span>
          <span className="text-2xl font-bold text-amber-400 mt-1 block">{status.queue_depth}</span>
          <span className="text-[11px] text-slate-500">Priority weighted</span>
        </div>
      </div>

      {/* Active Leases Table */}
      <div className="bg-slate-950/60 border border-slate-800 rounded-lg p-4 space-y-3">
        <div className="flex items-center justify-between">
          <h4 className="text-xs font-bold uppercase tracking-wider text-slate-300">
            Active Hardware Leases & Allocations
          </h4>
          <span className="text-[11px] font-mono text-slate-500">Supervised by OTP Engine</span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs font-mono">
            <thead>
              <tr className="border-b border-slate-800 text-slate-400 uppercase bg-slate-900/40">
                <th className="p-2.5">Lease ID</th>
                <th className="p-2.5">Worker Host</th>
                <th className="p-2.5">Mission</th>
                <th className="p-2.5">Capability</th>
                <th className="p-2.5">Priority</th>
                <th className="p-2.5">Preemption Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/40">
              {status.active_leases.length === 0 ? (
                <tr>
                  <td colSpan={6} className="p-4 text-center text-slate-500">
                    No active worker leases. All nodes in warm standby.
                  </td>
                </tr>
              ) : (
                status.active_leases.map((lease) => (
                  <tr key={lease.lease_id} className="hover:bg-slate-900/40">
                    <td className="p-2.5 text-indigo-300 font-bold">{lease.lease_id}</td>
                    <td className="p-2.5 text-slate-300">{lease.worker_id}</td>
                    <td className="p-2.5 text-slate-400">{lease.mission_id}</td>
                    <td className="p-2.5 text-cyan-300">{lease.capability_id}</td>
                    <td className="p-2.5">
                      <span className="px-2 py-0.5 rounded bg-indigo-500/20 text-indigo-400">
                        P{lease.priority}
                      </span>
                    </td>
                    <td className="p-2.5">
                      {lease.preempted ? (
                        <span className="text-rose-400 font-bold">PREEMPTED</span>
                      ) : (
                        <span className="text-emerald-400">EXCLUSIVE ACTIVE</span>
                      )}
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
