import React, { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';

export const DepartmentMonitorView: React.FC = () => {
  const [selectedDeptId, setSelectedDeptId] = useState('dept_extraction');

  const deptData: Record<string, any> = {
    dept_ocr: {
      name: 'Optical Perception & Ingestion',
      head: 'Lead Vision Agent',
      workers: [
        { id: 'w_ocr_1', type: 'LayoutLM GPU Worker', status: 'BUSY', load: '78%', latency: '180 ms', tasks: 420 },
        { id: 'w_ocr_2', type: 'Tesseract Fallback Worker', status: 'IDLE', load: '12%', latency: '140 ms', tasks: 210 },
      ],
      queue: [
        { id: 'q_01', doc: 'DOC-INV-2026-EU', priority: 'HIGH', pages: 4, waitingMs: '120 ms' },
        { id: 'q_02', doc: 'DOC-RECEIPT-8812', priority: 'NORMAL', pages: 1, waitingMs: '45 ms' },
      ],
      kpis: { throughput: '180 items/min', accuracy: '98.5%', errorRate: '0.8%', sla: '99.1%' },
    },
    dept_extraction: {
      name: 'Structured Intelligence & Extraction',
      head: 'Lead Extraction Specialist',
      workers: [
        { id: 'w_llm_1', type: 'Gemini 2.5 Flash Primary', status: 'BUSY', load: '85%', latency: '420 ms', tasks: 1250 },
        { id: 'w_llm_2', type: 'Gemini Flash Lite Secondary', status: 'BUSY', load: '65%', latency: '210 ms', tasks: 890 },
      ],
      queue: [
        { id: 'q_10', doc: 'DOC-HEALTH-REC-01', priority: 'CRITICAL', pages: 6, waitingMs: '210 ms' },
        { id: 'q_11', doc: 'DOC-TAX-1099-2026', priority: 'HIGH', pages: 2, waitingMs: '80 ms' },
        { id: 'q_12', doc: 'DOC-INV-VENDOR-44', priority: 'NORMAL', pages: 3, waitingMs: '40 ms' },
      ],
      kpis: { throughput: '240 items/min', accuracy: '99.1%', errorRate: '0.5%', sla: '98.9%' },
    },
    dept_validation: {
      name: 'Mathematical & Invariant Validation',
      head: 'Lead Verification Auditor',
      workers: [
        { id: 'w_val_1', type: 'Z3 Theorem Prover Engine', status: 'IDLE', load: '24%', latency: '45 ms', tasks: 1600 },
        { id: 'w_val_2', type: 'Zero-Fabrication Sentinel', status: 'BUSY', load: '32%', latency: '50 ms', tasks: 1580 },
      ],
      queue: [
        { id: 'q_20', doc: 'DOC-INV-TOTALS-CHECK', priority: 'HIGH', pages: 2, waitingMs: '30 ms' },
      ],
      kpis: { throughput: '320 items/min', accuracy: '100.0%', errorRate: '0.0%', sla: '100.0%' },
    },
  };

  const current = deptData[selectedDeptId] || deptData['dept_extraction'];

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 p-5 rounded-2xl bg-[#0F172A] border border-[#1E293B] shadow-xl">
        <div>
          <div className="flex items-center gap-2">
            <span className="text-2xl">⚙️</span>
            <h2 className="text-xl font-bold text-[#F8FAFC]">Department Operations & Workload Monitor</h2>
            <Badge variant="intelligence" size="sm">Live Telemetry</Badge>
          </div>
          <p className="text-sm text-[#94A3B8] mt-1">
            Real-time worker pool allocation, task queue pressure, throughput velocity, and SLA telemetry per department.
          </p>
        </div>

        {/* Department Selector Pills */}
        <div className="flex gap-2">
          {Object.keys(deptData).map((dId) => (
            <button
              key={dId}
              onClick={() => setSelectedDeptId(dId)}
              className={`px-3 py-1.5 rounded-lg text-xs font-mono font-semibold transition-all ${
                selectedDeptId === dId ? 'bg-[#0066FF] text-white' : 'bg-[#1E293B] text-[#94A3B8] hover:text-white'
              }`}
            >
              {deptData[dId].name.split(' ')[0]}
            </button>
          ))}
        </div>
      </div>

      {/* Department Overview Banner */}
      <Card className="p-5 bg-[#0F172A] border-[#1E293B]">
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2">
              <span className="text-lg font-bold text-[#F8FAFC]">{current.name}</span>
              <Badge variant="success" size="sm">OPERATIONAL</Badge>
            </div>
            <div className="text-xs text-[#94A3B8] font-mono mt-1">
              Lead Officer: <span className="text-[#38BDF8]">{current.head}</span>
            </div>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-xs font-mono">
            <div>
              <span className="text-[#64748B] block">THROUGHPUT</span>
              <span className="text-[#10B981] font-bold">{current.kpis.throughput}</span>
            </div>
            <div>
              <span className="text-[#64748B] block">ACCURACY</span>
              <span className="text-[#00D2FF] font-bold">{current.kpis.accuracy}</span>
            </div>
            <div>
              <span className="text-[#64748B] block">ERROR RATE</span>
              <span className="text-[#F59E0B] font-bold">{current.kpis.errorRate}</span>
            </div>
            <div>
              <span className="text-[#64748B] block">SLA COMPLIANCE</span>
              <span className="text-[#A855F7] font-bold">{current.kpis.sla}</span>
            </div>
          </div>
        </div>
      </Card>

      {/* Workers and Queue Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Active Worker Pool */}
        <Card className="p-5 bg-[#0F172A] border-[#1E293B] space-y-4">
          <div className="flex items-center justify-between">
            <span className="text-sm font-bold font-mono uppercase text-[#94A3B8]">Dedicated Worker Nodes</span>
            <Badge variant="intelligence" size="sm">{current.workers.length} Active</Badge>
          </div>

          <div className="space-y-3">
            {current.workers.map((w: any) => (
              <div key={w.id} className="p-3 rounded-xl bg-[#020617] border border-[#1E293B] flex items-center justify-between">
                <div>
                  <div className="text-xs font-bold text-[#F8FAFC] font-mono">{w.id}</div>
                  <div className="text-[11px] text-[#94A3B8]">{w.type}</div>
                  <div className="text-[10px] text-[#64748B] font-mono mt-1">Latency: {w.latency} | Total: {w.tasks} ops</div>
                </div>

                <div className="text-right">
                  <Badge variant={w.status === 'BUSY' ? 'warning' : 'success'} size="sm">{w.status}</Badge>
                  <div className="text-xs font-bold font-mono text-[#00D2FF] mt-1">{w.load} Load</div>
                </div>
              </div>
            ))}
          </div>
        </Card>

        {/* Live Workload Queue */}
        <Card className="p-5 bg-[#0F172A] border-[#1E293B] space-y-4">
          <div className="flex items-center justify-between">
            <span className="text-sm font-bold font-mono uppercase text-[#94A3B8]">Incoming Task Queue</span>
            <Badge variant="warning" size="sm">{current.queue.length} Queued</Badge>
          </div>

          <div className="space-y-3">
            {current.queue.map((q: any) => (
              <div key={q.id} className="p-3 rounded-xl bg-[#020617] border border-[#1E293B] flex items-center justify-between">
                <div>
                  <div className="text-xs font-bold text-[#F8FAFC] font-mono">{q.doc}</div>
                  <div className="text-[11px] text-[#94A3B8]">{q.pages} Pages | Task ID: {q.id}</div>
                </div>

                <div className="text-right">
                  <Badge variant={q.priority === 'CRITICAL' ? 'error' : 'default'} size="sm">{q.priority}</Badge>
                  <div className="text-[11px] font-mono text-[#64748B] mt-1">Wait: {q.waitingMs}</div>
                </div>
              </div>
            ))}
          </div>
        </Card>
      </div>
    </div>
  );
};
