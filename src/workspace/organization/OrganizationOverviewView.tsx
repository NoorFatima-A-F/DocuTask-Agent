import React, { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';

export const OrganizationOverviewView: React.FC = () => {
  const [selectedDept, setSelectedDept] = useState<string | null>(null);

  const departments = [
    {
      id: 'dept_executive',
      name: 'Executive Coordination & Strategy',
      head: 'Chief Executive Agent',
      workers: 2,
      concurrency: 8,
      queue: 1,
      health: 99.2,
      budget: '$50.00',
      spent: '$2.14',
      status: 'ACTIVE',
      slaTarget: '100 ms',
      responsibilities: ['Mission intake & portfolio arbitration', 'Organization-wide budgeting', 'Root escalation handling'],
    },
    {
      id: 'dept_ocr',
      name: 'Optical Perception & Ingestion',
      head: 'Lead Vision Agent',
      workers: 4,
      concurrency: 12,
      queue: 3,
      health: 96.5,
      budget: '$30.00',
      spent: '$4.82',
      status: 'ACTIVE',
      slaTarget: '250 ms',
      responsibilities: ['Multi-format document ingestion', 'Bilateral filter de-skewing', 'LayoutLM token bounding boxes'],
    },
    {
      id: 'dept_extraction',
      name: 'Structured Intelligence & Extraction',
      head: 'Lead Extraction Specialist',
      workers: 6,
      concurrency: 20,
      queue: 4,
      health: 98.1,
      budget: '$80.00',
      spent: '$12.45',
      status: 'ACTIVE',
      slaTarget: '600 ms',
      responsibilities: ['Key-value entity resolution', 'Line-item table parsing', 'Pareto model routing (Flash vs Pro)'],
    },
    {
      id: 'dept_validation',
      name: 'Mathematical & Invariant Validation',
      head: 'Lead Verification Auditor',
      workers: 3,
      concurrency: 16,
      queue: 1,
      health: 99.8,
      budget: '$20.00',
      spent: '$1.12',
      status: 'ACTIVE',
      slaTarget: '80 ms',
      responsibilities: ['Subtotal + Tax == Total verification', 'Zero-Fabrication bounding-box checks', 'Z3 SMT solver proving'],
    },
    {
      id: 'dept_memory',
      name: 'Enterprise Memory & Context',
      head: 'Chief Knowledge Custodian',
      workers: 2,
      concurrency: 10,
      queue: 0,
      health: 99.5,
      budget: '$25.00',
      spent: '$1.95',
      status: 'ACTIVE',
      slaTarget: '50 ms',
      responsibilities: ['Vector similarity lookup', 'Vendor historical graph indexing', 'Episodic memory recall'],
    },
    {
      id: 'dept_research',
      name: 'Research & Policy Synthesis',
      head: 'Director of Autonomous Research',
      workers: 2,
      concurrency: 6,
      queue: 1,
      health: 97.4,
      budget: '$40.00',
      spent: '$5.60',
      status: 'ACTIVE',
      slaTarget: '1200 ms',
      responsibilities: ['Counterfactual digital twin replays', 'Causal graph discovery', 'Prompt adaptation benchmarking'],
    },
    {
      id: 'dept_governance',
      name: 'Corporate Governance & Compliance',
      head: 'Chief Governance Officer',
      workers: 2,
      concurrency: 8,
      queue: 0,
      health: 100.0,
      budget: '$15.00',
      spent: '$0.85',
      status: 'ACTIVE',
      slaTarget: '75 ms',
      responsibilities: ['Dual-key cryptographic sign-off', 'ED25519 audit trail vaulting', 'Data privacy policy enforcement'],
    },
    {
      id: 'dept_qa',
      name: 'Continuous Quality Assurance',
      head: 'Lead QA Sentinel',
      workers: 3,
      concurrency: 12,
      queue: 2,
      health: 98.9,
      budget: '$30.00',
      spent: '$3.40',
      status: 'ACTIVE',
      slaTarget: '150 ms',
      responsibilities: ['Corpus-wide benchmark scoring', 'Confidence calibration & ECE', 'Data distribution drift detection'],
    },
  ];

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 p-5 rounded-2xl bg-[#0F172A] border border-[#1E293B] shadow-xl">
        <div>
          <div className="flex items-center gap-2">
            <span className="text-2xl">🏛️</span>
            <h2 className="text-xl font-bold text-[#F8FAFC]">Autonomous Enterprise Organization (AMAEOP)</h2>
            <Badge variant="intelligence" size="sm">Phase 7 Live Digital Org</Badge>
          </div>
          <p className="text-sm text-[#94A3B8] mt-1">
            Enterprise multi-agent organization with specialized departmental hierarchy, resource ownership, and autonomous governance.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <div className="text-right">
            <div className="text-xs text-[#94A3B8]">Organization Health Index</div>
            <div className="text-lg font-bold font-mono text-[#10B981]">98.7% (Tier 1 Optimal)</div>
          </div>
          <div className="w-px h-8 bg-[#1E293B]" />
          <div className="text-right">
            <div className="text-xs text-[#94A3B8]">Active AI Workforce</div>
            <div className="text-lg font-bold font-mono text-[#00D2FF]">24 Agents (8 Depts)</div>
          </div>
        </div>
      </div>

      {/* Organizational KPIs Strip */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <Card className="p-4 bg-[#0F172A]/80 border-[#1E293B]">
          <div className="text-xs font-mono text-[#94A3B8] uppercase">Macro SLA Compliance</div>
          <div className="text-2xl font-bold font-mono text-[#10B981] mt-1">99.7%</div>
          <div className="text-[11px] text-[#64748B] mt-1">Target: &gt; 99.0%</div>
        </Card>
        <Card className="p-4 bg-[#0F172A]/80 border-[#1E293B]">
          <div className="text-xs font-mono text-[#94A3B8] uppercase">Zero-Fabrication Rate</div>
          <div className="text-2xl font-bold font-mono text-[#00D2FF] mt-1">100.0%</div>
          <div className="text-[11px] text-[#64748B] mt-1">Invariant-verified arithmetic</div>
        </Card>
        <Card className="p-4 bg-[#0F172A]/80 border-[#1E293B]">
          <div className="text-xs font-mono text-[#94A3B8] uppercase">Total Org Budget</div>
          <div className="text-2xl font-bold font-mono text-[#F59E0B] mt-1">$290.00</div>
          <div className="text-[11px] text-[#64748B] mt-1">Spent: $32.33 (11.1% burn)</div>
        </Card>
        <Card className="p-4 bg-[#0F172A]/80 border-[#1E293B]">
          <div className="text-xs font-mono text-[#94A3B8] uppercase">Queued Workload</div>
          <div className="text-2xl font-bold font-mono text-[#A855F7] mt-1">12 Tasks</div>
          <div className="text-[11px] text-[#64748B] mt-1">Max cluster depth: 92 slots</div>
        </Card>
      </div>

      {/* Department Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {departments.map((dept) => {
          const isSelected = selectedDept === dept.id;
          return (
            <div
              key={dept.id}
              onClick={() => setSelectedDept(isSelected ? null : dept.id)}
              className={`p-4 rounded-xl border transition-all cursor-pointer flex flex-col justify-between ${
                isSelected
                  ? 'bg-[#131D35] border-[#00D2FF] shadow-[0_0_15px_rgba(0,210,255,0.2)]'
                  : 'bg-[#0F172A] border-[#1E293B] hover:border-[#334155]'
              }`}
            >
              <div>
                <div className="flex items-center justify-between gap-2">
                  <span className="text-xs font-mono font-bold text-[#F8FAFC] truncate">{dept.name}</span>
                  <Badge variant={dept.health >= 98 ? 'success' : 'warning'} size="sm">
                    {dept.health}%
                  </Badge>
                </div>

                <div className="text-[11px] text-[#94A3B8] mt-1">
                  Head: <span className="text-[#38BDF8] font-medium">{dept.head}</span>
                </div>

                <div className="grid grid-cols-2 gap-2 mt-3 pt-3 border-t border-[#1E293B]/60 text-xs font-mono">
                  <div>
                    <span className="text-[#64748B] text-[10px] block">AGENTS / SLOTS</span>
                    <span className="text-[#F8FAFC]">{dept.workers} / {dept.concurrency}</span>
                  </div>
                  <div>
                    <span className="text-[#64748B] text-[10px] block">QUEUE DEPTH</span>
                    <span className="text-[#F59E0B]">{dept.queue} items</span>
                  </div>
                  <div>
                    <span className="text-[#64748B] text-[10px] block">SLA TARGET</span>
                    <span className="text-[#10B981]">{dept.slaTarget}</span>
                  </div>
                  <div>
                    <span className="text-[#64748B] text-[10px] block">BUDGET SPENT</span>
                    <span className="text-[#CBD5E1]">{dept.spent} / {dept.budget}</span>
                  </div>
                </div>
              </div>

              <div className="mt-3 pt-2 border-t border-[#1E293B]/40">
                <div className="text-[10px] text-[#64748B] uppercase font-mono mb-1">Key Responsibility</div>
                <div className="text-[11px] text-[#94A3B8] line-clamp-1">
                  {dept.responsibilities[0]}
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Selected Department Deep-Dive Drawer */}
      {selectedDept && (
        <Card className="p-5 bg-[#0F172A] border-[#00D2FF]/40 animate-fadeIn">
          {(() => {
            const d = departments.find((dept) => dept.id === selectedDept)!;
            return (
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <span className="text-lg font-bold text-[#F8FAFC]">{d.name}</span>
                    <Badge variant="intelligence" size="sm">{d.id}</Badge>
                  </div>
                  <button
                    onClick={() => setSelectedDept(null)}
                    className="text-xs text-[#94A3B8] hover:text-[#F8FAFC] font-mono px-2 py-1 rounded bg-[#1E293B]"
                  >
                    ✕ Close
                  </button>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div className="p-3 rounded-lg bg-[#020617] border border-[#1E293B]">
                    <div className="text-xs font-mono text-[#94A3B8] uppercase">Department Leadership</div>
                    <div className="text-sm font-semibold text-[#38BDF8] mt-1">{d.head}</div>
                    <div className="text-xs text-[#64748B] mt-1">Autonomous decision authority under Delegation Policy</div>
                  </div>

                  <div className="p-3 rounded-lg bg-[#020617] border border-[#1E293B]">
                    <div className="text-xs font-mono text-[#94A3B8] uppercase">SLA & Health Governance</div>
                    <div className="text-sm font-semibold text-[#10B981] mt-1">{d.health}% Operational Health</div>
                    <div className="text-xs text-[#64748B] mt-1">Target latency ceiling: {d.slaTarget}</div>
                  </div>

                  <div className="p-3 rounded-lg bg-[#020617] border border-[#1E293B]">
                    <div className="text-xs font-mono text-[#94A3B8] uppercase">Fiscal Allocation</div>
                    <div className="text-sm font-semibold text-[#F59E0B] mt-1">{d.spent} spent of {d.budget}</div>
                    <div className="text-xs text-[#64748B] mt-1">Vickrey Auction bidding credits active</div>
                  </div>
                </div>

                <div>
                  <div className="text-xs font-mono text-[#94A3B8] uppercase mb-2">Charter & Responsibilities</div>
                  <ul className="grid grid-cols-1 md:grid-cols-2 gap-2 text-xs text-[#CBD5E1]">
                    {d.responsibilities.map((resp, idx) => (
                      <li key={idx} className="flex items-center gap-2 p-2 rounded bg-[#020617]/50 border border-[#1E293B]/60">
                        <span className="text-[#00D2FF]">✓</span>
                        <span>{resp}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            );
          })()}
        </Card>
      )}
    </div>
  );
};
