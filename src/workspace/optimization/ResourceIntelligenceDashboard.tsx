import React from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { Server, Activity } from 'lucide-react';

export const ResourceIntelligenceDashboard: React.FC = () => {
  const resources = [
    {
      id: 'res-pool-worker-01',
      name: 'General Async Worker Pool',
      type: 'WORKER_POOL',
      capacity: 16,
      allocated: 6,
      available: 10,
      utilization: 37.5,
      status: 'HEALTHY',
    },
    {
      id: 'res-llm-gemini-flash',
      name: 'Gemini 1.5 Flash Quota (RPM)',
      type: 'LLM_QUOTA',
      capacity: 1000,
      allocated: 150,
      available: 850,
      utilization: 15.0,
      status: 'HEALTHY',
    },
    {
      id: 'res-ocr-tesseract',
      name: 'Local Tesseract OCR Cluster',
      type: 'OCR_ENGINE',
      capacity: 8,
      allocated: 3,
      available: 5,
      utilization: 37.5,
      status: 'HEALTHY',
    },
    {
      id: 'res-gpu-v100',
      name: 'NVIDIA V100 Acceleration Node',
      type: 'GPU_NODE',
      capacity: 4,
      allocated: 1,
      available: 3,
      utilization: 25.0,
      status: 'HEALTHY',
    },
  ];

  return (
    <div className="p-6 space-y-6 bg-[#0B1120] min-h-screen text-[#F8FAFC]">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4 border-b border-[#1E293B] pb-6">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-gradient-to-br from-cyan-500/20 to-blue-500/20 border border-cyan-500/30 rounded-xl text-cyan-400">
            <Server className="w-5 h-5" />
          </div>
          <div>
            <h1 className="text-xl font-bold font-mono tracking-tight text-white flex items-center gap-2">
              Autonomous Resource Intelligence Dashboard
              <Badge variant="intelligence" size="sm">Phase 13.6 ARIA-EOP</Badge>
            </h1>
            <p className="text-xs text-[#94A3B8] font-mono">
              Live capacity inventory, worker thread pools, LLM quotas, and GPU node utilization tracking
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <Badge variant="success" size="md">System Capacity: 62.5% Available</Badge>
        </div>
      </div>

      {/* Resource Inventory Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 font-mono">
        {resources.map((res) => (
          <Card key={res.id} className="p-5 rounded-xl border border-[#1E293B] bg-[#0F172A] space-y-4">
            <div className="flex items-start justify-between">
              <div>
                <Badge variant="intelligence" size="sm">{res.type}</Badge>
                <h3 className="text-sm font-bold text-white mt-1.5">{res.name}</h3>
                <span className="text-[11px] text-[#64748B]">ID: {res.id}</span>
              </div>
              <Badge variant="success" size="sm">{res.status}</Badge>
            </div>

            {/* Utilization Progress */}
            <div className="space-y-1.5 text-xs">
              <div className="flex justify-between text-[#94A3B8]">
                <span>Allocated: {res.allocated} / {res.capacity} units</span>
                <span className="text-cyan-400 font-bold">{res.utilization}%</span>
              </div>
              <div className="w-full bg-[#1E293B] rounded-full h-2 overflow-hidden">
                <div
                  className="bg-gradient-to-r from-cyan-500 to-indigo-500 h-2 rounded-full"
                  style={{ width: `${res.utilization}%` }}
                />
              </div>
            </div>

            <div className="pt-2 border-t border-[#1E293B] flex items-center justify-between text-xs text-[#94A3B8]">
              <span>Available Capacity: <strong className="text-emerald-400">{res.available} units</strong></span>
              <span className="flex items-center gap-1 text-cyan-300">
                <Activity className="w-3.5 h-3.5" /> Live Monitored
              </span>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};
