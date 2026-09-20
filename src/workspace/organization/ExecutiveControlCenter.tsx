import React, { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';

export const ExecutiveControlCenter: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'MISSIONS' | 'DECISIONS' | 'BARRIERS'>('MISSIONS');

  const missions = [
    {
      id: 'mission_live_001',
      title: 'Enterprise Financial Document Processing',
      priority: 'CRITICAL',
      status: 'IN_PROGRESS',
      budget: '$0.050',
      spent: '$0.018',
      departments: ['dept_executive', 'dept_ocr', 'dept_extraction', 'dept_validation', 'dept_governance'],
      stages: [
        { name: 'Strategic Intake & Policy Check', dept: 'Executive', status: 'COMPLETED', dur: '35 ms' },
        { name: 'Optical Ingestion & Bounding Box Layout', dept: 'OCR', status: 'COMPLETED', dur: '180 ms' },
        { name: 'Structured Semantic Extraction', dept: 'Extraction', status: 'IN_PROGRESS', dur: '420 ms' },
        { name: 'Mathematical Cross-Field Invariant Check', dept: 'Validation', status: 'PENDING', dur: '—' },
        { name: 'Cryptographic Sign-off & Audit Vault', dept: 'Governance', status: 'PENDING', dur: '—' },
      ],
    },
  ];

  const decisions = [
    {
      id: 'exec_dec_001',
      title: 'Authorize Q3 Enterprise Invoices Multi-Department Processing',
      type: 'MISSION_INTAKE',
      rationale: 'Approved high-priority invoice corpus execution with target SLA < 1000ms and budget ceiling $0.05.',
      departments: ['Executive', 'OCR', 'Extraction', 'Validation', 'Governance'],
      authorizer: 'Chief Executive Agent',
      hash: 'sha256_exec_88a91f4c',
      time: '12 min ago',
    },
    {
      id: 'exec_dec_002',
      title: 'Grant Extraction Department Additional 4 Worker Threads',
      type: 'RESOURCE_REALLOCATION',
      rationale: 'Pre-emptive capacity boost to meet P95 latency guarantees during high throughput burst.',
      departments: ['Extraction', 'Research'],
      authorizer: 'Chief Executive Agent',
      hash: 'sha256_exec_31b0e9a2',
      time: '5 min ago',
    },
  ];

  const barriers = [
    {
      id: 'bar_ocr_extraction_01',
      title: 'Perception Handoff Barrier',
      participating: ['dept_ocr', 'dept_memory'],
      arrived: ['dept_ocr', 'dept_memory'],
      isReleased: true,
    },
    {
      id: 'bar_val_gov_02',
      title: 'Audit Sign-off Barrier',
      participating: ['dept_validation', 'dept_qa'],
      arrived: ['dept_validation'],
      isReleased: false,
    },
  ];

  return (
    <div className="space-y-6">
      {/* Top Controls */}
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 p-5 rounded-2xl bg-[#0F172A] border border-[#1E293B] shadow-xl">
        <div>
          <div className="flex items-center gap-2">
            <span className="text-2xl">👔</span>
            <h2 className="text-xl font-bold text-[#F8FAFC]">Executive Coordination & Strategy Control Center</h2>
            <Badge variant="intelligence" size="sm">C-Suite Autonomous Planner</Badge>
          </div>
          <p className="text-sm text-[#94A3B8] mt-1">
            Top-level organizational steering: mission intake, inter-department conflict arbitration, and strategic priority governance.
          </p>
        </div>

        <div className="flex gap-2">
          <button
            onClick={() => setActiveTab('MISSIONS')}
            className={`px-3 py-1.5 rounded-lg text-xs font-mono font-semibold transition-all ${
              activeTab === 'MISSIONS' ? 'bg-[#0066FF] text-white' : 'bg-[#1E293B] text-[#94A3B8] hover:text-white'
            }`}
          >
            Active Missions
          </button>
          <button
            onClick={() => setActiveTab('DECISIONS')}
            className={`px-3 py-1.5 rounded-lg text-xs font-mono font-semibold transition-all ${
              activeTab === 'DECISIONS' ? 'bg-[#0066FF] text-white' : 'bg-[#1E293B] text-[#94A3B8] hover:text-white'
            }`}
          >
            Executive Decisions
          </button>
          <button
            onClick={() => setActiveTab('BARRIERS')}
            className={`px-3 py-1.5 rounded-lg text-xs font-mono font-semibold transition-all ${
              activeTab === 'BARRIERS' ? 'bg-[#0066FF] text-white' : 'bg-[#1E293B] text-[#94A3B8] hover:text-white'
            }`}
          >
            Coordination Barriers
          </button>
        </div>
      </div>

      {/* Main Tab Content */}
      {activeTab === 'MISSIONS' && (
        <div className="space-y-4">
          {missions.map((m) => (
            <Card key={m.id} className="p-5 bg-[#0F172A] border-[#1E293B] space-y-4">
              <div className="flex items-start justify-between">
                <div>
                  <div className="flex items-center gap-2">
                    <span className="text-base font-bold text-[#F8FAFC]">{m.title}</span>
                    <Badge variant="error" size="sm">{m.priority}</Badge>
                    <Badge variant="warning" size="sm">{m.status}</Badge>
                  </div>
                  <div className="text-xs text-[#94A3B8] font-mono mt-1">
                    Mission ID: {m.id} | Budget Spent: <span className="text-[#F59E0B]">{m.spent}</span> / {m.budget}
                  </div>
                </div>

                <div className="text-right">
                  <div className="text-xs text-[#64748B] font-mono uppercase">Assigned Departments</div>
                  <div className="text-xs text-[#38BDF8] font-mono font-semibold mt-0.5">
                    {m.departments.length} Departments Active
                  </div>
                </div>
              </div>

              {/* Stage Progression Workflow */}
              <div className="space-y-2">
                <div className="text-xs font-mono text-[#94A3B8] uppercase">Departmental Stage Pipeline</div>
                <div className="grid grid-cols-1 md:grid-cols-5 gap-2">
                  {m.stages.map((st, idx) => (
                    <div
                      key={idx}
                      className={`p-3 rounded-lg border text-xs font-mono ${
                        st.status === 'COMPLETED'
                          ? 'bg-[#10B981]/10 border-[#10B981]/30 text-[#10B981]'
                          : st.status === 'IN_PROGRESS'
                          ? 'bg-[#00D2FF]/10 border-[#00D2FF]/40 text-[#00D2FF] shadow-[0_0_10px_rgba(0,210,255,0.15)]'
                          : 'bg-[#020617] border-[#1E293B] text-[#64748B]'
                      }`}
                    >
                      <div className="flex items-center justify-between text-[10px] mb-1">
                        <span>STAGE 0{idx + 1}</span>
                        <span>{st.dur}</span>
                      </div>
                      <div className="font-semibold text-[#F8FAFC] line-clamp-1">{st.name}</div>
                      <div className="text-[10px] text-[#94A3B8] mt-1">Dept: {st.dept}</div>
                    </div>
                  ))}
                </div>
              </div>
            </Card>
          ))}
        </div>
      )}

      {activeTab === 'DECISIONS' && (
        <div className="space-y-3">
          {decisions.map((dec) => (
            <Card key={dec.id} className="p-4 bg-[#0F172A] border-[#1E293B] flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
              <div className="space-y-1">
                <div className="flex items-center gap-2">
                  <span className="text-sm font-bold text-[#F8FAFC]">{dec.title}</span>
                  <Badge variant="intelligence" size="sm">{dec.type}</Badge>
                </div>
                <div className="text-xs text-[#94A3B8]">{dec.rationale}</div>
                <div className="flex items-center gap-3 text-[11px] text-[#64748B] font-mono pt-1">
                  <span>Authorizer: <span className="text-[#38BDF8]">{dec.authorizer}</span></span>
                  <span>•</span>
                  <span>Affected: <span className="text-[#F8FAFC]">{dec.departments.join(', ')}</span></span>
                  <span>•</span>
                  <span>Hash: <span className="text-[#10B981]">{dec.hash}</span></span>
                </div>
              </div>
              <div className="text-xs text-[#64748B] font-mono whitespace-nowrap">{dec.time}</div>
            </Card>
          ))}
        </div>
      )}

      {activeTab === 'BARRIERS' && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {barriers.map((b) => (
            <Card key={b.id} className="p-4 bg-[#0F172A] border-[#1E293B] space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-sm font-bold text-[#F8FAFC]">{b.title}</span>
                <Badge variant={b.isReleased ? 'success' : 'warning'} size="sm">
                  {b.isReleased ? 'RELEASED' : 'WAITING_ON_BARRIER'}
                </Badge>
              </div>
              <div className="text-xs text-[#94A3B8] font-mono">
                Required Departments: <span className="text-[#F8FAFC]">{b.participating.join(', ')}</span>
              </div>
              <div className="text-xs text-[#94A3B8] font-mono">
                Arrived Departments: <span className="text-[#00D2FF]">{b.arrived.join(', ')}</span>
              </div>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
};
