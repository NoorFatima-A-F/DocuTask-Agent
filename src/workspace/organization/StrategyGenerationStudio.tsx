import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import {
  Compass,
  RotateCw,
  Sparkles,
  Activity,
  CheckCircle2,
  ListOrdered,
} from 'lucide-react';
import { organizationPlatformApiClient } from '../../services/organizationPlatformApiClient';
import type { StrategyPlan } from '../../types/organizationPlatform';

export const StrategyGenerationStudio: React.FC = () => {
  const [strategies, setStrategies] = useState<StrategyPlan[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [generating, setGenerating] = useState<boolean>(false);
  const [evaluating, setEvaluating] = useState<boolean>(false);
  const [selectedStrategy, setSelectedStrategy] = useState<StrategyPlan | null>(null);
  const [simulationResult, setSimulationResult] = useState<Record<string, any> | null>(null);

  const loadStrategies = async () => {
    try {
      setLoading(true);
      const data = await organizationPlatformApiClient.getStrategies('msn_reduce_cost_40pct');
      setStrategies(data);
      if (data.length > 0 && !selectedStrategy) {
        setSelectedStrategy(data[0] || null);
      }
    } catch (err) {
      console.error('Failed to load strategies:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadStrategies();
  }, []);

  const handleGenerate = async () => {
    try {
      setGenerating(true);
      const created = await organizationPlatformApiClient.generateStrategies('msn_reduce_cost_40pct', 3);
      setStrategies(created);
      if (created.length > 0) setSelectedStrategy(created[0] || null);
    } catch (err) {
      console.error('Error generating strategies:', err);
    } finally {
      setGenerating(false);
    }
  };

  const handleRunMonteCarlo = async (strategyId: string) => {
    try {
      setEvaluating(true);
      const res = await fetch(`/api/v1/organization/strategies/${strategyId}/evaluate?iterations=500`, {
        method: 'POST',
      });
      const data = await res.json();
      setSimulationResult(data);
    } catch (err) {
      console.error('Error running strategy simulation:', err);
    } finally {
      setEvaluating(false);
    }
  };

  return (
    <div className="space-y-6 p-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 border-b border-border pb-4">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-primary/10 rounded-lg text-primary">
            <Compass className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-2xl font-bold tracking-tight">Strategy Generation Studio</h1>
            <p className="text-sm text-muted-foreground">
              Multi-Alternative Organizational Strategy Synthesis, Bayesian Utility Ranking & Monte Carlo Simulations
            </p>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <Button variant="outline" onClick={loadStrategies} disabled={loading}>
            <span className="flex items-center gap-2">
              <RotateCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
              Refresh
            </span>
          </Button>
          <Button variant="intelligence" onClick={handleGenerate} disabled={generating}>
            <span className="flex items-center gap-2">
              <Sparkles className="w-4 h-4" />
              {generating ? 'Synthesizing...' : 'Synthesize Alternative Strategies'}
            </span>
          </Button>
        </div>
      </div>

      {/* Main Two-Column View */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Strategy Candidates */}
        <div className="space-y-4">
          <h2 className="text-sm font-semibold flex items-center justify-between">
            <span>Generated Strategies ({strategies.length})</span>
          </h2>
          <div className="space-y-3">
            {strategies.map((s) => (
              <Card
                key={s.strategy_id}
                onClick={() => {
                  setSelectedStrategy(s);
                  setSimulationResult(null);
                }}
                className={`border cursor-pointer transition-all ${
                  selectedStrategy?.strategy_id === s.strategy_id
                    ? 'border-primary bg-primary/5 shadow-sm'
                    : 'border-border hover:bg-muted/30'
                }`}
              >
                <CardContent className="p-4 space-y-2">
                  <div className="flex justify-between items-start">
                    <span className="font-semibold text-sm line-clamp-1">{s.title}</span>
                    {s.is_selected && <Badge variant="success">OPTIMAL</Badge>}
                  </div>
                  <p className="text-xs text-muted-foreground line-clamp-2">{s.rationale}</p>
                  <div className="grid grid-cols-2 gap-2 pt-2 border-t border-border/60 text-xs">
                    <div>
                      <span className="text-muted-foreground">Expected ROI:</span>
                      <span className="font-semibold text-primary ml-1">{s.expected_roi_multiplier}x</span>
                    </div>
                    <div>
                      <span className="text-muted-foreground">Est. Cost:</span>
                      <span className="font-medium ml-1">${s.total_estimated_cost_usd.toLocaleString()}</span>
                    </div>
                    <div>
                      <span className="text-muted-foreground">Sim Pass Rate:</span>
                      <span className="font-semibold text-emerald-500 ml-1">
                        {(s.simulation_pass_rate * 100).toFixed(0)}%
                      </span>
                    </div>
                    <div>
                      <span className="text-muted-foreground">Risk Index:</span>
                      <span className="font-medium ml-1">{s.risk_score}</span>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>

        {/* Selected Strategy Deep Dive */}
        <div className="lg:col-span-2 space-y-6">
          {selectedStrategy ? (
            <>
              <Card className="border-border shadow-sm">
                <CardHeader className="flex flex-row items-center justify-between pb-3">
                  <div>
                    <CardTitle className="text-lg">{selectedStrategy.title}</CardTitle>
                    <p className="text-xs text-muted-foreground font-mono mt-0.5">{selectedStrategy.strategy_id}</p>
                  </div>
                  <Button
                    variant="outline"
                    onClick={() => handleRunMonteCarlo(selectedStrategy.strategy_id)}
                    disabled={evaluating}
                  >
                    <span className="flex items-center gap-2">
                      <Activity className="w-4 h-4 text-primary" />
                      {evaluating ? 'Simulating...' : 'Run Monte Carlo (500 runs)'}
                    </span>
                  </Button>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="p-3 bg-muted/40 border border-border rounded-lg text-xs leading-relaxed">
                    <span className="font-semibold text-foreground">Strategic Rationale: </span>
                    {selectedStrategy.rationale}
                  </div>

                  {/* Monte Carlo Results */}
                  {simulationResult && (
                    <div className="p-4 bg-primary/5 border border-primary/20 rounded-lg space-y-2">
                      <div className="font-semibold text-sm text-primary flex items-center gap-1.5">
                        <CheckCircle2 className="w-4 h-4" /> Monte Carlo Simulation Report ({simulationResult.iterations} runs)
                      </div>
                      <div className="grid grid-cols-2 md:grid-cols-4 gap-3 text-xs pt-1">
                        <div>
                          <span className="text-muted-foreground">Success Prob:</span>
                          <div className="font-bold text-emerald-500 text-sm">
                            {(simulationResult.probability_of_success * 100).toFixed(1)}%
                          </div>
                        </div>
                        <div>
                          <span className="text-muted-foreground">Mean ROI:</span>
                          <div className="font-bold text-sm">{simulationResult.mean_expected_roi}x</div>
                        </div>
                        <div>
                          <span className="text-muted-foreground">Mean Cost:</span>
                          <div className="font-bold text-sm">${simulationResult.mean_expected_cost_usd}</div>
                        </div>
                        <div>
                          <span className="text-muted-foreground">Verdict:</span>
                          <Badge variant="success">{simulationResult.verdict}</Badge>
                        </div>
                      </div>
                    </div>
                  )}

                  {/* Action Breakdown */}
                  <div>
                    <h3 className="text-sm font-semibold mb-2 flex items-center gap-2">
                      <ListOrdered className="w-4 h-4 text-primary" />
                      Operational Actions ({selectedStrategy.actions.length})
                    </h3>
                    <div className="space-y-2">
                      {selectedStrategy.actions.map((act) => (
                        <div key={act.action_id} className="p-3 bg-card border border-border rounded-lg text-xs">
                          <div className="flex justify-between items-start">
                            <span className="font-medium text-sm">{act.title}</span>
                            <Badge variant="outline">{act.target_department}</Badge>
                          </div>
                          <div className="grid grid-cols-3 gap-2 mt-2 text-muted-foreground">
                            <span>Cost: ${act.estimated_cost_usd.toLocaleString()}</span>
                            <span>Utility: {(act.expected_utility * 100).toFixed(0)}%</span>
                            <span>Timeline: {act.timeline_weeks} wks</span>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </CardContent>
              </Card>
            </>
          ) : (
            <Card className="border-border shadow-sm p-8 text-center text-muted-foreground">
              Select a strategy plan to inspect actions and utility parameters.
            </Card>
          )}
        </div>
      </div>
    </div>
  );
};
