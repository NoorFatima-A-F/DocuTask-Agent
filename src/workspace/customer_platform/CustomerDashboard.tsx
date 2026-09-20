import React, { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';

export const CustomerDashboard: React.FC = () => {
  const [selectedTenant, setSelectedTenant] = useState('Apex Global Financial');

  const stats = [
    { label: 'Documents Processed (30D)', value: '125,400', change: '+14.2%', color: 'from-blue-500 to-cyan-500' },
    { label: 'Straight-Through Processing', value: '91.5%', change: '+8.5%', color: 'from-emerald-500 to-teal-500' },
    { label: 'Labor Liberated', value: '4,790 hrs', change: '+18.0%', color: 'from-purple-500 to-indigo-500' },
    { label: 'Net Annual Savings', value: '$2,280,000', change: '4.2x ROI', color: 'from-amber-500 to-orange-500' },
  ];

  const liveFeeds = [
    { id: 'EVT-901', time: '10s ago', doc: 'INV-2026-8891.pdf', tenant: 'Apex Global Financial', status: 'STP_APPROVED', amount: '$14,500.50' },
    { id: 'EVT-902', time: '42s ago', doc: 'Resume_Rivera_AI.pdf', tenant: 'TalentPulse Staffing', status: 'SHORTLISTED', amount: '96.5% match' },
    { id: 'EVT-903', time: '1m ago', doc: 'MSA_Nexus_Final.pdf', tenant: 'Lexis Legal Partners', status: 'FLAGGED_HITL', amount: 'Indemnity Risk' },
    { id: 'EVT-904', time: '2m ago', doc: 'Auth_M54_Lumbar.pdf', tenant: 'BioHealth Integrated', status: 'AUTHORIZED', amount: 'ICD-10 M54.5' },
  ];

  return (
    <div className="space-y-6">
      {/* Top Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 p-6 rounded-2xl bg-gradient-to-r from-[#0F172A] to-[#1E293B] border border-[#334155]/60 shadow-xl">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <Badge variant="intelligence" size="sm">ENTERPRISE PLATINUM TENANT</Badge>
            <span className="text-xs text-[#94A3B8]">SOC2 Type II & HIPAA Verified</span>
          </div>
          <h1 className="text-2xl font-black text-white tracking-tight">
            Customer Operations & Value Center
          </h1>
          <p className="text-sm text-[#94A3B8] mt-0.5">
            Real-time multi-agent autonomous document operations across active business units.
          </p>
        </div>
        <div className="flex items-center gap-3">
          <select
            aria-label="Active Organization"
            value={selectedTenant}
            onChange={(e) => setSelectedTenant(e.target.value)}
            className="bg-[#0A0F1D] text-[#F8FAFC] text-sm border border-[#334155] rounded-xl px-4 py-2.5 outline-none focus:border-[#00D2FF]"
          >
            <option>Apex Global Financial</option>
            <option>BioHealth Integrated</option>
            <option>TalentPulse Staffing</option>
            <option>Lexis Legal Partners</option>
          </select>
          <Button variant="primary" size="md">
            + New Automation
          </Button>
        </div>
      </div>

      {/* KPI Cards Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {stats.map((stat, i) => (
          <div key={i} className="p-5 rounded-xl bg-[#0F172A]/80 border border-[#1E293B] shadow-lg relative overflow-hidden">
            <div className={`absolute -right-6 -bottom-6 w-24 h-24 rounded-full bg-gradient-to-br ${stat.color} opacity-10 blur-xl`} />
            <span className="text-xs text-[#94A3B8] font-medium block mb-1">{stat.label}</span>
            <div className="flex items-baseline justify-between">
              <span className="text-2xl font-black text-white">{stat.value}</span>
              <span className="text-xs font-bold text-emerald-400 bg-emerald-950/60 px-2 py-0.5 rounded-full border border-emerald-800/40">
                {stat.change}
              </span>
            </div>
          </div>
        ))}
      </div>

      {/* Real-Time Live Feed & Active Pipelines */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 p-6 rounded-2xl bg-[#0F172A]/80 border border-[#1E293B] shadow-xl">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-base font-bold text-white flex items-center gap-2">
              <span className="h-2 w-2 rounded-full bg-emerald-400 animate-ping" />
              Live Autonomous Execution Feed
            </h2>
            <Badge variant="outline" size="sm">Real-time Telemetry</Badge>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs text-[#94A3B8]">
              <thead className="bg-[#0A0F1D]/60 text-[#CBD5E1] uppercase font-mono border-b border-[#1E293B]">
                <tr>
                  <th className="py-2.5 px-3">Time</th>
                  <th className="py-2.5 px-3">Document</th>
                  <th className="py-2.5 px-3">Organization</th>
                  <th className="py-2.5 px-3">Outcome</th>
                  <th className="py-2.5 px-3">Details</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[#1E293B]">
                {liveFeeds.map((feed) => (
                  <tr key={feed.id} className="hover:bg-[#1E293B]/40 transition-colors">
                    <td className="py-3 px-3 font-mono text-gray-400">{feed.time}</td>
                    <td className="py-3 px-3 font-medium text-white">{feed.doc}</td>
                    <td className="py-3 px-3 text-[#94A3B8]">{feed.tenant}</td>
                    <td className="py-3 px-3">
                      <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                        feed.status === 'STP_APPROVED' || feed.status === 'AUTHORIZED' || feed.status === 'SHORTLISTED'
                          ? 'bg-emerald-950 text-emerald-400 border border-emerald-800/40'
                          : 'bg-amber-950 text-amber-400 border border-amber-800/40'
                      }`}>
                        {feed.status}
                      </span>
                    </td>
                    <td className="py-3 px-3 text-white font-mono">{feed.amount}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Integration Status Quick View */}
        <div className="p-6 rounded-2xl bg-[#0F172A]/80 border border-[#1E293B] shadow-xl space-y-4">
          <h2 className="text-base font-bold text-white">Connected Enterprise Systems</h2>
          <div className="space-y-2.5">
            {[
              { name: 'Microsoft 365 Exchange', category: 'Inbound Invoices', status: 'Healthy (28ms)' },
              { name: 'Intuit QuickBooks Online', category: 'General Ledger Sync', status: 'Healthy (64ms)' },
              { name: 'Slack Enterprise Grid', category: 'HITL Notifications', status: 'Active (18ms)' },
              { name: 'Salesforce CRM', category: 'Contract Attachments', status: 'Synced (48ms)' },
            ].map((conn, idx) => (
              <div key={idx} className="p-3 rounded-xl bg-[#0A0F1D] border border-[#1E293B] flex items-center justify-between">
                <div>
                  <span className="text-xs font-semibold text-white block">{conn.name}</span>
                  <span className="text-[10px] text-[#94A3B8]">{conn.category}</span>
                </div>
                <span className="text-[10px] font-mono text-emerald-400 bg-emerald-950/40 px-2 py-0.5 rounded border border-emerald-800/30">
                  {conn.status}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
