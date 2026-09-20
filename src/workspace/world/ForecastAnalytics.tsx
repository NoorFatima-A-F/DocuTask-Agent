import React, { useState } from 'react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import {
  Calendar,
} from 'lucide-react';

interface ForecastPoint {
  step: number;
  label: string;
  predicted_value: number;
  lower_bound: number;
  upper_bound: number;
}

interface ForecastItem {
  id: string;
  metric: string;
  horizon: string;
  predictedMean: number;
  ci95: [number, number];
  trend: string;
  points: ForecastPoint[];
}

export const ForecastAnalytics: React.FC = () => {
  const [selectedHorizon, setSelectedHorizon] = useState<string>('MEDIUM_TERM');

  const forecasts: ForecastItem[] = [
    {
      id: 'fcst-01',
      metric: 'LATENCY_MS',
      horizon: 'MEDIUM_TERM (Next 24 Hours)',
      predictedMean: 201.6,
      ci95: [186.6, 216.6],
      trend: 'STABLE',
      points: [
        { step: 1, label: 'T+2h', predicted_value: 182.0, lower_bound: 170.0, upper_bound: 194.0 },
        { step: 2, label: 'T+6h', predicted_value: 188.0, lower_bound: 176.0, upper_bound: 200.0 },
        { step: 3, label: 'T+12h', predicted_value: 195.0, lower_bound: 183.0, upper_bound: 207.0 },
        { step: 4, label: 'T+24h', predicted_value: 201.6, lower_bound: 189.6, upper_bound: 213.6 },
      ],
    },
    {
      id: 'fcst-02',
      metric: 'VRAM_UTILIZATION_PCT',
      horizon: 'LONG_TERM (Next 7 Days)',
      predictedMean: 60.6,
      ci95: [52.3, 68.9],
      trend: 'INCREASING',
      points: [
        { step: 1, label: 'Day 1', predicted_value: 50.0, lower_bound: 45.0, upper_bound: 55.0 },
        { step: 2, label: 'Day 3', predicted_value: 54.0, lower_bound: 48.0, upper_bound: 60.0 },
        { step: 3, label: 'Day 5', predicted_value: 57.5, lower_bound: 50.0, upper_bound: 65.0 },
        { step: 4, label: 'Day 7', predicted_value: 60.6, lower_bound: 52.3, upper_bound: 68.9 },
      ],
    },
    {
      id: 'fcst-03',
      metric: 'TOKEN_COST_USD',
      horizon: 'SHORT_TERM (Next 1 Hour)',
      predictedMean: 0.0252,
      ci95: [0.0222, 0.0282],
      trend: 'STABLE',
      points: [
        { step: 1, label: 'T+15m', predicted_value: 0.0242, lower_bound: 0.0220, upper_bound: 0.0264 },
        { step: 2, label: 'T+30m', predicted_value: 0.0246, lower_bound: 0.0224, upper_bound: 0.0268 },
        { step: 3, label: 'T+45m', predicted_value: 0.0249, lower_bound: 0.0226, upper_bound: 0.0272 },
        { step: 4, label: 'T+60m', predicted_value: 0.0252, lower_bound: 0.0228, upper_bound: 0.0276 },
      ],
    },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold tracking-tight">Probabilistic Forecast Analytics</h1>
            <Badge variant="intelligence" size="sm" hasDot isPulsing>
              TIME-SERIES FORECAST ACTIVE
            </Badge>
            <Badge variant="outline" size="sm">
              AWM-PSDTIP Phase 13.10
            </Badge>
          </div>
          <p className="text-xs text-muted-foreground mt-1">
            Multi-horizon forecasting of latency, GPU VRAM, token costs, throughput, and resource depletion horizons.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Button variant="outline" size="sm">
            <Calendar className="w-3.5 h-3.5 mr-1.5" />
            Adjust Forecast Windows
          </Button>
        </div>
      </div>

      {/* Horizon Filter Tabs */}
      <div className="flex items-center gap-2 border-b border-border/40 pb-2">
        {(['ALL', 'SHORT_TERM', 'MEDIUM_TERM', 'LONG_TERM'] as const).map((h) => (
          <Button
            key={h}
            variant={selectedHorizon === h ? 'primary' : 'ghost'}
            size="sm"
            onClick={() => setSelectedHorizon(h)}
          >
            {h.replace('_', ' ')}
          </Button>
        ))}
      </div>

      {/* Forecast Cards */}
      <div className="space-y-4">
        {forecasts.map((fcst) => (
          <Card key={fcst.id} className="p-5 border-border/40 space-y-4 hover:border-purple-500/30 transition-colors">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
              <div className="space-y-1">
                <div className="flex items-center gap-2">
                  <span className="text-xs font-mono font-bold text-foreground">{fcst.metric}</span>
                  <Badge variant="intelligence" size="sm">{fcst.horizon}</Badge>
                </div>
                <div className="text-xs text-muted-foreground font-mono">
                  Predicted Mean: <strong className="text-foreground">{fcst.predictedMean}</strong> (95% CI: [{fcst.ci95[0]}, {fcst.ci95[1]}])
                </div>
              </div>
              <Badge variant={fcst.trend === 'STABLE' ? 'success' : 'warning'} size="sm">
                Trend: {fcst.trend}
              </Badge>
            </div>

            {/* Trajectory Points Timeline */}
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs font-mono">
              {fcst.points.map((pt, idx) => (
                <div key={idx} className="p-3 rounded bg-secondary/20 border border-border/30 space-y-1">
                  <span className="text-muted-foreground">{pt.label}</span>
                  <div className="text-sm font-bold text-foreground">{pt.predicted_value}</div>
                  <span className="text-[10px] text-purple-300">[{pt.lower_bound} - {pt.upper_bound}]</span>
                </div>
              ))}
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};
