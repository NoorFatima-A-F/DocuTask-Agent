import React, { useState } from 'react';
import {
  FileCheck,
  Play,
  Layers,
} from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';

export const DecisionRulesStudio: React.FC = () => {
  const [testAmount, setTestAmount] = useState<number>(45000);
  const [testTier, setTestTier] = useState<string>('TIER_1');
  const [evaluatedAction, setEvaluatedAction] = useState<string>('ROUTE_MANAGER_APPROVAL');

  const handleEvaluate = () => {
    if (testAmount < 1000 && testTier === 'TIER_1') {
      setEvaluatedAction('AUTO_APPROVE (Micro-invoice Policy)');
    } else if (testAmount >= 50000) {
      setEvaluatedAction('ROUTE_CFO_APPROVAL (Executive Threshold)');
    } else {
      setEvaluatedAction('ROUTE_MANAGER_APPROVAL (Standard Review)');
    }
  };

  const rules = [
    { id: 'rule_1', name: 'Micro Invoice Auto-Approval', condition: 'amount < $1,000 & Tier-1', action: 'AUTO_APPROVE', priority: 1 },
    { id: 'rule_2', name: 'Standard Manager Review', condition: '$1,000 <= amount < $50,000', action: 'ROUTE_MANAGER_APPROVAL', priority: 2 },
    { id: 'rule_3', name: 'Executive CFO Sign-off', condition: 'amount >= $50,000', action: 'ROUTE_CFO_APPROVAL', priority: 3 },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-slate-900/60 p-6 rounded-2xl border border-slate-800 backdrop-blur-md">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-indigo-500/10 rounded-xl border border-indigo-500/20 text-indigo-400">
            <FileCheck className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-white">Enterprise Decision Rules Studio</h1>
            <p className="text-sm text-slate-400">
              DMN-style decision tables, conditional routing rules, and financial approval thresholds
            </p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Decision Tables View */}
        <Card className="lg:col-span-2 p-6 bg-slate-900/40 border-slate-800 space-y-4">
          <h2 className="text-base font-semibold text-white flex items-center gap-2">
            <Layers className="w-4 h-4 text-indigo-400" />
            Decision Table: Invoice Financial Approval Policy
          </h2>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs font-mono text-slate-300">
              <thead className="bg-slate-800/60 uppercase text-slate-400 border-b border-slate-700">
                <tr>
                  <th className="py-3 px-4">Priority</th>
                  <th className="py-3 px-4">Rule Name</th>
                  <th className="py-3 px-4">Condition Expression</th>
                  <th className="py-3 px-4">Action Decision</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60">
                {rules.map((r) => (
                  <tr key={r.id} className="hover:bg-slate-800/30">
                    <td className="py-3 px-4 text-indigo-400 font-bold">#{r.priority}</td>
                    <td className="py-3 px-4 font-sans font-medium text-white">{r.name}</td>
                    <td className="py-3 px-4 text-slate-300">{r.condition}</td>
                    <td className="py-3 px-4">
                      <Badge variant="intelligence">{r.action}</Badge>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </Card>

        {/* Live Policy Test Sandbox */}
        <Card className="lg:col-span-1 p-6 bg-slate-900/60 border-slate-800 space-y-4">
          <h2 className="text-base font-bold text-white border-b border-slate-800 pb-3">
            Interactive Policy Sandbox
          </h2>

          <div className="space-y-3 text-xs">
            <div>
              <label className="block text-slate-400 mb-1">Invoice Amount ($)</label>
              <input
                type="number"
                value={testAmount}
                onChange={(e) => setTestAmount(Number(e.target.value))}
                className="w-full bg-slate-800 border border-slate-700 text-white rounded-lg p-2.5 text-xs"
              />
            </div>

            <div>
              <label className="block text-slate-400 mb-1">Vendor Tier</label>
              <select
                value={testTier}
                onChange={(e) => setTestTier(e.target.value)}
                className="w-full bg-slate-800 border border-slate-700 text-white rounded-lg p-2.5 text-xs"
              >
                <option value="TIER_1">Tier 1 (Strategic Partner)</option>
                <option value="TIER_2">Tier 2 (Standard Vendor)</option>
                <option value="TIER_3">Tier 3 (New / High Risk)</option>
              </select>
            </div>

            <Button variant="intelligence" className="w-full" onClick={handleEvaluate}>
              <span className="flex items-center justify-center gap-2">
                <Play className="w-4 h-4" /> Evaluate Decision
              </span>
            </Button>

            <div className="pt-3 border-t border-slate-800">
              <span className="text-slate-400 block mb-1">Evaluated Action:</span>
              <div className="p-3 bg-slate-800/60 rounded-xl border border-indigo-500/40 font-mono text-emerald-300 font-bold text-xs">
                {evaluatedAction}
              </div>
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
};
