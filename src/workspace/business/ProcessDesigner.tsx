import React, { useState } from 'react';
import {
  Workflow,
  Plus,
  ArrowRight,
  Clock,
  Layers,
  CheckCircle,
} from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';

export const ProcessDesigner: React.FC = () => {
  const [steps, setSteps] = useState([
    { id: 'step_1', name: 'Multimodal OCR Data Extraction', type: 'TASK', dept: 'Finance', sla: '60s' },
    { id: 'step_2', name: 'Tax & Compliance Audit', type: 'TASK', dept: 'Finance', sla: '120s' },
    { id: 'step_3', name: 'Threshold Routing Gateway', type: 'GATEWAY_EXCLUSIVE', dept: 'Finance', sla: '10s' },
    { id: 'step_4', name: 'Manager Approval Gate', type: 'HUMAN_APPROVAL', dept: 'Finance', sla: '30m' },
    { id: 'step_5', name: 'SAP ERP Ledger Entry', type: 'TASK', dept: 'Finance', sla: '180s' },
  ]);
  const [selectedStep, setSelectedStep] = useState(steps[0]);
  const [feedback, setFeedback] = useState<string | null>(null);

  const handleAddStep = () => {
    const newStep = {
      id: `step_${steps.length + 1}`,
      name: `Automated Verification Gate #${steps.length + 1}`,
      type: 'TASK',
      dept: 'Finance',
      sla: '90s',
    };
    setSteps([...steps, newStep]);
    setSelectedStep(newStep);
    setFeedback(`Added step "${newStep.name}" to process graph.`);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-slate-900/60 p-6 rounded-2xl border border-slate-800 backdrop-blur-md">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-indigo-500/10 rounded-xl border border-indigo-500/20 text-indigo-400">
            <Workflow className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-white">BPMN Process Designer</h1>
            <p className="text-sm text-slate-400">
              Visual business process canvas with tasks, gateways, human gates, and SLA contracts
            </p>
          </div>
        </div>

        <Button variant="intelligence" onClick={handleAddStep}>
          <span className="flex items-center gap-2">
            <Plus className="w-4 h-4" /> Add Workflow Node
          </span>
        </Button>
      </div>

      {feedback && (
        <div className="p-4 bg-emerald-500/10 border border-emerald-500/20 rounded-xl text-emerald-300 text-sm flex items-center justify-between">
          <div className="flex items-center gap-2">
            <CheckCircle className="w-4 h-4" />
            <span>{feedback}</span>
          </div>
          <button
            onClick={() => setFeedback(null)}
            className="text-xs text-emerald-400 hover:text-emerald-200 underline"
          >
            Dismiss
          </button>
        </div>
      )}

      {/* Visual Canvas and Inspector */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Canvas Pipeline */}
        <Card className="lg:col-span-2 p-6 bg-slate-900/40 border-slate-800 space-y-4">
          <h2 className="text-base font-semibold text-white flex items-center gap-2">
            <Layers className="w-4 h-4 text-indigo-400" />
            Executable Business Process Graph
          </h2>

          <div className="space-y-3 pt-2">
            {steps.map((s, idx) => {
              const isSelected = selectedStep?.id === s.id;
              return (
                <div key={s.id} className="space-y-3">
                  <div
                    onClick={() => setSelectedStep(s)}
                    className={`p-4 rounded-xl border cursor-pointer transition-all flex items-center justify-between ${
                      isSelected
                        ? 'bg-slate-800/90 border-indigo-500 shadow-md'
                        : 'bg-slate-900/60 border-slate-800 hover:border-slate-700'
                    }`}
                  >
                    <div className="flex items-center gap-3">
                      <span className="w-6 h-6 rounded-full bg-slate-800 border border-slate-700 flex items-center justify-center text-xs font-mono text-indigo-300">
                        {idx + 1}
                      </span>
                      <div>
                        <span className="font-bold text-white text-sm block">{s.name}</span>
                        <span className="text-xs text-slate-400 font-mono">Department: {s.dept}</span>
                      </div>
                    </div>

                    <div className="flex items-center gap-3">
                      <Badge
                        variant={
                          s.type === 'HUMAN_APPROVAL'
                            ? 'warning'
                            : s.type === 'GATEWAY_EXCLUSIVE'
                            ? 'intelligence'
                            : 'default'
                        }
                      >
                        {s.type}
                      </Badge>
                      <span className="text-xs text-amber-400 font-mono flex items-center gap-1">
                        <Clock className="w-3.5 h-3.5" /> {s.sla}
                      </span>
                    </div>
                  </div>

                  {idx < steps.length - 1 && (
                    <div className="flex justify-center">
                      <ArrowRight className="w-4 h-4 text-slate-600 rotate-90" />
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </Card>

        {/* Node Inspector */}
        <Card className="lg:col-span-1 p-6 bg-slate-900/60 border-slate-800 space-y-4">
          <h2 className="text-base font-bold text-white border-b border-slate-800 pb-3">
            Node Configuration
          </h2>

          {selectedStep ? (
            <div className="space-y-4 text-xs">
              <div>
                <label className="block text-slate-400 mb-1">Step Name</label>
                <input
                  type="text"
                  value={selectedStep.name}
                  onChange={(e) => {
                    const updated = { ...selectedStep, name: e.target.value };
                    setSelectedStep(updated);
                    setSteps(steps.map((st) => (st.id === updated.id ? updated : st)));
                  }}
                  className="w-full bg-slate-800 border border-slate-700 text-white rounded-lg p-2.5 text-xs"
                />
              </div>

              <div>
                <label className="block text-slate-400 mb-1">Node Type</label>
                <select
                  value={selectedStep.type}
                  onChange={(e) => {
                    const updated = { ...selectedStep, type: e.target.value };
                    setSelectedStep(updated);
                    setSteps(steps.map((st) => (st.id === updated.id ? updated : st)));
                  }}
                  className="w-full bg-slate-800 border border-slate-700 text-white rounded-lg p-2.5 text-xs"
                >
                  <option value="TASK">Standard Agent Task</option>
                  <option value="GATEWAY_EXCLUSIVE">Exclusive Decision Gateway (XOR)</option>
                  <option value="GATEWAY_PARALLEL">Parallel Fork / Join Gateway (AND)</option>
                  <option value="HUMAN_APPROVAL">Human-in-the-Loop Approval Gate</option>
                </select>
              </div>

              <div>
                <label className="block text-slate-400 mb-1">Target SLA Duration</label>
                <input
                  type="text"
                  value={selectedStep.sla}
                  onChange={(e) => {
                    const updated = { ...selectedStep, sla: e.target.value };
                    setSelectedStep(updated);
                    setSteps(steps.map((st) => (st.id === updated.id ? updated : st)));
                  }}
                  className="w-full bg-slate-800 border border-slate-700 text-white rounded-lg p-2.5 text-xs"
                />
              </div>

              <div className="pt-2 border-t border-slate-800">
                <span className="text-slate-400 block mb-1">BPMN Validation</span>
                <span className="text-emerald-400 font-mono text-[11px] flex items-center gap-1.5">
                  <CheckCircle className="w-3.5 h-3.5" /> Syntax & Sagas Validated
                </span>
              </div>
            </div>
          ) : (
            <p className="text-slate-500 italic text-xs">Select a node to configure properties.</p>
          )}
        </Card>
      </div>
    </div>
  );
};
