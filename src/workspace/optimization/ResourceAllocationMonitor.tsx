import React from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { Cpu, Server } from 'lucide-react';

export const ResourceAllocationMonitor: React.FC = () => {
  const activeAllocations = [
    {
      ticketId: 'tkt_7b9d3e',
      missionId: 'mission-001',
      resource: 'General Async Worker Pool',
      allocatedUnits: 6,
      status: 'ALLOCATED',
      timestamp: '10:14:22 UTC',
    },
    {
      ticketId: 'tkt_8a1f4c',
      missionId: 'mission-001',
      resource: 'Gemini 1.5 Flash Quota',
      allocatedUnits: 150,
      status: 'ALLOCATED',
      timestamp: '10:14:22 UTC',
    },
    {
      ticketId: 'tkt_2d0e9a',
      missionId: 'mission-002',
      resource: 'Local Tesseract OCR Cluster',
      allocatedUnits: 3,
      status: 'ALLOCATED',
      timestamp: '10:14:25 UTC',
    },
  ];

  return (
    <div className="p-6 space-y-6 bg-[#0B1120] min-h-screen text-[#F8FAFC]">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4 border-b border-[#1E293B] pb-6">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-gradient-to-br from-indigo-500/20 to-teal-500/20 border border-indigo-500/30 rounded-xl text-indigo-400">
            <Cpu className="w-5 h-5" />
          </div>
          <div>
            <h1 className="text-xl font-bold font-mono tracking-tight text-white flex items-center gap-2">
              Resource Allocation Monitor
              <Badge variant="intelligence" size="sm">Phase 13.6 ARIA-EOP</Badge>
            </h1>
            <p className="text-xs text-[#94A3B8] font-mono">
              Live atomic reservation engine tracking active worker tickets, quota allocations, and concurrency headroom
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <Badge variant="success" size="md">3 Active Reservation Tickets</Badge>
        </div>
      </div>

      {/* Allocation Queue Cards */}
      <div className="space-y-4 font-mono">
        <h2 className="text-sm font-bold text-white flex items-center gap-2">
          <Server className="w-4 h-4 text-cyan-400" />
          Active Resource Allocation Tickets
        </h2>

        <div className="grid grid-cols-1 gap-4">
          {activeAllocations.map((alloc) => (
            <Card key={alloc.ticketId} className="p-5 rounded-xl border border-[#1E293B] bg-[#0F172A] flex flex-wrap items-center justify-between gap-4">
              <div className="space-y-1">
                <div className="flex items-center gap-2">
                  <span className="text-white font-bold">{alloc.resource}</span>
                  <Badge variant="success" size="sm">{alloc.status}</Badge>
                </div>
                <div className="text-xs text-[#64748B]">
                  Mission: <span className="text-indigo-400">{alloc.missionId}</span> | Ticket: {alloc.ticketId}
                </div>
              </div>

              <div className="flex items-center gap-6 text-xs">
                <div className="text-right">
                  <span className="text-[10px] text-[#64748B] block">ALLOCATED UNITS</span>
                  <span className="text-cyan-400 font-bold">{alloc.allocatedUnits} units</span>
                </div>
                <div className="text-right">
                  <span className="text-[10px] text-[#64748B] block">TIMESTAMP</span>
                  <span className="text-[#94A3B8]">{alloc.timestamp}</span>
                </div>
              </div>
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
};
