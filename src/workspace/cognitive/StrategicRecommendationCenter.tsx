import React, { useState, useEffect } from 'react';
import { Sparkles, RefreshCw } from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { cognitiveApiClient } from '../../services/cognitiveApiClient';
import { StrategicRecommendation } from '../../types/cognitive';

export const StrategicRecommendationCenter: React.FC = () => {
  const [recommendations, setRecommendations] = useState<StrategicRecommendation[]>([]);

  const loadData = async () => {
    const data = await cognitiveApiClient.getRecommendations();
    setRecommendations(data);
  };

  useEffect(() => {
    loadData();
  }, []);

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-slate-100 flex items-center gap-2">
            <Sparkles className="w-7 h-7 text-indigo-400" />
            Executive Strategic Recommendation Center
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Synthesizes weekly executive recommendations on Automation, Risk Prevention, Model Upgrades, and Budgeting.
          </p>
        </div>
        <Button variant="outline" onClick={loadData}>
          <span className="flex items-center gap-2">
            <RefreshCw className="w-4 h-4" />
            Refresh
          </span>
        </Button>
      </div>

      <div className="space-y-4">
        {recommendations.map((rec) => (
          <Card key={rec.id} className="p-5 bg-slate-900/60 border-slate-800 space-y-3">
            <div className="flex justify-between items-start">
              <div className="flex items-center gap-2">
                <Badge variant="outline" className="text-indigo-400 border-indigo-500/30">
                  {rec.category}
                </Badge>
                <Badge variant={rec.urgency === 'HIGH' ? 'warning' : 'info'}>
                  {rec.urgency} Urgency
                </Badge>
              </div>
              <span className="text-xs font-mono text-slate-500">{rec.id}</span>
            </div>

            <h3 className="text-base font-semibold text-slate-100">{rec.title}</h3>
            <p className="text-xs text-slate-300 bg-slate-800/40 p-3 rounded border border-slate-700/50">
              {rec.description}
            </p>
            <div className="pt-2 border-t border-slate-800 flex justify-between items-center text-xs text-emerald-400 font-mono">
              <span>Projected Impact: {rec.projected_business_impact}</span>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};
