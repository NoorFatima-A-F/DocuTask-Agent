import React from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';

export const ResourceSchedulerMonitorView: React.FC = () => {
  const workerPools = [
    {
      poolName: 'OCR Processing Pool',
      type: 'OCR_POOL',
      workers: '2 active instances',
      capacity: '4 concurrent slots',
      activeJobs: 1,
      utilization: '25.0%',
      latency: '180 ms',
      status: 'HEALTHY',
    },
    {
      poolName: 'LLM Reasoning & Inference Pool',
      type: 'LLM_POOL',
      workers: '2 active instances',
      capacity: '8 concurrent slots',
      activeJobs: 3,
      utilization: '37.5%',
      latency: '450 ms',
      status: 'HEALTHY',
    },
    {
      poolName: 'Schema & Invariant Validation Pool',
      type: 'VALIDATION_POOL',
      workers: '1 active instance',
      capacity: '8 concurrent slots',
      activeJobs: 0,
      utilization: '0.0%',
      latency: '45 ms',
      status: 'IDLE',
    },
    {
      poolName: 'Memory & Knowledge Retrieval Pool',
      type: 'MEMORY_POOL',
      workers: '1 active instance',
      capacity: '4 concurrent slots',
      activeJobs: 0,
      utilization: '0.0%',
      latency: '60 ms',
      status: 'IDLE',
    },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="p-6 rounded-2xl bg-[#0F172A] border border-[#1E293B] shadow-xl">
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2">
              <span className="text-xl">⚙️</span>
              <h2 className="text-lg font-bold font-mono text-[#F8FAFC]">
                Resource Scheduler & Priority Queue Orchestrator
              </h2>
              <Badge variant="success" size="sm">
                CLUSTER OPTIMAL
              </Badge>
            </div>
            <p className="text-sm font-mono text-[#94A3B8] mt-1">
              Heterogeneous worker pools, priority fair queuing (CRITICAL &gt; HIGH &gt; NORMAL), and backpressure management.
            </p>
          </div>
        </div>
      </div>

      {/* Cluster Overview Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card className="p-4 bg-[#0F172A] border-[#1E293B]">
          <div className="text-xs font-mono text-[#94A3B8]">Total Cluster Workers</div>
          <div className="text-2xl font-bold font-mono text-cyan-400 mt-1">6 Instances</div>
          <div className="text-[11px] font-mono text-[#64748B] mt-1">4 dedicated pools</div>
        </Card>
        <Card className="p-4 bg-[#0F172A] border-[#1E293B]">
          <div className="text-xs font-mono text-[#94A3B8]">Active Task Queue Depth</div>
          <div className="text-2xl font-bold font-mono text-emerald-400 mt-1">2 queued</div>
          <div className="text-[11px] font-mono text-[#64748B] mt-1">Max capacity 1,000 tasks</div>
        </Card>
        <Card className="p-4 bg-[#0F172A] border-[#1E293B]">
          <div className="text-xs font-mono text-[#94A3B8]">Backpressure Status</div>
          <div className="text-2xl font-bold font-mono text-emerald-400 mt-1">NOMINAL (0%)</div>
          <div className="text-[11px] font-mono text-[#64748B] mt-1">Zero dropped requests</div>
        </Card>
        <Card className="p-4 bg-[#0F172A] border-[#1E293B]">
          <div className="text-xs font-mono text-[#94A3B8]">Average Cluster Utilization</div>
          <div className="text-2xl font-bold font-mono text-indigo-400 mt-1">31.2%</div>
          <div className="text-[11px] font-mono text-[#64748B] mt-1">Balanced load across TPUs</div>
        </Card>
      </div>

      {/* Worker Pool Status Table */}
      <Card className="p-6 bg-[#0F172A] border-[#1E293B]">
        <h3 className="text-sm font-bold font-mono text-[#F8FAFC] mb-4">
          Dedicated Subsystem Worker Pools
        </h3>
        <div className="overflow-x-auto">
          <table className="w-full text-left font-mono text-xs">
            <thead>
              <tr className="border-b border-[#1E293B] text-[#94A3B8]">
                <th className="pb-3">Worker Pool</th>
                <th className="pb-3">Pool Type</th>
                <th className="pb-3">Active Instances</th>
                <th className="pb-3">Concurrency Capacity</th>
                <th className="pb-3">Utilization</th>
                <th className="pb-3">Average Latency</th>
                <th className="pb-3">Health Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#1E293B]">
              {workerPools.map((p, idx) => (
                <tr key={idx} className="hover:bg-[#1E293B]/40 transition-colors">
                  <td className="py-3 font-bold text-[#F8FAFC]">{p.poolName}</td>
                  <td className="py-3 text-cyan-400">{p.type}</td>
                  <td className="py-3 text-[#E2E8F0]">{p.workers}</td>
                  <td className="py-3 text-[#94A3B8]">{p.capacity}</td>
                  <td className="py-3 text-indigo-400 font-bold">{p.utilization}</td>
                  <td className="py-3 text-emerald-400">{p.latency}</td>
                  <td className="py-3">
                    <Badge variant={p.status === 'HEALTHY' ? 'success' : 'default'} size="sm">
                      {p.status}
                    </Badge>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
};
