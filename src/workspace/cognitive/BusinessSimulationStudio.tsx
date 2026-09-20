import React, { useState } from 'react';
import { Play, TrendingUp, Sliders } from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { cognitiveApiClient } from '../../services/cognitiveApiClient';
import { SimulationScenario } from '../../types/cognitive';

export const BusinessSimulationStudio: React.FC = () => {
  const [scenarioName, setScenarioName] = useState('Switch Document Classification from Pro to Flash Model');
  const [selectedModel, setSelectedModel] = useState('gemini-1.5-flash');
  const [scenario, setScenario] = useState<SimulationScenario | null>(null);
  const [simulating, setSimulating] = useState(false);

  const handleSimulate = async () => {
    setSimulating(true);
    try {
      const res = await cognitiveApiClient.simulate(scenarioName, { model: selectedModel });
      setScenario(res);
    } finally {
      setSimulating(false);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-100 flex items-center gap-2">
          <TrendingUp className="w-7 h-7 text-cyan-400" />
          Autonomous Business & Architecture Simulation Studio
        </h1>
        <p className="text-slate-400 text-sm mt-1">
          Perform multi-variable "what-if" simulations over model upgrades, concurrency limits, latency, and ROI scaling.
        </p>
      </div>

      <Card className="p-5 bg-slate-900/60 border-slate-800 space-y-4">
        <div className="space-y-3">
          <label className="text-xs font-semibold text-slate-400 uppercase">Simulation Scenario Hypothesis</label>
          <input
            value={scenarioName}
            onChange={(e: React.ChangeEvent<HTMLInputElement>) => setScenarioName(e.target.value)}
            className="w-full px-3 py-2 bg-slate-800/80 border border-slate-700 rounded-lg text-slate-200 text-sm focus:outline-none focus:border-cyan-500"
          />
        </div>

        <div className="flex flex-wrap items-center justify-between pt-2 border-t border-slate-800">
          <div className="flex items-center gap-3">
            <Sliders className="w-4 h-4 text-slate-400" />
            <span className="text-xs text-slate-400">Target Model Parameter:</span>
            {['gemini-1.5-flash', 'gemini-1.5-pro', 'claude-3-5-sonnet', 'gpt-4o'].map((m) => (
              <Button
                key={m}
                variant={selectedModel === m ? 'primary' : 'outline'}
                size="sm"
                onClick={() => setSelectedModel(m)}
              >
                {m}
              </Button>
            ))}
          </div>

          <Button variant="intelligence" onClick={handleSimulate} disabled={simulating}>
            <span className="flex items-center gap-2">
              <Play className="w-4 h-4" />
              {simulating ? 'Simulating...' : 'Run Simulation'}
            </span>
          </Button>
        </div>
      </Card>

      {scenario && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <Card className="p-5 bg-slate-900/60 border-slate-800">
            <span className="text-xs text-slate-400 uppercase font-semibold">Projected Latency Impact</span>
            <p className="text-2xl font-bold text-emerald-400 mt-2">{scenario.projected_latency_change_pct}%</p>
            <p className="text-xs text-slate-400 mt-1">Expected reduction in cycle time</p>
          </Card>
          <Card className="p-5 bg-slate-900/60 border-slate-800">
            <span className="text-xs text-slate-400 uppercase font-semibold">Projected Token Cost Impact</span>
            <p className="text-2xl font-bold text-cyan-400 mt-2">{scenario.projected_cost_change_pct}%</p>
            <p className="text-xs text-slate-400 mt-1">Monthly cloud expenditure delta</p>
          </Card>
          <Card className="p-5 bg-slate-900/60 border-slate-800">
            <span className="text-xs text-slate-400 uppercase font-semibold">Projected Business ROI Factor</span>
            <p className="text-2xl font-bold text-indigo-400 mt-2">{scenario.projected_roi_factor}x</p>
            <p className="text-xs text-slate-400 mt-1">Efficiency multiplier score</p>
          </Card>
        </div>
      )}
    </div>
  );
};
