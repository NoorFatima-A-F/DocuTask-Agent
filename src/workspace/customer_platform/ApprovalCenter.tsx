import React, { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';

export const ApprovalCenter: React.FC = () => {
  const [selectedApproval, setSelectedApproval] = useState('APP-2026-001');

  const pendingApprovals = [
    {
      id: 'APP-2026-001',
      doc: 'Invoice_GlobalLogistics_INV-8891.pdf',
      type: 'Vendor Invoice',
      confidence: 0.982,
      vendor: 'Acme Global Solutions Inc.',
      amount: '$14,500.50',
      reason: 'Standard AP Fast-Track. Matched PO #PO-9912.',
    },
    {
      id: 'APP-2026-002',
      doc: 'Master_Services_Agreement_Nexus.pdf',
      type: 'Legal Contract',
      confidence: 0.945,
      vendor: 'Nexus Enterprise Corp',
      amount: 'N/A',
      reason: 'Non-standard indemnification clause detected (Page 4).',
    },
  ];

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 p-6 rounded-2xl bg-gradient-to-r from-[#0F172A] to-[#1E293B] border border-[#334155]/60 shadow-xl">
        <div>
          <Badge variant="intelligence" size="sm">HUMAN-AI COLLABORATION WORKSPACE</Badge>
          <h1 className="text-2xl font-black text-white mt-1">Supervisory Approval & Exception Center</h1>
          <p className="text-sm text-[#94A3B8]">
            Review visual bounding-box citations, resolve edge cases, and train agent policies with single-click feedback.
          </p>
        </div>
        <Badge variant="warning" size="md">2 Pending Reviews</Badge>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Approvals Queue */}
        <div className="p-5 rounded-2xl bg-[#0F172A]/80 border border-[#1E293B] shadow-xl space-y-3">
          <h2 className="text-sm font-bold text-white uppercase tracking-wider text-[#94A3B8]">
            Pending Queue
          </h2>
          <div className="space-y-2.5">
            {pendingApprovals.map((item) => (
              <div
                key={item.id}
                onClick={() => setSelectedApproval(item.id)}
                className={`p-4 rounded-xl border transition-all cursor-pointer space-y-2 ${
                  selectedApproval === item.id
                    ? 'bg-[#0066FF]/10 border-[#00D2FF] shadow-[0_0_12px_rgba(0,210,255,0.2)]'
                    : 'bg-[#0A0F1D] border-[#1E293B] hover:border-gray-600'
                }`}
              >
                <div className="flex items-center justify-between">
                  <Badge variant="default" size="sm">{item.type}</Badge>
                  <span className="text-xs font-mono text-emerald-400 font-bold">
                    {(item.confidence * 100).toFixed(1)}% Conf
                  </span>
                </div>
                <h3 className="text-xs font-bold text-white truncate">{item.doc}</h3>
                <span className="text-[11px] text-[#94A3B8] block">{item.vendor}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Detailed Document & Bounding Box Viewer */}
        <div className="lg:col-span-2 p-6 rounded-2xl bg-[#0F172A]/80 border border-[#1E293B] shadow-xl space-y-5">
          <div className="flex items-center justify-between pb-3 border-b border-[#1E293B]">
            <div>
              <h2 className="text-base font-bold text-white">Invoice_GlobalLogistics_INV-8891.pdf</h2>
              <span className="text-xs text-[#94A3B8]">Acme Global Solutions Inc. • Total: $14,500.50</span>
            </div>
            <span className="text-xs font-mono text-emerald-400 bg-emerald-950 px-2.5 py-1 rounded-lg border border-emerald-800">
              Matched PO #PO-9912
            </span>
          </div>

          {/* Synthetic Document Visualizer with Bounding Boxes */}
          <div className="p-6 rounded-xl bg-[#0A0F1D] border border-[#1E293B] space-y-4 font-mono text-xs text-[#CBD5E1]">
            <div className="p-3 rounded bg-blue-950/40 border border-blue-500/50 flex items-center justify-between">
              <span>[Bounding Box P1:L2] Vendor Name:</span>
              <span className="text-cyan-300 font-bold">Acme Global Solutions Inc. (99.8% Conf)</span>
            </div>
            <div className="p-3 rounded bg-emerald-950/40 border border-emerald-500/50 flex items-center justify-between">
              <span>[Bounding Box P1:L8] Invoice Total Amount:</span>
              <span className="text-emerald-300 font-bold">$14,500.50 USD (99.5% Conf)</span>
            </div>
            <div className="p-3 rounded bg-purple-950/40 border border-purple-500/50 flex items-center justify-between">
              <span>[Bounding Box P1:L15] 3-Way NetSuite Match:</span>
              <span className="text-purple-300 font-bold">PO-9912 Verified (100.0% Match)</span>
            </div>
          </div>

          {/* Reviewer Action Buttons */}
          <div className="flex flex-col sm:flex-row gap-3 pt-2">
            <Button variant="primary" size="md" className="w-full sm:w-auto flex-1 bg-emerald-600 hover:bg-emerald-500">
              ✓ Approve &amp; Post to ERP
            </Button>
            <Button variant="secondary" size="md" className="w-full sm:w-auto flex-1">
              ✏️ Edit Extracted Fields
            </Button>
            <Button variant="outline" size="md" className="w-full sm:w-auto text-rose-400 border-rose-800/60 hover:bg-rose-950/30">
              ✕ Reject Invoice
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
};
