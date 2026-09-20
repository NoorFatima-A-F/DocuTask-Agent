import React, { useState } from 'react';
import { Layers, Plus } from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';

export const OntologyBuilder: React.FC = () => {
  const [conceptName, setConceptName] = useState('');

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-100 flex items-center gap-2">
          <Layers className="w-7 h-7 text-cyan-400" />
          Organizational Ontology & Concept Builder
        </h1>
        <p className="text-slate-400 text-sm mt-1">
          Define custom business concepts, relational rules, and semantic hierarchy for agent reasoning.
        </p>
      </div>

      <Card className="p-5 bg-slate-900/60 border-slate-800 space-y-4">
        <h2 className="text-base font-semibold text-slate-200">Add New Business Entity</h2>
        <div className="flex gap-3">
          <input
            value={conceptName}
            onChange={(e: React.ChangeEvent<HTMLInputElement>) => setConceptName(e.target.value)}
            placeholder="e.g., Enterprise SLA Tier-1 Protocol"
            className="flex-1 px-3 py-2 bg-slate-800/80 border border-slate-700 rounded-lg text-slate-200 text-sm focus:outline-none focus:border-cyan-500"
          />
          <Button variant="intelligence">
            <span className="flex items-center gap-2">
              <Plus className="w-4 h-4" />
              Add Concept Node
            </span>
          </Button>
        </div>
      </Card>
    </div>
  );
};
