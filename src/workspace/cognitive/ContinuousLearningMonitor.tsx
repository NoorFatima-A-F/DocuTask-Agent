import React from 'react';
import { Activity, ShieldCheck, BookOpen } from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';

export const ContinuousLearningMonitor: React.FC = () => {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-100 flex items-center gap-2">
          <Activity className="w-7 h-7 text-emerald-400" />
          Continuous Learning & Model Adaptation Pipeline
        </h1>
        <p className="text-slate-400 text-sm mt-1">
          Online learning loop updating policies, prompt libraries, and routing strategies without modifying foundation weights.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card className="p-5 bg-slate-900/60 border-slate-800 space-y-3">
          <BookOpen className="w-6 h-6 text-indigo-400" />
          <h3 className="text-base font-semibold text-slate-200">User Corrections Loop</h3>
          <p className="text-xs text-slate-400">
            Automatically distilled into procedural memory rules with instant policy propagation.
          </p>
          <Badge variant="success">Active Online</Badge>
        </Card>

        <Card className="p-5 bg-slate-900/60 border-slate-800 space-y-3">
          <ShieldCheck className="w-6 h-6 text-cyan-400" />
          <h3 className="text-base font-semibold text-slate-200">Evaluation Regressions</h3>
          <p className="text-xs text-slate-400">
            Autonomous rollback and canary isolation whenever prompt drift exceeds 1.5%.
          </p>
          <Badge variant="outline" className="text-cyan-400 border-cyan-500/30">Guarded</Badge>
        </Card>

        <Card className="p-5 bg-slate-900/60 border-slate-800 space-y-3">
          <Activity className="w-6 h-6 text-emerald-400" />
          <h3 className="text-base font-semibold text-slate-200">Trace Distillation</h3>
          <p className="text-xs text-slate-400">
            High-efficiency execution traces promoted to enterprise experience memory automatically.
          </p>
          <Badge variant="success">100% Convergence</Badge>
        </Card>
      </div>
    </div>
  );
};
